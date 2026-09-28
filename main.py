import pandas as pd
import plotly.express as px
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 개봉일(8자리 숫자)을 날짜형으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")
    # 장르가 '|'로 여러 개 적힌 영화는 첫 번째 장르만 사용
    df["genre"] = df["genre"].fillna("미분류").astype(str).str.split("|").str[0].str.strip()
    return df


df = load_data()

st.caption(f"1년간 박스오피스 10위권에 든 영화 중 이 기간에 개봉한 {len(df)}편의 요약 데이터")

# ------------------------------------------------------------
# 구역 1. 장르별 영화 편수 (도넛 그래프)
# ------------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = px.pie(genre_counts, names="genre", values="count", hole=0.5)
fig1.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}<br>%{value}편 (%{percent})<extra></extra>",
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** (여기에 한 문장을 적어 주세요.)")

st.divider()

# ------------------------------------------------------------
# 구역 2. 다음 그래프가 들어갈 자리
# ------------------------------------------------------------
