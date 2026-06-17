import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="연애 코칭: 성격 맞춤 대화 가이드", page_icon="❤️", layout="centered")

# 사이드바에서 API 키 입력 받기
st.sidebar.title("🛠️ 설정")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
st.sidebar.markdown("""
[API 키 발급받기](https://platform.openai.com/api-keys)
""")

# 앱 제목 및 소개
st.title("❤️ 연애 코칭: 다른 성격 극복하기")
st.markdown("""
서로 성격이 너무 달라서 부딪히시나요? 
서로의 성격 유형을 선택하고, 최근 있었던 상황이나 고민을 적어주세요. 
**AI 코치**가 두 사람이 상처받지 않고 대화할 수 있는 **구체적인 방향과 추천 멘트**를 알려드립니다.
""")

# 1. 주제 선택
st.subheader("1. 어떤 성격 차이로 고민 중이신가요?")
topic = st.selectbox(
    "갈등 주제를 선택하세요",
    [
        "외향형(E) vs 내향형(I) - 데이트 성향 및 에너지 충전 방식의 차이",
        "감성형(F) vs 이성형(T) - 공감과 해결책 중심의 대화 방식 차이",
        "계획형(J) vs 즉흥형(P) - 데이트 계획 및 라이프스타일의 차이"
    ]
)

# 2. 본인과 상대방의 성격 및 상황 입력
st.subheader("2. 두 사람의 상태를 알려주세요")
col1, col2 = st.columns(2)

with col1:
    my_status = st.text_input("나의 입장/성향 (예: 서운한 점, 내 생각)", placeholder="예: 주말엔 같이 밖에서 데이트하며 에너지를 얻고 싶어요.")

with col2:
    partner_status = st.text_input("상대방의 입장/성향 (예: 상대방이 한 말)", placeholder="예: 주중 일 때문에 지쳐서 주말엔 집에서 쉬고 싶어 해요.")

context = st.text_area("최근에 있었던 구체적인 갈등 상황 (선택사항)", placeholder="예: 이번 주말 데이트 계획을 짜다가 상대방이 집에서 쉬고 싶다고 해서 말다툼이 있었어요.")

# 코칭 받기 버튼
if st.button("💌 AI 연애 코칭 대화 가이드 받기"):
    if not openai_api_key:
        st.warning("왼쪽 사이드바에 OpenAI API Key를 입력해주세요.")
    elif not my_status or not partner_status:
        st.warning("나와 상대방의 입장/성향을 입력해주세요.")
    else:
        with st.spinner("AI 코치가 두 사람의 마음을 분석하여 대화법을 작성 중입니다..."):
            try:
                # OpenAI 클라이언트 초기화
                client = OpenAI(api_key=openai_api_key)
                
                # 프롬프트 구성
                prompt = f"""
                당신은 관계 심리학 전문가이자 다정한 연애 코치입니다. 
                서로 다른 성격을 가진 커플이 서로 상처 주지 않고 건설적인 대화를 나눌 수 있도록 도와주세요.

                [갈등 주제]: {topic}
                [사용자 입장]: {my_status}
                [상대방 입장]: {partner_status}
                [구체적 상황]: {context if context else '없음'}

                위 내용을 바탕으로 다음 세 가지 요소를 포함하여 친절하고 따뜻한 말투로 코칭을 제공해 주세요:
                1. 💡 **성격 차이 이해하기**: 두 사람의 성향 차이에서 오는 오해의 원인을 부드럽게 짚어주세요.
                2. 🧭 **대화의 방향성**: 대화를 시작할 때 어떤 태도와 마음가짐을 가져야 하는지 알려주세요.
                3. 💬 **추천 대화 멘트 (말투)**: 
                   - 상대방의 마음을 열 수 있는 '첫 마디'
                   - 나의 서운함을 상처 주지 않고 전달하는 '나-전달법(I-Message) 멘트'
                   - 함께 타협점을 찾기 위한 '제안의 한마디'
                """

                # API 호출 (최신 gpt-4o-mini 모델 활용)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "너는 커플들의 소통을 돕는 다정하고 전문적인 연애 코치야."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                # 결과 출력
                st.success("코칭 가이드가 준비되었습니다! 아래 내용을 참고해 대화를 시도해보세요.")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

st.caption("💡 대화는 이기기 위한 게임이 아니라, 서로를 이해해가는 과정입니다. 화이팅! 💕")
