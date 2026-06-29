# Report Workflow

## 학술트랙

1. 학회원은 발표자료 PDF/PPTX/PPT가 들어 있는 폴더를 준비합니다.
2. Codex 또는 Claude Code에서 `$research_weekly` / `research_weekly`를 실행합니다.
3. 스킬이 이름과 자료 경로를 확인합니다. 이름은 `OPT_AI_MEMBER_NAME`, 저장된 로컬 설정, CLI 입력/선택 순서로 확인합니다.
4. 자료 텍스트를 추출하고, 모델이 1~2문단 한국어 보고 요약을 작성합니다.
5. `reports/research_weekly.md`에 append하고 commit/push합니다.

## 개발트랙

1. 학회원은 자신의 개발 레포를 VS Code에서 엽니다.
2. Codex 또는 Claude Code에서 `$develop_weekly` / `develop_weekly`를 실행합니다.
3. 스킬이 이름과 필요 시 기간/author를 확인합니다. 이름은 `OPT_AI_MEMBER_NAME`, 저장된 로컬 설정, CLI 입력/선택 순서로 확인합니다.
4. 최근 14일 Git commit 내역을 수집하고, 모델이 1~2문단 한국어 보고 요약을 작성합니다.
5. `reports/develop_weekly.md`에 append하고 commit/push합니다.

## 중앙 레포 동기화

처음 실행 시 스킬 helper는 `~/.opt-ai-skills/repo`에 중앙 레포를 clone할 수 있습니다. 자동 push를 쓰려면 VS Code/Git CLI에 설정된 GitHub credential이 중앙 레포에 write 가능한 상태여야 합니다. 이미 로컬 clone이 있으면 다음 환경변수를 권장합니다.

```bash
export OPT_AI_SKILLS_REPO=/path/to/opt_ai_skills
```


## 이름 확인 방식

스킬 helper에는 공통 `identify-member` 명령이 있습니다.

```bash
python3 ${CODEX_HOME:-$HOME/.codex}/skills/develop_weekly/scripts/opt_report.py identify-member --remember
python3 ${CODEX_HOME:-$HOME/.codex}/skills/develop_weekly/scripts/opt_report.py identify-member --members-file config/members.txt --remember
```

`--members-file`은 한 줄에 한 명씩 적은 명단을 번호 선택지로 보여줍니다. 비대화형 Codex/Claude 실행에서 CLI prompt를 열 수 없으면, 에이전트가 대화로 이름을 한 번만 물은 뒤 `--member` 값으로 전달합니다.
