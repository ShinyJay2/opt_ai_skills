# OPT-AI Codex / Claude Skills

OPT-AI 학회에서 사용할 Codex / Claude Code 스킬 마켓플레이스입니다. 학술트랙 발표자료 기반 격주 보고, 개발트랙 Git commit 기반 격주 보고, Discord 격주 리마인더 자동화를 제공합니다.

현재 버전: **v0.1.0**

## 개요

이 레포는 Codex CLI의 plugin marketplace 형식과 Claude Code에서 복사해 사용할 수 있는 `SKILL.md` 형식을 함께 제공합니다.

```text
.agents/plugins/marketplace.json
plugins/opt-ai-skills/.codex-plugin/plugin.json
plugins/opt-ai-skills/skills/
claude/skills/
reports/
.github/workflows/biweekly-reminder.yml
.github/workflows/biweekly-kakaotalk-reminder.yml
```

Codex / Claude에서 사용하는 핵심 스킬은 아래 2개입니다.

```text
$research_weekly  → reports/research_weekly.md append → commit/push
$develop_weekly   → reports/develop_weekly.md append  → commit/push

GitHub Actions biweekly reminder → Discord channel reminder
```

| 스킬 | 목적 |
|---|---|
| `$research_weekly` | PDF/PPT/PPTX 발표자료를 읽고 학술트랙 2주 공부 내용을 1~2문단으로 요약해 중앙 보고서에 append |
| `$develop_weekly` | 최근 2주 Git commit 내역을 읽고 개발트랙 작업 내용을 1~2문단으로 요약해 중앙 보고서에 append |

보고서는 계속 업데이트되는 누적 문서입니다.

| 문서 | 설명 |
|---|---|
| `reports/research_weekly.md` | 학술트랙 발표자료 기반 격주 보고 누적 문서 |
| `reports/develop_weekly.md` | 개발트랙 Git commit 기반 격주 보고 누적 문서 |

## 설치 방법

### 방법 1. Codex Marketplace 등록

Codex CLI가 plugin marketplace를 지원하는 경우 아래 명령을 사용합니다.

```bash
codex plugin marketplace add ShinyJay2/opt_ai_skills
```

설치 후 Codex를 재시작합니다.

Codex 버전 확인:

```bash
codex --version
codex plugin marketplace --help
```

`codex plugin marketplace` 명령이 없으면 아래 수동 설치 방법을 사용합니다.

### 방법 2. Codex 수동 설치

```bash
# 1. 레포 클론
git clone https://github.com/ShinyJay2/opt_ai_skills.git
cd opt_ai_skills

# 2. Codex 스킬 디렉토리에 복사
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R plugins/opt-ai-skills/skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
# 또는 scripts/install.sh codex

# 3. Codex 재시작
```

이미 설치된 스킬을 최신화하려면:

```bash
cd opt_ai_skills
git pull
cp -R plugins/opt-ai-skills/skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

### 방법 3. Claude Code 수동 설치

Claude Code에서 `SKILL.md` 기반 스킬을 쓰는 환경이라면 아래처럼 복사합니다.

```bash
git clone https://github.com/ShinyJay2/opt_ai_skills.git
cd opt_ai_skills
mkdir -p "$HOME/.claude/skills"
cp -R claude/skills/* "$HOME/.claude/skills/"
# 또는 scripts/install.sh claude
```

Slash command 방식이 더 익숙하면 `claude/commands/*.md`를 Claude Code 명령 디렉토리로 복사해 사용할 수 있습니다.

## 사전 준비

### 중앙 레포 write 권한

각 학회원이 보고서를 자동 append/push하려면 `ShinyJay2/opt_ai_skills` 레포에 push 권한이 있거나, fork/PR 방식 운영 규칙이 필요합니다. VS Code에서 사용하는 GitHub 계정/SSH key/credential helper가 이 레포에 push 가능한 상태여야 합니다.

권장 로컬 설정:

```bash
git clone https://github.com/ShinyJay2/opt_ai_skills.git ~/workspace/opt_ai_skills
export OPT_AI_SKILLS_REPO=~/workspace/opt_ai_skills
```

### 발표자료 추출 도구

`$research_weekly`는 Python 표준 라이브러리로 PPTX를 읽고, PDF는 `pdftotext`가 있으면 우선 사용합니다.

```bash
# macOS
brew install poppler

# 선택: Python PDF fallback
python3 -m pip install pypdf
```

PPT는 구버전 binary 형식이라 추출 품질이 낮을 수 있습니다. 가능하면 PPTX 또는 PDF로 export해서 실행합니다.

### Discord 리마인더

GitHub repository secret에 아래 중 하나를 등록합니다.

- `DISCORD_WEBHOOK_URL` 권장
- 또는 `DISCORD_BOT_TOKEN`

대상 채널 기본값:

```text
https://discord.com/channels/1483124596688293899/1483389681239588864
```

## 스킬 상세

### `$research_weekly`

학술트랙 학회원이 2주마다 만든 발표자료를 읽어 공부 내용을 보고합니다. PDF/PPTX/PPT/Markdown/TXT가 담긴 폴더 또는 파일을 입력하면, 자료 내용을 근거로 1~2문단 한국어 요약을 만들고 `reports/research_weekly.md`에 날짜·이름·근거와 함께 append합니다.

사용 예시:

```text
$research_weekly 발표자료는 ./presentation 폴더야. 이름은 홍길동.
$research_weekly /path/to/paper-study.pdf 로 학술트랙 보고 작성해줘
```

내부 흐름:

1. 학회원 이름 확인
2. 발표자료 파일/폴더 확인
3. 자료 텍스트 추출
4. Codex/Claude가 1~2문단 보고 요약 작성
5. 중앙 레포 보고서 append
6. append commit 생성 및 push

주의:

- 이름이 없으면 먼저 물어봅니다.
- 자료 추출이 부족하면 PPTX/PDF 변환을 안내합니다.
- 근거 없이 학습 내용을 상상해서 쓰지 않습니다.

### `$develop_weekly`

개발트랙 학회원의 최근 2주 commit 내역을 읽어 개발 내용을 보고합니다. 현재 Git 레포 또는 지정한 레포에서 commit log를 수집하고, 구현/수정/리팩터링/검증 작업을 1~2문단으로 묶어 `reports/develop_weekly.md`에 append합니다.

사용 예시:

```text
$develop_weekly 이름은 김개발. 현재 레포 기준 최근 2주 보고 작성해줘
$develop_weekly --since 2026-06-01 --author "dev@example.com"
```

내부 흐름:

1. 학회원 이름 확인
2. Git 레포/기간/author 확인
3. commit log 수집
4. Codex/Claude가 1~2문단 보고 요약 작성
5. 중앙 레포 보고서 append
6. append commit 생성 및 push

주의:

- commit이 없으면 보고서를 append하지 않고 기간/author 확인을 요청합니다.
- raw commit 제목 나열 대신 개발 흐름으로 요약합니다.
- 여러 레포를 작업했다면 레포별 evidence를 모아 한 보고로 통합할 수 있습니다.

## 리마인더 봇

격주 금요일 12:00 KST 기준으로 GitHub Actions가 실행되고, `scripts/reminder_bot.py`가 격주 여부를 검사한 뒤 Discord에 보고 요청 메시지를 보냅니다.

```bash
# 로컬 테스트
DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...' python scripts/reminder_bot.py --dry-run --force
```

위 명령은 dry-run입니다. 실제 Discord에 보내려면 의도적으로 `--dry-run`을 제거합니다.

카카오톡은 공식 단톡방 incoming webhook이 없어 GitHub-hosted Actions에서 바로 쓰기 어렵습니다. 다만 OAuth 기반 Kakao MCP, macOS 카카오톡 자동화 MCP, Kakao Business 경로가 있으므로 `docs/kakaotalk-options.md`에 선택지를 정리했습니다. 현재 기본값은 Discord이고, 카카오톡은 self-hosted macOS runner + `kmsg` 방식도 함께 제공합니다. 자세한 구축 절차는 `docs/kakaotalk-self-hosted-runner.md`를 참고하세요. 자세한 내용은 `docs/reminder-bot.md`를 참고하세요.

## 공유 및 업데이트 절차

레포 변경 후 팀에 공유하려면:

```bash
git status
git add .
git commit -m "Update OPT-AI skills"
git push origin main
```

Teammate는 marketplace 등록을 사용한 경우:

```bash
codex plugin marketplace upgrade
```

수동 설치를 사용한 경우:

```bash
cd opt_ai_skills
git pull
cp -R plugins/opt-ai-skills/skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Claude Code 수동 설치를 사용한 경우:

```bash
cd opt_ai_skills
git pull
cp -R claude/skills/* "$HOME/.claude/skills/"
# 또는 scripts/install.sh claude
```

업데이트 후 Codex 또는 Claude Code를 재시작합니다.

## 문제 해결

### `codex plugin marketplace` 명령이 없음

Codex CLI가 오래된 버전일 수 있습니다.

```bash
codex update
codex plugin marketplace --help
```

업데이트가 어렵다면 수동 설치 방법을 사용합니다.

### 스킬이 Codex에 나타나지 않음

1. Codex를 재시작합니다.
2. `~/.codex/skills`에 스킬 폴더가 있는지 확인합니다.
3. `SKILL.md` frontmatter의 `name`이 올바른지 확인합니다.

```bash
find "${CODEX_HOME:-$HOME/.codex}/skills" -maxdepth 2 -name SKILL.md
```

### 중앙 보고서 push 실패

- `OPT_AI_SKILLS_REPO`가 올바른 clone을 가리키는지 확인합니다.
- GitHub 계정에 `ShinyJay2/opt_ai_skills` write 권한이 있는지 확인합니다.
- 권한이 없다면 fork 후 PR 방식으로 운영합니다.

### `$research_weekly`에서 PDF 내용이 비어 있음

```bash
brew install poppler
python3 -m pip install pypdf
```

그래도 부족하면 발표자료를 PPTX 또는 텍스트 포함 PDF로 다시 export합니다.

### Discord 리마인더가 오지 않음

1. GitHub Actions가 enabled인지 확인합니다.
2. `DISCORD_WEBHOOK_URL` secret이 등록되어 있는지 확인합니다.
3. Actions 탭에서 `Biweekly OPT-AI report reminder` workflow를 수동 실행합니다.
4. `REMINDER_ANCHOR_DATE` 기준 격주 gate에 걸리지 않았는지 확인합니다.

### Secret 보호

이 레포에는 Discord webhook, bot token, OAuth client secret을 포함하지 않습니다. `.env`, `client_secret.json`, `*.pem`, `*.key`는 commit하지 않습니다.

## 라이선스

MIT
