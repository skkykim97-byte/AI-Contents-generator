# Requirements Document

## Introduction

롯데백화점 콘텐츠 생성기의 "저장/불러오기" 기능이다. 유저가 점별 팝업 행사 페이지에서 폼을 채우고 JPG 내보내기를 하면, 고유 코드가 생성되고 모든 입력값이 Google Sheets에 저장된다. 나중에 같은 페이지에서 코드를 입력하면 이전 데이터를 불러와 수정할 수 있다. 추가로 branch popup.html의 인라인 Base64 폰트를 외부 파일로 분리하여 경량화한다.

## Glossary

- **Content_Generator**: 롯데백화점 콘텐츠 생성기 웹 애플리케이션 전체
- **Popup_Page**: 점별 팝업 행사 생성기 페이지 (`pages/branch popup.html`)
- **Form_Panel**: Popup_Page 좌측의 입력 폼 영역 (행사 기본정보, 브랜드 소개, Item 섹션, Special Benefit, 참고사항)
- **Save_Code**: JPG 내보내기 시 생성되는 유저별 고유 식별 코드 (형식: `POP-XXXXXX`, X는 대문자 영문 또는 숫자)
- **Form_Data**: Form_Panel에서 유저가 입력한 모든 텍스트 값의 집합 (행사 제목 첫째줄, 둘째줄, 기간, 장소, 헤더 배경 색상, 소개 문구, Item 목록, Special Benefit 목록, 참고사항). 이미지 데이터(Base64)는 용량 제한으로 포함하지 않는다.
- **Apps_Script**: Google Apps Script 백엔드 (`apps_script.gs`)
- **Data_Sheet**: Google Sheets의 기존 DATA 시트 (사번, 이름, 제작 사유, 콘텐츠 유형, 시간 기록용)
- **Save_Sheet**: Google Sheets의 "코드 보관" 시트 (Save_Code, 콘텐츠 유형, Form_Data JSON, 생성 시간 기록용)
- **Load_Dialog**: Popup_Page Form_Panel 상단에 표시되는 코드 입력 UI (Save_Code를 입력하여 이전 데이터를 불러오는 인터페이스)
- **Export_Button**: Popup_Page의 "JPG 내보내기" 버튼
- **Toast**: 화면 하단에 일시적으로 표시되는 알림 메시지 (3초 후 자동 사라짐)

## Requirements

### Requirement 1: Save_Code 생성

**User Story:** As a 콘텐츠 제작자, I want JPG 내보내기 시 고유 코드를 자동으로 부여받고 싶다, so that 나중에 해당 코드로 이전 작업을 식별할 수 있다.

#### Acceptance Criteria

1. WHEN 유저가 Export_Button을 클릭하여 JPG 내보내기를 실행하면, THE Popup_Page SHALL `POP-XXXXXX` 형식의 Save_Code를 생성한다 (X는 대문자 A-Z 또는 숫자 0-9 중 랜덤 6자리).
2. WHEN Save_Code가 생성되면, THE Popup_Page SHALL 생성된 Save_Code를 Toast로 표시한다 (예: "✓ 저장 완료 — 코드: POP-A3X7K2 (클립보드 복사됨)").
3. WHEN Save_Code가 생성되면, THE Popup_Page SHALL 생성된 Save_Code를 클립보드에 자동 복사한다.
4. WHEN 유저가 불러오기로 기존 데이터를 로드한 상태에서 재내보내기를 실행하면, THE Popup_Page SHALL 기존 Save_Code를 재사용하지 않고 새로운 Save_Code를 생성한다.

### Requirement 2: Form_Data 저장

**User Story:** As a 콘텐츠 제작자, I want JPG 내보내기 시 입력한 모든 텍스트 값이 자동으로 저장되길 원한다, so that 나중에 수정이 필요할 때 처음부터 다시 입력하지 않아도 된다.

#### Acceptance Criteria

1. WHEN JPG 내보내기가 실행되면, THE Popup_Page SHALL 다음 Form_Data를 JSON 객체로 수집한다: 행사 제목 첫째줄(`f-brand`), 행사 제목 둘째줄(`f-title`), 기간(`f-period`), 장소(`f-loc`), 헤더 배경 색상(`headerBg` hex 값), 소개 문구(`f-intro`), Item 목록(각 아이템의 상품명·가격·설명), Special Benefit 목록(각 혜택의 조건·혜택 내용), 참고사항(`f-notes`).
2. WHEN Form_Data JSON이 수집되면, THE Popup_Page SHALL Save_Code, 콘텐츠 유형 문자열 "popup", Form_Data JSON 문자열을 Apps_Script에 POST 요청으로 전송한다.
3. WHEN Apps_Script가 `action: "save"` POST 요청을 수신하면, THE Apps_Script SHALL Save_Sheet에 한 행을 추가하여 Save_Code, 콘텐츠 유형, Form_Data JSON 문자열, 저장 시각을 기록한다.
4. IF Apps_Script로의 전송이 실패하면, THEN THE Popup_Page SHALL "저장 실패" Toast를 표시하고 JPG 다운로드는 정상 진행한다.

### Requirement 3: Load_Dialog UI

**User Story:** As a 콘텐츠 제작자, I want 점별 팝업 페이지에서 이전 코드를 입력하여 데이터를 불러오고 싶다, so that 기존 콘텐츠를 수정할 수 있다.

#### Acceptance Criteria

1. THE Popup_Page SHALL Form_Panel 상단에 Load_Dialog를 표시한다 (Save_Code 입력 필드 1개와 "불러오기" 버튼 1개로 구성).
2. WHEN 유저가 Load_Dialog에 Save_Code를 입력하고 "불러오기" 버튼을 클릭하면, THE Popup_Page SHALL Apps_Script에 해당 Save_Code로 GET 조회 요청을 전송한다.
3. WHILE 조회 요청이 진행 중이면, THE Popup_Page SHALL "불러오기" 버튼 텍스트를 "불러오는 중..."으로 변경하고 버튼을 비활성화한다.
4. WHEN Form_Data JSON이 정상 반환되면, THE Popup_Page SHALL 모든 폼 필드를 반환된 데이터로 채우고 render() 함수를 호출하여 미리보기를 갱신한다.
5. IF 입력된 Save_Code와 일치하는 데이터가 Save_Sheet에 존재하지 않으면, THEN THE Popup_Page SHALL "해당 코드의 저장 데이터가 없습니다" Toast를 표시한다.
6. IF Apps_Script 조회 요청이 실패하면, THEN THE Popup_Page SHALL "불러오기 실패. 네트워크를 확인해 주세요" Toast를 표시한다.
7. WHEN 조회 요청이 완료되면(성공 또는 실패), THE Popup_Page SHALL "불러오기" 버튼 텍스트를 원래 상태로 복원하고 버튼을 활성화한다.

### Requirement 4: Form_Data 복원

**User Story:** As a 콘텐츠 제작자, I want 불러온 데이터가 폼에 정확히 복원되길 원한다, so that 이전 작업 상태 그대로 수정을 시작할 수 있다.

#### Acceptance Criteria

1. WHEN Form_Data가 복원되면, THE Popup_Page SHALL 행사 기본정보 필드(제목 첫째줄, 둘째줄, 기간, 장소)를 저장된 값으로 채운다.
2. WHEN Form_Data가 복원되면, THE Popup_Page SHALL 헤더 배경 색상을 저장된 hex 값으로 applyColor() 함수를 호출하여 적용한다.
3. WHEN Form_Data가 복원되면, THE Popup_Page SHALL 소개 문구 텍스트를 저장된 값으로 채운다.
4. WHEN Form_Data가 복원되면, THE Popup_Page SHALL 기존 Item 카드를 모두 제거한 후, 저장된 Item 목록 개수만큼 Item 카드를 생성하고 각 카드의 상품명, 가격, 설명을 채운다.
5. WHEN Form_Data가 복원되면, THE Popup_Page SHALL 기존 Special Benefit 카드를 모두 제거한 후, 저장된 혜택 목록 개수만큼 혜택 카드를 생성하고 각 카드의 조건, 혜택 내용을 채운다.
6. WHEN Form_Data가 복원되면, THE Popup_Page SHALL 참고사항 텍스트를 저장된 값으로 채운다.
7. WHEN 모든 필드 복원이 완료되면, THE Popup_Page SHALL render() 함수를 호출하여 우측 미리보기 패널을 갱신한다.

### Requirement 5: Apps_Script 조회 API

**User Story:** As a 시스템, I want Apps_Script가 Save_Code 기반 조회 기능을 제공하길 원한다, so that 클라이언트가 저장된 데이터를 요청할 수 있다.

#### Acceptance Criteria

1. WHEN Apps_Script가 `action=load&code=<Save_Code>` 쿼리 파라미터가 포함된 GET 요청을 수신하면, THE Apps_Script SHALL Save_Sheet에서 해당 Save_Code와 일치하는 가장 최근 행을 검색한다.
2. WHEN 일치하는 행이 존재하면, THE Apps_Script SHALL `{ "status": "ok", "data": <Form_Data JSON 문자열> }` 형태의 JSON 응답을 반환한다.
3. IF 일치하는 행이 존재하지 않으면, THEN THE Apps_Script SHALL `{ "status": "not_found" }` 형태의 JSON 응답을 반환한다.
4. IF 조회 처리 중 오류가 발생하면, THEN THE Apps_Script SHALL `{ "status": "error", "msg": "<오류 메시지>" }` 형태의 JSON 응답을 반환한다.

### Requirement 6: Save_Sheet 구조

**User Story:** As a 관리자, I want 저장 데이터가 구조화된 시트에 기록되길 원한다, so that 데이터를 관리하고 조회할 수 있다.

#### Acceptance Criteria

1. THE Apps_Script SHALL 기존 DATA 시트와 별도로 "코드 보관" 이름의 Save_Sheet를 사용한다.
2. WHEN Save_Sheet가 존재하지 않으면, THE Apps_Script SHALL 첫 저장 요청 시 Save_Sheet를 자동 생성하고 헤더 행을 추가한다.
3. THE Save_Sheet SHALL 각 행에 다음 4개 컬럼을 포함한다: 코드(열 A), 콘텐츠 유형(열 B), 데이터 JSON 문자열(열 C), 생성 시간(열 D, Asia/Seoul 기준 `yyyy-MM-dd HH:mm:ss` 형식).

### Requirement 7: 코드 경량화

**User Story:** As a 개발자, I want branch popup.html의 파일 크기를 줄이고 싶다, so that 유지보수가 용이하고 페이지 로딩이 개선된다.

#### Acceptance Criteria

1. THE Content_Generator SHALL MaisonNeue 폰트의 Base64 인라인 데이터를 `pages/branch popup.html`에서 분리하여 별도의 외부 CSS 파일(`static/css/maison-neue.css`)로 이동한다.
2. WHEN Popup_Page가 로드되면, THE Popup_Page SHALL 외부 CSS 파일을 `<link>` 태그로 참조하여 MaisonNeue 폰트를 로드한다.
