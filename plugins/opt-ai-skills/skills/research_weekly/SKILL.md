---
name: research_weekly
description: OPT-AI 학술트랙 학회원이 PDF/PPT/PPTX 발표자료를 근거로 최근 2주 공부 내용을 1~2문단으로 요약하고 중앙 보고서에 append할 때 사용합니다.
---

# research_weekly

OPT-AI 학술트랙 격주 보고 스킬입니다. 발표자료가 담긴 파일 또는 폴더를 근거로 학회원의 2주 학습 내용을 한국어 1~2문단으로 정리하고, `ShinyJay2/opt_ai_skills` 레포의 `reports/research_weekly.md`에 날짜·이름·근거와 함께 append합니다.

## 입력 흐름

1. 학회원 이름을 먼저 확인합니다. 이름이 프롬프트에 없으면 한 번만 물어봅니다.
2. PDF/PPT/PPTX 파일 또는 발표자료 폴더 경로를 확인합니다. 경로가 없으면 한 번만 물어봅니다.
3. 중앙 레포 위치는 아래 순서로 사용합니다.
   - `OPT_AI_SKILLS_REPO` 환경변수
   - 사용자가 준 `--repo-path`
   - 없으면 `~/.opt-ai-skills/repo`에 `https://github.com/ShinyJay2/opt_ai_skills.git` clone

## 실행 절차

1. 자료 텍스트 추출:

```bash
SCRIPT="${OPT_AI_REPORT_HELPER:-${CODEX_HOME:-$HOME/.codex}/skills/research_weekly/scripts/opt_report.py}"
EVIDENCE_FILE="$(mktemp "${TMPDIR:-/tmp}/opt-ai-research.XXXXXX")"
python3 "$SCRIPT" extract-research /path/to/materials > "$EVIDENCE_FILE"
```

2. `"$EVIDENCE_FILE"`를 읽고 다음 형식의 한국어 요약을 작성합니다.
   - 1~2문단
   - 무엇을 공부했는지, 어떤 개념/논문/모델/실험을 다뤘는지 포함
   - 단순 파일명 나열 금지
   - 자료에서 확인되지 않는 성과/결과는 추측하지 않음

3. 중앙 보고서에 append하고 commit/push합니다.

```bash
SCRIPT="${OPT_AI_REPORT_HELPER:-${CODEX_HOME:-$HOME/.codex}/skills/research_weekly/scripts/opt_report.py}"
python3 "$SCRIPT" append \
  --track research \
  --member "<학회원 이름>" \
  --summary "<1~2문단 요약>" \
  --evidence-file "$EVIDENCE_FILE" \
  --source "/path/to/materials" \
  --push
```

4. 결과로 append된 파일 경로와 commit/push 성공 여부를 보고합니다.

## 보고 품질 기준

- 발표자료의 핵심 주제, 공부한 방법, 배운 내용이 드러나야 합니다.
- 2주 활동 보고이므로 “이번 기간에는 …를 중심으로…”처럼 기간성을 살립니다.
- 수식/알고리즘/실험명이 중요하면 그대로 보존합니다.
- 자료 추출이 부족하면 부족한 파일과 대체 방법(PDF/PPTX export)을 명시합니다.

## 금지사항

- 사용자 이름 없이 append하지 않습니다.
- 근거 파일을 읽지 않고 일반적인 AI 공부 내용으로 꾸미지 않습니다.
- credential 파일을 commit하지 않습니다.
