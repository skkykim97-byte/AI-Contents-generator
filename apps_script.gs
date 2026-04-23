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

function doPost(e) {
  try {
    var data  = JSON.parse(e.postData.contents);
    var ss    = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName(SHEET_NAME);

    // 헤더가 없으면 첫 행에 추가
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['사번', '이름', '제작 사유', '콘텐츠 유형', '시간']);
    }

    var now = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss');
    sheet.appendRow([data.empno, data.name, data.reason, data.template, now]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', msg: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// GET 요청 테스트용 (브라우저에서 URL 직접 접근 시 동작 확인)
function doGet(e) {
  return ContentService
    .createTextOutput('Apps Script 정상 작동 중')
    .setMimeType(ContentService.MimeType.TEXT);
}
