# Contributing

## 보고서 append 운영 규칙

- `reports/research_weekly.md`와 `reports/develop_weekly.md`는 append-only 문서로 운영합니다.
- 기존 학회원의 보고 항목은 오탈자 수정 외에는 삭제하지 않습니다.
- push 권한이 없는 학회원은 fork 후 PR로 보고 항목을 제출합니다.
- 충돌이 나면 `git pull --rebase` 후 같은 항목을 다시 append합니다.

## Secret 규칙

- Discord webhook, bot token, OAuth client secret, private key는 commit하지 않습니다.
- GitHub Actions secret 또는 개인 로컬 설정에만 저장합니다.

## Skill 수정 검증

```bash
python3 -m py_compile plugins/opt-ai-skills/skills/research_weekly/scripts/opt_report.py \
  plugins/opt-ai-skills/skills/develop_weekly/scripts/opt_report.py \
  scripts/reminder_bot.py \
  scripts/test_opt_ai_skills.py
python3 scripts/test_opt_ai_skills.py
python3 /Users/jaehoon/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/opt-ai-skills
```

## KakaoTalk runner 검증

카카오톡 self-hosted runner 변경 시 `python3 scripts/test_opt_ai_skills.py`가 `kakao-kmsg` dry-run command 생성까지 검증합니다. 실제 운영 Mac에서는 `kmsg status`와 `python3 scripts/reminder_bot.py --transport kakao-kmsg --dry-run --force`를 추가로 실행합니다.
