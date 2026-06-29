#!/usr/bin/env python3
"""Biweekly OPT-AI reporting reminder.

Transports:
- discord: GitHub-hosted Actions friendly webhook/bot token path.
- kakao-kmsg: self-hosted macOS runner path using KakaoTalk.app + kmsg CLI.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request

DEFAULT_CHANNEL_ID = "1483389681239588864"
DEFAULT_ANCHOR = "2026-07-06"  # Monday KST anchor; adjust in workflow/env if needed.


def is_biweekly_due(today: dt.date, anchor: str) -> bool:
    start = dt.date.fromisoformat(anchor)
    weeks = (today - start).days // 7
    return weeks >= 0 and weeks % 2 == 0


def post_json(url: str, payload: dict, headers: dict | None = None) -> None:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as resp:  # nosec: configured URL secret
        if resp.status >= 300:
            raise RuntimeError(f"HTTP {resp.status}: {resp.read().decode('utf-8', errors='replace')}")


def send_discord(message: str, channel_id: str) -> str:
    webhook = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook:
        post_json(webhook, {"content": message})
        return "discord-webhook"
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if token:
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        post_json(url, {"content": message}, {"Authorization": f"Bot {token}"})
        return "discord-bot"
    raise RuntimeError("Set DISCORD_WEBHOOK_URL or DISCORD_BOT_TOKEN for Discord transport.")


def send_kakao_kmsg(message: str, dry_run: bool = False) -> str:
    kmsg_bin = os.environ.get("KMSG_BIN", "kmsg")
    chat_id = os.environ.get("KAKAOTALK_CHAT_ID")
    chat_name = os.environ.get("KAKAOTALK_CHAT_NAME")
    if not chat_id and not chat_name:
        raise RuntimeError("Set KAKAOTALK_CHAT_ID or KAKAOTALK_CHAT_NAME for kakao-kmsg transport.")
    if chat_id:
        cmd = [kmsg_bin, "send", "--chat-id", chat_id, message]
        target = f"chat-id:{chat_id}"
    else:
        cmd = [kmsg_bin, "send", chat_name or "", message]
        target = f"chat-name:{chat_name}"
    if dry_run:
        cmd.append("--dry-run")
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"kmsg send failed ({proc.returncode})\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return f"kakao-kmsg:{target}"


def default_message() -> str:
    return os.environ.get("REMINDER_MESSAGE") or (
        "OPT-AI 격주 보고 리마인더입니다.\n"
        "학술트랙: 발표자료 PDF/PPT 폴더에서 `$research_weekly` 실행 후 보고서를 append 해주세요.\n"
        "개발트랙: 작업 레포에서 `$develop_weekly` 실행 후 최근 2주 커밋 기반 보고서를 append 해주세요.\n"
        "중앙 레포: https://github.com/ShinyJay2/opt_ai_skills"
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Send OPT-AI biweekly report reminders")
    p.add_argument("--transport", choices=["discord", "kakao-kmsg"], default=os.environ.get("REMINDER_TRANSPORT", "discord"))
    p.add_argument("--channel-id", default=os.environ.get("DISCORD_CHANNEL_ID", DEFAULT_CHANNEL_ID))
    p.add_argument("--anchor-date", default=os.environ.get("REMINDER_ANCHOR_DATE", DEFAULT_ANCHOR))
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--message", default=default_message())
    args = p.parse_args()
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).date()
    if not args.force and not is_biweekly_due(today, args.anchor_date):
        print(f"Not a reminder week: today={today}, anchor={args.anchor_date}")
        return 0
    if args.dry_run and args.transport == "discord":
        print(args.message)
        return 0
    if args.transport == "discord":
        method = send_discord(args.message, args.channel_id)
    elif args.transport == "kakao-kmsg":
        method = send_kakao_kmsg(args.message, dry_run=args.dry_run)
    else:  # pragma: no cover; argparse enforces choices
        raise RuntimeError(f"Unsupported transport: {args.transport}")
    print(f"Sent reminder via {method}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
