# KakaoTalk Reminder Options

이 문서는 OPT-AI 격주 보고 리마인더를 카카오톡으로 보낼 수 있는지 검토한 결과입니다.

## 결론

카카오톡 리마인더는 가능성이 있지만, 운영 방식에 따라 제약이 큽니다.

| 경로 | 가능 여부 | 적합도 | 비고 |
|---|---:|---:|---|
| Discord webhook / bot | 가능 | 높음 | GitHub Actions에서 가장 안정적 |
| Kakao Developers Message API 기반 MCP | 일부 가능 | 중간 | OAuth, 친구 UUID, 권한 심사 필요. 단톡방 직접 자동 발송에는 부적합 |
| macOS KakaoTalk 자동화 MCP (`kmsg-mcp`류) | 가능 | 중간 | 로그인된 macOS + 카카오톡 앱 + 접근성 권한 필요. GitHub-hosted Actions에는 부적합 |
| KakaoTalk Share | 사용자 액션 필요 | 낮음 | 사용자가 공유 대상을 선택하는 구조. 자동 리마인더 발송용이 아님 |
| Kakao Business/알림톡/채널 | 가능성 있음 | 중간 | 비즈니스 채널/템플릿/심사/유료 또는 대행사 연동 필요 |

## 1. 공식 Kakao Talk Message API 제약

Kakao Developers의 Kakao Talk Message API는 같은 서비스 사용자 간 메시지 또는 나에게 보내기 중심입니다. 친구에게 보내려면 Kakao Talk Social API 권한, 친구 목록 동의, 메시지 전송 동의, 추가 권한 심사가 필요합니다. 공식 문서상 서비스가 임의로 사용자에게 직접 메시지를 보내는 용도는 KakaoTalk Message/Share보다 Brand Message, Info Talk, CS Talk 같은 비즈니스 상품 영역입니다.

즉, 학회 단톡방에 GitHub Actions가 자동으로 “격주 보고하세요”를 보내는 webhook 같은 단순 모델은 공식 Developers API만으로는 맞지 않습니다.

## 2. MCP 후보

### 2.1 OAuth 기반 KakaoTalk Remote MCP

커뮤니티 MCP 중에는 Kakao OAuth로 로그인하고 다음 도구를 제공하는 구현이 있습니다.

- `send_message_to_me`
- `send_message`
- `search_kakao_friends`

장점:

- 공식 Kakao OAuth/Message API 흐름에 가깝습니다.
- 개인/친구 대상 메시지 발송은 MCP tool로 추상화할 수 있습니다.

제약:

- Kakao Developers 앱 설정, redirect URL, OAuth token 저장소, ngrok/공개 callback URL이 필요합니다.
- 친구 UUID 기반이라 단톡방 채팅방 ID로 “단톡방에 직접 전송”하는 운영과는 다릅니다.
- 권한 심사 전에는 앱 팀 멤버 중심으로 제한될 수 있습니다.

### 2.2 macOS KakaoTalk 자동화 MCP (`kmsg-mcp`류)

macOS 카카오톡 앱을 Accessibility API로 제어해 Claude Code/MCP에서 메시지를 보내는 구현도 있습니다.

장점:

- 실제 카카오톡 앱의 대화방을 대상으로 자동화할 수 있어 단톡방 리마인더에 가장 가까운 경험을 만들 수 있습니다.
- 공식 API의 친구 UUID/서비스 사용자 제약을 우회하지 않고, 로컬 사용자의 카카오톡 클라이언트를 자동화합니다.

제약:

- 로그인된 macOS 세션, 카카오톡 데스크톱 앱, 접근성 권한이 필요합니다.
- GitHub-hosted Actions에서는 실행할 수 없습니다.
- self-hosted macOS runner 또는 항상 켜져 있는 운영 Mac이 필요합니다.

## 3. 권장 운영안

### 지금 바로 운영

Discord webhook을 기본 리마인더로 사용합니다.

```bash
DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...' python scripts/reminder_bot.py --dry-run --force
```

### 카카오톡 단톡방을 꼭 써야 할 때

아래 중 하나를 선택합니다.

1. **self-hosted macOS runner + KakaoTalk 자동화 MCP/kmsg**
   - 운영 Mac에 카카오톡 로그인
   - 접근성 권한 부여
   - `kmsg send --chat-id ...` 또는 MCP/CLI로 단톡방에 메시지 전송
   - GitHub Actions workflow를 self-hosted runner로 실행
   - 구체 절차: `docs/kakaotalk-self-hosted-runner.md`

2. **OAuth 기반 Kakao MCP + 개인/친구 대상 알림**
   - 학회원이 서비스 사용자로 OAuth 동의
   - 친구 UUID 기반 발송
   - 단톡방 리마인더가 아니라 개인 DM 리마인더에 적합

3. **Kakao Business 알림톡/채널**
   - 비즈니스 채널과 템플릿 심사 필요
   - 학회 내부 단톡방보다 공식 공지/알림성 메시지에 적합

## 4. 이 레포의 현재 결정

현재 기본 구현은 Discord와 self-hosted macOS `kakao-kmsg` transport입니다.

- GitHub-hosted Actions 또는 운영 Mac이 없을 때: `REMINDER_TRANSPORT=discord`
- 카카오톡 단톡방 운영 Mac이 있을 때: `REMINDER_TRANSPORT=kakao-kmsg`
- `kakao-kmsg` 필수 설정: `KAKAOTALK_CHAT_ID` 또는 `KAKAOTALK_CHAT_NAME`
- 실제 절차: `docs/kakaotalk-self-hosted-runner.md`

OAuth 기반 Kakao MCP는 개인/친구 대상 알림을 위한 별도 미래 옵션이며, 현재 단톡방 리마인더 구현명은 `kakao-kmsg`입니다.
