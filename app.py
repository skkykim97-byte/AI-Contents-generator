import base64
from pathlib import Path
from flask import Flask, Response

app = Flask(__name__)
base = Path(__file__).parent


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def get_logo_src() -> str:
    for p in [base / "static" / "img" / "logo.png",
              base / "static" / "img" / "logo.jpg"]:
        if p.exists():
            mime = "jpeg" if p.suffix in (".jpg", ".jpeg") else "png"
            return f"data:image/{mime};base64," + base64.b64encode(p.read_bytes()).decode()
    return ""


# ── 홈 ──────────────────────────────────────────────────
@app.route("/")
def home():
    html = read(base / "pages" / "home.html")
    logo = get_logo_src()
    if logo:
        html = html.replace('src="logo.png"', f'src="{logo}"')
    return Response(html, mimetype="text/html")


# ── 점별 팝업 행사 ────────────────────────────────────────
@app.route("/popup")
def popup():
    html = read(base / "pages" / "branch popup.html")
    back = (
        '<a href="/" class="tb-btn tb-btn-ghost" '
        'style="text-decoration:none;margin-right:4px">← 홈</a>'
        '<div class="tb-divider"></div>'
    )
    html = html.replace('<div class="tb-logo">', back + '<div class="tb-logo">', 1)
    return Response(html, mimetype="text/html")


# ── 준비 중 페이지 ────────────────────────────────────────
def coming_soon(title: str) -> Response:
    html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box;margin:0;padding:0 }}
  body {{ font-family:'Noto Sans KR',sans-serif;background:#F7F7F7;
          display:flex;align-items:center;justify-content:center;height:100vh }}
  .box {{ text-align:center }}
  .emoji {{ font-size:52px;margin-bottom:20px }}
  h2 {{ font-size:20px;font-weight:700;color:#111;margin-bottom:8px }}
  p  {{ font-size:13px;color:#999;margin-bottom:28px }}
  a  {{ display:inline-block;background:#111;color:white;text-decoration:none;
        padding:12px 28px;border-radius:10px;font-size:14px;font-weight:700 }}
  a:hover {{ background:#333 }}
</style>
</head>
<body>
<div class="box">
  <div class="emoji">🚧</div>
  <h2>{title}</h2>
  <p>준비 중입니다. 곧 만나요!</p>
  <a href="/">← 처음으로 돌아가기</a>
</div>
</body></html>"""
    return Response(html, mimetype="text/html")


@app.route("/anniversary")
def anniversary():
    html = read(base / "pages" / "branch anniversary.html")
    back = (
        '<a href="/" class="tb-btn tb-btn-ghost" '
        'style="text-decoration:none;margin-right:4px">← 홈</a>'
        '<div class="tb-divider"></div>'
    )
    html = html.replace('<div class="tb-logo">', back + '<div class="tb-logo">', 1)
    return Response(html, mimetype="text/html")


@app.route("/newopen")
def newopen():
    return coming_soon("New Open 브랜드")


@app.route("/sale")
def sale():
    return coming_soon("SALE 브랜드 안내")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8501, debug=True)
