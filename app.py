import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="팝업 행사 생성기",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit 기본 패딩 제거
st.markdown("""
<style>
#root > div:first-child { padding: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
header, footer { display: none !important; }
</style>
""", unsafe_allow_html=True)

base = Path(__file__).parent

fonts_css = (base / "static/css/fonts.css").read_text(encoding="utf-8")
style_css = (base / "static/css/style.css").read_text(encoding="utf-8")
app_js    = (base / "static/js/app.js").read_text(encoding="utf-8")
template  = (base / "templates/index.html").read_text(encoding="utf-8")

# Flask url_for 참조를 인라인 콘텐츠로 교체
html = template
html = html.replace(
    '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/fonts.css\') }}">',
    f"<style>\n{fonts_css}\n</style>",
)
html = html.replace(
    '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/style.css\') }}">',
    f"<style>\n{style_css}\n</style>",
)
html = html.replace(
    '<script src="{{ url_for(\'static\', filename=\'js/app.js\') }}"></script>',
    f"<script>\n{app_js}\n</script>",
)

st.components.v1.html(html, height=960, scrolling=True)
