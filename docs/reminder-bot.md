# Reminder Bot

## 권장 경로: Discord

Discord는 webhook 또는 bot token으로 GitHub Actions에서 안정적으로 격주 리마인더를 보낼 수 있습니다.

대상 채널:

```text
https://discord.com/channels/1483124596688293899/1483389681239588864
```

### 설정

1. GitHub repository secrets에 둘 중 하나를 등록합니다.
   - `DISCORD_WEBHOOK_URL` 권장
   - 또는 `DISCORD_BOT_TOKEN`
2. `.github/workflows/biweekly-reminder.yml`가 매주 금요일 12:00 KST에 실행됩니다.
3. `scripts/reminder_bot.py`가 `REMINDER_ANCHOR_DATE` 기준 격주인지 검사하고, 해당 주에만 메시지를 보냅니다.
4. 즉시 테스트하려면 Actions의 `workflow_dispatch`를 실행하거나 로컬에서 실행합니다.

```bash
DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...' python scripts/reminder_bot.py --dry-run --force
```

위 명령은 dry-run입니다. 실제 Discord에 보내려면 의도적으로 `--dry-run`을 제거합니다.

## KakaoTalk MCP 경로

카카오톡 MCP는 “불가능”이 아니라 운영 형태가 갈립니다. 자세한 검토는 `docs/kakaotalk-options.md`를 참고하세요.

- 공식 Kakao Developers Message API 기반 MCP: OAuth, 친구 UUID, 권한 심사가 필요하며 단톡방 직접 자동 발송에는 맞지 않습니다.
- macOS KakaoTalk 자동화 MCP: 실제 단톡방 전송에 가장 가깝지만 로그인된 macOS, 카카오톡 앱, 접근성 권한, self-hosted runner가 필요합니다.
- Kakao Business/알림톡: 공식 대량/공지성 메시지에는 가능성이 있지만 비즈니스 채널·템플릿 심사가 필요합니다.

따라서 현재 레포는 GitHub-hosted Actions에서 안정적으로 동작하는 Discord fallback을 기본 구현으로 제공하고, 카카오톡은 self-hosted macOS runner 또는 OAuth MCP가 준비되면 transport를 추가하는 방식으로 확장합니다.

## Self-hosted macOS KakaoTalk runner

단톡방 전송을 실제로 운영하려면 `docs/kakaotalk-self-hosted-runner.md`의 절차를 따릅니다. 이 레포에는 `scripts/reminder_bot.py --transport kakao-kmsg`와 `.github/workflows/biweekly-kakaotalk-reminder.yml`가 포함되어 있습니다.
