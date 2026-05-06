// ══════════════════════════════════════════════════════════════════
//  롯데백화점 콘텐츠 생성기 — Google Apps Script
//  시트 ID : 1PX8tFrDVpHciruGL-m06Bs0pkfoU4wtQ47SEP3eqxmg
//  시트명  : DATA
//
//  [배포 방법]
//  1. Google Sheets → 확장 프로그램 → Apps Script
//  2. 이 코드 전체를 붙여넣고 저장 (Ctrl+S)
//  3. 배포 → 새 배포 → 유형: 웹 앱
//     · 실행 계정  : 나 (본인)
//     · 액세스 권한: 모든 사용자 (익명 포함)
//  4. 배포 → URL 복사
//  5. pages/home.html 의 APPS_SCRIPT_URL 에 붙여넣기
// ══════════════════════════════════════════════════════════════════

var SHEET_ID   = '1PX8tFrDVpHciruGL-m06Bs0pkfoU4wtQ47SEP3eqxmg';
var SHEET_NAME = 'DATA';
var SAVE_SHEET_NAME = '코드 보관';

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    // action: "save" → 코드 보관 시트에 저장
    if (data.action === 'save') {
      return handleSave(data);
    }

    // DATA 시트 기록 (dept, reason, template, 시간)
    var ss    = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName(SHEET_NAME);

    // 헤더가 없으면 생성
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
    }
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['소속 점포/팀', '제작 사유', '콘텐츠 유형', '시간 (KST)']);
    }

    var dept     = data.dept     || '';
    var reason   = data.reason   || '';
    var template = data.template || '';
    var now = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss');
    sheet.appendRow([dept, reason, template, now]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', msg: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ── Save: "코드 보관" 시트에 코드·유형·데이터·시간 기록 ──
function handleSave(data) {
  try {
    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName(SAVE_SHEET_NAME);

    // 시트가 없으면 자동 생성 + 헤더 행
    if (!sheet) {
      sheet = ss.insertSheet(SAVE_SHEET_NAME);
      sheet.appendRow(['코드', '콘텐츠 유형', '데이터', '생성 시간']);
    }

    var now = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss');
    sheet.appendRow([data.code, data.type, data.data, now]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', msg: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// GET 요청 — action=load 시 코드 보관 시트에서 데이터 조회
function doGet(e) {
  var action = (e && e.parameter && e.parameter.action) || '';

  if (action === 'load') {
    return handleLoad(e.parameter.code);
  }

  // 기존 동작 유지 (브라우저에서 URL 직접 접근 시)
  return ContentService
    .createTextOutput('Apps Script 정상 작동 중')
    .setMimeType(ContentService.MimeType.TEXT);
}

// ── Load: "코드 보관" 시트에서 코드로 가장 최근 행 검색 ──
function handleLoad(code) {
  try {
    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName(SAVE_SHEET_NAME);

    if (!sheet) {
      return ContentService
        .createTextOutput(JSON.stringify({ status: 'not_found' }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    var lastRow = sheet.getLastRow();
    var searchCode = String(code || '').trim();

    // 역순 검색 — 가장 최근 행 우선
    for (var i = lastRow; i >= 2; i--) {
      var cellValue = String(sheet.getRange(i, 1).getValue()).trim();
      if (cellValue === searchCode) {
        var dataJSON = sheet.getRange(i, 3).getValue();
        return ContentService
          .createTextOutput(JSON.stringify({ status: 'ok', data: dataJSON }))
          .setMimeType(ContentService.MimeType.JSON);
      }
    }

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'not_found' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', msg: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
