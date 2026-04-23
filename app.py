import base64
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="롯데백화점 콘텐츠 생성기",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#root > div:first-child { padding: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
header, footer { display: none !important; }
</style>
""", unsafe_allow_html=True)

base = Path(__file__).parent

# 로고 이미지 fallback SVG (파일이 없을 때)
_LOGO_SVG = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "width='36' height='36'%3E%3Crect width='36' height='36' rx='9' fill='%23111'/%3E"
    "%3Ctext x='18' y='27' text-anchor='middle' font-family='Georgia,serif' "
    "font-style='italic' font-size='24' fill='white'%3E%E2%84%93%3C/text%3E%3C/svg%3E"
)


def get_logo_src() -> str:
    """static/img/logo.png(jpg) 를 base64로 반환. 없으면 SVG fallback."""
    for p in [
        base / "static" / "img" / "logo.png",
        base / "static" / "img" / "logo.jpg",
        base / "static" / "img" / "logo.jpeg",
    ]:
        if p.exists():
            mime = "jpeg" if p.suffix in (".jpg", ".jpeg") else "png"
            data = base64.b64encode(p.read_bytes()).decode()
            return f"data:image/{mime};base64,{data}"
    return _LOGO_SVG


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_home():
    html = read(base / "pages" / "home.html")
    html = html.replace("LOGO_PLACEHOLDER", get_logo_src())
    st.components.v1.html(html, height=900, scrolling=True)


def render_popup():
    """pages/branch popup.html — self-contained, 홈 버튼 주입."""
    html = read(base / "pages" / "branch popup.html")
    back_btn = (
        '<form method="GET" action="/" target="_top" style="display:inline">'
        '<button type="submit" class="tb-btn tb-btn-ghost" style="margin-right:4px">← 홈</button>'
        '</form>'
        '<div class="tb-divider"></div>'
    )
    html = html.replace('<div class="tb-logo">', back_btn + '<div class="tb-logo">', 1)
    st.components.v1.html(html, height=960, scrolling=True)


def render_coming_soon(title: str):
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Noto Sans KR', sans-serif; background: #F7F7F7;
          display: flex; align-items: center; justify-content: center; height: 100vh; }}
  .box {{ text-align: center; }}
  .emoji {{ font-size: 52px; margin-bottom: 20px; }}
  h2 {{ font-size: 20px; font-weight: 700; color: #111; margin-bottom: 8px; }}
  p  {{ font-size: 13px; color: #999; margin-bottom: 28px; }}
  .btn {{ background: #111; color: white; border: none; padding: 12px 28px;
          border-radius: 10px; font-size: 14px; font-weight: 700;
          cursor: pointer; font-family: inherit; }}
  .btn:hover {{ background: #333; }}
</style>
</head>
<body>
<div class="box">
  <div class="emoji">🚧</div>
  <h2>{title}</h2>
  <p>준비 중입니다. 곧 만나요!</p>
  <form method="GET" action="/" target="_top">
    <button type="submit" class="btn">← 처음으로 돌아가기</button>
  </form>
</div>
</body>
</html>"""
    st.components.v1.html(html, height=500, scrolling=False)


# ── 라우팅 ──────────────────────────────────────────────
page = st.query_params.get("page", "home")

if page == "popup":
    render_popup()
elif page == "anniversary":
    render_coming_soon("개점 N주년 행사")
elif page == "newopen":
    render_coming_soon("New Open 브랜드")
elif page == "sale":
    render_coming_soon("SALE 브랜드 안내")
else:
    render_home()
