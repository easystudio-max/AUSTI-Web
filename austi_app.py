import streamlit as st

st.set_page_config(page_title="AUSTI - AI 사용 성향 검사", page_icon="🌟", layout="centered")

st.title("🌟 AUSTI")
st.subheader("AI 사용 성향 검사")

# ==================== Likert 척도 설명 ====================
st.markdown("""
**응답 방법**  
각 문항을 읽고, **자신에게 해당하는 정도**를 선택해주세요.

**1점** = 전혀 그렇지 않다  
**2점** = 거의 그렇지 않다  
**3점** = 보통이다  
**4점** = 대체로 그렇다  
**5점** = 매우 그렇다
""")

# 사용자 정보
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
        # 채점
        final_scores = [6 - s if (i+1) in reverse else s for i, s in enumerate(st.session_state.answers)]
        p = sum(final_scores[0:5]) / 5
        t = sum(final_scores[5:10]) / 5
        r = sum(final_scores[10:15]) / 5
        s = sum(final_scores[15:20]) / 5

        # 기본 타입 (보고서용)
        base_type = ("P" if p <= 3 else "F") + ("T" if t <= 3 else "V") + ("R" if r <= 3 else "V") + ("S" if s <= 3 else "W")

        # 강도 표시용 타입
        display_type = ("P" if p <= 2.3 else "p" if p < 3.7 else "F") + \
                       ("T" if t <= 2.3 else "t" if t < 3.7 else "V") + \
                       ("R" if r <= 2.3 else "r" if r < 3.7 else "V") + \
                       ("S" if s <= 2.3 else "s" if s < 3.7 else "W")

        st.success("검사 완료되었습니다!")
        st.balloons()

        st.subheader(f"📌 당신의 타입: {display_type} ({base_type})")

        # ==================== 16개 타입 완전 강화 보고서 ====================
        reports = {
            "PTRS": {
                "catch": "너 PTRS야? 혼자서도 완벽한 AI 시스템을 레고처럼 정밀하게 쌓아올리는 마스터!",
                "desc": "강한 Precision과 Solo 성향으로 혼자서도 높은 완성도의 결과를 만들어내는 정밀 건축가 타입입니다.",
                "strength": "• 오류 제로의 정밀 시스템 구축\n• 혼자서도 안정적인 고품질 결과물 생산",
                "weakness": "• 여러 AI를 동시에 활용하는 Swarm 능력이 다소 약함",
                "tools": "Claude 4 + Cursor + Perplexity + NotebookLM",
                "growth": "Swarm 모드로 여러 AI를 연결해 협업 연습을 해보세요."
            },
            "PTRW": {
                "catch": "너 PTRW야? 여러 AI를 정밀하게 연결해 생산성을 폭발시키는 지휘관!",
                "desc": "Precision과 Task 성향이 강하면서 Swarm으로 여러 AI를 동시에 조율하는 최고의 전략가 타입입니다.",
                "strength": "• 다중 AI를 정밀하게 조율해 오류 최소화 + 속도 극대화\n• Task 중심으로 마감 압박에도 안정적",
                "weakness": "• 한 도구에 깊게 빠지지 않고 넓게 쓰는 경향\n• 도구 관리가 부담스러울 수 있음",
                "tools": "Claude 4 + Grok 3 + Perplexity + Cursor + Zapier",
                "growth": "가끔 Solo 모드로 한 AI와 깊이 대화하며 창의성을 키워보세요."
            },
            "PTVS": {
                "catch": "너 PTVS야? 철저한 검증과 정밀 실행으로 신뢰할 수 있는 결과를 만드는 완벽주의자!",
                "desc": "Precision과 Task, Verify 성향이 강해 정확하고 검증된 결과를 중요시하는 타입입니다.",
                "strength": "• 높은 정확성과 신뢰성\n• 체계적인 검증 프로세스",
                "weakness": "• 창의적 아이디어 탐색이 다소 제한될 수 있음",
                "tools": "Perplexity + Claude 4 + Cursor",
                "growth": "Vision 축을 강화해 장기적 아이디어를 탐색해보세요."
            },
            "PTVW": {
                "catch": "너 PTVW야? 정밀한 검증과 비전을 동시에 추구하는 전략적 분석가!",
                "desc": "Precision과 Task, Verify, Vision의 균형이 뛰어난 전략적 분석가 타입입니다.",
                "strength": "• 정확성과 장기적 비전의 조화",
                "weakness": "• Swarm 협업이 상대적으로 약함",
                "tools": "Perplexity + Claude 4 + Grok 3",
                "growth": "Swarm 도구를 적극 활용해보세요."
            },
            "PFRS": {
                "catch": "너 PFRS야? 정밀하지만 자연스럽게 흐르는 AI 빌더!",
                "desc": "Precision과 Flow의 균형이 뛰어난 희귀 타입으로, 정확성을 유지하면서 창의적 흐름을 잘 타는 스타일입니다.",
                "strength": "• 정확성과 창의적 흐름의 완벽한 균형",
                "weakness": "• Swarm 협업이 다소 약함",
                "tools": "Claude 4 + NotebookLM + Cursor",
                "growth": "Swarm 도구를 2~3개 추가해 협업 연습을 해보세요."
            },
            "PFRW": {
                "catch": "너 PFRW야? 정밀한 흐름을 여러 AI와 연결하는 창의적 조율자!",
                "desc": "Precision과 Flow, Swarm 성향이 강한 창의적 조율자 타입입니다.",
                "strength": "• 창의적 흐름과 다중 AI 조율 능력",
                "weakness": "• Task 중심의 즉시 실행력이 약할 수 있음",
                "tools": "Grok 3 + Claude 4 + Zapier",
                "growth": "Task 축을 강화해 아이디어를 빠르게 실행해보세요."
            },
            "PFVS": {
                "catch": "너 PFVS야? 창의적 흐름과 철저한 검증을 병행하는 균형형 분석가!",
                "desc": "Flow와 Verify 성향이 강하면서 Precision을 유지하는 타입입니다.",
                "strength": "• 창의성과 검증의 균형",
                "weakness": "• Swarm 능력이 다소 약함",
                "tools": "NotebookLM + Perplexity + Claude",
                "growth": "Swarm 모드를 적극 활용해보세요."
            },
            "PFVW": {
                "catch": "너 PFVW야? 자유로운 흐름과 비전을 여러 AI와 연결하는 창의적 탐험가!",
                "desc": "Flow, Vision, Swarm 성향이 강한 자유로운 창의형 타입입니다.",
                "strength": "• 창의적 아이디어 폭발력과 다중 AI 활용",
                "weakness": "• 정밀성과 즉시 실행력이 상대적으로 약함",
                "tools": "Grok 3 + Midjourney + Claude",
                "growth": "Task와 Precision 축을 강화해보세요."
            },
            "FTRS": {
                "catch": "너 FTRS야? 자유로운 흐름으로 장기적 비전을 추구하는 창의적 솔로 플레이어!",
                "desc": "Flow와 Vision, Trust, Solo 성향이 강한 창의적 솔로 타입입니다.",
                "strength": "• 창의적 아이디어 생성 능력\n• 깊이 있는 1:1 대화",
                "weakness": "• Swarm 협업이 다소 약함",
                "tools": "Grok 3 + Claude 4 + NotebookLM",
                "growth": "Swarm 도구를 도입해보세요."
            },
            "FTRW": {
                "catch": "너 FTRW야? 창의적 흐름을 여러 AI와 연결해 비전을 실현하는 혁신가!",
                "desc": "Flow, Vision, Swarm 성향이 강한 혁신가 타입입니다.",
                "strength": "• 창의적 아이디어와 다중 AI 조율 능력",
                "weakness": "• 정밀성과 검증이 다소 약함",
                "tools": "Grok 3 + Claude 4 + Zapier",
                "growth": "Precision과 Verify 축을 강화해보세요."
            },
            "FTVS": {
                "catch": "너 FTVS야? 창의적 흐름과 철저한 검증을 병행하는 전략적 창작자!",
                "desc": "Flow와 Vision, Verify 성향이 강한 전략적 창작자 타입입니다.",
                "strength": "• 창의성과 검증의 조화",
                "weakness": "• Swarm 능력이 다소 약함",
                "tools": "NotebookLM + Perplexity + Grok",
                "growth": "Swarm 모드를 활용해보세요."
            },
            "FTVW": {
                "catch": "너 FTVW야? 자유로운 흐름과 비전을 여러 AI와 연결하는 미래 지향적 혁신가!",
                "desc": "Flow, Vision, Swarm 성향이 강한 미래 지향적 혁신가 타입입니다.",
                "strength": "• 창의적 비전과 다중 AI 활용 능력",
                "weakness": "• Precision과 Task가 다소 약함",
                "tools": "Grok 3 + Midjourney + Zapier",
                "growth": "Precision과 Task 축을 강화해보세요."
            },
            "FFRS": {
                "catch": "너 FFRS야? 자유로운 흐름으로 창의적 비전을 혼자서도 깊이 탐구하는 예술가!",
                "desc": "Flow, Vision, Solo 성향이 강한 창의적 예술가 타입입니다.",
                "strength": "• 뛰어난 창의력과 깊이 있는 탐구",
                "weakness": "• Swarm 협업과 즉시 실행력이 약함",
                "tools": "Grok 3 + NotebookLM",
                "growth": "Swarm과 Task 축을 강화해보세요."
            },
            "FFRW": {
                "catch": "너 FFRW야? 자유로운 흐름과 비전을 여러 AI와 연결하는 창의적 에코시스템 마스터!",
                "desc": "Flow, Vision, Swarm 성향이 강한 창의적 에코시스템 마스터 타입입니다.",
                "strength": "• 창의적 아이디어와 다중 AI 조율 능력",
                "weakness": "• Precision과 검증이 다소 약함",
                "tools": "Grok 3 + Midjourney + Zapier",
                "growth": "Precision과 Verify 축을 강화해보세요."
            },
            "FFVS": {
                "catch": "너 FFVS야? 창의적 흐름과 비전을 철저히 검증하는 전략적 창작자!",
                "desc": "Flow, Vision, Verify 성향이 강한 전략적 창작자 타입입니다.",
                "strength": "• 창의성과 검증의 조화",
                "weakness": "• Swarm 능력이 다소 약함",
                "tools": "NotebookLM + Perplexity + Grok",
                "growth": "Swarm 모드를 활용해보세요."
            },
            "FFVW": {
                "catch": "너 FFVW야? 자유로운 흐름과 비전을 여러 AI와 연결하는 창의적 미래 개척자!",
                "desc": "Flow, Vision, Swarm 성향이 강한 창의적 미래 개척자 타입입니다.",
                "strength": "• 강력한 창의력과 다중 AI 활용 능력",
                "weakness": "• Precision과 Task가 다소 약함",
                "tools": "Grok 3 + Midjourney + Zapier",
                "growth": "Precision과 Task 축을 강화해보세요."
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
        st.markdown(f"**🔥 추천 AI 도구 조합**\n{data['tools']}")
        st.markdown(f"**📈 성장 포인트**\n{data['growth']}")

        if st.button("다시 검사하기"):
            st.session_state.clear()
            st.rerun()

st.sidebar.title("AUSTI")
st.sidebar.info("강도 포함 분석\n(대문자 = 강함, 소문자 = 중간)")
st.sidebar.caption("Developed by Jeong In Hun with SuperGrok")
