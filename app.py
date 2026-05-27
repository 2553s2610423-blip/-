import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="하트시그널 챗봇", page_icon="💖", layout="centered")
st.title("💖 연애 카운셀러, '하트' 챗봇")
st.caption("연애 고민, 썸, 이별 이야기까지... 무엇이든 편하게 털어놓으세요.")

# 2. API 키 설정 및 클라이언트 초기화 (오류 처리 포함)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("❌ `.streamlit/secrets.toml` 파일에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 3. 세션 상태(Session State) 초기화 (채팅 기록 및 대화 모델 유지)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    try:
        # gemini-2.5-flash-lite 모델 정의
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=(
                "당신은 공감 능력이 뛰어나고 다정한 연애 상담 전문가 '하트'입니다. "
                "사용자의 고민을 경청하고, 따뜻하게 위로하며, 현실적이고 현명한 조언을 건네세요. "
                "연애와 관련된 질문이 아닐 경우에도 친절하게 답변하되, 가급적 연애 비유를 섞어 재치 있게 답변해주세요."
            )
        )
        # Gemini 자체 내장 채팅 세션 시작 (과거 맥락 기억용)
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"🤖 모델 초기화 중 오류가 발생했습니다: {e}")
        st.stop()

# 4. 이전 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("연애 고민을 들려주세요..."):
    # 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6. 답변 생성 및 스트리밍 효과
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Gemini API 호출 (스트리밍 방식 적용)
            response = st.session_state.chat_session.send_message(user_input, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                # 글자가 타이핑되는 듯한 효과
                message_placeholder.markdown(full_response + "▌")
            
            # 최종 텍스트 표기 (커서 제거)
            message_placeholder.markdown(full_response)
            
            # 챗봇 답변 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"⚠️ 답변을 생성하는 중 오류가 발생했습니다: {e}")
            message_placeholder.empty() # 에러 발생 시 빈 커서 제거
