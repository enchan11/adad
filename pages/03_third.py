import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="글로벌 MBTI 통합 순위", page_icon="🏆", layout="wide")

if 'mbti_df' not in st.session_state:
    st.warning("홈 페이지에서 데이터를 로드 중입니다. 잠시만 기다리시거나 홈으로 이동해 주세요.")
    st.stop()

df = st.session_state['mbti_df']
mbti_columns = ['INFJ', 'ISFJ', 'INTP', 'ISFP', 'ENTP', 'INFP', 'ENTJ', 'ISTP', 
                'INTJ', 'ESFP', 'ESTJ', 'ENFP', 'ESTP', 'ISTJ', 'ENFJ', 'ESFJ']

st.title("🏆 글로벌 MBTI 통합 순위")
st.markdown("모든 국가 데이터의 평균치를 기준으로 파악한 전 세계 MBTI 순위입니다.")
st.write("---")

# 글로벌 평균 계산
global_avg = df[mbti_columns].mean().reset_index()
global_avg.columns = ['MBTI', '평균 비율']
global_avg = global_avg.sort_values(by='평균 비율', ascending=False).reset_index(drop=True)
global_avg['순위'] = global_avg.index + 1
global_avg = global_avg[['순위', 'MBTI', '평균 비율']]

global_avg_display = global_avg.copy()
global_avg_display['평균 비율'] = global_avg_display['평균 비율'].map(lambda x: f"{x*100:.2f}%")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🌐 글로벌 통합 순위표")
    st.dataframe(global_avg_display, use_container_width=True, hide_index=True)

with col2:
    fig_global = px.pie(
        global_avg, 
        values='평균 비율', 
        names='MBTI', 
        title='전 세계 MBTI 평균 비율 차지 비중'
    )
    st.plotly_chart(fig_global, use_container_width=True)
