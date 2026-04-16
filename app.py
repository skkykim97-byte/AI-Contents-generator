import streamlit as st
import base64
from datetime import datetime
import json

# 페이지 설정
st.set_page_config(
    page_title="롯데백화점 HTML 콘텐츠 생성기",
    page_icon="🎨",
    layout="wide"
)

# 세션 상태 초기화
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""
if 'preview_mode' not in st.session_state:
    st.session_state.preview_mode = "desktop"

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .template-card {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .template-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    .stButton>button {
        width: 100%;
    }
    .preview-container {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="main-header">
    <h1>🎨 HTML 콘텐츠 생성기</h1>
    <p>템플릿 기반으로 손쉽게 HTML 콘텐츠를 생성하세요</p>
</div>
""", unsafe_allow_html=True)

# 템플릿 정의
TEMPLATES = {
    "이벤트/프로모션 배너": {
        "icon": "🎉",
        "description": "프로모션, 할인 이벤트 배너",
        "fields": ["제목", "부제목", "이미지 URL", "버튼 텍스트", "버튼 링크", "배경색", "텍스트 색상"]
    },
    "랜딩 페이지 블록": {
        "icon": "📄",
        "description": "상품/서비스 소개 랜딩 페이지",
        "fields": ["메인 제목", "설명", "이미지 URL", "특징1", "특징2", "특징3", "CTA 버튼", "링크"]
    },
    "카드형 콘텐츠": {
        "icon": "🎴",
        "description": "카드 형태의 상품/정보 목록",
        "fields": ["카드 개수", "카드별 제목", "카드별 설명", "카드별 이미지", "카드별 링크"]
    },
    "공지/안내형": {
        "icon": "📢",
        "description": "공지사항, 안내 메시지",
        "fields": ["제목", "내용", "아이콘", "배경색", "강조 문구"]
    }
}

# HTML 생성 함수들
def generate_event_banner_html(data):
    """이벤트/프로모션 배너 HTML 생성"""
    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('제목', '이벤트 배너')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        .banner-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: {data.get('배경색', '#f5f5f5')};
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .banner-content {{
            display: flex;
            align-items: center;
            padding: 3rem;
            gap: 2rem;
        }}
        .banner-text {{
            flex: 1;
        }}
        .banner-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {data.get('텍스트 색상', '#333')};
            margin-bottom: 1rem;
            line-height: 1.2;
        }}
        .banner-subtitle {{
            font-size: 1.25rem;
            color: {data.get('텍스트 색상', '#666')};
            margin-bottom: 2rem;
        }}
        .banner-image {{
            flex: 1;
            max-width: 500px;
        }}
        .banner-image img {{
            width: 100%;
            height: auto;
            border-radius: 12px;
        }}
        .cta-button {{
            display: inline-block;
            padding: 1rem 2.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        @media (max-width: 768px) {{
            .banner-content {{
                flex-direction: column;
                padding: 2rem;
            }}
            .banner-title {{
                font-size: 2rem;
            }}
            .banner-subtitle {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="banner-container">
        <div class="banner-content">
            <div class="banner-text">
                <h1 class="banner-title">{data.get('제목', '이벤트 제목')}</h1>
                <p class="banner-subtitle">{data.get('부제목', '이벤트 설명')}</p>
                <a href="{data.get('버튼 링크', '#')}" class="cta-button">
                    {data.get('버튼 텍스트', '자세히 보기')}
                </a>
            </div>
            <div class="banner-image">
                <img src="{data.get('이미지 URL', 'https://via.placeholder.com/500x400')}" 
                     alt="{data.get('제목', '이벤트 이미지')}">
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html

def generate_landing_page_html(data):
    """랜딩 페이지 블록 HTML 생성"""
    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('메인 제목', '랜딩 페이지')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; }}
        .landing-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }}
        .hero-section {{
            text-align: center;
            margin-bottom: 4rem;
        }}
        .hero-title {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
        }}
        .hero-description {{
            font-size: 1.25rem;
            color: #666;
            max-width: 800px;
            margin: 0 auto 2rem;
            line-height: 1.6;
        }}
        .hero-image {{
            max-width: 100%;
            height: auto;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        }}
        .features-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 4rem 0;
        }}
        .feature-card {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s;
        }}
        .feature-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        .feature-icon {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        .feature-title {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #333;
        }}
        .cta-section {{
            text-align: center;
            margin-top: 4rem;
        }}
        .cta-button {{
            display: inline-block;
            padding: 1.25rem 3rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
        }}
        @media (max-width: 768px) {{
            .hero-title {{ font-size: 2rem; }}
            .hero-description {{ font-size: 1rem; }}
            .features-section {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="landing-container">
        <div class="hero-section">
            <h1 class="hero-title">{data.get('메인 제목', '환영합니다')}</h1>
            <p class="hero-description">{data.get('설명', '서비스 설명')}</p>
            <img src="{data.get('이미지 URL', 'https://via.placeholder.com/1200x600')}" 
                 alt="Hero Image" class="hero-image">
        </div>
        
        <div class="features-section">
            <div class="feature-card">
                <div class="feature-icon">✨</div>
                <h3 class="feature-title">특징 1</h3>
                <p>{data.get('특징1', '첫 번째 특징 설명')}</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3 class="feature-title">특징 2</h3>
                <p>{data.get('특징2', '두 번째 특징 설명')}</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💡</div>
                <h3 class="feature-title">특징 3</h3>
                <p>{data.get('특징3', '세 번째 특징 설명')}</p>
            </div>
        </div>
        
        <div class="cta-section">
            <a href="{data.get('링크', '#')}" class="cta-button">
                {data.get('CTA 버튼', '지금 시작하기')}
            </a>
        </div>
    </div>
</body>
</html>
"""
    return html

def generate_card_content_html(data):
    """카드형 콘텐츠 HTML 생성"""
    card_count = int(data.get('카드 개수', 3))
    cards_html = ""
    
    for i in range(card_count):
        cards_html += f"""
            <div class="card">
                <div class="card-image">
                    <img src="{data.get(f'카드{i+1} 이미지', 'https://via.placeholder.com/400x300')}" 
                         alt="Card {i+1}">
                </div>
                <div class="card-content">
                    <h3 class="card-title">{data.get(f'카드{i+1} 제목', f'카드 제목 {i+1}')}</h3>
                    <p class="card-description">{data.get(f'카드{i+1} 설명', '카드 설명')}</p>
                    <a href="{data.get(f'카드{i+1} 링크', '#')}" class="card-link">자세히 보기 →</a>
                </div>
            </div>
        """
    
    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>카드형 콘텐츠</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; padding: 2rem; }}
        .cards-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s;
        }}
        .card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }}
        .card-image {{
            width: 100%;
            height: 240px;
            overflow: hidden;
        }}
        .card-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }}
        .card:hover .card-image img {{
            transform: scale(1.05);
        }}
        .card-content {{
            padding: 1.5rem;
        }}
        .card-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 0.75rem;
        }}
        .card-description {{
            font-size: 1rem;
            color: #666;
            line-height: 1.6;
            margin-bottom: 1rem;
        }}
        .card-link {{
            display: inline-block;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .card-link:hover {{
            color: #764ba2;
            transform: translateX(5px);
        }}
        @media (max-width: 768px) {{
            .cards-container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="cards-container">
        {cards_html}
    </div>
</body>
</html>
"""
    return html

def generate_notice_html(data):
    """공지/안내형 HTML 생성"""
    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('제목', '공지사항')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; padding: 2rem; }}
        .notice-container {{
            max-width: 800px;
            margin: 0 auto;
            background: {data.get('배경색', '#fff3cd')};
            border-left: 5px solid #ffc107;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .notice-header {{
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
        }}
        .notice-icon {{
            font-size: 2.5rem;
            margin-right: 1rem;
        }}
        .notice-title {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #333;
        }}
        .notice-content {{
            font-size: 1.1rem;
            color: #555;
            line-height: 1.8;
            margin-bottom: 1.5rem;
        }}
        .notice-highlight {{
            background: #fff;
            padding: 1rem;
            border-radius: 6px;
            border-left: 3px solid #667eea;
            margin-top: 1rem;
            font-weight: 600;
            color: #667eea;
        }}
        @media (max-width: 768px) {{
            .notice-container {{
                padding: 1.5rem;
            }}
            .notice-title {{
                font-size: 1.4rem;
            }}
            .notice-content {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="notice-container">
        <div class="notice-header">
            <div class="notice-icon">{data.get('아이콘', '📢')}</div>
            <h1 class="notice-title">{data.get('제목', '공지사항')}</h1>
        </div>
        <div class="notice-content">
            {data.get('내용', '공지 내용을 입력하세요.')}
        </div>
        {f'<div class="notice-highlight">{data.get("강조 문구", "")}</div>' if data.get('강조 문구') else ''}
    </div>
</body>
</html>
"""
    return html

# 사이드바 - 템플릿 선택
with st.sidebar:
    st.header("📋 템플릿 선택")
    selected_template = st.radio(
        "콘텐츠 유형을 선택하세요",
        list(TEMPLATES.keys()),
        format_func=lambda x: f"{TEMPLATES[x]['icon']} {x}"
    )
    
    st.markdown("---")
    st.markdown(f"**선택된 템플릿:**  \n{TEMPLATES[selected_template]['description']}")
    
    st.markdown("---")
    st.markdown("### 📊 사용 통계")
    st.metric("금주 생성 건수", "23")
    st.metric("시간 절감", "42시간")

# 메인 영역
col1, col2 = st.columns([1, 1])

with col1:
    st.header("✏️ 콘텐츠 입력")
    
    form_data = {}
    
    # 템플릿별 입력 필드 생성
    if selected_template == "이벤트/프로모션 배너":
        form_data['제목'] = st.text_input("제목", "봄맞이 특별 세일")
        form_data['부제목'] = st.text_input("부제목", "최대 50% 할인 혜택")
        form_data['이미지 URL'] = st.text_input("이미지 URL", "https://via.placeholder.com/500x400")
        form_data['버튼 텍스트'] = st.text_input("버튼 텍스트", "지금 쇼핑하기")
        form_data['버튼 링크'] = st.text_input("버튼 링크", "#")
        
        col_a, col_b = st.columns(2)
        with col_a:
            form_data['배경색'] = st.color_picker("배경색", "#f5f5f5")
        with col_b:
            form_data['텍스트 색상'] = st.color_picker("텍스트 색상", "#333333")
    
    elif selected_template == "랜딩 페이지 블록":
        form_data['메인 제목'] = st.text_input("메인 제목", "새로운 쇼핑 경험")
        form_data['설명'] = st.text_area("설명", "롯데백화점에서 제공하는 프리미엄 서비스를 경험해보세요")
        form_data['이미지 URL'] = st.text_input("이미지 URL", "https://via.placeholder.com/1200x600")
        form_data['특징1'] = st.text_input("특징 1", "빠른 배송")
        form_data['특징2'] = st.text_input("특징 2", "품질 보증")
        form_data['특징3'] = st.text_input("특징 3", "최저가 보장")
        form_data['CTA 버튼'] = st.text_input("CTA 버튼", "지금 시작하기")
        form_data['링크'] = st.text_input("링크", "#")
    
    elif selected_template == "카드형 콘텐츠":
        form_data['카드 개수'] = st.number_input("카드 개수", min_value=1, max_value=6, value=3)
        
        for i in range(int(form_data['카드 개수'])):
            st.markdown(f"**카드 {i+1}**")
            form_data[f'카드{i+1} 제목'] = st.text_input(f"카드 {i+1} 제목", f"상품 {i+1}", key=f"title_{i}")
            form_data[f'카드{i+1} 설명'] = st.text_input(f"카드 {i+1} 설명", "상품 설명", key=f"desc_{i}")
            form_data[f'카드{i+1} 이미지'] = st.text_input(f"카드 {i+1} 이미지", "https://via.placeholder.com/400x300", key=f"img_{i}")
            form_data[f'카드{i+1} 링크'] = st.text_input(f"카드 {i+1} 링크", "#", key=f"link_{i}")
    
    elif selected_template == "공지/안내형":
        form_data['제목'] = st.text_input("제목", "중요 공지사항")
        form_data['내용'] = st.text_area("내용", "안내 드릴 내용을 입력하세요.", height=150)
        form_data['아이콘'] = st.text_input("아이콘 (이모지)", "📢")
        form_data['배경색'] = st.color_picker("배경색", "#fff3cd")
        form_data['강조 문구'] = st.text_input("강조 문구 (선택)", "")
    
    st.markdown("---")
    
    if st.button("🎨 HTML 생성하기", type="primary"):
        # 템플릿별 HTML 생성
        if selected_template == "이벤트/프로모션 배너":
            st.session_state.generated_html = generate_event_banner_html(form_data)
        elif selected_template == "랜딩 페이지 블록":
            st.session_state.generated_html = generate_landing_page_html(form_data)
        elif selected_template == "카드형 콘텐츠":
            st.session_state.generated_html = generate_card_content_html(form_data)
        elif selected_template == "공지/안내형":
            st.session_state.generated_html = generate_notice_html(form_data)
        
        st.success("✅ HTML이 생성되었습니다!")

with col2:
    st.header("👁️ 미리보기 및 다운로드")
    
    # 뷰 모드 선택
    view_mode = st.radio(
        "뷰 모드",
        ["데스크톱", "모바일"],
        horizontal=True
    )
    
    if st.session_state.generated_html:
        # 미리보기
        st.markdown("### 미리보기")
        
        if view_mode == "모바일":
            st.markdown(f"""
            <div style="width: 375px; margin: 0 auto; border: 2px solid #ddd; border-radius: 12px; overflow: hidden;">
                {st.session_state.generated_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.components.v1.html(st.session_state.generated_html, height=600, scrolling=True)
        
        st.markdown("---")
        
        # 다운로드 및 복사
        col_a, col_b = st.columns(2)
        
        with col_a:
            # 다운로드 버튼
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{selected_template.replace('/', '_')}_{timestamp}.html"
            
            st.download_button(
                label="📥 HTML 파일 다운로드",
                data=st.session_state.generated_html,
                file_name=filename,
                mime="text/html"
            )
        
        with col_b:
            # 코드 복사
            if st.button("📋 코드 복사"):
                st.code(st.session_state.generated_html, language="html")
                st.info("👆 위 코드를 복사하세요")
        
        # HTML 코드 표시
        with st.expander("🔍 HTML 코드 보기"):
            st.code(st.session_state.generated_html, language="html")
    
    else:
        st.info("👈 왼쪽에서 콘텐츠를 입력하고 'HTML 생성하기' 버튼을 눌러주세요")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>🏢 롯데백화점 DX팀 | HTML 콘텐츠 생성기 v1.0</p>
    <p style="font-size: 0.9rem;">템플릿 기반 자동 생성으로 퍼블리싱 시간 60% 단축</p>
</div>
""", unsafe_allow_html=True)
