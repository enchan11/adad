import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="글로벌 MBTI 데이터 대시보드",
    page_icon="🌍",
    layout="wide"
)

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    # 제공해주신 CSV 파일명을 그대로 사용합니다.
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()
except Exception as e:
    st.error("데이터 파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일이 main.py와 같은 위치에 있는지 확인해주세요.")
    st.stop()

# MBTI 16가지 컬럼 리스트 정의
mbti_columns = ['INFJ', 'ISFJ', 'INTP', 'ISFP', 'ENTP', 'INFP', 'ENTJ', 'ISTP', 
                'INTJ', 'ESFP', 'ESTJ', 'ENFP', 'ESTP', 'ISTJ', 'ENFJ', 'ESFJ']

# 3. 사이트 제목
st.title("🌍 나라별 MBTI 데이터 대시보드")
st.markdown("국가별 MBTI 비율 순위와 전 세계에서 가장 흔한 MBTI 순위를 확인해 보세요.")
st.write("---")

# 4. [기능 1] 나라별 MBTI 많은 순서 보기
st.header("📍 국가별 MBTI 순위")

# 국가 선택 박스
countries = sorted(df['Country'].unique())
selected_country = st.selectbox("분석할 국가를 선택하세요:", countries)

# 선택된 국가의 데이터 추출 및 변환
country_data = df[df['Country'] == selected_country].iloc[0]

# MBTI별 비율을 데이터프레임으로 변환 후 많은 순으로 정렬
country_mbti = pd.DataFrame({
    'MBTI': mbti_columns,
    '비율': [country_data[mbti] for mbti in mbti_columns]
})
# 비율이 높은 순서대로 정렬 및 순위 매기기
country_mbti = country_mbti.sort_values(by='비율', ascending=False).reset_index(drop=True)
country_mbti['순위'] = country_mbti.index + 1
country_mbti = country_mbti[['순위', 'MBTI', '비율']]

# 백분율(%) 표기를 위해 포맷팅
country_mbti_display = country_mbti.copy()
country_mbti_display['비율'] = country_mbti_display['비율'].map(lambda x: f"{x*100:.2f}%")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📊 {selected_country}의 MBTI 순위")
    st.dataframe(country_mbti_display, use_container_width=True, hide_index=True)

with col2:
    # 바 차트 시각화
    fig_country = px.bar(
        country_mbti, 
        x='MBTI', 
        y='비율', 
        title=f"{selected_country} MBTI 분포 (높은 순)",
        color='비율',
        color_continuous_scale='Blues'
    )
    # y축을 % 포맷으로 변경
    fig_country.update_layout(yaxis_tickformat='.1%')
    st.plotly_chart(fig_country, use_container_width=True)

st.write("---")

# 5. [기능 2] 전 세계 MBTI 평균 순위
st.header("🏆 글로벌 MBTI 통합 순위")
st.markdown("모든 국가 데이터의 평균 값을 기준으로 낸 전 세계 MBTI 순위입니다.")

# 전체 국가의 평균값 계산
global_avg = df[mbti_columns].mean().reset_index()
global_avg.columns = ['MBTI', '평균 비율']
global_avg = global_avg.sort_values(by='평균 비율', ascending=False).reset_index(drop=True)
global_avg['순위'] = global_avg.index + 1
global_avg = global_avg[['순위', 'MBTI', '평균 비율']]

# 백분율 표기용 포맷팅
global_avg_display = global_avg.copy()
global_avg_display['평균 비율'] = global_avg_display['평균 비율'].map(lambda x: f"{x*100:.2f}%")

col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("🌐 글로벌 통합 순위표")
    st.dataframe(global_avg_display, use_container_width=True, hide_index=True)

with col4:
    # 파이 차트로 글로벌 비중 시각화
    fig_global = px.pie(
        global_avg, 
        values='평균 비율', 
        names='MBTI', 
        title='전 세계 MBTI 평균 비율'
    )
    st.plotly_chart(fig_global, use_container_width=True)
