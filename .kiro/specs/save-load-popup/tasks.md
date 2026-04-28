# Implementation Plan: Save/Load Popup

## Overview

점별 팝업 행사 생성기에 저장/불러오기 기능을 구현한다. 클라이언트(JavaScript)에서 Save_Code 생성, Form_Data 수집/복원을 처리하고, Apps Script에서 "코드 보관" 시트 CRUD를 담당한다. 마지막으로 인라인 Base64 폰트를 외부 CSS로 분리하여 파일을 경량화한다.

## Tasks

- [x] 1. 코드 경량화 — Base64 폰트 외부 CSS 분리
  - [x] 1.1 `pages/branch popup.html`에서 인라인 `@font-face` MaisonNeue Base64 블록을 제거하고, `<head>`에 `<link rel="stylesheet" href="/static/css/fonts.css">` 태그를 추가한다
    - 기존 `static/css/fonts.css`에 동일한 MaisonNeue Base64 `@font-face`가 이미 존재하므로 새 파일 생성 불필요
    - `<link>` 태그는 기존 Google Fonts `<link>` 태그 아래에 배치
    - _Requirements: 7.1, 7.2_
  - [x] 1.2 Flask `app.py`에서 `/static/` 경로가 정상 서빙되는지 확인하고, 필요 시 `static_folder` 설정 점검
    - Flask 기본 설정으로 `static/` 폴더를 자동 서빙하므로 별도 수정 불필요할 수 있음
    - _Requirements: 7.2_

- [x] 2. Apps Script 백엔드 확장 — Save/Load API
  - [x] 2.1 `apps_script.gs`의 `doPost()` 함수에 `action` 분기 추가
    - `action: "save"` 시 `handleSave(data)` 호출
    - 기존 DATA 시트 기록 로직(사번, 이름, 제작 사유)은 `action`이 없는 경우 그대로 유지
    - `handleSave(data)`: "코드 보관" 시트가 없으면 자동 생성 + 헤더 행(`코드`, `콘텐츠 유형`, `데이터`, `생성 시간`) 추가, 이후 `[code, type, dataJSON, timestamp]` 행 append
    - 시간 형식: `Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss')`
    - 성공 시 `{ status: "ok" }`, 오류 시 `{ status: "error", msg: "..." }` JSON 응답
    - _Requirements: 2.3, 6.1, 6.2, 6.3_
  - [x] 2.2 `apps_script.gs`의 `doGet()` 함수에 `action=load` 분기 추가
    - `action=load&code=POP-XXXXXX` 파라미터 수신 시 `handleLoad(code)` 호출
    - `handleLoad(code)`: "코드 보관" 시트에서 A열을 역순 검색하여 해당 코드의 가장 최근 행을 찾고, C열의 데이터 JSON 문자열을 반환
    - 매칭 행 존재 시 `{ status: "ok", data: <JSON문자열> }` 응답
    - 매칭 행 미존재 시 `{ status: "not_found" }` 응답
    - 오류 시 `{ status: "error", msg: "..." }` 응답
    - 기존 `doGet` 기본 동작(action 없을 때 텍스트 응답)은 유지
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 3. Checkpoint — Apps Script 변경 확인
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. 클라이언트 — Save_Code 생성 및 Form_Data 수집/저장
  - [ ] 4.1 `pages/branch popup.html`의 `<script>` 블록에 `generateSaveCode()` 함수 추가
    - `crypto.getRandomValues()`로 6자리 영숫자 생성, `POP-XXXXXX` 형식 반환
    - _Requirements: 1.1_
  - [ ] 4.2 `collectFormData()` 함수 추가
    - `f-brand`, `f-title`, `f-period`, `f-loc`, `headerBg`, `f-intro`, `f-notes` 텍스트 값과 `items` 배열(각 아이템의 name, price, desc), `bns` 배열(각 혜택의 cond, gift)을 JSON 객체로 수집
    - 이미지 데이터는 제외
    - _Requirements: 2.1_
  - [ ] 4.3 기존 `doExport()` 함수 수정 — 저장 로직 통합
    - JPG 내보내기 성공 후 `generateSaveCode()` 호출하여 코드 생성
    - `collectFormData()`로 Form_Data JSON 수집
    - `APPS_SCRIPT_URL`에 `{ action: "save", code, type: "popup", data: JSON문자열 }` POST 전송 (fetch 사용)
    - POST 성공 시 Toast에 "✓ 저장 완료 — 코드: POP-XXXXXX (클립보드 복사됨)" 표시
    - `navigator.clipboard.writeText(code)`로 클립보드 복사
    - POST 실패 시 "저장 실패" Toast 표시, JPG 다운로드는 정상 진행
    - 불러오기로 로드한 상태에서 재내보내기 시에도 항상 새 코드 생성 (기존 코드 재사용 안 함)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.2, 2.4_
  - [ ]* 4.4 Write property test for Save_Code format validity
    - **Property 1: Save_Code format validity**
    - `generateSaveCode()`를 100회 이상 호출하여 모든 결과가 `^POP-[A-Z0-9]{6}$` 패턴에 매칭되는지 검증 (fast-check)
    - **Validates: Requirements 1.1**

- [ ] 5. 클라이언트 — Load_Dialog UI 및 불러오기 기능
  - [ ] 5.1 `pages/branch popup.html`의 Form_Panel 상단(첫 번째 `<div class="sec">` 이전)에 Load_Dialog HTML 삽입
    - `<div class="load-bar">` 안에 `<input id="load-code" placeholder="POP-XXXXXX" maxlength="10">` + `<button id="load-btn" onclick="doLoad()">불러오기</button>` 구성
    - Load_Dialog용 CSS 스타일 추가 (`.load-bar` 레이아웃, 입력 필드, 버튼 스타일)
    - _Requirements: 3.1_
  - [ ] 5.2 `doLoad()` 함수 추가
    - 빈 입력값 검증 (빈 값이면 무시)
    - 버튼 텍스트를 "불러오는 중..."으로 변경 + 비활성화
    - `APPS_SCRIPT_URL?action=load&code=<입력값>` GET 요청 전송
    - 응답 `status: "ok"` 시 `restoreFormData(JSON.parse(data))` 호출
    - 응답 `status: "not_found"` 시 "해당 코드의 저장 데이터가 없습니다" Toast
    - 네트워크 오류 시 "불러오기 실패. 네트워크를 확인해 주세요" Toast
    - JSON 파싱 실패 시 "데이터 형식 오류" Toast
    - 완료 후(성공/실패) 버튼 텍스트 원래 상태 복원 + 활성화
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  - [ ] 5.3 `restoreFormData(data)` 함수 추가
    - 행사 기본정보 필드 복원: `f-brand`, `f-title`, `f-period`, `f-loc`
    - `applyColor(data.headerBg, '', '')` 호출하여 헤더 배경 색상 복원
    - `f-intro`, `f-notes` 텍스트 복원
    - 기존 `items` 배열 초기화 후 저장된 Item 목록만큼 재생성 (`iIdx` 증가, `rebuildItems()` 호출)
    - 기존 `bns` 배열 초기화 후 저장된 혜택 목록만큼 재생성 (`bIdx` 증가, `rebuildBns()` 호출)
    - 모든 복원 완료 후 `render()` 호출하여 미리보기 갱신
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_
  - [ ]* 5.4 Write property test for Form_Data round-trip preservation
    - **Property 2: Form_Data round-trip preservation**
    - fast-check로 임의의 Form_Data 객체(문자열 필드, 가변 길이 items/benefits 배열)를 생성하고, `restoreFormData()` → `collectFormData()` 라운드트립 후 원본과 동일한지 검증 (jsdom 모킹 필요)
    - **Validates: Requirements 2.1, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6**

- [ ] 6. Checkpoint — 전체 기능 통합 확인
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. APPS_SCRIPT_URL 연결 확인
  - [ ] 7.1 `pages/branch popup.html`에 `APPS_SCRIPT_URL` 상수가 정의되어 있는지 확인하고, `pages/home.html`에 이미 존재하는 URL과 동일한 값을 사용하도록 설정
    - `doExport()`의 POST 전송과 `doLoad()`의 GET 요청 모두 이 URL을 사용
    - _Requirements: 2.2, 3.2_

- [ ] 8. Final checkpoint — 전체 테스트 및 최종 확인
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- 기존 `static/css/fonts.css`에 MaisonNeue Base64 폰트가 이미 존재하므로 새 파일(`maison-neue.css`) 생성 대신 기존 파일을 재활용
- `APPS_SCRIPT_URL`은 `pages/home.html`에 이미 정의된 값을 동일하게 사용
- Google Sheets ID: `1PX8tFrDVpHciruGL-m06Bs0pkfoU4wtQ47SEP3eqxmg`, Save_Sheet 이름: "코드 보관"
- Property tests use fast-check library with jsdom for DOM mocking
