import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Love Coach Studio",
    page_icon="💕",
    layout="wide"
)

# -----------------------
# 데이터
# -----------------------

MISSIONS = [
    "상대방에게 진심 어린 칭찬 한 번 하기",
    "감사한 일을 문자로 보내기",
    "오늘 먼저 안부 연락하기",
    "상대 이야기 10분 이상 집중해서 듣기",
    "감정을 솔직하게 표현해보기",
    "긍정적인 추억 하나 공유하기",
    "상대의 장점 3가지 적어보기",
    "비난 대신 요청 형태로 말해보기"
]

COACHING = {
    "썸": """
    💡 썸 단계에서는 너무 빠른 감정 표현보다 자연스러운 대화 빈도를 유지하는 것이 중요합니다.

    - 공통 관심사를 찾으세요.
    - 상대 반응을 관찰하세요.
    - 과도한 연락은 피하세요.
    """,

    "연애 중": """
    💡 연애는 호감보다 유지가 중요합니다.

    - 감정 표현을 자주 하세요.
    - 갈등은 빠르게 해결하세요.
    - 상대를 바꾸려 하기보다 이해하려고 노력하세요.
    """,

    "재회 고민": """
    💡 재회는 감정보다 원인 분석이 먼저입니다.

    - 이별 원인을 객관적으로 정리하세요.
    - 같은 문제가 반복되지 않을 준비가 필요합니다.
    - 충동적인 연락은 피하세요.
    """,

    "짝사랑": """
    💡 상대를 이상화하기보다 실제 모습을 파악하세요.

    - 자연스럽게 접점을 늘리세요.
    - 작은 대화를 시작하세요.
    - 거절 가능성도 건강하게 받아들이세요.
    """,

    "소개팅 준비": """
    💡 첫인상은 완벽함보다 편안함이 중요합니다.

    - 질문을 미리 준비하세요.
    - 웃는 표정을 연습하세요.
    - 상대에게 관심을 보여주세요.
    """
}


# -----------------------
# 함수
# -----------------------

def analyze_score(text, satisfaction):
    """
    단순하고 안정적인 규칙 기반 분석
    """

    positive_keywords = [
        "좋아", "행복", "즐거", "고마", "사랑",
        "설레", "관심", "데이트", "웃음"
    ]

    negative_keywords = [
        "싸움", "이별", "불안", "무시",
        "답장", "힘들", "외로", "갈등"
    ]

    positive = sum(
        text.count(word)
        for word in positive_keywords
    )

    negative = sum(
        text.count(word)
        for word in negative_keywords
    )

    communication = min(
        100,
        max(20, 60 + positive * 5 - negative * 3)
    )

    stability = min(
        100,
        max(20, satisfaction * 10 + positive * 2)
    )

    growth = min(
        100,
        max(20, 50 + positive * 4 - negative * 2)
    )

    total = int(
        (communication + stability + growth) / 3
    )

    return communication, stability, growth, total


# -----------------------
# 세션
# -----------------------

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------
# 화면
# -----------------------

st.title("💕 Love Coach Studio")
st.caption("연애 고민 분석 및 맞춤 코칭 서비스")

col1, col2 = st.columns([2, 1])

with col1:

    status = st.selectbox(
        "현재 연애 상황",
        ["썸", "연애 중", "재회 고민", "짝사랑", "소개팅 준비"]
    )

    concern = st.text_area(
        "현재 고민을 자유롭게 작성해주세요",
        height=180,
        placeholder="예: 상대방 답장이 늦어서 불안합니다..."
    )

    satisfaction = st.slider(
        "현재 관계 만족도",
        1,
        10,
        5
    )

    if st.button("📊 코칭 분석 시작"):

        try:
            comm, stable, growth, total = analyze_score(
                concern,
                satisfaction
            )

            st.subheader("분석 결과")

            result_df = pd.DataFrame({
                "항목": [
                    "소통",
                    "감정 안정성",
                    "관계 발전 가능성"
                ],
                "점수": [
                    comm,
                    stable,
                    growth
                ]
            })

            st.bar_chart(
                result_df.set_index("항목")
            )

            st.metric(
                "종합 연애 점수",
                f"{total}점"
            )

            st.subheader("맞춤 코칭")

            st.info(
                COACHING.get(
                    status,
                    "관계를 천천히 관찰해보세요."
                )
            )

            st.session_state.history.append({
                "상황": status,
                "종합점수": total
            })

        except Exception as e:
            st.error(
                f"분석 중 오류가 발생했습니다: {e}"
            )

with col2:

    st.subheader("🎯 오늘의 연애 미션")

    if st.button("미션 받기"):
        st.success(
            random.choice(MISSIONS)
        )

    st.divider()

    st.subheader("📈 성장 기록")

    if st.session_state.history:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

    else:
        st.write("아직 기록이 없습니다.")

st.divider()

st.markdown("""
### ❤️ 활용 팁

- 고민은 구체적으로 작성할수록 좋습니다.
- 점수는 참고용이며 절대적인 평가가 아닙니다.
- 중요한 관계 문제는 직접적인 대화가 가장 효과적입니다.
""")

