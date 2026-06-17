import time  # 코드 최상단에 추가

# ... 기존 코드 생략 ...

with st.spinner("AI 연애 코치가 두 사람의 성격을 분석 중입니다... 💌"):
    # 최대 3번까지 재시도하는 안전장치
    max_retries = 3
    for attempt in range(max_retries):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            
            response = model.generate_content(prompt)
            
            st.success("✨ 분석이 완료되었습니다!")
            st.markdown("---")
            st.markdown(response.text)
            st.markdown("---")
            break  # 성공하면 반복문 탈출
            
        except Exception as e:
            # 429 할당량 초과 에러인 경우
            if "429" in str(e) or "Quota exceeded" in str(e):
                if attempt < max_retries - 1:
                    st.warning(f"⚠️ 사용자가 많아 요청이 지연되고 있습니다. {attempt + 1}차 재시도 중... (5초만 기다려주세요)")
                    time.sleep(5)  # 5초 쉬고 다시 시도
                    continue
            
            # 다른 종류의 에러이거나 재시도를 모두 실패한 경우
            st.error(f"❌ 오류가 발생했습니다: {e}")
            break
