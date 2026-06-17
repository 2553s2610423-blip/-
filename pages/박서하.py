import streamlit as st
import google.generativeai as genai

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="연애의 온도 - 맞춤형 대화 코칭룸",
    page_icon="💌",
    layout="centered"
)

# 세션 상태 초기화 (퀴즈 점수 등 보관용)
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# API 키 설정 및 클라이언트 초기화 (Streamlit Secrets 연동)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 모델은 요구사항에 따라 gemini-2.5-flash-lite 지정
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
except Exception as e:
    st.error("⚠️ API 키 설정을 확인해주세요. Streamlit Secrets에 'GEMINI_API_KEY'가 필요합니다.")
    st.stop()

# 2. 앱 타이틀 & 소개
st.title("💌 연애의 온도")
st.subtitle("오래가는 연락, 센스 있는 대화를 위한 AI 맞춤형 대화 코칭룸")
st.markdown("---")

# 3. 사이드바 - 미니 연애 센스 퀴즈 (차별화 요소)
with st.sidebar:
    st.header("🧠 재미로 보는 연애 센스 퀴즈")
    st.write("**Q. 상대방이 '오늘 회사에서 너무 힘들었어...'라고 했을 때, 가장 좋은 답장은?**")
    
    quiz_choice = st.radio(
        "선택지를 골라보세요:",
        ["1. 무슨 일 있었어? 누가 괴롭혀?", "2. 토닥토닥, 고생 많았어. 맛있는 거 먹자.", "3. 원래 다 그러면서 크는 거지, 힘내!"]
    )
    
    if st.button("정답 확인하기"):
        st.session_state.quiz_submitted = True
        
    if st.session_state.quiz_submitted:
        if "2." in quiz_choice:
            st.success("🎉 정답입니다! 감정 공감 후 해결책(맛있는 것) 제시가 가장 부드러운 대화를 이끌어냅니다.")
        else:
            st.warning("😢 아쉬워요! 상대방은 해결책이나 훈계보다는 '공감과 위로'를 먼저 원했을 확률이 높습니다.")

# 4. 메인 기능 탭 구성
tab1, tab2 = st.tabs(["💬 대화 심폐소생술 (상담)", "💡 오래가는 대화 꿀팁 가이드"])

with tab1:
    st.header("🎯 AI 맞춤 대화 솔루션")
    st.write("현재 고민 상황이나 주고받은 대화를 적어주시면, 대화를 좋은 쪽으로 이끌어갈 치트키를 드립니다.")
    
    # 입력 폼
    with st.form("love_consulting_form"):
        relationship_status = st.selectbox(
            "현재 상대방과의 관계는 어떤가요?",
            ["썸/소개팅 단계", "연애 초기 (100일 이내)", "장기 연애 중", "권태기/냉각기", "짝사랑 중"]
        )
        
        chat_context = st.text_area(
            "고민되는 상황이나, 최근 주고받은 대화 내용을 적어주세요:",
            placeholder="예시: 소개팅 후 일주일째 선톡은 오는데 대화가 자꾸 '할 말 없음'으로 끝나요. 어떻게 이어가야 할까요?"
        )
        
        focus_point = st.multiselect(
            "어떤 부분에 초점을 맞춰 코칭해 드릴까요? (중복 선택 가능)",
            ["오랫동안 연락을 이끌어가는 방법", "대화를 좋은 쪽으로 리드하는 방법", "상대방 호감도 유추하기", "자연스러운 만남 약속 잡기"],
            default=["오랫동안 연락을 이끌어가는 방법", "대화를 좋은 쪽으로 리드하는 방법"]
        )
        
        submitted = st.form_submit_button("AI 코칭 받기 ✨")
        
    if submitted:
        if not chat_context.strip():
            st.warning("내용을 입력한 후 버튼을 눌러주세요!")
        else:
            with st.spinner("AI 연애 코치가 대화 내용을 분석 중입니다... ☕"):
                # 프롬프트 엔지니어링 구조화
                prompt = f"""
                당신은 따뜻하고 센스 있는 전문 연애 코칭 전문가입니다. 
                아래 사용자 고민을 듣고, 구체적이고 바로 쓸 수 있는 대화 솔루션을 제공해주세요.

                [사용자 정보]
                - 관계 단계: {relationship_status}
                - 집중 코칭 요청 항목: {', '.join(focus_point)}
                - 상세 고민 및 대화 내용: {chat_context}

                [답변 규칙]
                1. 친근하고 공감하는 말투(~요, ~해보세요)를 사용하세요.
                2. 요청한 집중 코칭 항목에 맞춰 '실제 바로 전송할 수 있는 답장 예시문'을 최소 2-3개 포함해주세요.
                3. 대화가 끊기지 않고 오랫동안 티키타카가 이어질 수 있는 '질문법'이나 '리액션 팁'을 명확히 짚어주세요.
                4. 가독성이 좋게 이모지와 마크다운 서식을 활용해 출력하세요.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success("🍀 AI 코치의 솔루션이 도착했습니다!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                except Exception as e:
                    st.error(f"오류가 발생했습니다. 다시 시도해주세요. (에러 내용: {e})")

with tab2:
    st.header("📚 대화의 정석: 필수 꿀팁 리스트")
    st.write("누구와 대화하든 호감을 사고 연락을 오래 유지하는 핵심 원칙입니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏳ 연락을 오래 이어가는 법")
        st.markdown("""
        * **단답형 질문 피하기**: "오늘 뭐 했어요?" 보다는 "오늘 날씨 되게 좋았는데 맛있는 거 드셨어요?" 처럼 답변의 폭을 넓혀주세요.
        * **'나도' 법칙 활용**: 상대방이 취미를 말했을 때, 격하게 공감하며 나의 관련 경험을 살짝 얹으면 대화가 끊이지 않습니다.
        * **마무리는 열린 질문으로**: 대화 문장 끝에 가볍게 질문을 던져 상대방이 답장할 명분을 만들어주세요.
        """)
        
    with col2:
        st.subheader("📈 대화를 좋은 쪽으로 리드하는 법")
        st.markdown("""
        * **감정 리액션 먼저**: "나 오늘 지각했어" 라는 말에 "왜 지각함?" 대신 "헐 고생했겠네, 아침부터 가슴 철렁했겠다"가 먼저입니다.
        * **상대방의 키워드 포착**: 상대가 흘리듯 말한 관심사(영화, 반려견, 맛집)를 기억해 두었다가 다음 대화의 주제로 삼으세요.
        * **긍정적 에너지 전달**: 불평불만보다는 소소하더라도 기분 좋은 일상 공유가 대화방의 온도를 높입니다.
        """)
