import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 MBTI 순위", page_icon="📍", layout="wide")

# main.py에서 로드한 데이터 가져오기
if 'mbti_df' not in st.session_state:
    st.warning("홈 페이지에서 데이터를 로드 중입니다. 잠시만 기다리시거나 홈으로 이동해 주세요.")
    st.stop()

df = st.session_state['mbti_df']
mbti_columns = ['INFJ', 'ISFJ', 'INTP', 'ISFP', 'ENTP', 'INFP', 'ENTJ', 'ISTP', 
                'INTJ', 'ESFP', 'ESTJ', 'ENFP', 'ESTP', 'ISTJ', 'ENFJ', 'ESFJ']

st.title("📍 국가별 MBTI 순위 탐색")
st.markdown("선택한 국가의 MBTI 분포와 순위를 확인할 수 있습니다.")
st.write("---")

# 국가 선택
countries = sorted(df['Country'].unique())
selected_country = st.selectbox("분석할 국가를 선택하세요:", countries)

# 선택 국가 데이터 가공
country_data = df[df['Country'] == selected_country].iloc[0]
country_mbti = pd.DataFrame({
    'MBTI': mbti_columns,
    '비율': [country_data[mbti] for mbti in mbti_columns]
})
country_mbti = country_mbti.sort_values(by='비율', ascending=False).reset_index(drop=True)
country_mbti['순위'] = country_mbti.index + 1
country_mbti = country_mbti[['순위', 'MBTI', '비율']]

# 표기용 포맷팅
country_mbti_display = country_mbti.copy()
country_mbti_display['비율'] = country_mbti_display['비율'].map(lambda x: f"{x*100:.2f}%")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📊 {selected_country}의 MBTI 순위 (많은 순)")
    st.dataframe(country_mbti_display, use_container_width=True, hide_index=True)

with col2:
    fig_country = px.bar(
        country_mbti, 
        x='MBTI', 
        y='비율', 
        title=f"{selected_country} MBTI 분포 차트",
        color='비율',
        color_continuous_scale='Blues'
    )
    fig_country.update_layout(yaxis_tickformat='.1%')
    st.plotly_chart(fig_country, use_container_width=True)
