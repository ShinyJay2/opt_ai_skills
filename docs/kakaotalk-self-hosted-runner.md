# KakaoTalk Self-hosted Runner Setup

이 문서는 운영 Mac 한 대를 GitHub Actions self-hosted runner로 두고, macOS KakaoTalk 자동화 CLI인 `kmsg`로 OPT-AI 단톡방에 격주 보고 리마인더를 보내는 절차입니다.

## 전체 구조

```text
GitHub Actions schedule
  → self-hosted macOS runner
  → scripts/reminder_bot.py --transport kakao-kmsg
  → kmsg send "단톡방 이름" "리마인더 메시지"
  → KakaoTalk.app 단톡방 전송
```

## 0. 전제와 주의

- 이 방식은 공식 KakaoTalk webhook이 아니라 **로그인된 macOS KakaoTalk 앱을 자동화**하는 방식입니다.
- 운영 Mac은 잠자기 상태가 아니어야 하며, KakaoTalk 로그인 상태를 유지해야 합니다.
- `kmsg`는 Kakao Corp. 공식 도구가 아니므로 학회/조직 정책과 카카오톡 이용약관 리스크를 확인해야 합니다.
- GitHub-hosted runner에서는 카카오톡 앱/접근성 권한을 유지할 수 없으므로 self-hosted Mac이 필요합니다.

## 1. 운영 Mac 준비

권장:

- macOS 13 이상
- 항상 켜져 있는 Mac mini 또는 MacBook
- KakaoTalk.app 설치 및 로그인
- 화면 잠금/잠자기 정책 완화

```bash
# 예시: 절전 방지. 조직 정책에 맞게 조정하세요.
sudo pmset -a sleep 0 displaysleep 30 disksleep 0
```

## 2. kmsg 설치

Homebrew가 있으면:

```bash
brew install channprj/tap/kmsg
```

직접 다운로드 방식:

```bash
mkdir -p ~/.local/bin
curl -fL https://github.com/channprj/kmsg/releases/latest/download/kmsg-macos-universal \
  -o ~/.local/bin/kmsg
chmod +x ~/.local/bin/kmsg
export PATH="$HOME/.local/bin:$PATH"
```

설치 확인:

```bash
kmsg status
```

권한 팝업이 뜨면 허용합니다. macOS 설정에서 다음 권한을 확인합니다.

- System Settings → Privacy & Security → Accessibility
- Terminal 또는 runner를 실행할 앱/서비스에 권한 부여
- 필요 시 Automation/Screen Recording 권한도 확인

## 3. 단톡방 식별

먼저 채팅방 목록을 확인합니다.

```bash
kmsg chats --json
```

가능하면 단톡방 이름보다 `chat_id`를 쓰는 것을 권장합니다.

```bash
# 실제 전송 전 dry-run
kmsg send --chat-id "chat_xxxxx" "OPT-AI 리마인더 테스트" --dry-run

# 실제 전송
kmsg send --chat-id "chat_xxxxx" "OPT-AI 리마인더 테스트"
```

단톡방 이름으로도 가능합니다.

```bash
kmsg send "OPT-AI 단톡방" "OPT-AI 리마인더 테스트" --dry-run
```

## 4. GitHub self-hosted runner 등록

GitHub 공식 경로:

1. GitHub repo → Settings → Actions → Runners
2. `New self-hosted runner`
3. OS는 macOS, architecture는 운영 Mac에 맞게 선택
4. 화면에 나오는 Download/Configure 명령을 운영 Mac에서 실행
5. label에 최소 아래를 포함합니다.

```text
self-hosted, macOS, kakaotalk
```

runner는 GUI 세션과 카카오톡 접근성 권한을 안정적으로 쓰기 위해 운영 사용자 계정에서 실행하는 것을 권장합니다.

```bash
# GitHub가 안내한 runner 디렉토리에서
./run.sh
```

장기 운영은 macOS LaunchAgent로 등록할 수 있지만, 처음에는 `./run.sh` foreground로 테스트하세요.

## 5. GitHub repo variables 설정

GitHub repo → Settings → Secrets and variables → Actions → Variables 에 등록합니다.

둘 중 하나를 사용합니다.

```text
KAKAOTALK_CHAT_ID=chat_xxxxx
```

또는

```text
KAKAOTALK_CHAT_NAME=OPT-AI 단톡방 이름
```

`chat_id`가 더 안정적입니다.

## 6. Workflow 테스트

이 레포에는 `.github/workflows/biweekly-kakaotalk-reminder.yml`가 포함되어 있습니다.

1. Actions 탭 → `Biweekly OPT-AI KakaoTalk reminder`
2. `Run workflow`
3. 처음에는 `dry_run=true`, `force=true`
4. 로그에서 `kmsg status`와 `kmsg send ... --dry-run` 성공 확인
5. 실제 전송은 `dry_run=false`, `force=true`로 한 번만 테스트

## 7. 로컬 직접 테스트

```bash
export KAKAOTALK_CHAT_ID="chat_xxxxx"
python3 scripts/reminder_bot.py --transport kakao-kmsg --dry-run --force

# 실제 전송
python3 scripts/reminder_bot.py --transport kakao-kmsg --force
```

## 문제 해결

### runner가 job을 잡지 않음

- repo Settings → Actions → Runners에서 runner가 Online인지 확인
- workflow의 `runs-on: [self-hosted, macOS, kakaotalk]`와 runner label이 일치하는지 확인

### `kmsg status`가 실패

- KakaoTalk.app 설치/로그인 확인
- 운영 Mac의 Accessibility 권한 확인
- runner가 Terminal과 다른 서비스 계정에서 실행 중인지 확인

### 채팅방을 못 찾음

- `kmsg chats --json`로 chat_id를 확보
- 단톡방 이름이 중복되면 `KAKAOTALK_CHAT_ID` 사용
- 카카오톡 창이 이상한 상태면 KakaoTalk 재시작 후 `kmsg status` 재실행

### GitHub-hosted runner로 실행하고 싶음

불가능에 가깝습니다. GitHub-hosted runner는 KakaoTalk.app 로그인 세션과 macOS Accessibility 권한을 지속적으로 유지할 수 없습니다. Discord workflow를 사용하세요.
