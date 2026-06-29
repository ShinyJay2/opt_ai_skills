#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "plugins/opt-ai-skills/skills/research_weekly/scripts/opt_report.py"
REMINDER = ROOT / "scripts/reminder_bot.py"


def load_helper():
    spec = importlib.util.spec_from_file_location("opt_report", HELPER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=True)


def test_append_format_and_fence():
    helper = load_helper()
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        out = helper.append_report(
            repo,
            "research",
            "테스터",
            "첫 문단입니다.\n\n둘째 문단입니다.",
            "자료 일부\n```\n탈출 시도\n```",
            "sample.pdf",
            "2026-06-29",
            False,
        )
        text = out.read_text(encoding="utf-8")
        assert "\n## 2026-06-29 · 테스터\n" in text
        assert "\n### 보고 요약\n\n첫 문단입니다.\n\n둘째 문단입니다." in text
        assert "````text" in text
        assert "\n````\n" in text


def test_commit_pathspec_keeps_unrelated_staged_changes():
    helper = load_helper()
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        run(["git", "init", "-b", "main"], cwd=repo)
        run(["git", "config", "user.name", "Tester"], cwd=repo)
        run(["git", "config", "user.email", "tester@example.com"], cwd=repo)
        (repo / "reports").mkdir()
        (repo / "reports/research_weekly.md").write_text("# R\n", encoding="utf-8")
        (repo / "notes.txt").write_text("do not commit\n", encoding="utf-8")
        run(["git", "add", "."], cwd=repo)
        run(["git", "commit", "-m", "initial"], cwd=repo)
        (repo / "notes.txt").write_text("staged unrelated\n", encoding="utf-8")
        run(["git", "add", "notes.txt"], cwd=repo)
        (repo / "reports/research_weekly.md").write_text("# R\nentry\n", encoding="utf-8")
        helper.git_commit_push(repo, "append report", False, Path("reports/research_weekly.md"))
        committed = run(["git", "show", "--name-only", "--format=", "HEAD"], cwd=repo).stdout.strip().splitlines()
        assert committed == ["reports/research_weekly.md"]
        staged = run(["git", "diff", "--cached", "--name-only"], cwd=repo).stdout.strip()
        assert staged == "notes.txt"


def test_reminder_dry_run():
    proc = run(["python3", str(REMINDER), "--dry-run", "--force"])
    assert "OPT-AI 격주 보고 리마인더" in proc.stdout


def test_kakao_kmsg_dry_run_command():
    helper_spec = importlib.util.spec_from_file_location("reminder_bot", REMINDER)
    assert helper_spec and helper_spec.loader
    reminder = importlib.util.module_from_spec(helper_spec)
    helper_spec.loader.exec_module(reminder)
    with tempfile.TemporaryDirectory() as td:
        fake = Path(td) / "kmsg"
        log = Path(td) / "kmsg.log"
        fake.write_text(
            "#!/usr/bin/env bash\n"
            f"printf '%s\n' \"$@\" > {log}\n"
            "exit 0\n",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        import os
        old_bin = os.environ.get("KMSG_BIN")
        old_chat = os.environ.get("KAKAOTALK_CHAT_ID")
        os.environ["KMSG_BIN"] = str(fake)
        os.environ["KAKAOTALK_CHAT_ID"] = "chat_test"
        try:
            method = reminder.send_kakao_kmsg("테스트 메시지", dry_run=True)
            assert method == "kakao-kmsg:chat-id:chat_test"
            args = log.read_text(encoding="utf-8").splitlines()
            assert args == ["send", "--chat-id", "chat_test", "테스트 메시지", "--dry-run"]
        finally:
            if old_bin is None:
                os.environ.pop("KMSG_BIN", None)
            else:
                os.environ["KMSG_BIN"] = old_bin
            if old_chat is None:
                os.environ.pop("KAKAOTALK_CHAT_ID", None)
            else:
                os.environ["KAKAOTALK_CHAT_ID"] = old_chat


if __name__ == "__main__":
    test_append_format_and_fence()
    test_commit_pathspec_keeps_unrelated_staged_changes()
    test_reminder_dry_run()
    test_kakao_kmsg_dry_run_command()
    print("behavior tests ok")
