# Report Workflow

학회원이 알아야 할 내용만 간단히 정리합니다.

## 처음 한 번만 설치

Codex:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ShinyJay2/opt_ai_skills/main/scripts/bootstrap.sh)" codex
```

Claude Code:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ShinyJay2/opt_ai_skills/main/scripts/bootstrap.sh)" claude
```

설치 후 Codex / Claude Code를 재시작합니다.

## 학술트랙 보고

1. 발표자료 PDF/PPTX가 있는 폴더를 VS Code로 엽니다.
2. Codex 또는 Claude Code에서 실행합니다.

```text
$research_weekly
```

3. 이름을 물어보면 입력합니다.
4. 스킬이 자료를 읽고 `reports/research_weekly.md`에 보고를 추가합니다.

## 개발트랙 보고

1. 본인 개발 레포를 VS Code로 엽니다.
2. Codex 또는 Claude Code에서 실행합니다.

```text
$develop_weekly
```

3. 이름을 물어보면 입력합니다.
4. 스킬이 최근 14일 commit을 읽고 `reports/develop_weekly.md`에 보고를 추가합니다.

## 이름 저장

매번 이름을 입력하기 싫으면 한 번 저장할 수 있습니다.

```bash
python3 ~/.codex/skills/develop_weekly/scripts/opt_report.py identify-member --remember
```

## GitHub에 안 올라갈 때

운영자에게 받은 GitHub 초대를 수락했는지 확인하세요.

그래도 안 되면 VS Code에서 GitHub 로그인을 하거나 아래 명령을 실행합니다.

```bash
gh auth login
```
