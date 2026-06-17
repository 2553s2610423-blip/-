수입 streamlit ~로서 st
수입 google.generativeai ~로서 genai

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="연애 코칭: 우리 잘 맞출 수 있을까?",
    page_icon="💖",
    layout="중심"
)

# 커스텀 스타일 적용 (감성적인 연애 코칭 앱 분위기)
st.마크다운("""
<스타일>
.main-title { font-size: 2.5rem; font-weight: 굵은 글씨; color: #FF4B4B; text-align: center; margin-bottom: 5px; } 
.sub-title { font-size: 1.1rem; color: #666666; text-align: center; margin-bottom: 30px; }
.section-header { font-size: 1.4rem; font-weight: bold; color: #333333; margin-top: 20px; }  
</style>
""" , unsafe_allow_html=진실)

st.markdown('<div class="main-title">💖 연애 코칭: 서로 다른 우리</div>', unsafe_allow_html=진실)
st.markdown('<div class="sub-title">우리가 가진 서로 다른 성격, 어떻게 하면 예쁘게 맞춰나갈 수 있을까요?</div>', unsafe_allow_html=진실)

# 2. API 키 및 설정 (Secrets 우선, 없을 시 사이드바에서 입력 가능)
API_key = ST.secrets.get("gemini_api_key")  아니면 st.sidebar.텍스트  입력  입력("GEMINI_API_KEY 입력", type="비밀번호")

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
st.markdown('<div class="section-header">🙋‍♂️ 나의 성격 키워드</div>', unsafe_allow_html=진실)
my_keywords = st.multiselect(
    "자신의 성격을 나타내는 키워드를 원하는 만큼 선택해 주세요.",
    options=KEYWORD_OPTIONS,
    key="my_tags"
)

st.markdown('<div class="section-header">🙋‍♀️ 상대방의 성격 키워드</div>', unsafe_allow_html=진실)
partner_keywords = st.multiselect(
    "상대방의 성격을 나타내는 키워드를 원하는 만큼 선택해 주세요.",
    options=KEYWORD_OPTIONS,
    key="파트너_태그"
)

# 5. 분석 및 AI 코칭 실행
IF st.button("💖 맞춤형 연애 가이드 받기", use_container_width=진실):
    # 예외 처리: 키가 없는 경우
     IF 아니야.  api_key:
        st.error("⚠️ GEMINI_API_KEY가 설정되지 않았습니다. 사이드바에 입력하거나 Streamlit Secrets에 등록해 주세요.")
    # 예외 처리: 키워드를 선택하지 않은 경우
     엘리프 아니야.  my_keywords 아니면 아니야. partner_keywords:
        st.warning("⚠️ 나와 상대방의 성격 키워드를 최소 1개 이상 선택해 주세요!")
    다른 사람:
         ~와 함께 st. spinner("AI 연애 코치가 두 사람의 성격을 분석 중입니다... 💌"):
            해봐.:
                # Gemini API 초기화# Gemini API 초기화 # Gemini API 초기화
                genai.configure(api_key=api_key)Genai.configure(api_key=api_key) genai.configure(api_key=api_key)
                 model = genai.GenerativeModel(제미니-2.5-플래시라이트) GenerativeModel(제미니-2.5-플래시라이트)
                
                # 프롬프트 작성# 프롬프트 작성 # 프롬프트 작성
 프롬프트 = f"" :  {', '.join(my_keywords)}                 [나의 성격 키워드]:  
                    당신은 전문 연애 코칭 전문가입니다.   아래   두 사람의 성격 키워드를 바탕으로, 서로 다른 성격을 극복하고 예쁜 사랑을 이어갈 수 있는 구체적인 맞춤형 조언을 작성해 주세요.   아래f"""나의 성격 키워드]:   아래f"""나의 성격 키워드]:  나의 성격 키워드]:   
[
                  [나의 성격 키워드]:   {', '.join(my_keywords                 )상대방의 성격 키워드]: {', '.join(partner_keywords)} }
                  [상대방의 성격 키워드]:   {', '.join(partner_keywords                 )코칭 스타일]: {coach_tone} }
                  [코칭 스타일]:   {coach_tone}
                
                  다음 형식에 맞춰 가독성 좋게 작성해 주세요:  
                  1. 🌟 **두 사람의 성격 케미 요약**: 두 사람의 성격 조합이 가지는 특징을 한 줄로 요약해줘.  
                 """ 
                  3. 💡  **서로를 위한 맞춤형 행동 지침**: 내가 상대방에게 해야 할 행동/말, 그리고 상대방이 나에게 해주면 좋은 행동/말을 구체적이고 실천 가능한 팁으로 제안해줘.   
                
                   친근하고 가독성 좋게 이모지를 섞어서  마크다운(Markdown)  형식으로 출력해 주세요.   
                """
                
                   마크다운
                response = model.generate_content(prompt)
                
                  # 결과 출력 # 결과 출력 
                  st.success("✨ 분석이 완료되었습니다!") success("✨ 분석이 완료되었습니다!") 
                st.markdown("---")
                   st.caption("💡 성격은 서로 다른 매력이 될 수 있습니다. 서로 조금씩만 배려해 보세요!") caption("💡 성격은 서로 다른 매력이 될 수 있습니다. 서로 조금씩만 배려해 보세요!")  markdown(response.text)
 ST. 
                   st.caption("💡 성격은 서로 다른 매력이 될 수 있습니다. 서로 조금씩만 배려해 보세요!") caption("💡 성격은 서로 다른 매력이 될 수 있습니다. 서로 조금씩만 배려해 보세요!"                  st.f"❌ 오류가 발생했습니다: {e}\nAPI 키가 올바른지 혹은 네트워크 상태를 확인해 주세요."    
                
                제외하고.  Exception  ~로서 e: Exception ~로서 e:  
                   st.f"❌ 오류가 발생했습니다: {e}\nAPI 키가 올바른지 혹은 네트워크 상태를 확인해 주세요."   (f"❌ 오류가 발생했습니다: {e}\nAPI 키가 올바른지 혹은 네트워크 상태를 확인해 주세요."{e}\nAPI 키가 올바른지 혹은 네트워크 상태를 확인해 주세요.")
