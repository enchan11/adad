import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="글로벌 MBTI 데이터 대시보드",
    page_icon="🌍",
    layout="wide"
)

# 데이터 로드 및 세션 상태(Session State) 저장하여 하위 페이지와 공유
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

if 'mbti_df' not in st.session_state:
    try:
        st.session_state['mbti_df'] = load_data()
    except Exception as e:
        st.error("데이터 파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일이 최상위 위치에 있는지 확인해주세요.")
        st.stop()

# 홈 화면 구성
st.title("🌍 글로벌 MBTI 데이터 대시보드")
st.markdown("### 전 세계 국가들의 MBTI 성향 데이터를 한눈에 확인하는 대시보드입니다.")
st.write("")

st.info("👈 왼쪽의 사이드바 메뉴를 이용해 원하는 분석 페이지로 이동하세요!")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📍 국가별 MBTI 순위 페이지")
    st.write("특정 국가를 선택하여 해당 국가에서 가장 높은 비율을 차지하는 MBTI 순위와 차트를 볼 수 있습니다.")

with col2:
    st.subheader("🏆 글로벌 MBTI 통합 순위 페이지")
    st.write("모든 국가 데이터의 평균을 바탕으로 전 세계에서 가장 흔한 MBTI 유형 분포를 비교할 수 있습니다.")

# 원본 데이터 미리보기
st.write("---")
st.subheader("📊 수집된 원본 데이터 미리보기")
st.dataframe(st.session_state['mbti_df'].head(10), use_container_width=True)
