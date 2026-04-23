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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_home():
    html = read(base / "pages" / "home.html")
    st.components.v1.html(html, height=900, scrolling=True)


def render_popup():
    fonts_css = read(base / "static/css/fonts.css")
    style_css = read(base / "static/css/style.css")
    app_js    = read(base / "static/js/app.js")
    html      = read(base / "templates/index.html")

    html = html.replace(
        "<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/fonts.css') }}\">",
        f"<style>\n{fonts_css}\n</style>",
    )
    html = html.replace(
        "<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/style.css') }}\">",
        f"<style>\n{style_css}\n</style>",
    )
    html = html.replace(
        "<script src=\"{{ url_for('static', filename='js/app.js') }}\"></script>",
        f"<script>\n{app_js}\n</script>",
    )

    # 상단 바에 '← 홈' 버튼 주입
    back_btn = (
        '<button class="tb-btn tb-btn-ghost" '
        'onclick="window.parent.location.href=\'/?\'">← 홈</button>'
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
  body {{
    font-family: 'Noto Sans KR', sans-serif;
    background: #F7F7F7;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }}
  .box {{ text-align: center; }}
  .emoji {{ font-size: 52px; margin-bottom: 20px; }}
  h2 {{ font-size: 20px; font-weight: 700; color: #111; margin-bottom: 8px; }}
  p  {{ font-size: 13px; color: #999; margin-bottom: 28px; }}
  .btn {{
    background: #111;
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    font-family: inherit;
  }}
  .btn:hover {{ background: #333; }}
</style>
</head>
<body>
<div class="box">
  <div class="emoji">🚧</div>
  <h2>{title}</h2>
  <p>준비 중입니다. 곧 만나요!</p>
  <button class="btn" onclick="window.parent.location.href='/?'">← 처음으로 돌아가기</button>
</div>
</body>
</html>"""
    st.components.v1.html(html, height=500, scrolling=False)


# ── 라우팅 ──────────────────────────────────────────────
params = st.query_params
page = params.get("page", "home")

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
