import streamlit as st

st.set_page_config(page_title="AUSTI - AI 사용 성향 검사", page_icon="🌟", layout="centered")

# 로고
st.image("https://raw.githubusercontent.com/easystudio-max/AUSTI-Web/main/austi-logo.png", width=320)

st.title("🌟 AUSTI")
st.subheader("AI Usage Style Tendency Indicator")

st.info("""
**응답 방법**  
각 문항을 읽고 자신에게 해당하는 정도를 선택해주세요.

**1** = 전혀 그렇지 않다 **2** = 거의 그렇지 않다 **3** = 보통이다  
**4** = 대체로 그렇다 **5** = 매우 그렇다
""")

name = st.text_input("이름 또는 별명", placeholder="예: 인훈")
background = st.text_input("직업/전공/분야", placeholder="예: IT계열")

if st.button("검사 시작하기", type="primary"):
    if not name.strip():
        st.error("이름을 입력해주세요.")
    else:
        st.session_state.name = name.strip()
        st.session_state.background = background.strip()
        st.session_state.answers = []
        st.session_state.step = 1
        st.rerun()

if 'step' in st.session_state and st.session_state.step == 1:
    questions = [
        "1. AI에게 지시할 때 세부 단계와 예시를 반드시 포함한다.",
        "2. AI와 대화할 때 자유로운 아이디어 폭발을 즐긴다.",
        "3. 출력 결과의 정확성과 일관성을 가장 중요하게 생각한다.",
        "4. AI와의 대화가 자연스럽게 흘러가도록 유도하는 편이다.",
        "5. 프롬프트를 여러 번 수정하면서 완벽에 가깝게 다듬는다.",
        "6. AI는 구체적인 업무(보고서 작성, 코드 디버깅 등)를 빠르게 처리하는 데 최적이라고 믿는다.",
        "7. AI와 함께 장기적인 프로젝트 아이디어를 brainstorm하는 시간을 즐긴다.",
        "8. AI 사용 목적은 대부분 ‘오늘 당장 끝내야 할 일’이다.",
        "9. AI를 통해 새로운 가능성이나 창의적 방향을 탐색한다.",
        "10. AI에게 구체적인 효율 개선 방안을 요청하는 편이다.",
        "11. AI가 준 답변을 대부분 그대로 받아들이고 활용한다.",
        "12. AI 출력은 항상 다른 출처와 비교·검증한다.",
        "13. AI가 틀릴 가능성은 낮다고 생각한다.",
        "14. 중요한 결정 전에 AI 답변의 출처와 논리를 직접 확인한다.",
        "15. AI를 ‘믿을 만한 조언자’로 대한다.",
        "16. 하나의 AI와 깊이 있게 대화하며 문제를 해결하는 걸 선호한다.",
        "17. 여러 AI 도구(Claude, Grok, Perplexity 등)를 동시에 사용해 비교한다.",
        "18. AI와 1:1로 집중하는 시간이 가장 생산적이다.",
        "19. AI 결과를 Slack/노션/다른 사람과 공유하며 협업한다.",
        "20. AI를 ‘혼자서만 쓰는 개인 비서’처럼 활용한다."
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

        st.success("검사 완료되었습니다!")
        st.balloons()

        st.subheader(f"📌 당신의 타입: {base_type}")

        # ==================== 16개 타입 완전 보고서 (최신 도구 반영) ====================
        reports = {
            "PTRS": {
                "catch": "정밀 실행 신뢰 솔로형",
                "desc": "AI에게 매우 구체적이고 구조적인 지시를 주며, 혼자서도 오류 없이 완성도 높은 결과를 만들어냅니다.",
                "strength": "• 높은 정확도와 완성도\n• 혼자서도 체계적인 작업 가능",
                "weakness": "• 여러 AI를 동시에 활용하는 데 익숙하지 않을 수 있음",
                "tools": "Claude 4 + GPT-4o + Cursor + Perplexity\n(정밀 작업에 최적화된 도구들)",
                "growth": "Swarm 모드로 Gemini나 Grok을 추가해 협업 능력을 키워보세요."
            },
            "PTRW": {
                "catch": "정밀 실행 신뢰 스웜형",
                "desc": "정밀한 지시와 실행력을 바탕으로 여러 AI를 동시에 조율합니다. 생산성을 극대화하는 AI 에코시스템 마스터입니다.",
                "strength": "• 다중 AI 정밀 조율\n• 마감 압박에도 안정적",
                "weakness": "• 한 도구에 깊게 빠지지 않고 넓게 쓰는 경향",
                "tools": "GPT-4o + Claude 4 + Gemini + Zapier + Notion AI\n(자동화와 생산성 극대화에 강함)",
                "growth": "가끔 Solo 모드로 Claude와 깊이 대화하며 창의성을 키워보세요."
            },
            "PTCS": {
                "catch": "정밀 실행 검증 솔로형",
                "desc": "정밀한 지시와 철저한 검증을 혼자서 해내는 신중한 분석가입니다.",
                "strength": "• 최고 수준의 정확성과 신뢰성",
                "weakness": "• 창의적 아이디어 탐색이 다소 제한될 수 있음",
                "tools": "Perplexity + Claude 4 + Felo + GPT-4o\n(검증과 사실 확인에 최적)",
                "growth": "Insight 축을 강화해 장기적 비전을 탐색해보세요."
            },
            "PTCW": {
                "catch": "정밀 실행 검증 스웜형",
                "desc": "정밀한 실행과 검증을 여러 AI와 연결해 최적의 결과를 도출합니다.",
                "strength": "• 철저한 검증 + 다중 AI 활용",
                "weakness": "• 창의적 통찰이 상대적으로 약함",
                "tools": "Perplexity + Claude 4 + Grok 3 + Zapier + Felo\n(검증과 자동화의 완벽 조합)",
                "growth": "Insight 축을 강화해 장기적 아이디어를 탐색해보세요."
            },
            "PIRS": {
                "catch": "통찰 실행 신뢰 솔로형",
                "desc": "통찰력 있는 큰 그림을 정밀하게 실행하며, 혼자서도 깊이 있는 AI 결과를 만들어냅니다.",
                "strength": "• 깊이 있는 통찰 + 정밀 실행",
                "weakness": "• Swarm 협업이 다소 약함",
                "tools": "Claude 4 + NotebookLM + Notion AI + GPT-4o\n(통찰과 정리·기록에 강함)",
                "growth": "Swarm 도구를 도입해 협업 능력을 키워보세요."
            },
            "PIRW": {
                "catch": "통찰 실행 신뢰 스웜형",
                "desc": "통찰을 바탕으로 여러 AI를 연결해 큰 그림을 실현하는 미래 지향적 건축가입니다.",
                "strength": "• 통찰과 다중 AI 조율의 완벽 조화",
                "weakness": "• 즉시 실행력이 다소 약할 수 있음",
                "tools": "Grok 3 + Claude 4 + Gemini + Notion AI + Zapier\n(통찰과 자동화의 강력 조합)",
                "growth": "Task 축을 강화해 아이디어를 빠르게 실행해보세요."
            },
            "PICS": {
                "catch": "통찰 실행 검증 솔로형",
                "desc": "통찰과 검증을 동시에 추구하며 혼자서도 신뢰할 수 있는 AI 결과를 만드는 타입입니다.",
                "strength": "• 통찰과 철저한 검증의 균형",
                "weakness": "• Swarm 능력이 다소 약함",
                "tools": "NotebookLM + Perplexity + Claude + Felo\n(통찰과 검증에 최적)",
                "growth": "Swarm 모드를 적극 활용해보세요."
            },
            "PICW": {
                "catch": "통찰 실행 검증 스웜형",
                "desc": "통찰과 검증을 바탕으로 여러 AI를 연결해 새로운 가능성을 여는 전략적 혁신가입니다.",
                "strength": "• 통찰 + 검증 + 다중 AI",
                "weakness": "• Task 중심 실행력이 약할 수 있음",
                "tools": "Perplexity + Grok 3 + Claude 4 + Zapier + Felo\n(검증 중심 다중 AI 활용)",
                "growth": "Task 축을 강화해 아이디어를 빠르게 실행해보세요."
            },
            "FTRS": {
                "catch": "자유로운 통찰 신뢰 솔로형",
                "desc": "자유로운 흐름과 통찰로 혼자서도 창의적이고 깊이 있는 AI 결과를 만들어내는 예술가형입니다.",
                "strength": "• 뛰어난 창의력과 깊이 있는 탐구",
                "weakness": "• Swarm 협업과 즉시 실행력이 약함",
                "tools": "Grok 3 + NotebookLM + Canva AI + Notion AI\n(창의적 아이디어 생성과 정리)",
                "growth": "Swarm과 Task 축을 강화해 아이디어를 실행으로 연결해보세요."
            },
            "FTRW": {
                "catch": "자유로운 통찰 신뢰 스웜형",
                "desc": "자유로운 흐름을 여러 AI와 연결해 혁신적인 비전을 실현하는 창의적 혁신가입니다.",
                "strength": "• 창의적 아이디어와 다중 AI 조율",
                "weakness": "• 정밀성과 검증이 다소 약함",
                "tools": "Grok 3 + Claude 4 + ZenSpark + Zapier + Notion AI\n(창의적 연결과 자동화)",
                "growth": "Precision과 Check 축을 강화해보세요."
            },
            "FTCS": {
                "catch": "자유로운 통찰 검증 솔로형",
                "desc": "자유로운 흐름과 철저한 검증을 병행하는 전략적 창작자입니다.",
                "strength": "• 창의성과 검증의 조화",
                "weakness": "• Swarm 능력이 다소 약함",
                "tools": "NotebookLM + Perplexity + Grok + Canva AI\n(창의적 검증에 최적)",
                "growth": "Swarm 모드를 활용해보세요."
            },
            "FTCW": {
                "catch": "자유로운 통찰 검증 스웜형",
                "desc": "자유로운 흐름을 검증하며 여러 AI를 연결하는 미래 지향적 혁신가입니다.",
                "strength": "• 창의적 비전과 다중 AI 활용",
                "weakness": "• Precision과 Task가 다소 약함",
                "tools": "Grok 3 + Midjourney + ZenSpark + Zapier + Felo\n(창의적 시각화와 연결)",
                "growth": "Precision과 Task 축을 강화해보세요."
            },
            "FIRS": {
                "catch": "자유로운 통찰 신뢰 솔로형",
                "desc": "통찰과 자유로운 흐름으로 혼자서도 깊이 있는 창의성을 발휘합니다.",
                "strength": "• 뛰어난 창의력과 깊이 있는 탐구",
                "weakness": "• Swarm 협업과 즉시 실행력이 약함",
                "tools": "Grok 3 + NotebookLM + Canva AI + Notion AI\n(개인 창의 작업에 강함)",
                "growth": "Swarm과 Task 축을 강화해보세요."
            },
            "FIRW": {
                "catch": "자유로운 통찰 신뢰 스웜형",
                "desc": "통찰을 바탕으로 여러 AI를 연결해 미래를 개척하는 창의적 에코시스템 마스터입니다.",
                "strength": "• 창의적 통찰과 다중 AI 조율",
                "weakness": "• Precision과 검증이 다소 약함",
                "tools": "Grok 3 + Midjourney + ZenSpark + Zapier + Notion AI\n(창의적 연결과 자동화)",
                "growth": "Precision과 Check 축을 강화해보세요."
            },
            "FICS": {
                "catch": "자유로운 통찰 검증 솔로형",
                "desc": "통찰과 검증을 자유롭게 활용하는 전략적 창의가입니다.",
                "strength": "• 창의성과 검증의 완벽 조화",
                "weakness": "• Swarm 능력이 다소 약함",
                "tools": "NotebookLM + Perplexity + Grok + Canva AI\n(창의적 검증에 최적)",
                "growth": "Swarm 모드를 활용해보세요."
            },
            "FICW": {
                "catch": "자유로운 통찰 검증 스웜형",
                "desc": "통찰과 검증을 바탕으로 여러 AI를 연결해 새로운 가능성을 여는 미래 개척자입니다.",
                "strength": "• 통찰 + 검증 + 다중 AI",
                "weakness": "• Task 중심 실행력이 약할 수 있음",
                "tools": "Grok 3 + Perplexity + ZenSpark + Zapier + Felo\n(창의적 검증과 연결)",
                "growth": "Task 축을 강화해 아이디어를 빠르게 실행해보세요."
            }
        }

        data = reports.get(base_type, {
            "catch": f"너 {base_type}야? AI를 자신만의 방식으로 활용하는 독특한 스타일!",
            "desc": f"{base_type} 타입은 AI를 효과적으로 활용하는 독특한 패턴을 가지고 있습니다.",
            "strength": "강점 분석 중",
            "weakness": "약점 분석 중",
            "tools": "추천 도구 준비 중",
            "growth": "성장 포인트 준비 중"
        })

        st.markdown(f"### 💬 {data['catch']}")
        st.info(data['desc'])
        st.success(f"**강점**\n{data['strength']}")
        st.warning(f"**약점**\n{data['weakness']}")
        st.markdown(f"**🔥 추천 AI 도구 조합**  \n{data['tools']}")
        st.markdown(f"**📈 성장 포인트**\n{data['growth']}")

        if st.button("다시 검사하기"):
            st.session_state.clear()
            st.rerun()

st.sidebar.title("AUSTI")
st.sidebar.caption("Developed by Prof. In Hun Jeong with SuperGrok")
