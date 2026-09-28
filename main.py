import numpy as np
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
# 구역 2. 장르 안의 영화별 총 관객 (트리맵)
# ------------------------------------------------------------
st.header("2. 장르별 영화 총 관객 트리맵")

tree_df = df.dropna(subset=["total_audi"])
tree_df = tree_df[tree_df["total_audi"] > 0]

fig2 = px.treemap(
    tree_df,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
)
fig2.update_traces(
    hovertemplate="%{label}<br>총 관객 %{value:,}명<extra></extra>",
    textinfo="label",
)
fig2.update_layout(margin=dict(t=30, l=10, r=10, b=10))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** (여기에 한 문장을 적어 주세요.)")

st.divider()

# ------------------------------------------------------------
# 구역 3. 총 관객 히스토그램
# ------------------------------------------------------------
st.header("3. 총 관객 히스토그램")

hist_df = df.dropna(subset=["total_audi"])
values = hist_df["total_audi"]

# 구간(막대) 경계를 직접 계산해서 그래프와 아래 문구가 같은 구간을 쓰도록 함
n_bins = 30
size = values.max() / n_bins
edges = np.arange(0, values.max() + size * 2, size)  # 최댓값이 마지막 구간 안에 들어가도록
counts, _ = np.histogram(values, bins=edges)

fig3 = px.histogram(hist_df, x="total_audi", labels={"total_audi": "총 관객(명)"})
fig3.update_traces(
    xbins=dict(start=edges[0], end=edges[-1], size=size),
    hovertemplate="총 관객 %{x}명<br>%{y}편<extra></extra>",
)
fig3.update_layout(yaxis_title="영화 편수", bargap=0.05)
st.plotly_chart(fig3, use_container_width=True)

# 가장 영화가 많이 몰린 구간과 관객이 가장 많은 영화
peak = int(np.argmax(counts))
peak_lo, peak_hi = edges[peak], edges[peak + 1]
peak_count = int(counts[peak])
peak_ratio = peak_count / len(values) * 100
top_movie = hist_df.loc[hist_df["total_audi"].idxmax()]

st.markdown(
    f"**이 그래프로 알 수 있는 것:** 가장 많은 영화({peak_count}편, {peak_ratio:.1f}%)가 "
    f"총 관객 {peak_lo:,.0f}명 이상 {peak_hi:,.0f}명 미만 구간에 몰려 있고, "
    f"관객이 가장 많은 영화는 '{top_movie['movieNm']}'({top_movie['total_audi']:,.0f}명)예요."
)

st.divider()

# ------------------------------------------------------------
# 구역 4. 개봉일 스크린수와 총 관객 (산점도)
# ------------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객")

scatter_df = df.dropna(subset=["first_scrn", "total_audi"])

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={"genre": False, "first_scrn": ":,", "total_audi": ":,"},
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객(명)",
        "genre": "장르",
    },
)
fig4.update_traces(marker=dict(size=9, opacity=0.8))
st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** (여기에 한 문장을 적어 주세요.)")

st.divider()

# ------------------------------------------------------------
# 구역 5. 장르별 총 관객 분포 (상자 그림)
# ------------------------------------------------------------
st.header("5. 장르별 총 관객 상자 그림")

box_df = df.dropna(subset=["total_audi"])
genre_n = box_df["genre"].value_counts()
big_genres = genre_n[genre_n >= 10].index.tolist()  # 영화가 10편 이상인 장르만
box_df = box_df[box_df["genre"].isin(big_genres)]

if big_genres:
    fig5 = px.box(
        box_df,
        x="genre",
        y="total_audi",
        color="genre",
        points="outliers",  # 상자 밖으로 튀는 점만 표시
        hover_name="movieNm",
        hover_data={"genre": False, "total_audi": ":,"},
        category_orders={"genre": big_genres},
        labels={"genre": "장르", "total_audi": "총 관객(명)"},
    )
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("영화가 10편 이상인 장르가 없어요.")

st.markdown("**이 그래프로 알 수 있는 것:** (여기에 한 문장을 적어 주세요.)")

st.divider()

# ------------------------------------------------------------
# 구역 6. 개봉일 스크린수와 총 관객 (버블 그래프)
# ------------------------------------------------------------
st.header("6. 개봉일 스크린수와 총 관객 - 첫 주 관객을 점 크기로")

bubble_df = df.dropna(subset=["first_scrn", "total_audi", "first_week_audi"])

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    size_max=45,
    hover_name="movieNm",
    hover_data={
        "genre": False,
        "first_scrn": ":,",
        "total_audi": ":,",
        "first_week_audi": ":,",
    },
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객(명)",
        "first_week_audi": "첫 주 관객(명)",
        "genre": "장르",
    },
)
fig6.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color="white")))
st.plotly_chart(fig6, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** (여기에 한 문장을 적어 주세요.)")

st.divider()

# ------------------------------------------------------------
# 구역 7. 다음 그래프가 들어갈 자리
# ------------------------------------------------------------
