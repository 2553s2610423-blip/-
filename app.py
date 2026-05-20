import streamlit as st

st.title("📅 간단한 스케줄 관리")

# 세션 상태에 일정 저장
if "todos" not in st.session_state:
    st.session_state.todos = []

# 일정 입력
todo = st.text_input("할 일을 입력하세요")

# 추가 버튼
if st.button("추가"):
    if todo:
        st.session_state.todos.append(todo)

# 일정 출력
st.subheader("할 일 목록")

for i, item in enumerate(st.session_state.todos, 1):
    st.write(f"{i}. {item}")
