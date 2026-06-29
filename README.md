# OPT-AI Codex / Claude Skills

OPT-AI 학회 보고를 쉽게 하기 위한 스킬 모음입니다.

- **학술트랙**: PDF/PPT/PPTX 발표자료를 읽고 2주 공부 내용을 요약합니다.
- **개발트랙**: 본인 개발 레포의 최근 2주 commit을 읽고 개발 내용을 요약합니다.
- 결과는 이 레포의 누적 문서에 자동으로 추가됩니다.
- 리마인더는 **2주마다 금요일 12:00 KST**에 카카오톡 단톡방으로 올라가도록 운영합니다.

현재 버전: **v0.1.1**

---

## 학회원 Quickstart

처음 쓰는 사람은 아래만 따라 하면 됩니다.

### 1. GitHub 초대 수락

운영자가 `ShinyJay2/opt_ai_skills` 레포 초대를 보내면 먼저 수락하세요.

> 이걸 해야 보고서가 GitHub 문서에 올라갑니다.

### 2. 스킬 설치

Codex를 쓰면 터미널에 아래 한 줄을 복사해서 실행하세요.

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ShinyJay2/opt_ai_skills/main/scripts/bootstrap.sh)" codex
```

Claude Code를 쓰면 마지막만 `claude`로 바꿉니다.

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ShinyJay2/opt_ai_skills/main/scripts/bootstrap.sh)" claude
```

둘 다 쓰면:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ShinyJay2/opt_ai_skills/main/scripts/bootstrap.sh)" both
```

설치가 끝나면 **Codex / Claude Code를 재시작**하세요.

### 3. 보고하기

#### 학술트랙

발표자료가 있는 폴더를 VS Code로 열고 실행합니다.

```text
$research_weekly
```

Claude Code에서는 `/research_weekly` 또는 `research_weekly`로 실행하면 됩니다.

또는 자료 위치와 이름을 같이 적어도 됩니다.

```text
$research_weekly 발표자료는 ./presentation 폴더야. 이름은 홍길동.
```

스킬이 하는 일:

1. 이름을 확인합니다.
2. PDF/PPT/PPTX 내용을 읽습니다.
3. 1~2문단으로 공부 내용을 요약합니다.
4. `reports/research_weekly.md`에 추가합니다.

#### 개발트랙

본인 개발 레포를 VS Code로 열고 실행합니다.

```text
$develop_weekly
```

Claude Code에서는 `/develop_weekly` 또는 `develop_weekly`로 실행하면 됩니다.

또는 이름을 같이 적어도 됩니다.

```text
$develop_weekly 이름은 김개발.
```

스킬이 하는 일:

1. 이름을 확인합니다.
2. 현재 레포의 최근 14일 commit을 읽습니다.
3. 1~2문단으로 개발 내용을 요약합니다.
4. `reports/develop_weekly.md`에 추가합니다.

---

## 이름은 어떻게 입력하나요?

이름을 프롬프트에 적으면 그대로 사용합니다.

```text
$develop_weekly 이름은 김개발.
```

이름을 안 적으면 스킬이 먼저 물어봅니다.

한 번 저장해두고 싶으면:

```bash
python3 ~/.codex/skills/develop_weekly/scripts/opt_report.py identify-member --remember
```

저장된 이름은 다음 실행부터 자동으로 사용됩니다.

---

## GitHub 로그인이 안 되어 있으면

보고서가 내 컴퓨터에서는 만들어졌는데 GitHub에 안 올라갈 수 있습니다.

그럴 때는 아래 중 하나만 하면 됩니다.

### 쉬운 방법: VS Code에서 GitHub 로그인

VS Code 왼쪽 아래 계정 아이콘에서 GitHub에 로그인하세요.

### 터미널 방법

GitHub CLI가 있으면:

```bash
gh auth login
```

잘 모르겠으면 운영자에게 “보고서 push가 실패했다”고 말하면 됩니다.

---

## 업데이트 방법

스킬이 업데이트되면 아래 명령을 다시 실행하면 됩니다.

Codex:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ShinyJay2/opt_ai_skills/main/scripts/bootstrap.sh)" codex
```

Claude Code:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ShinyJay2/opt_ai_skills/main/scripts/bootstrap.sh)" claude
```

---

## 리마인더

운영 Mac에서 자동으로 카카오톡 단톡방에 리마인더를 보냅니다.

- 시간: **2주마다 금요일 12:00 KST**
- 기준일: **2026-07-03**
- 방식: GitHub Actions → self-hosted macOS runner → KakaoTalk `kmsg`
- 메시지는 운영 Mac에 로그인된 카카오톡 프로필로 전송됩니다.

학회원은 따로 설정할 것이 없습니다.

Discord 리마인더도 fallback으로 남겨두었습니다.

---

## 보고서 위치

| 문서 | 내용 |
|---|---|
| `reports/research_weekly.md` | 학술트랙 보고 누적 문서 |
| `reports/develop_weekly.md` | 개발트랙 보고 누적 문서 |

---

## 발표자료 팁

학술트랙은 PDF 또는 PPTX가 가장 잘 됩니다.

PDF 내용이 잘 안 읽히면 아래를 한 번 설치하세요.

```bash
brew install poppler
```

구버전 `.ppt`는 잘 안 읽힐 수 있습니다. 가능하면 `.pptx` 또는 `.pdf`로 저장해서 사용하세요.

---

## 관리자 / 개발자용

### 레포 구조

```text
.agents/plugins/marketplace.json
plugins/opt-ai-skills/.codex-plugin/plugin.json
plugins/opt-ai-skills/skills/
claude/skills/
claude/commands/
reports/
scripts/bootstrap.sh
scripts/install.sh
scripts/reminder_bot.py
.github/workflows/biweekly-kakaotalk-reminder.yml
.github/workflows/biweekly-reminder.yml
```

### 수동 설치

```bash
git clone https://github.com/ShinyJay2/opt_ai_skills.git ~/.opt-ai-skills/repo
~/.opt-ai-skills/repo/scripts/install.sh codex
```

Claude Code:

```bash
~/.opt-ai-skills/repo/scripts/install.sh claude
```

Claude 설치는 `~/.claude/skills`와 `~/.claude/commands`를 함께 업데이트합니다.

### Codex marketplace 설치

Codex CLI가 plugin marketplace를 지원하면 아래도 가능합니다.

```bash
codex plugin marketplace add ShinyJay2/opt_ai_skills
```

지원하지 않으면 위 Quickstart 설치를 사용하세요.

### 테스트

```bash
python3 scripts/test_opt_ai_skills.py
python3 -m py_compile \
  plugins/opt-ai-skills/skills/research_weekly/scripts/opt_report.py \
  plugins/opt-ai-skills/skills/develop_weekly/scripts/opt_report.py \
  scripts/reminder_bot.py \
  scripts/test_opt_ai_skills.py
```

### 관련 문서

- `docs/report-workflow.md`: 보고 흐름
- `docs/reminder-bot.md`: Discord 리마인더 fallback
- `docs/kakaotalk-self-hosted-runner.md`: 카카오톡 runner 설정
- `docs/kakaotalk-options.md`: 카카오톡 연동 선택지

---

## 자주 묻는 질문

### `$research_weekly`나 `$develop_weekly`가 안 보여요

1. Codex / Claude Code를 재시작하세요.
2. 그래도 안 되면 Quickstart 설치 명령을 다시 실행하세요.

### 보고서 push가 실패해요

대부분은 GitHub 권한 또는 로그인 문제입니다.

1. 운영자 초대를 수락했는지 확인하세요.
2. VS Code 또는 `gh auth login`으로 GitHub에 로그인하세요.
3. 계속 안 되면 운영자에게 말하세요.

### 개발트랙은 어떤 commit을 보나요?

기본은 **현재 레포의 최근 14일 commit 전체**입니다.

학회원 각자가 자기 레포에서 실행하는 것을 기준으로 만들었습니다.

### 학술트랙 자료를 못 읽어요

PDF/PPTX로 다시 저장해서 실행하세요. PDF는 `brew install poppler`를 설치하면 더 잘 읽습니다.

---

## 라이선스

MIT
