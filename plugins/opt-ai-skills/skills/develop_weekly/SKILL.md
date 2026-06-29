---
name: develop_weekly
description: OPT-AI 개발트랙 학회원이 최근 2주 Git commit 내역을 근거로 개발 내용을 1~2문단으로 요약하고 중앙 보고서에 append할 때 사용합니다.
---

# develop_weekly

OPT-AI 개발트랙 격주 보고 스킬입니다. 현재 개발 레포의 최근 2주 commit 내역을 근거로 개발 내용을 한국어 1~2문단으로 정리하고, `ShinyJay2/opt_ai_skills` 레포의 `reports/develop_weekly.md`에 날짜·이름·commit 근거와 함께 append합니다.

## 입력 흐름

1. 학회원 이름을 먼저 확인합니다. 이름이 프롬프트에 없으면 아래 helper로 CLI 입력/선택을 띄우거나, 비대화형 환경에서는 한 번만 물어봅니다.
2. Git 레포 경로를 확인합니다. 기본값은 현재 작업 디렉토리입니다.
3. 기간은 기본 최근 14일입니다. 사용자가 기간을 주면 `--since`, `--until`로 반영합니다.
4. 중앙 레포 위치는 아래 순서로 사용합니다.
   - `OPT_AI_SKILLS_REPO` 환경변수
   - 사용자가 준 `--repo-path`
   - 없으면 `~/.opt-ai-skills/repo`에 `https://github.com/ShinyJay2/opt_ai_skills.git` clone

## 실행 절차

0. 학회원 이름 확인:

```bash
SCRIPT="${OPT_AI_REPORT_HELPER:-${CODEX_HOME:-$HOME/.codex}/skills/develop_weekly/scripts/opt_report.py}"
MEMBER="$(python3 "$SCRIPT" identify-member --remember)"
```

- `OPT_AI_MEMBER_NAME`이 있거나 `~/.config/opt-ai-skills/member.json`에 저장된 이름이 있으면 그대로 사용합니다.
- `--members-file /path/to/members.txt`를 주면 번호 선택지를 띄웁니다. 파일은 한 줄에 한 명씩 작성합니다.
- Codex/Claude 비대화형 실행에서 CLI prompt가 열리지 않으면 사용자에게 이름을 한 번만 물은 뒤 `--member "<이름>"`으로 재실행합니다.

1. commit 근거 수집:

```bash
SCRIPT="${OPT_AI_REPORT_HELPER:-${CODEX_HOME:-$HOME/.codex}/skills/develop_weekly/scripts/opt_report.py}"
EVIDENCE_FILE="$(mktemp "${TMPDIR:-/tmp}/opt-ai-develop.XXXXXX")"
python3 "$SCRIPT" collect-develop \
  --git-repo /path/to/member/project \
  --since "2 weeks ago" > "$EVIDENCE_FILE"
```

특정 author만 보고하려면 `--author "이름 또는 이메일"`을 추가합니다.

2. `"$EVIDENCE_FILE"`를 읽고 다음 형식의 한국어 요약을 작성합니다.
   - 1~2문단
   - 구현한 기능, 수정한 버그, 리팩터링/테스트/문서화 작업을 묶어서 설명
   - commit hash를 본문에 과하게 나열하지 말고 “근거 스냅샷”에 남김
   - commit이 없으면 보고서를 append하지 말고 사용자에게 기간/author 확인을 요청

3. 중앙 보고서에 append하고 commit/push합니다.

```bash
SCRIPT="${OPT_AI_REPORT_HELPER:-${CODEX_HOME:-$HOME/.codex}/skills/develop_weekly/scripts/opt_report.py}"
python3 "$SCRIPT" append \
  --track develop \
  --member "$MEMBER" \
  --summary "<1~2문단 요약>" \
  --evidence-file "$EVIDENCE_FILE" \
  --source "/path/to/member/project git log --since=2weeks" \
  --push
```

4. 결과로 append된 파일 경로와 commit/push 성공 여부를 보고합니다.

## 보고 품질 기준

- raw commit 제목을 그대로 붙이지 말고 개발 흐름으로 묶습니다.
- “무엇을 만들었는지 / 왜 수정했는지 / 검증이나 정리 작업이 있었는지”가 드러나야 합니다.
- 여러 레포를 작업했다면 레포별로 commit 근거를 수집한 뒤 하나의 1~2문단으로 통합합니다.

## 금지사항

- 사용자 이름 없이 append하지 않습니다.
- commit 근거가 없는데 개발 내용을 추측하지 않습니다.
- 중앙 보고서 push 실패를 성공처럼 보고하지 않습니다.
