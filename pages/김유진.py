import streamlit as st
import google.generativeai as genai
import time  # 💡 [해결] Quota 429 에러 발생 시 대기 처리를 위한 라이브러리

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="연애 코칭: 우리 잘 맞출 수 있을까?",
    page_icon="💖",
    layout="centered"
)

# 🎨 [수정] 메인 타이틀과 포인트 컬러를 러블리한 분홍색(#FF69B4) 계열로 변경
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #FF69B4; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1.1rem; color: #666666; text-align: center; margin-bottom: 30px; }
    .section-header { font-size: 1.4rem; font-weight: bold; color: #444444; margin-top: 20px; }
    
    /* 기본 스트림릿 버튼 색상도 분홍색 계열로 매칭 */
    div.stButton > button {
        background-color: #FFB6C1 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #FF69B4 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💖 연애 코칭: 서로 다른 우리</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">우리가 가진 서로 다른 성격, 어떻게 하면 예쁘게 맞춰나갈 수 있을까요?</div>', unsafe_allow_html=True)

# 2. API 키 및 설정 (Secrets 우선, 없을 시 사이드바에서 입력 가능)
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("GEMINI_API_KEY 입력", type="password")

st.sidebar.title("🛠️ 코칭 설정")
coach_tone = st.sidebar.selectbox(
    "코칭 스타일을 선택하세요",
    ["다정다감하고 달콤하게", "팩트 폭격! 현실적이게", "위트 있고 유머러스하게"]
)

# 3. 성격 키워드 데이터셋 정의
KEYWORD_OPTIONS = [
    "외향적인", "내향적인", "감정표현이 솔직한", "마음을 잘 숨기는", 
    "계획적인", "즉흥적인", "논리적인", "공감능력이 뛰어난", 
    "연락을 자주 하는", "자기 시간이 중요한", "갈등을 바로 푸는", "생각할 시간이 필요한",
    "집순이/집돌이", "밖돌이/밖순이", "소소한 행복이 좋은", "열정적이고 야심찬"
]

# 4. 사용자 입력 UI 구성
st.markdown('<div class="section-header">🙋‍♂️ 나의 성격 키워드</div>', unsafe_allow_html=True)
my_keywords = st.multiselect(
    "자신의 성격을 나타내는 키워드를 원하는 만큼 선택해 주세요.",
    options=KEYWORD_OPTIONS,
    key="my_tags"
)

st.markdown('<div class="section-header">🙋‍♀️ 상대방의 성격 키워드</div>', unsafe_allow_html=True)
partner_keywords = st.multiselect(
    "상대방의 성격을 나타내는 키워드를 원하는 만큼 선택해 주세요.",
    options=KEYWORD_OPTIONS,
    key="partner_tags"
)

# 5. 분석 및 AI 코칭 실행
if st.button("💖 맞춤형 연애 가이드 받기", use_container_width=True):
    # 예외 처리: 키가 없는 경우
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY가 설정되지 않았습니다. 사이드바에 입력하거나 Streamlit Secrets에 등록해 주세요.")
    # 예외 처리: 키워드를 선택하지 않은 경우
    elif not my_keywords or not partner_keywords:
        st.warning("⚠️ 나와 상대방의 성격 키워드를 최소 1개 이상 선택해 주세요!")
    else:
        with st.spinner("AI 연애 코치가 두 사람의 성격을 분석 중입니다... 💌"):
            max_retries = 3      # 최대 재시도 횟수
            retry_delay = 5      # 재시도 전 대기 시간 (초)
            
            # 프롬프트 작성
            prompt = f"""
            당신은 전문 연애 코칭 전문가입니다. 아래 두 사람의 성격 키워드를 바탕으로, 서로 다른 성격을 극복하고 예쁜 사랑을 이어갈 수 있는 구체적인 맞춤형 조언을 작성해 주세요.
            
            [나의 성격 키워드]: {', '.join(my_keywords)}
            [상대방의 성격 키워드]: {', '.join(partner_keywords)}
            [코칭 스타일]: {coach_tone}
            
            다음 형식에 맞춰 가독성 좋게 작성해 주세요:
            1. 🌟 **두 사람의 성격 케미 요약**: 두 사람의 성격 조합이 가지는 특징을 한 줄로 요약해줘.
            2. ⚡ **부딪힐 수 있는 갈등 포인트**: 선택된 키워드들을 비교했을 때, 어떤 상황에서 주로 서운함이나 오해가 생길 수 있는지 분석해줘.
            3. 💡 **서로를 위한 맞춤형 행동 지침**: 내가 상대방에게 해야 할 행동/말, 그리고 상대방이 나에게 해주면 좋은 행동/말을 구체적이고 실천 가능한 팁으로 제안해줘.
            
            친근하고 가독성 좋게 이모지를 섞어서 마크다운(Markdown) 형식으로 출력해 주세요.
            """
            
            # 💡 [해결] Quota 429 에러 감지 및 자동 재시도 루프
            for attempt in range(max_retries):
                try:
                    # Gemini API 초기화 및 호출
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    response = model.generate_content(prompt)
                    
                    # 성공 시 결과 출력 후 안전하게 루프 종료
                    st.success("✨ 분석이 완료되었습니다!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                    st.caption("💡 성격은 서로 다른 매력이 될 수 있습니다. 서로 조금씩만 배려해 보세요!")
                    break
                    
                except Exception as e:
                    error_msg = str(e)
                    # 429 에러가 확인되면 잠시 대기 후 재시도
                    if "429" in error_msg or "Quota exceeded" in error_msg:
                        if attempt < max_retries - 1:
                            st.warning(f"⚠️ 현재 이용자가 많아 순차적으로 처리 중입니다. {retry_delay}초 후 자동으로 다시 시도합니다. (시도 {attempt + 1}/{max_retries})")
                            time.sleep(retry_delay)
                            continue 
                    
                    # 그 외 치명적인 에러 처리
                    st.error(f"❌ 오류가 발생했습니다: {e}\nAPI 키가 올바른지 혹은 잠시 후 다시 실행해 주세요.")
                    break
