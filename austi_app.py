import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="AUSTI - AI Usage Style Tendency Indicator Test", page_icon="🌟", layout="centered")

st.image("https://raw.githubusercontent.com/easystudio-max/AUSTI-Web/main/austi-logo.png", width=280)

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🌟 AUSTI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #424242;'>AI Usage Style Tendency Indicator Test</h3>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_resource(show_spinner="Google Sheets 연결 중...")
def get_google_sheet():
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_key("1u6GIzlf0jnUT_1EHzdyfPvxrdNv2r-58mO2UFITAYbo")
        return spreadsheet.sheet1
    except Exception as e:
        st.error(f"❌ Google Sheets 연결 실패: {type(e).__name__}")
        return None

if 'step' not in st.session_state:
    st.session_state.step = 0

# Step 0: 동의 + 기본 정보 (교수님 수정 버전 유지)
if st.session_state.step == 0:
    st.subheader("📜 연구 참여 동의서")
    st.write("본 검사는 충북보건과학대학교 글로벌IT학과 정인훈 교수팀의 연구에 활용될 수있으며, 모든 데이터는 익명 처리되어 학술 목적으로만 사용됩니다.")
    consent = st.checkbox("위 내용을 이해하였으며, 연구 참여에 동의합니다.", value=False)
   
    name = st.text_input("이름 또는 별명", placeholder="예: 인훈")
    background = st.text_input("직업/전공/분야", placeholder="예: 공간정보공학")
   
    if st.button("동의하고 검사 시작하기", type="primary") and consent:
        st.session_state.name = name.strip() if name.strip() else f"익명_{datetime.now().strftime('%H%M%S')}"
        st.session_state.background = background.strip()
        st.session_state.answers = []
        st.session_state.step = 1
        st.rerun()

# Step 1: 20문항 + 리커트 척도 설명 (추가 완료)
elif st.session_state.step == 1:
    # ==================== 리커트 척도 설명 ====================
    st.info("""
    **답변 방식 (1~5점 리커트 척도)**  
    1점 : 전혀 그렇지 않다  
    2점 : 그렇지 않은 편이다  
    3점 : 보통이다  
    4점 : 그런 편이다  
    5점 : 매우 그렇다
    """)

    questions = [
        "1. AI에게 지시할 때 세부 단계, 예시, 출력 형식을 구체적으로 지정한다.",
        "2. AI와 자유롭게 대화하면서 새로운 아이디어가 자연스럽게 떠오르는 것을 즐긴다.",
        "3. 출력 결과의 정확성과 일관성을 가장 중요하게 생각한다.",
        "4. AI와의 대화가 자연스럽고 유연하게 흘러가도록 유도한다.",
        "5. 프롬프트를 여러 번 수정하면서 완벽에 가깝게 다듬는다.",
        "6. AI를 주로 오늘 당장 끝내야 할 구체적인 업무 처리에 사용한다.",
        "7. AI와 함께 장기적인 프로젝트 아이디어나 미래 비전을 brainstorm한다.",
        "8. AI 사용 목적은 대부분 실용적이고 즉각적인 효율 향상이다.",
        "9. AI를 통해 새로운 가능성이나 창의적 방향성을 탐색한다.",
        "10. AI에게 구체적인 효율 개선 방안을 요청하는 편이다.",
        "11. AI가 준 답변을 대부분 그대로 받아들이고 활용한다.",
        "12. AI 출력은 항상 다른 출처와 비교·검증한다.",
        "13. AI가 틀릴 가능성은 낮다고 생각한다.",
        "14. 중요한 결정 전에 AI 답변의 출처와 논리를 직접 확인한다.",
        "15. AI를 ‘믿을 만한 조언자’로 대한다.",
        "16. 하나의 AI와 깊이 있게 집중해서 대화하며 문제를 해결하는 걸 선호한다.",
        "17. 여러 AI 도구를 동시에 사용해 비교하고 조율한다.",
        "18. AI와 1:1로 집중하는 시간이 가장 생산적이라고 생각한다.",
        "19. AI 결과를 다른 사람이나 도구와 공유하며 협업한다.",
        "20. AI를 여러 개 연결해서 하나의 시스템처럼 활용하는 편이다."
    ]
    reverse = [2, 4, 7, 9, 12, 14, 17, 19, 20]

    current = len(st.session_state.answers)
    if current < 20:
        st.progress((current + 1) / 20.0)
        st.caption(f"문항 {current + 1} / 20")
        ans = st.slider(questions[current], 1, 5, 3, key=f"q{current}")
        if st.button("다음 문항" if current < 19 else "검사 완료하기", type="primary"):
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
        st.session_state.step = 2
        st.rerun()

# Step 2: 풍성한 보고서 (16개 타입 모두 포함)
elif st.session_state.step == 2:
    reports = {
        "PTRS": {"catch": "정밀 실행 신뢰 솔로형", "desc": "당신은 AI를 '완벽한 개인 비서'처럼 다루는 전략가입니다. 한 번 지시하면 끝까지 철저하게 완성합니다.", "strength": "• 압도적인 정확도와 완성도\n• 혼자서도 체계적으로 일할 수 있는 능력", "weakness": "• 여러 AI를 동시에 다루는 데 익숙하지 않을 수 있음", "tools": "Claude 4 + GPT-4o + Cursor + Perplexity", "tools_reason": "Claude 4와 GPT-4o는 정밀 작업의 최강자, Cursor는 코딩 작업 시 최고, Perplexity는 사실 확인에 최적", "growth": "가끔 Gemini나 Grok을 불러서 'Swarm 모드'로 협업 연습을 해보세요. 생각보다 재미있을 거예요!"},
        "PTRW": {"catch": "정밀 실행 신뢰 스웜형", "desc": "당신은 AI를 '정밀하게 조율된 오케스트라'처럼 다루는 지휘자입니다. 여러 AI를 동시에 움직여 최고의 결과를 냅니다.", "strength": "• 다중 AI 정밀 조율 능력\n• 마감 압박에도 흔들리지 않는 안정감", "weakness": "• 한 도구에 깊게 빠지지 않고 넓게 쓰는 경향", "tools": "GPT-4o + Claude 4 + Gemini + Zapier + Notion AI", "tools_reason": "GPT-4o와 Claude 4로 핵심 작업, Gemini로 창의 보완, Zapier+Notion AI로 자동화 연결", "growth": "가끔 Claude와 1:1로 깊이 대화하며 '창의성 근육'도 키워보세요. 의외로 중독될 수 있어요!"},
        "PTCS": {"catch": "정밀 실행 검증 솔로형", "desc": "당신은 AI를 '철저한 검사관'처럼 다루는 신중한 분석가입니다. 한 번 나온 결과도 끝까지 검증합니다.", "strength": "• 최고 수준의 정확성과 신뢰성", "weakness": "• 창의적 아이디어 탐색이 다소 제한될 수 있음", "tools": "Perplexity + Claude 4 + Felo + GPT-4o", "tools_reason": "Perplexity와 Felo로 빠른 사실 확인, Claude 4로 깊이 있는 분석", "growth": "가끔 Grok이나 Gemini를 불러서 '미친 아이디어'도 실험해보세요. 생각보다 재미있습니다!"},
        "PTCW": {"catch": "정밀 실행 검증 스웜형", "desc": "당신은 AI를 '정밀하게 검증하는 팀'처럼 다루는 전략적 혁신가입니다.", "strength": "• 철저한 검증 + 다중 AI 활용", "weakness": "• 창의적 통찰이 상대적으로 약함", "tools": "Perplexity + Claude 4 + Grok 3 + Zapier + Felo", "tools_reason": "Perplexity+Felo로 검증, Claude 4+Grok 3로 분석, Zapier로 연결", "growth": "Insight 축을 조금만 키우면 진짜 무적 타입이 됩니다!"},
        "PIRS": {"catch": "통찰 실행 신뢰 솔로형", "desc": "당신은 AI를 '깊이 있는 철학자와의 대화'처럼 즐기는 통찰형 솔로 플레이어입니다.", "strength": "• 깊이 있는 통찰 + 정밀 실행", "weakness": "• Swarm 협업이 다소 약함", "tools": "Claude 4 + NotebookLM + Notion AI + GPT-4o", "tools_reason": "Claude 4로 통찰, NotebookLM으로 자료 정리, Notion AI로 연결", "growth": "Swarm 도구를 조금씩 추가하면 완전체가 됩니다!"},
        "PIRW": {"catch": "통찰 실행 신뢰 스웜형", "desc": "당신은 AI를 '미래를 설계하는 건축팀'처럼 다루는 통찰형 스웜 마스터입니다.", "strength": "• 통찰과 다중 AI 조율의 완벽 조화", "weakness": "• 즉시 실행력이 다소 약할 수 있음", "tools": "Grok 3 + Claude 4 + Gemini + Notion AI + Zapier", "tools_reason": "Grok 3와 Claude 4로 통찰, Gemini로 창의, Notion AI+Zapier로 연결", "growth": "Task 축을 조금만 강화하면 진짜 게임 체인저가 됩니다!"},
        "PICS": {"catch": "통찰 실행 검증 솔로형", "desc": "당신은 AI를 '통찰과 검증을 동시에 하는 철학자'처럼 다루는 신중한 솔로 플레이어입니다.", "strength": "• 통찰과 철저한 검증의 균형", "weakness": "• Swarm 능력이 다소 약함", "tools": "NotebookLM + Perplexity + Claude + Felo", "tools_reason": "NotebookLM으로 자료 분석, Perplexity+Felo로 검증, Claude로 종합", "growth": "Swarm 모드를 적극 활용하면 더 강력해집니다!"},
        "PICW": {"catch": "통찰 실행 검증 스웜형", "desc": "당신은 AI를 '통찰과 검증을 연결하는 전략가'처럼 다루는 미래 지향적 혁신가입니다.", "strength": "• 통찰 + 검증 + 다중 AI", "weakness": "• Task 중심 실행력이 약할 수 있음", "tools": "Perplexity + Grok 3 + Claude 4 + Zapier + Felo", "tools_reason": "Perplexity+Felo로 검증, Grok 3+Claude 4로 통찰, Zapier로 연결", "growth": "Task 축을 강화하면 완전체가 됩니다!"},
        "FTRS": {"catch": "자유로운 통찰 신뢰 솔로형", "desc": "당신은 AI를 '창의적인 예술가와의 대화'처럼 즐기는 자유로운 통찰형 솔로 플레이어입니다.", "strength": "• 뛰어난 창의력과 깊이 있는 탐구", "weakness": "• Swarm 협업과 즉시 실행력이 약함", "tools": "Grok 3 + NotebookLM + Canva AI + Notion AI", "tools_reason": "Grok 3로 창의적 통찰, NotebookLM으로 정리, Canva AI로 시각화", "growth": "Swarm과 Task를 조금씩 연습하면 진짜 무적이 됩니다!"},
        "FTRW": {"catch": "자유로운 통찰 신뢰 스웜형", "desc": "당신은 AI를 '혁신적인 아이디어 팩토리'처럼 다루는 자유로운 통찰형 스웜 마스터입니다.", "strength": "• 창의적 아이디어와 다중 AI 조율", "weakness": "• 정밀성과 검증이 다소 약함", "tools": "Grok 3 + Claude 4 + ZenSpark + Zapier + Notion AI", "tools_reason": "Grok 3로 창의, Claude 4로 보완, ZenSpark+Notion AI로 연결", "growth": "Precision과 Check 축을 강화하면 완전체가 됩니다!"},
        "FTCS": {"catch": "자유로운 통찰 검증 솔로형", "desc": "당신은 AI를 '창의성과 검증을 동시에 하는 전략적 창작자'처럼 다룹니다.", "strength": "• 창의성과 검증의 조화", "weakness": "• Swarm 능력이 다소 약함", "tools": "NotebookLM + Perplexity + Grok + Canva AI", "tools_reason": "NotebookLM으로 자료 정리, Perplexity로 검증, Grok으로 창의", "growth": "Swarm 모드를 활용하면 더 강력해집니다!"},
        "FTCW": {"catch": "자유로운 통찰 검증 스웜형", "desc": "당신은 AI를 '미래를 그리는 혁신가'처럼 다루는 자유로운 통찰형 스웜 플레이어입니다.", "strength": "• 창의적 비전과 다중 AI 활용", "weakness": "• Precision과 Task가 다소 약함", "tools": "Grok 3 + Midjourney + ZenSpark + Zapier + Felo", "tools_reason": "Grok 3로 창의, Midjourney로 시각화, ZenSpark+Felo로 검색", "growth": "Precision과 Task를 강화하면 진짜 게임 체인저가 됩니다!"},
        "FIRS": {"catch": "자유로운 통찰 신뢰 솔로형", "desc": "당신은 AI를 '혼자만의 창의적인 철학 대화'처럼 즐기는 자유로운 통찰형 솔로 플레이어입니다.", "strength": "• 뛰어난 창의력과 깊이 있는 탐구", "weakness": "• Swarm 협업과 즉시 실행력이 약함", "tools": "Grok 3 + NotebookLM + Canva AI + Notion AI", "tools_reason": "Grok 3로 통찰, NotebookLM으로 정리, Canva AI로 시각화", "growth": "Swarm과 Task를 조금씩 연습해보세요!"},
        "FIRW": {"catch": "자유로운 통찰 신뢰 스웜형", "desc": "당신은 AI를 '미래를 개척하는 창의적 에코시스템 마스터'처럼 다룹니다.", "strength": "• 창의적 통찰과 다중 AI 조율", "weakness": "• Precision과 검증이 다소 약함", "tools": "Grok 3 + Midjourney + ZenSpark + Zapier + Notion AI", "tools_reason": "Grok 3로 창의, Midjourney로 시각화, ZenSpark+Notion AI로 연결", "growth": "Precision과 Check를 강화하면 완전체가 됩니다!"},
        "FICS": {"catch": "자유로운 통찰 검증 솔로형", "desc": "당신은 AI를 '창의성과 검증을 자유롭게 오가는 전략적 창의가'처럼 다룹니다.", "strength": "• 창의성과 검증의 완벽 조화", "weakness": "• Swarm 능력이 다소 약함", "tools": "NotebookLM + Perplexity + Grok + Canva AI", "tools_reason": "NotebookLM으로 자료 정리, Perplexity로 검증, Grok으로 창의", "growth": "Swarm 모드를 적극 활용해보세요!"},
        "FICW": {"catch": "자유로운 통찰 검증 스웜형", "desc": "당신은 AI를 '통찰과 검증을 연결해 새로운 세상을 만드는 미래 개척자'입니다.", "strength": "• 통찰 + 검증 + 다중 AI", "weakness": "• Task 중심 실행력이 약할 수 있음", "tools": "Grok 3 + Perplexity + ZenSpark + Zapier + Felo", "tools_reason": "Grok 3로 통찰, Perplexity+Felo로 검증, ZenSpark+Zapier로 연결", "growth": "Task 축을 강화하면 진짜 무적이 됩니다!"}
    }

    data = reports.get(st.session_state.test_type, {"catch": "독특한 AI 활용자형", "desc": "AI를 자신만의 독특한 방식으로 활용하는 특별한 타입입니다.", "strength": "강점 분석 중", "weakness": "약점 분석 중", "tools": "추천 도구 준비 중", "tools_reason": "", "growth": "성장 포인트 준비 중"})

    st.subheader(f"📌 당신의 타입: {st.session_state.test_type} - {data['catch']}")
    st.info(data['desc'])
    st.success(f"**💪 강점**\n{data['strength']}")
    st.warning(f"**⚠️ 약점**\n{data['weakness']}")
    st.markdown("**🔥 추천 AI 도구 조합**")
    st.write(data['tools'])
    st.caption(data['tools_reason'])
    st.markdown("**📈 성장 포인트**")
    st.write(data['growth'])

    if st.button("추가 설문으로 이동하기", type="primary"):
        st.session_state.step = 3
        st.rerun()

# Step 3: 추가 설문 + 저장
elif st.session_state.step == 3:
    st.subheader("📋 추가 설문")
    age = st.selectbox("연령대", ["18세 이하", "19~29세", "30~39세", "40~49세", "50세 이상"])
    gender = st.selectbox("성별", ["남성", "여성", "기타", "응답 안함"])
    ai_freq = st.selectbox("AI 도구 사용 빈도", ["매일 사용", "주 3회 이상", "주 1~2회", "월 1회 이하", "거의 사용 안 함"])
    main_tools = st.multiselect("주로 사용하는 AI 도구", ["ChatGPT", "Claude", "Grok", "Gemini", "Perplexity", "ZenSpark", "Notion AI", "Felo", "Canva AI", "기타"])
    usefulness = st.slider("AUSTI 검사가 AI 활용에 얼마나 도움이 되었나요?", 1, 5, 4)
    feedback = st.text_area("AUSTI 검사에 대한 자유로운 의견이나 개선점")

    if st.button("모든 데이터 제출하기", type="primary"):
        sheet = get_google_sheet()
        if sheet is not None:
            data_row = [
                f"AUSTI-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                st.session_state.name,
                st.session_state.background,
                st.session_state.test_type,
                round(sum(st.session_state.final_scores[0:5])/5, 2),
                round(sum(st.session_state.final_scores[5:10])/5, 2),
                round(sum(st.session_state.final_scores[10:15])/5, 2),
                round(sum(st.session_state.final_scores[15:20])/5, 2),
                age, gender, ai_freq, ", ".join(main_tools), usefulness, feedback, True
            ]
            sheet.append_row(data_row)
            st.success("✅ 데이터가 Google Sheets에 성공적으로 저장되었습니다!")
            st.balloons()
            st.session_state.step = 4
            st.rerun()

# Step 4: 완료
elif st.session_state.step == 4:
    st.success("🎉 모든 검사가 완료되었습니다! 연구에 큰 도움이 됩니다.")
    st.balloons()
    if st.button("처음부터 다시 시작하기"):
        st.session_state.clear()
        st.rerun()

st.sidebar.title("AUSTI")
st.sidebar.caption("Developed by Prof. Jeong In Hun with SuperGrok")
