import streamlit as st
import base64
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="팝업 행사 생성기",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if 'items' not in st.session_state:
    st.session_state.items = []
if 'benefits' not in st.session_state:
    st.session_state.benefits = []
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""
if 'header_bg' not in st.session_state:
    st.session_state.header_bg = "#FFFFFF"
if 'hero_image' not in st.session_state:
    st.session_state.hero_image = ""

# 롯데 컬러 팔레트
LOTTE_COLORS = [
    {"name": "화이트", "hex": "#FFFFFF"},
    {"name": "아이보리", "hex": "#FFF8F0"},
    {"name": "베이지", "hex": "#F0EFE8"},
    {"name": "핑크", "hex": "#FFF0F3"},
    {"name": "라벤더", "hex": "#F5F0FF"},
    {"name": "민트", "hex": "#F0FFF8"},
    {"name": "스카이", "hex": "#F0F8FF"},
    {"name": "피치", "hex": "#FFF5F0"},
    {"name": "레드", "hex": "#C8102E"},
    {"name": "골드", "hex": "#B07310"},
    {"name": "네이비", "hex": "#1A2B3C"},
    {"name": "그레이", "hex": "#767670"}
]

# 원본 HTML UI 스타일 적용
st.markdown("""
<style>
/* 전체 리셋 */
* {box-sizing: border-box;}
.stApp {background: #F0EFE8;}

/* 컨테이너 제거 */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* 사이드바 숨기기 */
[data-testid="stSidebar"] {display: none;}

/* Top Bar */
.topbar {
    height: 50px;
    background: #fff;
    border-bottom: 1px solid #E0DFD8;
    display: flex;
    align-items: center;
    padding: 0 20px;
    gap: 10px;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;
}
.tp-chip {
    background: #FFF0F3;
    color: #C8102E;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 0.5px;
}
.tp-title {
    font-size: 13px;
    font-weight: 700;
    color: #1A1A18;
}
.tp-sub {
    font-size: 12px;
    color: #767670;
    flex: 1;
}

/* Main Layout */
.main-layout {
    display: flex;
    height: calc(100vh - 50px);
    margin-top: 50px;
}

/* Form Panel */
.form-panel {
    width: 400px;
    min-width: 400px;
    overflow-y: auto;
    background: #F0EFE8;
    border-right: 1px solid #E0DFD8;
}

/* Preview Panel */
.preview-panel {
    flex: 1;
    overflow-y: auto;
    background: #C8C7BE;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 28px 20px;
}
.prev-lbl {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    margin-bottom: 14px;
}
.prev-device {
    background: #fff;
    width: 390px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    border-radius: 2px;
}

/* Block Styles */
.blk {
    background: #fff;
    border: 1px solid #ECEAE3;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 8px;
}
.blk-head {
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #ECEAE3;
    background: #fff;
}
.blk-ico {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
    flex-shrink: 0;
}
.blk-name {
    flex: 1;
    font-size: 12px;
    font-weight: 700;
    color: #1A1A18;
    letter-spacing: 0.2px;
}
.blk-badge {
    font-size: 10px;
    color: #767670;
    background: #F0EFE8;
    border: 1px solid #E0DFD8;
    padding: 2px 6px;
    border-radius: 8px;
}
.blk-body {
    padding: 14px;
}

/* Form Elements */
.field {
    margin-bottom: 11px;
}
.lbl {
    font-size: 11px;
    font-weight: 700;
    color: #767670;
    letter-spacing: 0.2px;
    margin-bottom: 4px;
    display: block;
}

/* Streamlit Input Override */
.stTextInput input, .stTextArea textarea {
    border: 1px solid #E0DFD8 !important;
    border-radius: 6px !important;
    font-size: 13px !important;
    padding: 7px 9px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    background: #fff !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #C8102E !important;
    box-shadow: 0 0 0 2px rgba(200,16,46,0.07) !important;
}

/* Color Palette */
.color-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    margin-bottom: 8px;
}
.color-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    cursor: pointer;
}
.color-dot {
    width: 36px;
    height: 36px;
    border-radius: 6px;
    border: 2px solid transparent;
    transition: all 0.12s;
    cursor: pointer;
}
.color-dot:hover {
    transform: scale(1.08);
}
.color-dot.selected {
    box-shadow: 0 0 0 2px #fff, 0 0 0 4px #1A1A18;
    transform: scale(1.08);
}
.color-name {
    font-size: 9px;
    color: #767670;
    font-weight: 500;
}

/* Variable Cards */
.vcard {
    background: #F0EFE8;
    border: 1px solid #ECEAE3;
    border-radius: 7px;
    padding: 12px;
    margin-bottom: 8px;
}
.vc-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 9px;
}
.vc-num {
    font-size: 10px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
}

/* Button Styles */
.stButton > button {
    width: 100%;
    background: #1A1A18 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    padding: 8px 14px !important;
    height: 32px !important;
}
.stButton > button:hover {
    background: #333 !important;
}

/* Number Input */
.stNumberInput input {
    border: 1px solid #E0DFD8 !important;
    border-radius: 6px !important;
    font-size: 13px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #F0EFE8 !important;
    border: 1px solid #ECEAE3 !important;
    border-radius: 7px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    padding: 8px 12px !important;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def calculate_luminance(hex_color):
    """색상 밝기 계산"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
    r = r/12.92 if r <= 0.03928 else ((r+0.055)/1.055)**2.4
    g = g/12.92 if g <= 0.03928 else ((g+0.055)/1.055)**2.4
    b = b/12.92 if b <= 0.03928 else ((b+0.055)/1.055)**2.4
    return 0.2126*r + 0.7152*g + 0.0722*b

def generate_popup_html(data):
    """점별 팝업행사 HTML 생성"""
    hdr_bg = data.get('header_bg', '#FFFFFF')
    lum = calculate_luminance(hdr_bg)
    hdr_tx = '#111' if lum > 0.45 else 'rgba(255,255,255,0.95)'
    hdr_muted = '#888' if lum > 0.45 else 'rgba(255,255,255,0.7)'
    meta_val = '#444' if lum > 0.45 else 'rgba(255,255,255,0.85)'
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{data.get('title','팝업행사')}</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Noto Sans KR',sans-serif;background:#fff;-webkit-font-smoothing:antialiased}}
#c{{width:390px;background:#fff}}
.hd{{padding:20px 20px 18px;background:{hdr_bg}}}
.hd-brand{{font-size:12px;font-weight:400;letter-spacing:.3px;margin-bottom:7px;line-height:1.4;color:{hdr_muted}}}
.hd-title{{font-size:19px;font-weight:700;letter-spacing:-.4px;line-height:1.35;margin-bottom:14px;word-break:keep-all;color:{hdr_tx}}}
.hd-meta{{display:flex;flex-direction:column;gap:4px}}
.hd-row{{display:flex;align-items:baseline;font-size:12px;font-weight:400}}
.hd-key{{min-width:26px;margin-right:8px;flex-shrink:0;color:{hdr_muted}}}
.hd-val{{line-height:1.5;color:{meta_val}}}
.hero img{{width:390px;display:block}}
.hero-ph{{width:390px;height:210px;background:#ECEAE3;display:flex;align-items:center;justify-content:center;font-size:12px;color:#B0AFA8}}
.intro{{padding:22px 20px;border-bottom:1px solid #EAEAE4}}
.intro p{{font-size:13px;font-weight:400;color:#333;line-height:1.9;word-break:keep-all}}
.intro p+p{{margin-top:12px}}
.sec{{padding:22px 20px 6px;display:flex;align-items:center;gap:11px}}
.sec-txt{{font-size:14.5px;font-weight:700;color:#111;letter-spacing:.3px;white-space:nowrap}}
.sec-line{{flex:1;height:1px;background:#DDDBD2}}
.item{{display:flex;align-items:flex-start;gap:14px;padding:18px 20px;border-bottom:1px solid #ECEAE4}}
.item-img{{width:130px;height:130px;object-fit:cover;flex-shrink:0;display:block;background:#F5F4EF}}
.item-img-ph{{width:130px;height:130px;flex-shrink:0;background:#ECEAE3;display:flex;align-items:center;justify-content:center;font-size:11px;color:#B0AFA8}}
.item-info{{flex:1;min-width:0;padding-top:2px}}
.item-name{{font-size:13.5px;font-weight:700;color:#111;line-height:1.45;margin-bottom:5px;word-break:keep-all}}
.item-price{{font-size:15.5px;font-weight:700;color:#111;margin-bottom:9px;letter-spacing:-.2px}}
.item-desc{{font-size:11.5px;font-weight:400;color:#888;line-height:1.75;word-break:keep-all}}
.bn{{display:flex;align-items:flex-start;gap:11px;padding:15px 20px;border-bottom:1px solid #ECEAE4}}
.bn-num{{width:22px;height:22px;border-radius:50%;background:#1A1A18;color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:3px}}
.bn-img{{width:80px;height:80px;object-fit:cover;flex-shrink:0;display:block;background:#F5F4EF}}
.bn-img-ph{{width:80px;height:80px;flex-shrink:0;background:#ECEAE3;display:flex;align-items:center;justify-content:center;font-size:10px;color:#B0AFA8}}
.bn-info{{flex:1;min-width:0;padding-top:2px}}
.bn-cond{{font-size:11px;font-weight:400;color:#999;line-height:1.6;margin-bottom:4px;word-break:keep-all}}
.bn-gift{{font-size:12.5px;font-weight:700;color:#111;line-height:1.55;word-break:keep-all}}
.notes{{padding:20px;background:#FAFAF8;border-top:1px solid #EAEAE4}}
.notes-ttl{{font-size:12px;font-weight:700;color:#111;margin-bottom:10px;letter-spacing:.2px}}
.notes-txt{{font-size:11.5px;font-weight:400;color:#666;line-height:1.8;white-space:pre-line;word-break:keep-all}}
</style>
</head>
<body><div id="c">"""
    
    # 헤더
    html += '<div class="hd">'
    if data.get('brand'):
        html += f'<div class="hd-brand">{data["brand"]}</div>'
    html += f'<div class="hd-title">{data.get("title","제목 입력")}</div><div class="hd-meta">'
    if data.get('period') or data.get('store'):
        html += f'<div class="hd-row"><span class="hd-key">기간</span><span class="hd-val">{data.get("period","")}'
        if data.get('store'):
            html += f'&nbsp;&nbsp;{data["store"]}'
        html += '</span></div>'
    if data.get('location'):
        html += f'<div class="hd-row"><span class="hd-key">장소</span><span class="hd-val">{data["location"]}</span></div>'
    html += '</div></div>'
    
    # 대표 이미지
    html += '<div class="hero">'
    if data.get('hero_image'):
        html += f'<img src="{data["hero_image"]}" alt="대표">'
    else:
        html += '<div class="hero-ph">대표 이미지를 업로드하세요</div>'
    html += '</div>'
    
    # 소개
    if data.get('intro'):
        html += '<div class="intro">'
        for p in data['intro'].split('\n\n'):
            html += f'<p>{p.replace(chr(10),"<br>")}</p>'
        html += '</div>'
    
    # Items
    if data.get('items'):
        html += '<div class="sec"><span class="sec-txt">Item</span><div class="sec-line"></div></div>'
        for it in data['items']:
            html += '<div class="item">'
            html += f'<img src="{it["image"]}" class="item-img">' if it.get('image') else '<div class="item-img-ph">이미지</div>'
            html += '<div class="item-info">'
            if it.get('name'):
                html += f'<div class="item-name">{it["name"]}</div>'
            if it.get('price'):
                html += f'<div class="item-price">{it["price"]}</div>'
            if it.get('desc'):
                html += f'<div class="item-desc">{it["desc"].replace(chr(10),"<br>")}</div>'
            html += '</div></div>'
    
    # Benefits
    if data.get('benefits'):
        html += '<div class="sec"><span class="sec-txt">Special Benefit</span><div class="sec-line"></div></div>'
        for i, bn in enumerate(data['benefits']):
            html += '<div class="bn">'
            html += f'<div class="bn-num">{i+1}</div>'
            html += f'<img src="{bn["image"]}" class="bn-img">' if bn.get('image') else '<div class="bn-img-ph">이미지</div>'
            html += '<div class="bn-info">'
            if bn.get('cond'):
                html += f'<div class="bn-cond">{bn["cond"]}</div>'
            if bn.get('gift'):
                html += f'<div class="bn-gift">{bn["gift"]}</div>'
            html += '</div></div>'
    
    # 유의사항
    if data.get('notes'):
        html += f'<div class="notes"><div class="notes-ttl">유의사항</div><div class="notes-txt">{data["notes"]}</div></div>'
    
    html += '</div></body></html>'
    return html

# Top Bar
st.markdown("""
<div class="topbar">
    <span class="tp-chip">TOOL</span>
    <span class="tp-title">팝업 행사 생성기</span>
    <span class="tp-sub">롯데백화점 DX팀</span>
</div>
""", unsafe_allow_html=True)

# Main Layout
col_form, col_preview = st.columns([400, None], gap="none")

with col_form:
    st.markdown('<div class="form-panel"><div style="padding: 16px;">', unsafe_allow_html=True)
    
    # 1. 행사 기본정보
    st.markdown("""
    <div class="blk">
        <div class="blk-head">
            <div class="blk-ico" style="background:#FFF0F3;color:#C8102E">1</div>
            <div class="blk-name">행사 기본정보</div>
        </div>
        <div class="blk-body">
    """, unsafe_allow_html=True)
    
    st.markdown('<span class="lbl">브랜드명</span>', unsafe_allow_html=True)
    brand = st.text_input("브랜드명", label_visibility="collapsed", placeholder="루이비통", key="brand")
    
    st.markdown('<span class="lbl">행사 제목</span>', unsafe_allow_html=True)
    title = st.text_input("행사 제목", label_visibility="collapsed", placeholder="2025 S/S 팝업 스토어", key="title")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<span class="lbl">기간</span>', unsafe_allow_html=True)
        period = st.text_input("기간", label_visibility="collapsed", placeholder="1.15 ~ 1.31", key="period")
    with col_b:
        st.markdown('<span class="lbl">매장</span>', unsafe_allow_html=True)
        store = st.text_input("매장", label_visibility="collapsed", placeholder="본점", key="store")
    
    st.markdown('<span class="lbl">장소</span>', unsafe_allow_html=True)
    location = st.text_input("장소", label_visibility="collapsed", placeholder="9F 명품관", key="location")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 2. 헤더 색상
    st.markdown("""
    <div class="blk">
        <div class="blk-head">
            <div class="blk-ico" style="background:#FFF8EC;color:#B07310">2</div>
            <div class="blk-name">헤더 색상</div>
        </div>
        <div class="blk-body">
    """, unsafe_allow_html=True)
    
    # 컬러 팔레트 그리드
    st.markdown('<div class="color-grid">', unsafe_allow_html=True)
    cols = st.columns(4)
    for idx, color in enumerate(LOTTE_COLORS):
        with cols[idx % 4]:
            selected_class = "selected" if st.session_state.header_bg == color['hex'] else ""
            if st.button(f"⬤", key=f"color_{idx}", help=color['name']):
                st.session_state.header_bg = color['hex']
                st.rerun()
            st.markdown(f'<div style="text-align:center;margin-top:-20px;"><div class="color-dot {selected_class}" style="background:{color["hex"]};margin:0 auto;"></div><div class="color-name">{color["name"]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 3. 대표 이미지
    st.markdown("""
    <div class="blk">
        <div class="blk-head">
            <div class="blk-ico" style="background:#F0F8FF;color:#1E3A8A">3</div>
            <div class="blk-name">대표 이미지</div>
        </div>
        <div class="blk-body">
    """, unsafe_allow_html=True)
    
    st.markdown('<span class="lbl">이미지 URL</span>', unsafe_allow_html=True)
    hero_image = st.text_input("이미지 URL", label_visibility="collapsed", placeholder="https://...", key="hero_img", value=st.session_state.hero_image)
    st.session_state.hero_image = hero_image
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 4. 브랜드 소개
    st.markdown("""
    <div class="blk">
        <div class="blk-head">
            <div class="blk-ico" style="background:#F5F0FF;color:#7C3AED">4</div>
            <div class="blk-name">브랜드 소개</div>
        </div>
        <div class="blk-body">
    """, unsafe_allow_html=True)
    
    st.markdown('<span class="lbl">소개 텍스트</span>', unsafe_allow_html=True)
    intro = st.text_area("소개", label_visibility="collapsed", placeholder="브랜드 및 행사 소개를 입력하세요.\n\n단락 구분은 빈 줄로 합니다.", height=100, key="intro")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 5. Item 목록
    st.markdown(f"""
    <div class="blk">
        <div class="blk-head">
            <div class="blk-ico" style="background:#FFF5F0;color:#EA580C">5</div>
            <div class="blk-name">Item 목록</div>
            <span class="blk-badge">{len(st.session_state.items)}개</span>
        </div>
        <div class="blk-body">
    """, unsafe_allow_html=True)
    
    num_items = st.number_input("아이템 개수", 0, 10, len(st.session_state.items), label_visibility="collapsed", key="num_items")
    
    while len(st.session_state.items) < num_items:
        st.session_state.items.append({"name": "", "price": "", "desc": "", "image": ""})
    while len(st.session_state.items) > num_items:
        st.session_state.items.pop()
    
    for i in range(len(st.session_state.items)):
        st.markdown(f'<div class="vcard"><div class="vc-head"><span class="vc-num" style="background:#FFF5F0;color:#EA580C">아이템 {i+1}</span></div>', unsafe_allow_html=True)
        
        st.markdown('<span class="lbl">상품명</span>', unsafe_allow_html=True)
        st.session_state.items[i]['name'] = st.text_input(f"상품명{i}", st.session_state.items[i]['name'], label_visibility="collapsed", key=f"item_name_{i}", placeholder="상품명")
        
        st.markdown('<span class="lbl">가격</span>', unsafe_allow_html=True)
        st.session_state.items[i]['price'] = st.text_input(f"가격{i}", st.session_state.items[i]['price'], label_visibility="collapsed", key=f"item_price_{i}", placeholder="₩1,200,000")
        
        st.markdown('<span class="lbl">설명</span>', unsafe_allow_html=True)
        st.session_state.items[i]['desc'] = st.text_area(f"설명{i}", st.session_state.items[i]['desc'], label_visibility="collapsed", key=f"item_desc_{i}", height=60, placeholder="상품 설명")
        
        st.markdown('<span class="lbl">이미지 URL</span>', unsafe_allow_html=True)
        st.session_state.items[i]['image'] = st.text_input(f"이미지{i}", st.session_state.items[i]['image'], label_visibility="collapsed", key=f"item_img_{i}", placeholder="https://...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 6. Special Benefit
    st.markdown(f"""
    <div class="blk">
        <div class="blk-head">
            <div class="blk-ico" style="background:#FFF8EC;color:#B07310">6</div>
            <div class="blk-name">Special Benefit</div>
            <span class="blk-badge">{len(st.session_state.benefits)}개</span>
        </div>
        <div class="blk-body">
    """, unsafe_allow_html=True)
    
    num_benefits = st.number_input("혜택 개수", 0, 10, len(st.session_state.benefits), label_visibility="collapsed", key="num_benefits")
    
    while len(st.session_state.benefits) < num_benefits:
        st.session_state.benefits.append({"cond": "", "gift": "", "image": ""})
    while len(st.session_state.benefits) > num_benefits:
        st.session_state.benefits.pop()
    
    for i in range(len(st.session_state.benefits)):
        st.markdown(f'<div class="vcard"><div class="vc-head"><span class="vc-num" style="background:#FFF8EC;color:#B07310">혜택 {i+1}</span></div>', unsafe_allow_html=True)
        
        st.markdown('<span class="lbl">조건 (연한 글씨)</span>', unsafe_allow_html=True)
        st.session_state.benefits[i]['cond'] = st.text_input(f"조건{i}", st.session_state.benefits[i]['cond'], label_visibility="collapsed", key=f"bn_cond_{i}", placeholder="행사 SNS 이벤트 참여 시")
        
        st.markdown('<span class="lbl">혜택 내용 (굵은 글씨)</span>', unsafe_allow_html=True)
        st.session_state.benefits[i]['gift'] = st.text_input(f"혜택{i}", st.session_state.benefits[i]['gift'], label_visibility="collapsed", key=f"bn_gift_{i}", placeholder="2ml 바이알 1개 증정")
        
        st.markdown('<span class="lbl">이미지 URL</span>', unsafe_allow_html=True)
        st.session_state.benefits[i]['image'] = st.text_input(f"혜택이미지{i}", st.session_state.benefits[i]['image'], label_visibility="collapsed", key=f"bn_img_{i}", placeholder="https://...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 7. 유의사항
    st.markdown("""
    <div class="blk">
        <div class="blk-head">
            <div class="blk-ico" style="background:#FEF3C7;color:#92400E">7</div>
            <div class="blk-name">유의사항</div>
        </div>
        <div class="blk-body">
    """, unsafe_allow_html=True)
    
    st.markdown('<span class="lbl">유의사항 텍스트</span>', unsafe_allow_html=True)
    notes = st.text_area("유의사항", label_visibility="collapsed", placeholder="행사 유의사항을 입력하세요", height=80, key="notes")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 생성 버튼
    if st.button("HTML 생성하기", key="generate"):
        data = {
            'brand': brand, 'title': title, 'period': period, 'store': store,
            'location': location, 'header_bg': st.session_state.header_bg,
            'hero_image': hero_image, 'intro': intro,
            'items': st.session_state.items, 'benefits': st.session_state.benefits,
            'notes': notes
        }
        st.session_state.generated_html = generate_popup_html(data)
        st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

with col_preview:
    st.markdown('<div class="preview-panel">', unsafe_allow_html=True)
    st.markdown('<div class="prev-lbl">PREVIEW — 390px mobile</div>', unsafe_allow_html=True)
    
    if st.session_state.generated_html:
        st.markdown('<div class="prev-device">', unsafe_allow_html=True)
        st.components.v1.html(st.session_state.generated_html, height=800, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 다운로드 버튼
        st.markdown('<div style="margin-top:20px;width:390px;">', unsafe_allow_html=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"[팝업]_{brand or '행사'}_{title or 'content'}_{timestamp}.html"
        st.download_button(
            "📥 HTML 다운로드",
            st.session_state.generated_html,
            filename,
            "text/html",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:rgba(255,255,255,0.6);font-size:13px;text-align:center;margin-top:100px;">← 왼쪽 폼을 작성하고<br>HTML 생성하기 버튼을 눌러주세요</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
