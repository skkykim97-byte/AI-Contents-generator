import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, List
import html
import json

st.set_page_config(
    page_title="HTML 콘텐츠 생성기",
    page_icon="🧩",
    layout="wide",
)

BASE_CSS = """
* { box-sizing: border-box; }
body { font-family: Arial, sans-serif; }
.content-wrap {
    width: 100%;
    max-width: 960px;
    margin: 0 auto;
    background: #ffffff;
    color: #111827;
}
.hero, .notice, .card-grid, .landing-block {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin: 16px 0;
}
.hero {
    padding: 48px 32px;
    text-align: center;
}
.hero h1 {
    margin: 0 0 12px;
    font-size: 34px;
    line-height: 1.25;
}
.hero p {
    margin: 0 0 24px;
    font-size: 16px;
    line-height: 1.7;
}
.cta-btn {
    display: inline-block;
    text-decoration: none;
    padding: 14px 22px;
    border-radius: 999px;
    font-weight: 700;
}
.notice {
    padding: 24px;
    border-left: 8px solid var(--accent, #4f46e5);
    background: #f8fafc;
}
.notice h3 {
    margin: 0 0 8px;
}
.notice p {
    margin: 0;
    line-height: 1.7;
}
.card-grid {
    padding: 28px;
}
.card-grid h2 {
    margin-top: 0;
    margin-bottom: 18px;
}
.card-grid-inner {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 18px;
}
.card-item {
    padding: 20px;
    border-radius: 14px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
}
.card-item h4 {
    margin: 0 0 8px;
    font-size: 18px;
}
.card-item p {
    margin: 0 0 14px;
    line-height: 1.6;
}
.landing-block {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    min-height: 280px;
    background: #ffffff;
}
.landing-copy {
    padding: 40px 32px;
}
.landing-copy h2 {
    margin: 0 0 12px;
    font-size: 28px;
}
.landing-copy p {
    margin: 0 0 18px;
    line-height: 1.7;
}
.landing-media {
    min-height: 280px;
    background-size: cover;
    background-position: center;
}
.meta-box {
    padding: 18px;
    border: 1px dashed #cbd5e1;
    border-radius: 12px;
    background: #f8fafc;
}
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-top: 14px;
}
.kpi {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
}
.kpi .label {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 8px;
}
.kpi .value {
    font-size: 24px;
    font-weight: 700;
}
@media (max-width: 768px) {
    .hero { padding: 32px 20px; }
    .hero h1 { font-size: 28px; }
    .landing-block { grid-template-columns: 1fr; }
    .landing-media { min-height: 220px; }
}
"""

DEFAULT_TEMPLATES = {
    "이벤트/프로모션 배너": {
        "description": "반복형 프로모션 배너를 빠르게 생성합니다.",
        "fields": [
            {"key": "title", "label": "메인 카피", "type": "text", "default": "제작 시간을 줄이는 HTML 자동 생성 도구"},
            {"key": "subtitle", "label": "서브 카피", "type": "textarea", "default": "반복형 콘텐츠를 템플릿화해 초안 생성부터 퍼블리싱 검수까지 더 빠르게 연결합니다."},
            {"key": "button_text", "label": "버튼 텍스트", "type": "text", "default": "도입안 보기"},
            {"key": "button_link", "label": "버튼 링크", "type": "text", "default": "https://example.com"},
            {"key": "bg_color", "label": "배경 색상", "type": "color", "default": "#EEF2FF"},
            {"key": "text_color", "label": "텍스트 색상", "type": "color", "default": "#111827"},
            {"key": "accent_color", "label": "버튼 색상", "type": "color", "default": "#4F46E5"},
        ],
    },
    "랜딩 페이지 블록": {
        "description": "카피와 이미지 중심의 블록형 랜딩 섹션을 생성합니다.",
        "fields": [
            {"key": "headline", "label": "헤드라인", "type": "text", "default": "반복형 콘텐츠 제작, 이제 더 가볍게"},
            {"key": "body", "label": "본문", "type": "textarea", "default": "템플릿 기반 입력만으로 HTML 초안을 자동 생성해 퍼블리싱 병목을 줄이고 제작 리드타임을 단축합니다."},
            {"key": "button_text", "label": "버튼 텍스트", "type": "text", "default": "템플릿 선택하기"},
            {"key": "button_link", "label": "버튼 링크", "type": "text", "default": "https://example.com"},
            {"key": "image_url", "label": "이미지 URL", "type": "text", "default": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80"},
            {"key": "section_bg", "label": "섹션 배경", "type": "color", "default": "#FFFFFF"},
            {"key": "accent_color", "label": "포인트 색상", "type": "color", "default": "#0F766E"},
        ],
    },
    "카드형 콘텐츠": {
        "description": "기능/효과/안내를 카드 리스트 형태로 구성합니다.",
        "fields": [
            {"key": "section_title", "label": "섹션 제목", "type": "text", "default": "핵심 기대 효과"},
            {"key": "section_desc", "label": "섹션 설명", "type": "textarea", "default": "반복 작업을 줄이고, 퍼블리싱 병목을 완화하며, 표준화된 결과물을 빠르게 만듭니다."},
            {"key": "card1_title", "label": "카드 1 제목", "type": "text", "default": "시간 절감"},
            {"key": "card1_desc", "label": "카드 1 설명", "type": "textarea", "default": "기존 2~3시간 작업을 30분~1시간 수준으로 단축"},
            {"key": "card2_title", "label": "카드 2 제목", "type": "text", "default": "병목 완화"},
            {"key": "card2_desc", "label": "카드 2 설명", "type": "textarea", "default": "퍼블리셔가 고난도 작업에 집중할 수 있는 구조로 전환"},
            {"key": "card3_title", "label": "카드 3 제목", "type": "text", "default": "표준화"},
            {"key": "card3_desc", "label": "카드 3 설명", "type": "textarea", "default": "브랜드 가이드와 UI 일관성을 템플릿 기반으로 유지"},
            {"key": "bg_color", "label": "배경 색상", "type": "color", "default": "#F8FAFC"},
            {"key": "accent_color", "label": "포인트 색상", "type": "color", "default": "#DC2626"},
        ],
    },
    "공지/안내형 콘텐츠": {
        "description": "운영 공지, 안내, 변경사항 전달에 적합한 포맷입니다.",
        "fields": [
            {"key": "title", "label": "공지 제목", "type": "text", "default": "콘텐츠 제작 프로세스가 더 빨라집니다"},
            {"key": "message", "label": "공지 내용", "type": "textarea", "default": "반복형 콘텐츠는 템플릿 기반 자동 생성 구조로 전환되어, 초안 제작과 검수 리드타임이 단축됩니다."},
            {"key": "accent_color", "label": "강조 색상", "type": "color", "default": "#2563EB"},
            {"key": "bg_color", "label": "배경 색상", "type": "color", "default": "#EFF6FF"},
        ],
    },
}


@dataclass
class TemplateDef:
    name: str
    description: str
    fields: List[Dict] = field(default_factory=list)


def escape(value: str) -> str:
    return html.escape(str(value or ""), quote=True)


def render_field(field: Dict, value: str):
    label = field["label"]
    key = f"field_{field['key']}"
    field_type = field.get("type", "text")
    if field_type == "textarea":
        return st.text_area(label, value=value, key=key, height=110)
    if field_type == "color":
        return st.color_picker(label, value=value or "#000000", key=key)
    return st.text_input(label, value=value, key=key)


def build_html(template_name: str, data: Dict[str, str]) -> str:
    if template_name == "이벤트/프로모션 배너":
        return f"""
<div class="content-wrap">
  <section class="hero" style="background:{escape(data['bg_color'])}; color:{escape(data['text_color'])};">
    <h1>{escape(data['title'])}</h1>
    <p>{escape(data['subtitle'])}</p>
    <a class="cta-btn" href="{escape(data['button_link'])}" style="background:{escape(data['accent_color'])}; color:#ffffff;">{escape(data['button_text'])}</a>
  </section>
</div>
"""
    if template_name == "랜딩 페이지 블록":
        image_style = f"background-image:url('{escape(data['image_url'])}');"
        return f"""
<div class="content-wrap">
  <section class="landing-block" style="background:{escape(data['section_bg'])};">
    <div class="landing-copy">
      <h2 style="color:{escape(data['accent_color'])};">{escape(data['headline'])}</h2>
      <p>{escape(data['body'])}</p>
      <a class="cta-btn" href="{escape(data['button_link'])}" style="background:{escape(data['accent_color'])}; color:#ffffff;">{escape(data['button_text'])}</a>
    </div>
    <div class="landing-media" style="{image_style}"></div>
  </section>
</div>
"""
    if template_name == "카드형 콘텐츠":
        cards = "".join([
            f'''<div class="card-item"><h4 style="color:{escape(data['accent_color'])};">{escape(data[f'card{i}_title'])}</h4><p>{escape(data[f'card{i}_desc'])}</p></div>'''
            for i in range(1, 4)
        ])
        return f"""
<div class="content-wrap">
  <section class="card-grid" style="background:{escape(data['bg_color'])};">
    <h2>{escape(data['section_title'])}</h2>
    <p>{escape(data['section_desc'])}</p>
    <div class="card-grid-inner">{cards}</div>
  </section>
</div>
"""
    if template_name == "공지/안내형 콘텐츠":
        return f"""
<div class="content-wrap">
  <section class="notice" style="background:{escape(data['bg_color'])}; --accent:{escape(data['accent_color'])};">
    <h3>{escape(data['title'])}</h3>
    <p>{escape(data['message'])}</p>
  </section>
</div>
"""
    return "<div>지원하지 않는 템플릿입니다.</div>"


def wrap_full_html(body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>유형별 HTML 콘텐츠 생성기</title>
  <style>{BASE_CSS}</style>
</head>
<body>
{body_html}
</body>
</html>
"""


def init_state():
    if "templates" not in st.session_state:
        st.session_state.templates = {
            name: TemplateDef(name=name, description=v["description"], fields=v["fields"])
            for name, v in DEFAULT_TEMPLATES.items()
        }
    if "generated_history" not in st.session_state:
        st.session_state.generated_history = []


def add_custom_template(name: str, description: str):
    if not name.strip():
        st.warning("템플릿 이름을 입력해주세요.")
        return
    if name in st.session_state.templates:
        st.warning("같은 이름의 템플릿이 이미 존재합니다.")
        return
    st.session_state.templates[name] = TemplateDef(
        name=name,
        description=description,
        fields=[
            {"key": "title", "label": "제목", "type": "text", "default": "새 템플릿 제목"},
            {"key": "body", "label": "본문", "type": "textarea", "default": "새 템플릿 설명"},
            {"key": "accent_color", "label": "포인트 색상", "type": "color", "default": "#7C3AED"},
        ],
    )
    st.success(f"'{name}' 템플릿이 추가되었습니다.")


def management_panel():
    with st.expander("관리자 옵션: 템플릿 관리", expanded=False):
        st.caption("운영 담당자가 템플릿 구조를 확장하는 상황을 가정한 MVP 영역입니다.")
        col_a, col_b = st.columns(2)
        with col_a:
            new_name = st.text_input("신규 템플릿 이름", value="")
        with col_b:
            new_desc = st.text_input("신규 템플릿 설명", value="")
        if st.button("신규 템플릿 추가"):
            add_custom_template(new_name, new_desc)

        template_export = {
            name: {"description": t.description, "fields": t.fields}
            for name, t in st.session_state.templates.items()
        }
        st.download_button(
            "현재 템플릿 정의 JSON 다운로드",
            data=json.dumps(template_export, ensure_ascii=False, indent=2),
            file_name="template_definitions.json",
            mime="application/json",
        )


def sidebar_overview():
    st.sidebar.title("운영 개요")
    st.sidebar.markdown(
        """
- 반복형 콘텐츠를 템플릿화
- 입력값 기반 HTML 초안 자동 생성
- 실시간 미리보기 및 다운로드 지원
- 퍼블리싱 병목 완화와 표준화 목표
"""
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("기대 효과")
    st.sidebar.metric("제작 시간", "30분~1시간", "기존 대비 단축")
    st.sidebar.metric("예상 절감", "60~70%", "반복 작업 기준")
    st.sidebar.metric("주간 요청량", "20~30건", "반복형 중심 대응")


def main():
    init_state()
    sidebar_overview()

    st.title("유형별 HTML 콘텐츠 생성기 / 퍼블리싱 도입 기획 MVP")
    st.caption("반복형 콘텐츠의 초안 생성과 표준화를 지원하는 Streamlit 기반 내부 도구 예시")

    top1, top2 = st.columns([1.2, 1])
    with top1:
        st.markdown(
            """
<div class="meta-box">
  <strong>도입 목적</strong><br/>
  반복형 콘텐츠를 템플릿 기반으로 생성하여, 디자인/퍼블리싱 이중 작업을 줄이고 실무형 초안 생성 + 검수 구조로 전환합니다.
</div>
""",
            unsafe_allow_html=True,
        )
    with top2:
        st.markdown(
            """
<div class="kpi-grid">
  <div class="kpi"><div class="label">현재 제작 시간</div><div class="value">2~3시간</div></div>
  <div class="kpi"><div class="label">도입 후 목표</div><div class="value">30~60분</div></div>
  <div class="kpi"><div class="label">운영 방식</div><div class="value">초안+검수</div></div>
</div>
""",
            unsafe_allow_html=True,
        )

    management_panel()

    template_names = list(st.session_state.templates.keys())
    selected_template = st.selectbox("콘텐츠 유형 선택", template_names)
    template = st.session_state.templates[selected_template]

    st.info(template.description)

    left, right = st.columns([1, 1.1])

    with left:
        st.subheader("입력 폼")
        form_values = {}
        for field in template.fields:
            form_values[field["key"]] = render_field(field, field.get("default", ""))

        generate = st.button("HTML 생성", type="primary", use_container_width=True)

        if generate:
            body_html = build_html(selected_template, form_values)
            full_html = wrap_full_html(body_html)
            st.session_state.current_body_html = body_html
            st.session_state.current_full_html = full_html
            st.session_state.generated_history.insert(0, {
                "template": selected_template,
                "title": form_values.get("title") or form_values.get("headline") or form_values.get("section_title") or "Untitled",
            })
            st.success("HTML 초안을 생성했습니다.")

        if "current_full_html" in st.session_state:
            st.download_button(
                "HTML 파일 다운로드",
                data=st.session_state.current_full_html,
                file_name="generated_content.html",
                mime="text/html",
                use_container_width=True,
            )
            st.code(st.session_state.current_full_html, language="html")

    with right:
        st.subheader("실시간 미리보기")
        if "current_body_html" in st.session_state:
            preview_mode = st.radio("뷰 옵션", ["Desktop", "Mobile"], horizontal=True)
            width = 390 if preview_mode == "Mobile" else None
            preview_html = f"<style>{BASE_CSS}</style>{st.session_state.current_body_html}"
            st.components.v1.html(preview_html, height=700, width=width, scrolling=True)
        else:
            st.markdown("미리보기를 보려면 왼쪽에서 값을 입력하고 **HTML 생성**을 눌러주세요.")

    st.markdown("---")
    hist_col, summary_col = st.columns([1, 1.2])
    with hist_col:
        st.subheader("최근 생성 이력")
        if st.session_state.generated_history:
            for item in st.session_state.generated_history[:5]:
                st.write(f"- [{item['template']}] {item['title']}")
        else:
            st.write("아직 생성 이력이 없습니다.")

    with summary_col:
        st.subheader("기획 반영 포인트")
        st.markdown(
            """
- **반복형 콘텐츠 중심**으로 템플릿을 제공
- **비전문 인력도 초안 생성 가능**하도록 입력 폼 구성
- **HTML 자동 생성 + 다운로드**로 퍼블리싱 전환 비용 축소
- **실시간 미리보기**로 검수/수정 속도 향상
- **관리자 템플릿 관리 영역**으로 확장 가능성 반영
"""
        )


if __name__ == "__main__":
    main()
