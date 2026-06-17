import streamlit as st
import openai

# -------------------------
# 설정
# -------------------------
st.set_page_config(page_title="연애 성격 코칭 AI", page_icon="💗")

st.title("💗 연애 성격 코칭 AI")
st.write("서로 다른 성격을 어떻게 맞춰갈지 + 대화 방법 + AI 추천 문장을 제공합니다.")

# -------------------------
# API 키 입력
# -------------------------
api_key = st.sidebar.text_input("OpenAI API Key 입력", type="password")

if api_key:
    openai.api_key = api_key
else:
    st.warning("왼쪽 사이드바에 OpenAI API Key를 입력하세요.")
    st.stop()

# -------------------------
# 성격 입력
# -------------------------
st.header("1️⃣ 두 사람의 성격 입력")

col1, col2 = st.columns(2)

with col1:
    person_a = st.text_area("A의 성격", placeholder="예: 감정 표현이 적고 혼자 있는 걸 좋아함")

with col2:
    person_b = st.text_area("B의 성격", placeholder="예: 감정 표현이 많고 대화를 중요시함")

relationship_stage = st.selectbox(
    "관계 단계",
    ["썸", "연애 초기", "장기 연애", "갈등 중"]
)

goal = st.text_input("원하는 목표",
                     placeholder="예: 싸움을 줄이고 대화를 잘하고 싶다")

# -------------------------
# AI 프롬프트 생성
# -------------------------
def generate_advice(a, b, stage, goal):
    prompt = f"""
너는 전문 연애 코치이자 커뮤니케이션 전문가다.

다음 정보를 기반으로 현실적이고 실행 가능한 조언을 제공하라:

A 성격: {a}
B 성격: {b}
관계 단계: {stage}
목표: {goal}

출력 형식:

1. 성격 차이 핵심 분석 (간단하게)
2. 자주 발생할 수 있는 갈등 상황
3. 서로 맞추는 핵심 전략 3가지
4. 실제로 사용할 수 있는 대화 예시 (A가 B에게 / B가 A에게)
5. 싸움이 나기 전 예방 방법
6. 관계 개선을 위한 한 줄 핵심 조언
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 따뜻하지만 현실적인 연애 코치다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# -------------------------
# 실행 버튼
# -------------------------
st.header("2️⃣ 분석 결과")

if st.button("💡 AI 코칭 받기"):
    if not person_a or not person_b:
        st.error("두 사람의 성격을 모두 입력해주세요.")
    else:
        with st.spinner("AI가 관계를 분석 중입니다..."):
            result = generate_advice(person_a, person_b, relationship_stage, goal)
            st.markdown(result)

# -------------------------
# 대화 연습 기능
# -------------------------
st.header("3️⃣ 대화 코칭 (실전 말투 추천)")

topic = st.text_input("대화 상황 입력", placeholder="예: 연락이 너무 늦어서 서운할 때")

if st.button("💬 대화 추천 받기"):
    if not topic:
        st.warning("상황을 입력해주세요.")
    else:
        chat_prompt = f"""
너는 연애 커뮤니케이션 코치다.

상황: {topic}
A 성격: {person_a}
B 성격: {person_b}

다음 형식으로 답하라:
- 감정 상하지 않게 말하는 방법
- A가 말해야 할 문장 2개
- B가 말해야 할 문장 2개
- 상황이 악화되지 않게 하는 핵심 팁
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 갈등을 줄이는 커뮤니케이션 전문가다."},
                {"role": "user", "content": chat_prompt}
            ],
            temperature=0.7
        )

        st.markdown(response.choices[0].message.content)
