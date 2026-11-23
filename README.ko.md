# webapp6

**웹앱 6원칙을 Antigravity CLI(`agy`), Claude Code, Codex에 한 번에 설치하는 스킬 플러그인입니다.**
AI 코딩 에이전트가 웹앱을 만들거나 고치거나 검토할 때 씁니다. 선택 항목으로 카운트업 숫자와
스크롤 애니메이션 규칙이 들어 있습니다.

[English README](README.md) · MIT 라이선스 · v0.1.0

## 6원칙

| # | 원칙 | 지켜야 할 결과 |
|---|---|---|
| 1 | JavaScript를 책임별 모듈로 | 진입점·화면·서비스·공통 기능을 모듈로 나눈다. 배포를 HTML 한 파일로 묶는 것은 괜찮다. |
| 2 | CSS 계층 분리 | 디자인 토큰·기본 스타일·컴포넌트 스타일을 소스에서 나눈다. 이미 이렇게 하는 스타일 체계는 그대로 둔다. |
| 3 | 화면·서비스 책임 경계 | 다른 관례가 없는 새 코드는 책임별 클래스로 나누고, hooks·composables 같은 프로젝트 관례는 유지한다. |
| 4 | 비동기 로딩과 렌더링 | I/O는 `async`/`await`로 처리하고 로딩·빈 값·성공·오류를 구분한다. 취소나 요청 식별자로 이전 요청의 오래된 응답이 최신 화면을 덮어쓰지 않게 한다. |
| 5 | 단일 진입점과 화면 URL | 화면마다 URL이 있고 deep link·새로고침·Back/Forward가 동작하며, 없는 자산·API는 진짜 404를 준다. |
| 6 | 안전한 배포 갱신 | 열려 있던 탭도 바뀐 배포(롤백 포함)를 알아채고, 다음 안전한 이동에서 수락 버튼 없이 대상 URL을 문서 전체로 자동으로 새로 받는다. 초안·저장은 지킨다. |

실제 앱 합격 기준까지 담은 정본은
[`references/webapp-principles.md`](plugins/webapp6/skills/webapp6/references/webapp-principles.md)입니다.

## 선택 항목: 카운트업·스크롤 애니메이션

랜딩·포트폴리오·소개 화면, KPI 요약 영역, 또는 요청할 때만 씁니다. 애니메이션 없이도 내용이 완전해야
하고, 움직임 줄이기 설정을 존중하며, `transform`·`opacity`만 움직입니다. 인쇄와 BFCache 복원에서 내용이
숨지 않게 하고, API로 받는 숫자에 `0`을 자리표시로 쓰지 않으며, 별도 검증 항목을 둡니다.
[`references/motion.md`](plugins/webapp6/skills/webapp6/references/motion.md)를 보세요.

## 설치

### Antigravity CLI (`agy`)

```sh
agy plugin install https://github.com/Technoetic/webapp6/tree/main/plugins/webapp6
```

이 릴리스에 고정: `https://github.com/Technoetic/webapp6/tree/v0.1.0/plugins/webapp6`

### Claude Code

```sh
claude plugin marketplace add Technoetic/webapp6
claude plugin install webapp6@technoetic-webapp6
```

Claude Code 2.1.275 이상에서는 세션 안에서 한 번에 설치할 수도 있습니다:
`/plugin install webapp6 --marketplace Technoetic/webapp6`

### Codex

```sh
codex plugin marketplace add Technoetic/webapp6
codex plugin add webapp6@technoetic-webapp6
```

## 사용

| 호스트 | 부르는 법 |
|---|---|
| Claude Code | `/webapp6:webapp6 결제 화면 검토해 줘` (웹앱 작업이면 스킬이 스스로 불리기도 합니다) |
| Codex | `$webapp6:webapp6 결제 화면 검토해 줘` |
| Antigravity CLI | `/webapp6 결제 화면 검토해 줘` (Antigravity 문서 기준. 웹앱 작업이면 스스로 불리기도 합니다) |

대상을 적지 않으면 스킬은 지금 대화의 웹앱 작업에 적용하라고 지시합니다. 그런 작업이 없으면 앱을 새로
만들지 말고 규칙과 부르는 법만 설명하라고 지시합니다.

## 하는 일과 하지 않는 일

- 아이콘 PNG 하나 말고는 글만 들어 있습니다. 스킬 하나(`SKILL.md`), 참고 문서 두 개, 에이전트 표시 파일(`agents/openai.yaml`), 매니페스트, README, 라이선스이며 스크립트·훅·MCP 서버·네트워크 호출이 없습니다.
- 스킬은 에이전트에게 스스로 설치·배포·호스트 설정 변경을 하지 말고, 배포는 사용자가 정한 곳과 범위에서만 하라고 지시합니다. 호스트의 권한·승인 절차는 그대로 적용됩니다.
- 스킬은 에이전트에게 실제로 검증한 것과 검증하지 못한 것을 나눠 보고하라고 지시합니다. 호스트가 이 스킬을 고르는지, 에이전트가 지키는지는 보장되지 않습니다. 스킬이 발견됐다는 것은 전달을 뜻할 뿐 준수를 증명하지 않습니다.

## 출처

6원칙은 [Technoetic/agentic-vault](https://github.com/Technoetic/agentic-vault)의 `docs/webapp-principles.md`(MIT)를
따로 설치할 수 있게 옮긴 것입니다.

## 라이선스

[MIT](LICENSE)
