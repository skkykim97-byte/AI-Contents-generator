// ─── COLOR SYSTEM ─────────────────────────────────────────────
const PRESETS = [
  { h:'#FFFFFF', n:'화이트', white:true },
  { h:'#18181A', n:'블랙' },
  { h:'#C8102E', n:'레드' },
  { h:'#1B2A4A', n:'네이비' },
  { h:'#2A4438', n:'딥그린' },
  { h:'#F5F0E6', n:'아이보리', light:true },
  { h:'#EAE0CC', n:'베이지', light:true },
  { h:'#3C3858', n:'딥퍼플' },
  { h:'#3A3A3A', n:'차콜' },
];

let headerBg = '#FFFFFF';
let headerTx = '#18181A';
let headerMuted = 'rgba(0,0,0,0.35)';

function getLuminance(hex) {
  const r = parseInt(hex.slice(1,3),16)/255;
  const g = parseInt(hex.slice(3,5),16)/255;
  const b = parseInt(hex.slice(5,7),16)/255;
  return 0.299*r + 0.587*g + 0.114*b;
}

function applyColor(hex, idx, name) {
  headerBg = hex;
  const lum = getLuminance(hex);
  headerTx = lum > 0.42 ? '#18181A' : '#FFFFFF';
  headerMuted = lum > 0.42 ? 'rgba(0,0,0,0.35)' : 'rgba(255,255,255,0.5)';
  // 피커 업데이트
  const dot = document.getElementById('cdot-preview');
  if (dot) {
    dot.style.background = hex;
    dot.style.border = (hex === '#FFFFFF' || lum > 0.85) ? '1.5px solid #DDD' : '1px solid rgba(0,0,0,.06)';
  }
  const hexEl = document.getElementById('chex');
  if (hexEl) hexEl.textContent = hex.toUpperCase();
  const picker = document.getElementById('cpicker');
  if (picker) picker.value = hex;
  // 스와치 active 상태
  document.querySelectorAll('.cswatch').forEach(s => s.classList.remove('active'));
  if (idx !== '') {
    const sw = document.getElementById('sw-'+idx);
    if (sw) sw.classList.add('active');
  }
  render();
}

function buildSwatches() {
  const row = document.getElementById('swatch-row');
  PRESETS.forEach((p, i) => {
    const d = document.createElement('div');
    d.className = 'cswatch' + (i === 0 ? ' active' : '') + (p.white ? ' white-swatch' : '');
    d.id = 'sw-' + i;
    d.style.background = p.h;
    d.title = p.n;
    d.onclick = () => applyColor(p.h, i, p.n);
    row.appendChild(d);
  });
  applyColor('#FFFFFF', 0, '화이트');
}

// ─── IMAGE ────────────────────────────────────────────────────
const imgStore = { hero: null };

function loadImg(input, key) {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    imgStore[key] = e.target.result;
    renderUploaderFilled('hero-zone', e.target.result, 'hero');
    render();
  };
  reader.readAsDataURL(file);
}

function loadItemImg(input, id) {
  const file = input.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const it = items.find(i => i.id === id);
    if (it) it.img = e.target.result;
    renderUploaderFilled('zone-it'+id, e.target.result, 'it'+id);
    render();
  };
  reader.readAsDataURL(file);
}

function loadBnImg(input, id) {
  const file = input.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const bn = bns.find(b => b.id === id);
    if (bn) bn.img = e.target.result;
    renderUploaderFilled('zone-bn'+id, e.target.result, 'bn'+id);
    render();
  };
  reader.readAsDataURL(file);
}

function renderUploaderFilled(zoneId, src, clearKey) {
  const zone = document.getElementById(zoneId);
  if (!zone) return;
  zone.onclick = null;
  zone.innerHTML = `<div class="upl-filled">
    <img src="${src}" />
    <button class="upl-remove" onclick="clearUpload('${clearKey}');event.stopPropagation()">✕</button>
  </div>`;
}

function clearUpload(key) {
  if (key === 'hero') {
    imgStore.hero = null;
    const z = document.getElementById('hero-zone');
    z.innerHTML = `<div class="upl-empty"><div class="upl-icon">🖼</div><div class="upl-title">클릭하여 이미지 업로드</div><div class="upl-sub">JPG · PNG · WEBP</div></div>`;
    z.onclick = () => document.getElementById('hero-file').click();
  } else if (key.startsWith('it')) {
    const id = parseInt(key.slice(2));
    const it = items.find(i => i.id === id);
    if (it) it.img = null;
    restoreZone('zone-it'+id, '상품 이미지', 'file-it'+id, false);
  } else if (key.startsWith('bn')) {
    const id = parseInt(key.slice(2));
    const bn = bns.find(b => b.id === id);
    if (bn) bn.img = null;
    restoreZone('zone-bn'+id, '혜택 이미지', 'file-bn'+id, true);
  }
  render();
}

function restoreZone(zoneId, label, fileId, small) {
  const z = document.getElementById(zoneId);
  if (!z) return;
  z.innerHTML = `<div class="upl-empty" style="${small?'padding:12px 10px':''}">
    <div class="upl-icon">🖼</div>
    <div class="upl-title">${label}</div>
    <div class="upl-sub">클릭하여 선택</div>
  </div>`;
  z.onclick = () => document.getElementById(fileId).click();
}

// ─── STATE ────────────────────────────────────────────────────
let items = [], bns = [], iIdx = 0, bIdx = 0;

const ITEM_EX = [
  { name:'플뢰리에 네롤리 이리야 EDP 75ml', price:'318,000원', desc:'한 송이 꽃향을 떠올리게 하는 시트러스와 그린의 조화.\n신선하고 에너제틱한 향기의 매혹적인 향수입니다.' },
  { name:'플뢰리에 떼 이마라 EDP 75ml', price:'380,000원', desc:'부드럽고 고혹적인 꽃잎의 잔향, 우아한 우드 베이스가\n오래도록 지속되는 깊은 향수' },
  { name:'상탈 봉봉 프 레장 75ml', price:'', desc:'달콤한 바닐라와 따뜻한 샌달우드가 어우러진\n안락하고 감각적인 향' },
  { name:'레 클레마시크 컬렉션 100ml', price:'427,000원', desc:'우아하고 고급스러운 플로럴 무스크 향.\n클래식 콜렉션 라인의 대표 향수' },
];
const BN_EX = [
  { cond:'행사 SNS 이벤트 참여 시', gift:'2ml 바이알 1개 증정' },
  { cond:'모든 구매 고객', gift:'2ml 바이알 3종 슬리브 세트 증정' },
  { cond:'40만원 이상 구매 시', gift:'75ml 미니어처 추가 증정' },
  { cond:'50만원 이상 구매 시', gift:'75ml × 3 디스커버리 세트 추가 증정' },
  { cond:'캘리그래피 & 플라워 드로잉 카드 이벤트', gift:'참여 고객 기념 엽서 제공' },
];

function addItem() {
  const id = ++iIdx;
  const ex = ITEM_EX[items.length] || { name:'', price:'', desc:'' };
  items.push({ id, img: null, name: ex.name, price: ex.price, desc: ex.desc });
  rebuildItems();
  render();
}
function delItem(id) {
  items = items.filter(i => i.id !== id);
  rebuildItems();
  render();
}

function rebuildItems() {
  const list = document.getElementById('items-list');
  list.innerHTML = '';
  items.forEach((it, idx) => {
    const card = document.createElement('div');
    card.className = 'vcard';
    card.innerHTML = `
      <div class="vcard-head">
        <span class="vcard-label" style="background:#EEF9F1;color:#2A8847">Item ${idx+1}</span>
        <button class="vcard-del" onclick="delItem(${it.id})">✕</button>
      </div>
      <div class="vcard-body">
        <div class="field">
          <span class="field-label-ko">상품 이미지</span>
          <div class="uploader" id="zone-it${it.id}" onclick="document.getElementById('file-it${it.id}').click()">
            ${it.img
              ? `<div class="upl-filled"><img src="${it.img}"/><button class="upl-remove" onclick="clearUpload('it${it.id}');event.stopPropagation()">✕</button></div>`
              : `<div class="upl-empty"><div class="upl-icon">🖼</div><div class="upl-title">상품 이미지 업로드</div><div class="upl-sub">클릭하여 선택</div></div>`}
          </div>
          <input type="file" id="file-it${it.id}" accept="image/*" onchange="loadItemImg(this,${it.id})"/>
        </div>
        <div class="field">
          <span class="field-label-ko">상품명 · 용량 포함</span>
          <input type="text" value="${it.name}" placeholder="플뢰리에 네롤리 이리야 EDP 75ml"
            oninput="items.find(i=>i.id===${it.id}).name=this.value;render()"/>
        </div>
        <div class="field">
          <span class="field-label-ko">가격</span>
          <input type="text" value="${it.price}" placeholder="318,000원"
            oninput="items.find(i=>i.id===${it.id}).price=this.value;render()"/>
        </div>
        <div class="field">
          <span class="field-label-ko">상품 설명</span>
          <textarea oninput="items.find(i=>i.id===${it.id}).desc=this.value;render()">${it.desc}</textarea>
        </div>
      </div>`;
    list.appendChild(card);
  });
  document.getElementById('item-cnt').textContent = items.length + '개';
}

function addBenefit() {
  const id = ++bIdx;
  const ex = BN_EX[bns.length] || { cond:'', gift:'' };
  bns.push({ id, img: null, cond: ex.cond, gift: ex.gift });
  rebuildBns();
  render();
}
function delBn(id) {
  bns = bns.filter(b => b.id !== id);
  rebuildBns();
  render();
}

function rebuildBns() {
  const list = document.getElementById('bn-list');
  list.innerHTML = '';
  bns.forEach((bn, idx) => {
    const card = document.createElement('div');
    card.className = 'vcard';
    card.innerHTML = `
      <div class="vcard-head">
        <span class="vcard-label" style="background:#FFF8EC;color:#B07010">혜택 ${idx+1}</span>
        <button class="vcard-del" onclick="delBn(${bn.id})">✕</button>
      </div>
      <div class="vcard-body">
        <div class="field">
          <span class="field-label-ko">혜택 이미지</span>
          <div class="uploader" id="zone-bn${bn.id}" onclick="document.getElementById('file-bn${bn.id}').click()">
            ${bn.img
              ? `<div class="upl-filled"><img src="${bn.img}"/><button class="upl-remove" onclick="clearUpload('bn${bn.id}');event.stopPropagation()">✕</button></div>`
              : `<div class="upl-empty"><div class="upl-icon">🖼</div><div class="upl-title">혜택 이미지 업로드</div><div class="upl-sub">클릭하여 선택</div></div>`}
          </div>
          <input type="file" id="file-bn${bn.id}" accept="image/*" onchange="loadBnImg(this,${bn.id})"/>
        </div>
        <div class="field">
          <span class="field-label-ko">조건 <span style="color:var(--tx-hint);font-weight:300;font-size:11px">· 연한 글씨</span></span>
          <input type="text" value="${bn.cond}" placeholder="행사 SNS 이벤트 참여 시"
            oninput="bns.find(b=>b.id===${bn.id}).cond=this.value;render()"/>
        </div>
        <div class="field">
          <span class="field-label-ko">혜택 내용 <span style="color:var(--tx-hint);font-weight:300;font-size:11px">· 굵은 글씨</span></span>
          <input type="text" value="${bn.gift}" placeholder="2ml 바이알 1개 증정"
            oninput="bns.find(b=>b.id===${bn.id}).gift=this.value;render()"/>
        </div>
      </div>`;
    list.appendChild(card);
  });
  document.getElementById('bn-cnt').textContent = bns.length + '개';
}

// ─── RENDER ──────────────────────────────────────────────────
function v(id) {
  const el = document.getElementById(id);
  return el ? el.value.trim() : '';
}

function render() {
  const brand = v('f-brand'), title = v('f-title');
  const period = v('f-period'), loc = v('f-loc');
  const intro = v('f-intro'), notes = v('f-notes');
  const lum = getLuminance(headerBg);
  const valColor = lum > 0.42 ? '#333' : 'rgba(255,255,255,.82)';

  let h = '';

  // 헤더
  h += `<div class="o-hd" style="background:${headerBg}">`;
  if (brand) h += `<div class="o-hd-title" style="color:${headerTx}">${brand}</div>`;
  h += `<div class="o-hd-title" style="color:${headerTx};margin-top:${brand?'0':'0'}">${title || '행사 제목 둘째줄을 입력하세요'}</div>`;
  h += `<div class="o-hd-meta" style="margin-top:10px">`;
  if (period) {
    h += `<div class="o-hd-row"><span class="o-hd-key" style="color:${headerMuted}">기간</span>`;
    h += `<span class="o-hd-val" style="color:${valColor}">${period}</span></div>`;
  }
  if (loc) {
    h += `<div class="o-hd-row"><span class="o-hd-key" style="color:${headerMuted}">장소</span>`;
    h += `<span class="o-hd-val" style="color:${valColor}">${loc}</span></div>`;
  }
  h += `</div></div>`;

  // 대표 이미지
  h += `<div class="o-hero">`;
  if (imgStore.hero) h += `<img src="${imgStore.hero}" style="width:390px;display:block"/>`;
  else h += `<div class="o-hero-ph">대표 이미지를 업로드하세요</div>`;
  h += `</div>`;

  // 소개
  if (intro) {
    const paras = intro.split(/\n{2,}/).map(p => p.replace(/\n/g,'<br>'));
    h += `<div class="o-intro">` + paras.map(p => `<p>${p}</p>`).join('') + `</div>`;
  }

  // Items
  if (items.length > 0) {
    h += `<div class="o-sec"><span class="o-sec-txt">Item</span><div class="o-sec-line"></div></div>`;
    items.forEach(it => {
      h += `<div class="o-item">`;
      h += it.img ? `<img src="${it.img}" class="o-item-img"/>` : `<div class="o-item-img-ph">이미지</div>`;
      h += `<div class="o-item-info">`;
      if (it.name)  h += `<div class="o-item-name">${it.name}</div>`;
      if (it.price) h += `<div class="o-item-price">${it.price}</div>`;
      if (it.desc)  h += `<div class="o-item-desc">${it.desc.replace(/\n/g,'<br>')}</div>`;
      h += `</div></div>`;
    });
  }

  // Benefits
  if (bns.length > 0) {
    h += `<div class="o-sec"><span class="o-sec-txt">Special Benefit</span><div class="o-sec-line"></div></div>`;
    bns.forEach((bn, idx) => {
      h += `<div class="o-bn">`;
      h += `<div class="o-bn-num">${idx+1}</div>`;
      h += bn.img ? `<img src="${bn.img}" class="o-bn-img"/>` : `<div class="o-bn-img-ph">이미지</div>`;
      h += `<div class="o-bn-txt">`;
      if (bn.cond) h += `<div class="o-bn-cond">${bn.cond}</div>`;
      if (bn.gift) h += `<div class="o-bn-gift">${bn.gift}</div>`;
      h += `</div></div>`;
    });
  }

  // 유의사항
  if (notes) {
    h += `<div class="o-notes">`;
    h += `<div class="o-notes-ttl">참고사항</div>`;
    h += `<div class="o-notes-txt">${notes}</div>`;
    h += `</div>`;
  }

  document.getElementById('output').innerHTML = h;
}

// ─── EXPORT ──────────────────────────────────────────────────
async function doExport() {
  const btn = document.getElementById('expbtn');
  btn.disabled = true;
  btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 14 14" fill="none"><path d="M7 1v8M3.5 5.5L7 9l3.5-3.5M1 11.5h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg> 생성 중...`;
  try {
    await document.fonts.ready;
    const canvas = await html2canvas(document.getElementById('output'), {
      scale: 3, useCORS: true, allowTaint: true,
      backgroundColor: '#ffffff',
      scrollX: 0, scrollY: 0, width: 390, windowWidth: 390, logging: false,
    });
    const brand = v('f-brand') || '팝업행사';
    const title = v('f-title') || 'content';
    const fname = `[팝업]_${brand}_${title}`.replace(/[<>:"/\\|?*\s]/g,'_').slice(0,50) + '.jpg';
    canvas.toBlob(blob => {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = fname;
      a.click();
      showToast('✓  저장 완료 — ' + fname);
    }, 'image/jpeg', 0.95);
  } catch(e) {
    showToast('⚠  내보내기 실패: ' + e.message);
  }
  btn.disabled = false;
  btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 14 14" fill="none"><path d="M7 1v8M3.5 5.5L7 9l3.5-3.5M1 11.5h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg> JPG 내보내기`;
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

function resetAll() {
  ['f-brand','f-title','f-period','f-loc','f-intro','f-notes'].forEach(id => {
    const el = document.getElementById(id); if(el) el.value = '';
  });
  imgStore.hero = null;
  const hz = document.getElementById('hero-zone');
  hz.innerHTML = `<div class="upl-empty"><div class="upl-icon">🖼</div><div class="upl-title">클릭하여 이미지 업로드</div><div class="upl-sub">JPG · PNG · WEBP</div></div>`;
  hz.onclick = () => document.getElementById('hero-file').click();
  items = []; bns = []; iIdx = 0; bIdx = 0;
  rebuildItems(); rebuildBns();
  applyColor('#FFFFFF', 0, '화이트');
  render();
}

// ─── INIT ─────────────────────────────────────────────────────
buildSwatches();
document.getElementById('hero-zone').onclick = () => document.getElementById('hero-file').click();
render();
