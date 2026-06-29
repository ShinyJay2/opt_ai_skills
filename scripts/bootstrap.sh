#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-codex}"
REPO_URL="${OPT_AI_SKILLS_REPO_URL:-https://github.com/ShinyJay2/opt_ai_skills.git}"
BASE_DIR="${OPT_AI_SKILLS_HOME:-$HOME/.opt-ai-skills}"
REPO_DIR="$BASE_DIR/repo"

case "$TARGET" in
  codex|claude|both) ;;
  *)
    echo "Usage: bootstrap.sh [codex|claude|both]" >&2
    exit 2
    ;;
esac

if ! command -v git >/dev/null 2>&1; then
  echo "git이 필요합니다. 먼저 Git을 설치해 주세요." >&2
  exit 1
fi

mkdir -p "$BASE_DIR"
if [ -d "$REPO_DIR/.git" ]; then
  echo "OPT-AI 스킬 레포 업데이트 중: $REPO_DIR"
  git -C "$REPO_DIR" pull --ff-only
else
  echo "OPT-AI 스킬 레포 받는 중: $REPO_DIR"
  git clone "$REPO_URL" "$REPO_DIR"
fi

"$REPO_DIR/scripts/install.sh" "$TARGET"

cat <<MSG

완료되었습니다.
1. Codex 또는 Claude Code를 재시작하세요.
2. 개발트랙: 본인 개발 레포에서 \$develop_weekly 를 실행하세요.
3. 학술트랙: 발표자료 폴더에서 \$research_weekly 를 실행하세요.

보고서 push가 실패하면 GitHub 초대 수락/로그인 상태를 확인하세요.
MSG
