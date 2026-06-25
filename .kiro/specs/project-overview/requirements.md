# AI Contents Generator — 전체 요구사항

## 개요

롯데백화점 점별 콘텐츠(팝업 행사, 개점 주년 행사, New Open 브랜드 등)를 폼 입력 → 실시간 미리보기 → JPG 내보내기로 제작하는 웹 생성기 애플리케이션.

---

## 페이지 목록

| 파일 | 용도 | 저장 코드 접두사 |
|---|---|---|
| `pages/branch popup.html` | 점별 팝업 행사 콘텐츠 | POP- |
| `pages/branch anniversary.html` | 개점 N주년 행사 콘텐츠 | ANN- |
| `pages/new open.html` | New Open 브랜드 콘텐츠 | NEW- |
| `index.html` | 콘텐츠 센터 진입 페이지 | — |
| `pages/home.html` | 홈 / 메뉴 선택 | — |

---

## 공통 요구사항

### R-C1: 저장 / 불러오기
- JPG 내보내기 시 고유 코드 자동 생성, Google Sheets(`코드 보관` 시트)에 폼 데이터 JSON 저장
- `임시저장` 버튼으로 내보내기 없이 미리 저장 가능
- 코드 입력으로 기존 데이터 불러오기 (상세: `.kiro/specs/save-load-popup/requirements.md`)

### R-C2: 예시 이미지 팝업
- 각 생성기 페이지 topbar에 `예시` 버튼 배치
- 클릭 시 해당 콘텐츠의 예시 이미지를 모달로 표시
- 세로가 긴 콘텐츠도 스크롤 가능 (`max-height: calc(100vh - 64px)`, `overflow-y: auto`)
- 오버레이 클릭 또는 ✕ 버튼으로 닫기

| 페이지 | 예시 이미지 경로 |
|---|---|
| branch anniversary | `examples/ex_branch anniversary.jpg` |
| branch popup | `examples/ex_branch popup.jpg` |
| new open | `examples/ex_newopen.jpg` |

### R-C3: 헤더 배경색 선택
- 프리셋 색상 스와치 + 컬러피커 커스텀 색상 지원
- 색상 변경 시 프리뷰 즉시 반영

### R-C4: JPG 내보내기
- html2canvas (scale:3) 사용, 390px 폭 기준
- 16:9 이미지 크롭: 원본 비율에 따라 슬라이더로 crop 위치 조정 → 내보내기 시 Canvas로 크롭 적용
- 파일명 형식: `[유형] 이름_코드.jpg`

### R-C5: 폰트
- MaisonNeue (영문/숫자) + Noto Sans KR (한글)
- Base64 폰트는 `static/css/fonts.css`로 외부 분리

---

## branch anniversary.html 전용 요구사항

### R-A1: 헤더 고정 배경색 프리셋

| 색상 | 이름 |
|---|---|
| `#FDE8F0` | 핑크 |
| `#67434a` | 다크로즈 |
| `#000000` | 블랙 |
| `#59789f` | 블루 |
| `#ff9548` | 오렌지 |
| `#6f4898` | 퍼플 |
| `#4d6c46` | 그린 |
| `#1b2664` | 네이비 |

### R-A2: 타이틀 · 점포명 색상 규칙

타이틀 색 결정 (프리셋별 명시, 커스텀은 luminance 0.55 기준):

| 배경 | titleDark | 타이틀 색 |
|---|---|---|
| `#FDE8F0` | true | `#222222` |
| 나머지 7종 | false | `#FFFFFF` |

점포명 색 규칙:
- **타이틀이 어두운 색 (titleDark=true)** → 점포명은 배경의 **진한 유사 컬러** (직접 매핑)
- **타이틀이 흰색 (titleDark=false)** → 점포명도 **`#FFFFFF`**

프리셋별 점포명 storeAccent:

| 배경 | storeAccent |
|---|---|
| `#FDE8F0` | `#9B2550` |
| `#59789f` | `#195AA9` |
| `#ff9548` | `#C05200` |

커스텀 컬러 시: HSL 기반 자동 계산 (채도 +25%, 명도 -45%)

### R-A3: 섹션 구성
1. 행사 기본 정보 (점포명, 타이틀 2줄, 기간, 로고 이미지, 헤더 배경색)
2. Special Benefit (가변 카드: 이미지 필수 + 타이틀 + 내용 + 단서조항)
3. 브랜드데이 (기간 + 가변 할인율 카드 + 단서조항)
4. 구매 금액대별 프로모션 (기간 + 가변 브랜드 카드)
5. Special Event (가변 카드: 이미지 필수 + 타이틀 + 내용 + 단서조항)
6. 참고사항

---

## branch popup.html 전용 요구사항

### R-P1: 헤더 배경색 프리셋
그린, 네이비, 핑크, 퍼플, 블루, 오렌지, 버건디, 블랙 (기본값: 블랙)

### R-P2: 타이틀 색상 규칙
luminance > 0.42 → 어두운 타이틀(`#18181A`), 이하 → 흰색

### R-P3: 섹션 구성
1. 행사 기본정보 (제목 2줄, 기간, 장소, 헤더 배경색)
2. 브랜드 소개 (대표 정방형 이미지 + 소개 문구)
3. Item (가변 카드: 정방형 이미지 + 상품명 + 가격 + 설명)
4. Special Benefit (가변 카드: 넘버링 + 이미지 + 조건 + 혜택)
5. 참고사항

---

## new open.html 전용 요구사항

### R-N1: 헤더 배경색 프리셋
네이비, 블랙, 그린, 퍼플, 다크로즈, 블루, 오렌지, 핑크 (기본값: 네이비 `#1b2664`)

### R-N2: 타이틀 색상 규칙
프리셋별 `titleDark` 플래그 (핑크만 true, 나머지 false), 커스텀은 luminance 0.55 기준

### R-N3: 섹션 구성
1. **헤더** — 상단 라벨(예: NEW OPEN), 타이틀, 행사 설명(font-size 15px), 배경색 선택
2. **Brand New Drop** (섹션 타이틀 수정 가능)
   - `+ 브랜드 추가` 동적 카드
   - 각 카드: 정방형 브랜드 이미지(선택), 브랜드명, 브랜드 설명
   - 복수 브랜드 시 구분선(divider) 자동 적용
3. **Open SALE** (섹션 타이틀 수정 가능)
   - `+ 프로모션 추가` 동적 카드
   - 각 카드: 16:9 이미지(선택, 필수 아님), 프로모션 타이틀, 상세 설명
4. **Special Event** (섹션 타이틀 수정 가능)
   - `+ 이벤트 추가` 동적 카드
   - 각 카드: 넘버링(검정 원 20×20px, font 10px), 이벤트명, 16:9 이미지(선택, 필수 아님), 상세 설명, 단서조항(회색 작은 글씨)
   - 이미지 미첨부 시 이미지 영역 자체 미출력 + 상하 간격 최소화 (margin-bottom: 6px)
5. **참고사항** (선택)

### R-N4: 이미지 출력 규칙
- 모든 출력 이미지에 `border-radius: 0` (테두리 R값 없음)
- 이미지 미첨부 시 placeholder 미출력 (빈 상태)

### R-N5: 저장 구조
```json
{
  "label", "title", "desc",
  "secBrand", "secSale", "secEvt",
  "headerBg", "notes",
  "brands": [{ "name", "desc" }],
  "sales": [{ "title", "desc" }],
  "events": [{ "name", "desc", "note" }]
}
```
