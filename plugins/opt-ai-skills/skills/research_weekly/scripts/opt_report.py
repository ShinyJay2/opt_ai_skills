#!/usr/bin/env python3
"""OPT-AI report helper.

This script intentionally does not call an LLM. The Codex/Claude skill reads the
extracted evidence, writes the Korean 1-2 paragraph summary, then passes that
summary back to this helper for append/commit/push.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

DEFAULT_REPO_URL = "https://github.com/ShinyJay2/opt_ai_skills.git"
DEFAULT_CACHE_DIR = Path.home() / ".opt-ai-skills" / "repo"
REPORT_FILES = {
    "research": Path("reports/research_weekly.md"),
    "develop": Path("reports/develop_weekly.md"),
}


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=check)


def today() -> str:
    return dt.date.today().isoformat()


def ensure_repo(repo_path: str | None, repo_url: str, no_clone: bool = False) -> Path:
    candidate = Path(repo_path or os.environ.get("OPT_AI_SKILLS_REPO", "")).expanduser() if (repo_path or os.environ.get("OPT_AI_SKILLS_REPO")) else None
    if candidate:
        candidate.mkdir(parents=True, exist_ok=True)
        if (candidate / ".git").exists() or no_clone:
            return candidate.resolve()
    target = candidate or DEFAULT_CACHE_DIR
    if not (target / ".git").exists() and not no_clone:
        target.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", repo_url, str(target)])
    return target.resolve()


def git_sync(repo: Path, do_pull: bool) -> None:
    if do_pull and (repo / ".git").exists():
        run(["git", "pull", "--ff-only"], cwd=repo)


def git_commit_push(repo: Path, message: str, do_push: bool, rel_path: Path) -> None:
    if not (repo / ".git").exists():
        return
    rel = rel_path.as_posix()
    run(["git", "add", "--", rel], cwd=repo)
    staged = run(["git", "diff", "--cached", "--quiet", "--", rel], cwd=repo, check=False)
    if staged.returncode == 0:
        print(f"No report changes to commit for {rel}.")
        return
    run(["git", "commit", "-m", message, "--", rel], cwd=repo)
    if do_push:
        run(["git", "push"], cwd=repo)


def iter_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
    else:
        for suffix in ("*.pdf", "*.pptx", "*.ppt", "*.md", "*.txt"):
            yield from sorted(path.rglob(suffix))


def extract_pdf(path: Path) -> tuple[str, str]:
    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        proc = run([pdftotext, "-layout", str(path), "-"], check=False)
        if proc.stdout.strip():
            return proc.stdout, "pdftotext"
    try:
        import pypdf  # type: ignore
        reader = pypdf.PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages), "pypdf"
    except Exception as exc:
        return f"[PDF text extraction unavailable for {path.name}: {exc}]", "unavailable"


def extract_pptx(path: Path) -> tuple[str, str]:
    texts: list[str] = []
    try:
        with zipfile.ZipFile(path) as zf:
            slide_names = sorted(n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml"))
            for name in slide_names:
                root = ET.fromstring(zf.read(name))
                slide_texts = [node.text.strip() for node in root.iter() if node.tag.endswith("}t") and node.text and node.text.strip()]
                if slide_texts:
                    texts.append(f"# {Path(name).stem}\n" + "\n".join(slide_texts))
        return "\n\n".join(texts), "pptx-xml"
    except Exception as exc:
        return f"[PPTX text extraction unavailable for {path.name}: {exc}]", "unavailable"


def extract_text_file(path: Path) -> tuple[str, str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace"), "text"
    except Exception as exc:
        return f"[Text extraction unavailable for {path.name}: {exc}]", "unavailable"


def extract_materials(path: Path, max_chars: int) -> str:
    blocks: list[str] = []
    for file in iter_files(path):
        suffix = file.suffix.lower()
        if suffix == ".pdf":
            text, method = extract_pdf(file)
        elif suffix == ".pptx":
            text, method = extract_pptx(file)
        elif suffix == ".ppt":
            text, method = ("[Legacy .ppt cannot be reliably parsed without LibreOffice/pandoc. Export to PDF/PPTX if this is insufficient.]", "ppt-legacy")
        elif suffix in {".md", ".txt"}:
            text, method = extract_text_file(file)
        else:
            continue
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        blocks.append(f"## {file}\nExtraction: {method}\n\n{text[:max_chars]}")
    return "\n\n---\n\n".join(blocks) if blocks else "[No supported PDF/PPTX/PPT/MD/TXT files found.]"


def collect_commits(repo: Path, since: str, until: str | None, author: str | None, max_count: int) -> str:
    args = ["git", "log", f"--since={since}", "--date=short", "--pretty=format:%h%x09%ad%x09%an%x09%s"]
    if until:
        args.insert(3, f"--until={until}")
    if author:
        args.append(f"--author={author}")
    args.append(f"-{max_count}")
    proc = run(args, cwd=repo, check=False)
    if proc.returncode != 0:
        return f"[git log failed in {repo}: {proc.stderr.strip()}]"
    return proc.stdout.strip() or "[No commits found for the selected range.]"


def markdown_fence_for(text: str) -> str:
    runs = [len(match.group(0)) for match in re.finditer(r"`+", text)]
    return "`" * max(3, (max(runs) + 1) if runs else 3)


def build_report_entry(track: str, member: str, summary: str, evidence: str, source: str, report_date: str) -> str:
    evidence_snapshot = evidence.strip()[:4000]
    fence = markdown_fence_for(evidence_snapshot)
    track_label = "학술트랙" if track == "research" else "개발트랙"
    summary_text = summary.strip()
    return "\n".join([
        f"## {report_date} · {member}",
        "",
        f"- 트랙: {track_label}",
        f"- 근거: {source}",
        "",
        "### 보고 요약",
        "",
        summary_text,
        "",
        "### 근거 스냅샷",
        "",
        f"{fence}text",
        evidence_snapshot,
        fence,
        "",
    ])


def append_report(repo: Path, track: str, member: str, summary: str, evidence: str, source: str, report_date: str, dry_run: bool) -> Path:
    rel = REPORT_FILES[track]
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        title = "학술트랙 격주 보고" if track == "research" else "개발트랙 격주 보고"
        path.write_text(f"# OPT-AI {title}\n\n이 문서는 각 학회원이 스킬을 실행할 때마다 append 되는 누적 보고서입니다.\n\n", encoding="utf-8")
    entry = build_report_entry(track, member, summary, evidence, source, report_date)
    if dry_run:
        print(entry)
    else:
        with path.open("a", encoding="utf-8") as f:
            f.write("\n" + entry)
    return path


def default_since(days: int = 14) -> str:
    return (dt.datetime.now() - dt.timedelta(days=days)).strftime("%Y-%m-%d")


def cmd_extract_research(args: argparse.Namespace) -> None:
    print(extract_materials(Path(args.path).expanduser().resolve(), args.max_chars))


def cmd_collect_develop(args: argparse.Namespace) -> None:
    repo = Path(args.git_repo).expanduser().resolve()
    print(collect_commits(repo, args.since or default_since(), args.until, args.author, args.max_count))


def cmd_append(args: argparse.Namespace) -> None:
    repo = ensure_repo(args.repo_path, args.repo_url, args.no_clone)
    git_sync(repo, args.pull)
    evidence = args.evidence or ""
    if args.evidence_file:
        evidence = Path(args.evidence_file).read_text(encoding="utf-8", errors="replace")
    source = args.source or (args.evidence_file or "manual")
    out = append_report(repo, args.track, args.member, args.summary, evidence, source, args.date or today(), args.dry_run)
    if not args.dry_run:
        git_commit_push(repo, f"Append {args.track} report for {args.member} ({args.date or today()})", args.push, REPORT_FILES[args.track])
    print(out)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OPT-AI biweekly report helper")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("extract-research", help="Extract text evidence from PDF/PPTX/PPT/MD/TXT path")
    r.add_argument("path")
    r.add_argument("--max-chars", type=int, default=12000)
    r.set_defaults(func=cmd_extract_research)

    d = sub.add_parser("collect-develop", help="Collect git commit evidence")
    d.add_argument("--git-repo", default=".")
    d.add_argument("--since", help="Default: 14 days ago")
    d.add_argument("--until")
    d.add_argument("--author")
    d.add_argument("--max-count", type=int, default=80)
    d.set_defaults(func=cmd_collect_develop)

    a = sub.add_parser("append", help="Append a completed report summary to the central repo")
    a.add_argument("--track", choices=sorted(REPORT_FILES), required=True)
    a.add_argument("--member", required=True)
    a.add_argument("--summary", required=True)
    a.add_argument("--evidence")
    a.add_argument("--evidence-file")
    a.add_argument("--source")
    a.add_argument("--date")
    a.add_argument("--repo-path")
    a.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    a.add_argument("--no-clone", action="store_true")
    a.add_argument("--pull", action="store_true", default=True)
    a.add_argument("--no-pull", dest="pull", action="store_false")
    a.add_argument("--push", action="store_true")
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_append)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
