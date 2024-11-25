import streamlit as st

st.title("출생률 지도 시각화")

# Google Drive에서 공유한 HTML 파일 URL
html_file_url = "https://drive.google.com/uc?id=10gKYvzUJuRajHIxsWeRH4rysdbT9MRJ8"

# HTML 파일을 iframe으로 표시
st.markdown(f'<iframe src="{html_file_url}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
