import streamlit as st

st.set_page_config(page_title="AUSTI - AI 사용 성향 검사", page_icon="🌟", layout="centered")

st.title("🌟 AUSTI")
st.subheader("AI 사용 성향 검사")

name = st.text_input("이름 또는 별명", placeholder="예: 인훈")
background = st.text_input("직업/전공/분야", placeholder="예: IT분야")

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

        # 강도 판단 (표시용)
        def get_strength(score):
            if score <= 2.3:
                return "강함"
            elif score >= 3.7:
                return "강함"
            else:
                return "중간"

        # 기본 타입 (대문자) - 보고서용
        base_type = ("P" if p <= 3 else "F") + ("T" if t <= 3 else "V") + ("R" if r <= 3 else "V") + ("S" if s <= 3 else "W")

        # 강도 표시용 타입 (대/소문자)
        p_char = "P" if p <= 2.3 else "p" if p < 3.7 else "F"
        t_char = "T" if t <= 2.3 else "t" if t < 3.7 else "V"
        r_char = "R" if r <= 2.3 else "r" if r < 3.7 else "V"
        s_char = "S" if s <= 2.3 else "s" if s < 3.7 else "W"
        display_type = p_char + t_char + r_char + s_char

        st.success("검사 완료되었습니다!")
        st.balloons()

        st.subheader(f"📌 당신의 타입: {display_type} ({base_type})")
        st.caption(f"Precision: {get_strength(p)} | Task: {get_strength(t)} | Trust: {get_strength(r)} | Swarm: {get_strength(s)}")

        # 16개 타입 보고서 데이터베이스 (현재는 주요 타입 위주로 작성, 필요시 더 추가)
        reports = {
            "PTRW": {
                "catch": "너 PTRW야? 여러 AI를 정밀하게 연결해 생산성을 폭발시키는 지휘관!",
                "desc": "당신은 AI를 **정밀하게 설계된 에코시스템**으로 보는 최고의 전략가입니다. 정확성과 효율을 최우선으로 하면서 여러 AI를 동시에 조율합니다.",
                "strength": "• 다중 AI 정밀 조율로 오류 최소화\n• Task 중심으로 마감 압박에도 강함",
                "weakness": "• 한 도구에 깊게 빠지지 않는 경향\n• 도구 관리 부담 가능성",
                "tools": "Claude 4 + Grok 3 + Perplexity + Cursor + Zapier",
                "growth": "가끔 한 AI와 깊이 대화하며 창의성을 키우세요."
            },
            "PTRS": {
                "catch": "너 PTRS야? 혼자서도 완벽한 AI 시스템을 구축하는 정밀 건축가!",
                "desc": "강한 Precision과 Solo 성향으로 혼자서도 높은 완성도의 결과를 만들어내는 타입입니다.",
                "strength": "• 정밀하고 안정적인 시스템 구축 능력\n• 혼자서도 고품질 결과 생산",
                "weakness": "• 여러 AI를 동시에 활용하는 능력이 상대적으로 약함",
                "tools": "Claude 4 + Cursor + Perplexity + NotebookLM",
                "growth": "Swarm 모드로 여러 AI를 연결해보세요."
            }
            # 여기에 나머지 14개 타입도 추가 가능
        }

        data = reports.get(base_type, {
            "catch": f"너 {base_type}야? AI를 활용하는 독특한 스타일!",
            "desc": f"{base_type} 타입은 AI를 자신만의 방식으로 효과적으로 활용하는 스타일입니다.",
            "strength": "강점 분석 중",
            "weakness": "약점 분석 중",
            "tools": "추천 도구 준비 중",
            "growth": "성장 포인트 준비 중"
        })

        st.markdown(f"### 💬 {data['catch']}")
        st.info(data['desc'])
        st.success(f"**강점**\n{data['strength']}")
        st.warning(f"**약점**\n{data['weakness']}")
        st.markdown(f"**🔥 추천 AI 도구 조합**\n{data['tools']}")
        st.markdown(f"**📈 성장 포인트**\n{data['growth']}")

        if st.button("다시 검사하기"):
            st.session_state.clear()
            st.rerun()

st.sidebar.title("AUSTI")
st.sidebar.info("강도 포함 분석\n(대문자 = 강함, 소문자 = 중간)")
st.sidebar.caption("Developed by Jeong In Hun with SuperGrok")