import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_daily.csv"

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, dtype={"movieCd": str, "openDt": str})

    # 장르: 세로막대(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"].fillna("").astype(str).str.split("|").str[0].str.strip()
    )
    df.loc[df["genre"] == "", "genre"] = "미분류"

    # 개봉일: 여덟 자리 숫자(예: 20240131) -> 날짜
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")
    return df


def insight_box(placeholder="여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요."):
    """그래프 아래 '이 그래프로 알 수 있는 것' 한 문장 자리."""
    st.markdown("**💡 이 그래프로 알 수 있는 것**")
    st.info(placeholder)


# ---------- 제목 ----------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("1년간 박스오피스 10위권에 든 영화 가운데 이 기간에 개봉한 영화의 요약표를 그래프로 살펴봅니다.")

df = load_data()

col1, col2, col3 = st.columns(3)
col1.metric("영화 편수", f"{len(df):,}편")
col2.metric("장르 수", f"{df['genre'].nunique()}개")
col3.metric("제작 국가 수", f"{df['nation'].nunique()}개")

# ---------- 구역 1: 장르별 영화 편수 ----------
st.divider()
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig = go.Figure(
    go.Pie(
        labels=genre_counts["genre"],
        values=genre_counts["count"],
        hole=0.5,
        sort=True,
        textinfo="label+percent",
        hovertemplate="%{label}<br>%{value}편 (%{percent})<extra></extra>",
    )
)
fig.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    legend_title_text="장르",
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

insight_box()

# ---------- 다음 구역은 이 아래에 같은 방식으로 추가 ----------
# st.divider()
# st.header("2. ...")
# (그래프 코드)
# insight_box()
