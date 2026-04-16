import streamlit as st
import base64
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="롯데백화점 콘텐츠 생성기",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'items' not in st.session_state:
    st.session_state.items = []
if 'benefits' not in st.session_state:
    st.session_state.benefits = []
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""

# CSS 스타일
st.markdown("""
<style>
    :root {
        --lotte-red: #C8102E;
        --lotte-bg: #F0EFE8;
    }
    
    .main-header {
        background: linear-gradient(135deg, #C8102E 0%, #8B0A1F 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        box-shadow: 0 4px 20px rgba(200, 16, 46, 0.2);
    }
    
    .stButton>button {
        background: #C8102E !important;
        color: white !important;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
    }
    
    .stButton>button:hover {
        background: #8B0A1F !important;
        box-shadow: 0 4px 12px rgba(200, 16, 46, 0.3);
    }
    
    .preview-container {
        background: #C8C7BE;
        border-radius: 12px;
        padding: 2rem;
        display: flex;
        justify-content: center;
        min-height: 600px;
    }
    
    .section-badge {
        background: #FFF0F3;
        color: #C8102E;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 템플릿 정의
TEMPLATES = {
    "점별 팝업행사": {"icon": "🎪", "color": "#C8102E"},
    "우수고객 혜택 안내": {"icon": "👑", "color": "#B07310"},
    "뉴오픈 or 리뉴얼": {"icon": "✨", "color": "#2C5F2D"},
    "스페셜 베네핏 + 상품": {"icon": "🎁", "color": "#1E3A8A"}
}

# 롯데백화점 컬러 팔레트
LOTTE_COLORS = {
    "화이트": "#FFFFFF", "아이보리": "#FFF8F0", "베이지": "#F0EFE8",
    "핑크": "#FFF0F3", "라벤더": "#F5F0FF", "민트": "#F0FFF8",
    "스카이": "#F0F8FF", "피치": "#FFF5F0", "레드": "#C8102E",
    "골드": "#B07310", "네이비": "#1A2B3C", "그레이": "#767670"
}

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
#c{{width:390px;margin:0 auto;background:#fff}}
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
        html += '<div class="hero-ph">대표 이미지</div>'
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

# 헤더
st.markdown('<div class="main-header"><h1>🏢 롯데백화점 콘텐츠 생성기</h1><p>점별 팝업행사 템플릿으로 빠르게 HTML 콘텐츠를 생성하세요</p></div>', unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown("### 📋 템플릿 선택")
    
    selected_template = st.selectbox(
        "콘텐츠 유형",
        list(TEMPLATES.keys()),
        format_func=lambda x: f"{TEMPLATES[x]['icon']} {x}"
    )
    
    st.markdown("---")
    st.info(f"**{selected_template}** 템플릿이 선택되었습니다.\n\n현재는 점별 팝업행사 템플릿만 완전 구현되어 있습니다.")

# 메인 영역
if selected_template == "점별 팝업행사":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ✏️ 콘텐츠 입력")
        
        # 헤더 정보
        st.markdown('<div class="section-badge">📌 기본 정보</div>', unsafe_allow_html=True)
        brand = st.text_input("브랜드명", placeholder="예: 루이비통")
        title = st.text_input("행사 제목*", placeholder="예: 2025 S/S 팝업 스토어")
        
        col_a, col_b = st.columns(2)
        with col_a:
            period = st.text_input("기간", placeholder="1.15 ~ 1.31")
        with col_b:
            store = st.text_input("매장", placeholder="본점")
        
        location = st.text_input("장소", placeholder="9F 명품관")
        
        # 헤더 배경색
        st.markdown('<div class="section-badge">🎨 헤더 색상</div>', unsafe_allow_html=True)
        color_cols = st.columns(6)
        selected_color = "#FFFFFF"
        
        for idx, (name, color) in enumerate(LOTTE_COLORS.items()):
            with color_cols[idx % 6]:
                if st.button(name, key=f"color_{name}", use_container_width=True):
                    selected_color = color
        
        header_bg = st.color_picker("또는 직접 선택", selected_color, key="custom_color")
        
        # 대표 이미지
        st.markdown('<div class="section-badge">🖼️ 대표 이미지</div>', unsafe_allow_html=True)
        hero_image = st.text_input("이미지 URL", placeholder="https://...")
        
        # 소개 텍스트
        st.markdown('<div class="section-badge">📝 소개</div>', unsafe_allow_html=True)
        intro = st.text_area("소개 텍스트", placeholder="행사 소개 내용을 입력하세요.\n\n단락 구분은 빈 줄로 합니다.", height=100)
        
        # Items
        st.markdown('<div class="section-badge">🎁 아이템 목록</div>', unsafe_allow_html=True)
        num_items = st.number_input("아이템 개수", 0, 10, len(st.session_state.items))
        
        # 아이템 개수 조정
        while len(st.session_state.items) < num_items:
            st.session_state.items.append({"name": "", "price": "", "desc": "", "image": ""})
        while len(st.session_state.items) > num_items:
            st.session_state.items.pop()
        
        for i, item in enumerate(st.session_state.items):
            with st.expander(f"아이템 {i+1}"):
                item['name'] = st.text_input(f"상품명 {i+1}", item['name'], key=f"item_name_{i}")
                item['price'] = st.text_input(f"가격 {i+1}", item['price'], key=f"item_price_{i}", placeholder="₩1,200,000")
                item['desc'] = st.text_area(f"설명 {i+1}", item['desc'], key=f"item_desc_{i}", height=60)
                item['image'] = st.text_input(f"이미지 URL {i+1}", item['image'], key=f"item_img_{i}")
        
        # Benefits
        st.markdown('<div class="section-badge">⭐ 특별 혜택</div>', unsafe_allow_html=True)
        num_benefits = st.number_input("혜택 개수", 0, 10, len(st.session_state.benefits))
        
        while len(st.session_state.benefits) < num_benefits:
            st.session_state.benefits.append({"cond": "", "gift": "", "image": ""})
        while len(st.session_state.benefits) > num_benefits:
            st.session_state.benefits.pop()
        
        for i, bn in enumerate(st.session_state.benefits):
            with st.expander(f"혜택 {i+1}"):
                bn['cond'] = st.text_input(f"조건 {i+1}", bn['cond'], key=f"bn_cond_{i}", placeholder="행사 SNS 이벤트 참여 시")
                bn['gift'] = st.text_input(f"혜택 내용 {i+1}", bn['gift'], key=f"bn_gift_{i}", placeholder="2ml 바이알 1개 증정")
                bn['image'] = st.text_input(f"이미지 URL {i+1}", bn['image'], key=f"bn_img_{i}")
        
        # 유의사항
        st.markdown('<div class="section-badge">⚠️ 유의사항</div>', unsafe_allow_html=True)
        notes = st.text_area("유의사항", placeholder="행사 유의사항을 입력하세요", height=80)
        
        st.markdown("---")
        if st.button("🎨 HTML 생성하기", type="primary", use_container_width=True):
            data = {
                'brand': brand, 'title': title, 'period': period, 'store': store,
                'location': location, 'header_bg': header_bg, 'hero_image': hero_image,
                'intro': intro, 'items': st.session_state.items,
                'benefits': st.session_state.benefits, 'notes': notes
            }
            st.session_state.generated_html = generate_popup_html(data)
            st.success("✅ HTML이 생성되었습니다!")
    
    with col2:
        st.markdown("### 👁️ 미리보기 및 다운로드")
        
        if st.session_state.generated_html:
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            st.components.v1.html(st.session_state.generated_html, height=800, scrolling=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            col_a, col_b = st.columns(2)
            with col_a:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"팝업행사_{title or '콘텐츠'}_{timestamp}.html"
                st.download_button(
                    "📥 HTML 다운로드",
                    st.session_state.generated_html,
                    filename,
                    "text/html",
                    use_container_width=True
                )
            
            with col_b:
                if st.button("📋 코드 보기", use_container_width=True):
                    st.code(st.session_state.generated_html, language="html")
        else:
            st.info("👈 왼쪽에서 내용을 입력하고 'HTML 생성하기' 버튼을 눌러주세요")

else:
    st.warning(f"**{selected_template}** 템플릿은 현재 개발 중입니다.")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#888;padding:1rem">
<p>🏢 롯데백화점 DX팀 | 콘텐츠 생성기 v1.0</p>
<p style="font-size:0.9rem">템플릿 기반 자동 생성으로 퍼블리싱 시간 60% 단축</p>
</div>
""", unsafe_allow_html=True)
