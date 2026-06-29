# Reminder Bot

현재 운영 기준은 **카카오톡 단톡방 리마인더**입니다.

- 시간: 2주마다 금요일 12:00 KST
- 기준일: 2026-07-03
- 방식: GitHub Actions → self-hosted macOS runner → KakaoTalk.app → `kmsg`
- 메시지는 운영 Mac에 로그인된 카카오톡 프로필로 전송됩니다.

## KakaoTalk 운영 경로

자동 발송 workflow:

```text
.github/workflows/biweekly-kakaotalk-reminder.yml
```

동작 방식:

1. GitHub Actions가 매주 금요일 12:00 KST에 self-hosted Mac runner에서 실행됩니다.
2. `scripts/reminder_bot.py`가 `REMINDER_ANCHOR_DATE=2026-07-03` 기준으로 격주 여부를 검사합니다.
3. 발송 주차이면 `kmsg`로 카카오톡 단톡방에 메시지를 보냅니다.
4. 발송 주차가 아니면 아무 메시지도 보내지 않고 종료합니다.

필요한 repo variable:

- `KAKAOTALK_CHAT_ID` 권장
- 또는 `KAKAOTALK_CHAT_NAME`

로컬 dry-run:

```bash
KAKAOTALK_CHAT_ID='chat_xxx' python3 scripts/reminder_bot.py --transport kakao-kmsg --dry-run --force
```

운영 Mac 설정 절차는 `docs/kakaotalk-self-hosted-runner.md`를 참고하세요.

## Discord fallback

Discord는 카카오톡이 안 될 때 수동으로 사용할 fallback입니다.

Fallback workflow:

```text
.github/workflows/biweekly-reminder.yml
```

이 workflow는 **자동 schedule이 꺼져 있고**, Actions에서 직접 수동 실행할 때만 동작합니다.

필요한 GitHub repository secret:

- `DISCORD_WEBHOOK_URL` 권장
- 또는 `DISCORD_BOT_TOKEN`

대상 채널 기본값:

```text
https://discord.com/channels/1483124596688293899/1483389681239588864
```

로컬 dry-run:

```bash
DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...' python3 scripts/reminder_bot.py --transport discord --dry-run --force
```

실제 Discord에 보내려면 의도적으로 `--dry-run`을 제거합니다.

## KakaoTalk MCP 참고

카카오톡 MCP는 “불가능”이 아니라 운영 형태가 갈립니다. 자세한 검토는 `docs/kakaotalk-options.md`를 참고하세요.

- 공식 Kakao Developers Message API 기반 MCP: OAuth, 친구 UUID, 권한 심사가 필요하며 단톡방 직접 자동 발송에는 맞지 않습니다.
- macOS KakaoTalk 자동화 MCP: 실제 단톡방 전송에 가장 가깝지만 로그인된 macOS, 카카오톡 앱, 접근성 권한, self-hosted runner가 필요합니다.
- Kakao Business/알림톡: 공식 대량/공지성 메시지에는 가능성이 있지만 비즈니스 채널·템플릿 심사가 필요합니다.
