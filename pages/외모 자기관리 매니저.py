import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 기본 설정 및 테마 디자인
st.set_page_config(
    page_title="GlowUp AI - 외모 자기관리 매니저",
    page_icon="✨",
    layout="centered"
)

# 2. API 키 로드 및 클라이언트 초기화
# Streamlit Community Cloud의 Secrets 기능을 활용합니다.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
else:
    st.error("⚠️ GEMINI_API_KEY가 설정되지 않았습니다. 사이드바나 Secrets 설정을 확인해주세요.")
    st.info("로컬에서 테스트 시 .streamlit/secrets.toml 파일에 GEMINI_API_KEY='본인키'를 입력하세요.")
    st.stop()

# 3. 세션 상태(Session State) 초기화 (대화 기록 저장용)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 당신의 매력을 한층 더 높여줄 **GlowUp AI 매니저**입니다. ✨\n\n화장법, 다이어트, 헤어스타일, 퍼스널 컬러, 호감형 인상을 만드는 표정 연습 등 외모 자기관리에 대해 궁금한 점을 무엇이든 편하게 물어보세요! 친절하게 알려드릴게요. 😊"
        }
    ]

# 4. 사이드바 구성 (차별화된 기능: 체크리스트 및 퀵 팁)
with st.sidebar:
    st.header("✨ 오늘의 GlowUp 루틴")
    st.write("작은 습관이 모여 호감형 외모를 만듭니다!")
    
    # 데일리 체크리스트
    st.checkbox("물 2L 마시기 💧")
    st.checkbox("외출 전 자외선 차단제 바르기 ☀️")
    st.checkbox("바른 자세 유지하기 (어깨 펴기) 🧘")
    st.checkbox("저녁 세안 후 보습제 꼼꼼히 바르기 🧴")
    st.checkbox("거울 보고 3초간 미소 짓기 연습 😊")
    
    st.divider()
    st.caption("💡 **GlowUp Tip:** 호감형 인상의 70%는 '밝은 미소'와 '자신감 있는 자세'에서 나옵니다. 지금 어깨를 쫙 펴보세요!")

# 5. 메인 화면 타이틀 및 소개
st.title("✨ GlowUp AI : 외모 자기관리 매니저")
st.subheader("더 호감 가는 나를 만드는 첫걸음")
st.write("외모 관리, 다이어트, 메이크업 고민을 입력하시면 친절하고 상세한 솔루션을 제공합니다.")

# 6. 추천 키워드 버튼 (초보자를 위한 가이드)
st.write("💡 **이런 질문은 어떠세요? 버튼을 클릭해보세요!**")
col1, col2, col3 = st.columns(3)

preset_question = None
with col1:
    if st.button("💄 초보자 데일리 화장법"):
        preset_question = "화장을 처음 시작하는 초보자를 위한 자연스럽고 깔끔한 데일리 메이크업 순서와 방법을 상세하게 알려줘."
with col2:
    if st.button("🥗 건강한 다이어트 식단"):
        preset_question = "굶지 않고 요요 없이 건강하게 체중을 감량할 수 있는 현실적인 다이어트 식단과 팁을 알려줘."
with col3:
    if st.button("😊 호감형 인상 만들기"):
        preset_question = "첫인상에서 호감을 주고 밝은 인상을 만들기 위한 표정 연습법과 일상 속 외모 관리 습관을 알려줘."

# 7. 이전 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. 사용자 입력 처리 (채팅창 또는 추천 버튼)
user_input = st.chat_input("메이크업, 다이어트, 스타일링 등 고민을 입력하세요...")

# 추천 버튼을 눌렀다면 해당 질문을 입력값으로 사용
if preset_question:
    user_input = preset_question

if user_input:
    # 사용자 메시지 화면에 표시 및 세션 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI 답변 생성 프로세스
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("당신만을 위한 맞춤형 뷰티 가이드를 작성 중입니다... 📝"):
            try:
                # 페르소나 주입을 위한 시스템 지시문(System Instruction) 설정
                system_instruction = (
                    "당신은 친절하고 따뜻하며 전문적인 외모 자기관리 멘토입니다. "
                    "사용자가 메이크업, 다이어트, 패션, 인상 관리 등에 대해 질문하면 "
                    "위로와 응원을 담아 매우 친절하고 구체적이며 가독성 좋게 단계별(1, 2, 3...)로 설명해주세요. "
                    "답변 끝에는 항상 따뜻한 응원의 한마디를 덧붙여 주세요."
                )

                # gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
                
                # 결과 출력 및 세션 저장
                ai_response = response.text
                response_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except APIError as e:
                error_msg = f"❌ Gemini API 오류가 발생했습니다: {e}"
                response_placeholder.markdown(error_msg)
                streamlit>=1.30.0
google-genai
            except Exception as e:
                error_msg = f"❌ 예기치 못한 오류가 발생했습니다: {str(e)}"
                response_placeholder.markdown(error_msg)
