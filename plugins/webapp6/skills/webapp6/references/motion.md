# 선택 항목: 카운트업·스크롤 애니메이션 / Optional: count-up and scroll animations

랜딩·포트폴리오·소개 화면, 요약 지표(KPI) 영역, 또는 사용자가 요청한 경우에만 쓴다.
업무 입력 화면, 표, 실시간으로 바뀌는 값에는 넣지 않는다.
[6원칙](webapp-principles.md)과 부딪히면 6원칙이 우선한다.

Use these rules only for landing, portfolio, and introduction pages, KPI summary areas, or when the
user asks. Do not add motion to data-entry screens, tables, or live values. The six principles win
any conflict.

## 공통 / Common

- 애니메이션이 없어도 내용이 완전해야 한다. HTML에는 최종 숫자와 본문을 넣는다. 시작 상태(숫자 0,
  `opacity: 0`, 필요하면 `transform` 이동)는 스크립트가 붙이는 클래스로만 적용한다. 그러면 스크립트가
  꺼진 환경과 검색엔진에는 최종값과 본문이 그대로 남는다.
- 숨길 때 `visibility: hidden`, `display: none`, `hidden` 속성을 쓰지 않는다. 화면 낭독기, 키보드 초점,
  페이지 내 찾기에서 본문이 사라진다. 첫 화면에 보이는 요소는 최종값이 0으로 바뀌며 깜박이지 않도록
  첫 그리기 전에 시작 상태를 정하거나 아예 움직이지 않는다.
- API로 받는 지표(4원칙)는 HTML에 최종값을 넣을 수 없다. 로딩·빈 값·오류를 각각의 상태 표시로 보이고,
  '0'을 자리표시로 쓰지 않는다. 카운트업은 성공 응답의 값으로만 시작하고, 그 사이 화면이 해제됐거나
  더 최신 요청이 끝났으면 시작하지 않는다. 같은 화면에서 다시 받은 값은 0부터 다시 세지 않고 새 값으로 바로 바꾼다.
- `prefers-reduced-motion: reduce`이면 움직이지 않고 최종 상태를 바로 보인다.
- 스크립트 방식은 화면에 보일 때 한 번만 시작한다(IntersectionObserver, 시작 뒤 관찰 해제).
  스크롤 이벤트마다 위치를 읽지 않는다.
- `transform`과 `opacity`만 움직인다. 레이아웃을 바꾸는 속성(top, width, height, margin)은 쓰지 않고,
  자리를 미리 잡아 화면이 밀리지 않게 한다.
- 인쇄는 스크립트가 켜진 채 현재 상태로 찍히므로 따로 처리한다. `@media print`에서 시작 상태를 무효로
  하고(`opacity: 1; transform: none; animation: none; transition: none`) 낭독용 최종값 글자가 보이게 하거나,
  `beforeprint`에서 모든 카운트업을 최종값으로 확정한다.
- 1·3원칙: 기능마다 모듈을 하나씩 둔다. 별도 관례가 없는 새 코드에서는 기능마다 클래스도 하나씩 둔다
  (예: `CountUp`, `Reveal`). 프로젝트가 함수 컴포넌트·hooks·composables 관례를 쓰면 그 방식으로 같은
  책임을 나누고 클래스로 다시 쓰지 않는다. 2원칙: 지속시간과 곡선은 디자인 토큰으로 둔다.
- 4·5원칙: SPA에서 화면(라우트)을 해제할 때는 진행 중인 `requestAnimationFrame`을 `cancelAnimationFrame`으로
  취소하고 관찰자를 `disconnect()`한다. 문서 전체를 떠날 때는 `unload`로 정리하지 않는다. `pagehide`에서
  관찰자를 끊거나 프레임 반복을 취소했다면 `pageshow`에서 `event.persisted`가 참일 때 다시 연결한다
  (BFCache 복원에서는 초기화 코드가 다시 돌지 않는다). 아직 시작하지 않은 요소는 다시 관찰하고, 중단된
  카운트업은 최종값으로 확정한다. deep link, 새로고침, Back/Forward로 화면 중간(#앵커, 복원된 스크롤 위치)에
  들어와도 보이는 영역의 내용이 숨은 채 남지 않아야 한다.

## 카운트업 / Count-up

- `requestAnimationFrame`과 끝에서 느려지는 곡선(ease-out, 1~2초)으로 올리고, 마지막 값은 목표값과 정확히 같게 맞춘다.
- `Intl.NumberFormat`으로 자릿수 쉼표, 소수 자릿수, `%`, 통화 형식을 맞춘다. '건·명·개' 같은 한국어 단위는
  `style: 'unit'`이 받지 않으므로(`RangeError`) 숫자 밖의 별도 글자로 둔다.
- `font-variant-numeric: tabular-nums`로 숫자 한 자의 폭을 맞춘다(글꼴이 `tnum`을 지원해야 한다). 자리 수와
  쉼표가 늘어나는 만큼은 최종 문자열 폭으로 자리를 미리 잡는다(예: `display: inline-block; min-width: 6ch; text-align: end`).
- 화면 낭독기가 중간값을 읽지 않게 한다. 움직이는 숫자에는 `aria-hidden="true"`를 값까지 적어 달고, 최종값은
  화면에서만 감춘 낭독용 글자(`.sr-only` 등)로 따로 둔다. 낭독용 글자를 `display: none`이나 `hidden` 속성으로
  감추지 않고, 움직이는 숫자에 `aria-live`를 달지 않는다.
- 기본은 스크립트 방식이다. CSS만 쓰는 방식(`@property` 정수와 `counter()`)은 쉼표 표기와 접근성 처리가 어려워
  요청이 있을 때만 쓴다.

## 스크롤 애니메이션 / Scroll animations

- 나타나기·떠오르기 같은 등장 효과와 진행 표시 정도로 제한한다. 스크롤 속도나 방향을 가로채지 않는다(스크롤 하이재킹 금지).
- 등장 효과: CSS 스크롤 기반 애니메이션(`animation-timeline: view()`)은 `@supports`로 지원 브라우저에만 적용하고,
  그 밖의 브라우저는 IntersectionObserver로 클래스를 붙이는 방식으로 대체한다. `view()` 등장 효과는 스크롤을
  되돌리면 다시 숨겨지므로, 한 번만 보여야 하면 지원 브라우저에서도 IntersectionObserver 방식을 쓴다.
- 진행 표시: `@supports (animation-timeline: scroll())`일 때만 보인다. 지원하지 않는 브라우저와 움직임 줄이기
  설정에서는 진행 표시를 숨기고, IntersectionObserver나 스크롤 이벤트로 흉내 내거나 100%로 고정하지 않는다.
- 시작·끝 조건(`rootMargin`·`threshold`, `animation-range`)은 페이지 맨 아래 요소와 화면보다 큰 요소도 끝까지
  도달하게 잡는다. 음수 아래쪽 `rootMargin`이나 `animation-range: 0% 50%`처럼 화면 중앙에 닿아야 끝나는 값은 쓰지 않는다.

## 검증 / Verification

실제 앱 합격 기준에 더하고, 실행하지 못한 항목은 `미검증 / untested`로 적는다.

- 움직임 줄이기 설정, 스크립트 끈 상태, 인쇄 미리보기
- 화면 중간 #앵커 직접 열기, Back/Forward(BFCache 복원 포함) 뒤 스크롤 복원
- 페이지 맨 아래까지 스크롤했을 때 마지막 요소와 화면보다 큰 요소까지 최종 상태로 보이는지
- CPU를 4배 감속한 조건에서 프레임 끊김과 레이아웃 이동이 없는지
- API 지표: 로딩·빈 값·오류 상태가 각각 보이는지, 다시 받은 값이 0부터 다시 세지 않는지
