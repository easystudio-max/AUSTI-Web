import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="AUSTI - AI 사용 성향 검사", page_icon="🌟", layout="centered")

st.image("https://raw.githubusercontent.com/easystudio-max/AUSTI-Web/main/austi-logo.png", width=320)

st.title("🌟 AUSTI")
st.subheader("AI 사용 성향 검사")

# ==================== Google Sheets 연결 ====================
@st.cache_resource
def get_google_sheet():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    gc = gspread.authorize(credentials)
    return gc.open("AUSTI_연구데이터").sheet1

if 'step' not in st.session_state:
    st.session_state.step = 0

# Step 0: 연구 동의서
if st.session_state.step == 0:
    st.subheader("📜 연구 참여 동의서")
    st.write("본 검사는 충북보건과학대학교 글로벌IT학과 정인훈 교수 연구를 위한 것입니다. 모든 데이터는 익명 처리되어 학술 목적으로만 사용됩니다.")
    consent = st.checkbox("위 내용을 이해하였으며, 연구 참여에 동의합니다.", value=False)
    
    name = st.text_input("이름 또는 별명", placeholder="예: 인훈")
    background = st.text_input("직업/전공/분야", placeholder="예: 공간정보공학")
    
    if st.button("동의하고 검사 시작하기", type="primary") and consent:
        st.session_state.name = name.strip() if name.strip() else f"익명_{uuid.uuid4().hex[:6]}"
        st.session_state.background = background.strip()
        st.session_state.answers = []
        st.session_state.step = 1
        st.rerun()

# Step 1: AUSTI 검사
elif st.session_state.step == 1:
    questions = [
        "1. AI에게 지시할 때 세부 단계와 예시를 반드시 포함한다.", "2. AI와 대화할 때 자유로운 아이디어 폭발을 즐긴다.",
        "3. 출력 결과의 정확성과 일관성을 가장 중요하게 생각한다.", "4. AI와의 대화가 자연스럽게 흘러가도록 유도하는 편이다.",
        "5. 프롬프트를 여러 번 수정하면서 완벽에 가깝게 다듬는다.", "6. AI는 구체적인 업무를 빠르게 처리하는 데 최적이라고 믿는다.",
        "7. AI와 함께 장기적인 프로젝트 아이디어를 brainstorm하는 시간을 즐긴다.", "8. AI 사용 목적은 대부분 ‘오늘 당장 끝내야 할 일’이다.",
        "9. AI를 통해 새로운 가능성이나 창의적 방향을 탐색한다.", "10. AI에게 구체적인 효율 개선 방안을 요청하는 편이다.",
        "11. AI가 준 답변을 대부분 그대로 받아들이고 활용한다.", "12. AI 출력은 항상 다른 출처와 비교·검증한다.",
        "13. AI가 틀릴 가능성은 낮다고 생각한다.", "14. 중요한 결정 전에 AI 답변의 출처와 논리를 직접 확인한다.",
        "15. AI를 ‘믿을 만한 조언자’로 대한다.", "16. 하나의 AI와 깊이 있게 대화하며 문제를 해결하는 걸 선호한다.",
        "17. 여러 AI 도구를 동시에 사용해 비교한다.", "18. AI와 1:1로 집중하는 시간이 가장 생산적이다.",
        "19. AI 결과를 Slack/노션/다른 사람과 공유하며 협업한다.", "20. AI를 ‘혼자서만 쓰는 개인 비서’처럼 활용한다."
    ]
    reverse = [2,4,7,9,12,14,17,19]

    current = len(st.session_state.answers)
    if current < 20:
        st.progress((current + 1) / 20.0)
        st.write(f"**문항 {current + 1} / 20**")
        ans = st.slider(questions[current], 1, 5, 3, key=f"q{current}")
        if st.button("다음 문항"):
            st.session_state.answers.append(ans)
            st.rerun()
    else:
        final_scores = [6 - s if (i+1) in reverse else s for i, s in enumerate(st.session_state.answers)]
        p = sum(final_scores[0:5]) / 5
        t = sum(final_scores[5:10]) / 5
        r = sum(final_scores[10:15]) / 5
        s = sum(final_scores[15:20]) / 5
        base_type = ("P" if p <= 3 else "F") + ("T" if t <= 3 else "I") + ("R" if r <= 3 else "C") + ("S" if s <= 3 else "W")
        
        st.session_state.test_type = base_type
        st.session_state.final_scores = final_scores
        st.success("검사 완료되었습니다!")
        st.balloons()
        st.subheader(f"📌 당신의 타입: {base_type}")
        st.session_state.step = 2
        st.rerun()

# Step 2: 연구용 추가 설문
elif st.session_state.step == 2:
    st.subheader("📋 연구용 추가 설문")
    age = st.selectbox("연령대", ["18세 이하", "19~29세", "30~39세", "40~49세", "50세 이상"])
    gender = st.selectbox("성별", ["남성", "여성", "기타", "응답 안함"])
    ai_freq = st.selectbox("AI 도구 사용 빈도", ["매일 사용", "주 3회 이상", "주 1~2회", "월 1회 이하", "거의 사용 안 함"])
    main_tools = st.multiselect("주로 사용하는 AI 도구", ["ChatGPT", "Claude", "Grok", "Gemini", "Perplexity", "ZenSpark", "Notion AI", "Felo", "Canva AI", "기타"])
    usefulness = st.slider("AUSTI 검사가 AI 활용에 얼마나 도움이 되었나요?", 1, 5, 4)
    feedback = st.text_area("AUSTI 검사에 대한 자유로운 의견이나 개선점")

    if st.button("모든 데이터 제출하기", type="primary"):
        sheet = get_google_sheet()
        data = {
            "unique_id": f"AUSTI-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": st.session_state.name,
            "background": st.session_state.background,
            "type": st.session_state.test_type,
            "p_score": round(sum(st.session_state.final_scores[0:5])/5, 2),
            "t_score": round(sum(st.session_state.final_scores[5:10])/5, 2),
            "r_score": round(sum(st.session_state.final_scores[10:15])/5, 2),
            "s_score": round(sum(st.session_state.final_scores[15:20])/5, 2),
            "age": age,
            "gender": gender,
            "ai_freq": ai_freq,
            "main_tools": ", ".join(main_tools),
            "usefulness": usefulness,
            "feedback": feedback,
            "consent": True
        }
        sheet.append_row(list(data.values()))
        st.session_state.step = 3
        st.rerun()

# Step 3: 감사 페이지
elif st.session_state.step == 3:
    st.success("🎉 모든 검사가 완료되었습니다! 연구에 큰 도움이 됩니다.")
    st.balloons()
    if st.button("처음부터 다시 시작하기"):
        st.session_state.clear()
        st.rerun()

st.sidebar.title("AUSTI")
st.sidebar.caption("Developed by 정인훈 교수 with SuperGrok")
