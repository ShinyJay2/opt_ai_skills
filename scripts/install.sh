#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-codex}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case "$TARGET" in
  codex)
    mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
    cp -R "$ROOT/plugins/opt-ai-skills/skills/"* "${CODEX_HOME:-$HOME/.codex}/skills/"
    echo "Installed OPT-AI skills to ${CODEX_HOME:-$HOME/.codex}/skills"
    ;;
  claude)
    mkdir -p "$HOME/.claude/skills" "$HOME/.claude/commands"
    cp -R "$ROOT/claude/skills/"* "$HOME/.claude/skills/"
    cp -R "$ROOT/claude/commands/"* "$HOME/.claude/commands/"
    echo "Installed OPT-AI skills to $HOME/.claude/skills"
    echo "Installed OPT-AI Claude commands to $HOME/.claude/commands"
    ;;
  both)
    "$0" codex
    "$0" claude
    ;;
  *)
    echo "Usage: scripts/install.sh [codex|claude|both]" >&2
    exit 2
    ;;
esac
