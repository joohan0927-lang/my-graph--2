import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 여러 장르가 |로 연결된 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].fillna("미상").astype(str).str.split("|").str[0]

    # 총 관객을 숫자로 변환
    df["total_audi"] = pd.to_numeric(df["total_audi"], errors="coerce").fillna(0)

    return df


df = load_data()


# --------------------------------------------------
# 1. 장르별 영화 편수
# --------------------------------------------------
st.subheader("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="편수")
)

fig = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.55,
    title="장르별 영화 편수",
)

fig.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    ),
)

fig.update_layout(
    legend_title="장르",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_area(
    "첫 번째 그래프 설명",
    placeholder="예: 이 기간에는 ○○ 장르의 영화가 가장 많았다.",
    label_visibility="collapsed",
)


# --------------------------------------------------
# 2. 장르별 영화 관객수 트리맵
# --------------------------------------------------
st.subheader("2. 장르 안의 영화별 총 관객")

fig = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화의 총 관객",
)

fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_area(
    "두 번째 그래프 설명",
    placeholder="예: ○○ 장르에서는 ○○ 영화가 가장 많은 관객을 모았다.",
    label_visibility="collapsed",
)
# --------------------------------------------------
# 3. 총 관객 수 분포 히스토그램
# --------------------------------------------------
st.subheader("3. 총 관객 수의 분포")

fig = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수",
    },
)

fig.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)


# 가장 많은 영화가 들어 있는 구간 계산
counts, bin_edges = pd.np.histogram(
    df["total_audi"],
    bins=20,
)

max_bin_index = counts.argmax()
bin_start = bin_edges[max_bin_index]
bin_end = bin_edges[max_bin_index + 1]

# 총 관객이 가장 많은 영화
max_audi_index = df["total_audi"].idxmax()
max_audi_movie = df.loc[max_audi_index, "movieNm"]
max_audi = df.loc[max_audi_index, "total_audi"]


st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    f"대부분의 영화는 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** "
    f"구간에 몰려 있습니다."
)

st.write(
    f"총 관객이 가장 많은 영화는 **{max_audi_movie}**로, "
    f"총 **{max_audi:,.0f}명**의 관객을 기록했습니다."
)
# --------------------------------------------------
# 4. 개봉일 스크린 수와 총 관객의 관계
# --------------------------------------------------
st.subheader("4. 개봉일 스크린 수와 총 관객")

scatter_df = df.copy()

scatter_df["first_scrn"] = pd.to_numeric(
    scatter_df["first_scrn"], errors="coerce"
)
scatter_df["total_audi"] = pd.to_numeric(
    scatter_df["total_audi"], errors="coerce"
)

scatter_df = scatter_df.dropna(
    subset=["first_scrn", "total_audi", "movieNm", "genre"]
)

fig = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르",
    },
)

fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_area(
    "네 번째 그래프 설명",
    placeholder="예: 개봉일 스크린 수가 많은 영화일수록 총 관객도 많은 경향이 나타나는지 살펴볼 수 있다.",
    label_visibility="collapsed",
)
# --------------------------------------------------
# 5. 장르별 총 관객 분포 박스플롯
# --------------------------------------------------
st.subheader("5. 장르별 총 관객 분포")

# 장르별 영화 수가 10편 이상인 장르만 선택
genre_movie_counts = df["genre"].value_counts()

selected_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index

box_df = df[df["genre"].isin(selected_genres)].copy()

box_df["total_audi"] = pd.to_numeric(
    box_df["total_audi"],
    errors="coerce"
)

box_df = box_df.dropna(
    subset=["genre", "total_audi", "movieNm"]
)

fig = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수",
    },
)

fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    showlegend=False,
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_area(
    "다섯 번째 그래프 설명",
    placeholder="예: 장르별로 총 관객의 중앙값과 분포 범위에 차이가 있으며, 상자 밖의 점은 해당 장르에서 특히 관객이 많거나 적은 영화이다.",
    label_visibility="collapsed",
)
# --------------------------------------------------
# 6. 개봉일 스크린 수, 총 관객, 첫 주 관객의 관계
# --------------------------------------------------
st.subheader("6. 개봉일 스크린 수와 총 관객 — 첫 주 관객 버블")

bubble_df = df.copy()

bubble_df["first_scrn"] = pd.to_numeric(
    bubble_df["first_scrn"], errors="coerce"
)
bubble_df["total_audi"] = pd.to_numeric(
    bubble_df["total_audi"], errors="coerce"
)
bubble_df["first_week_audi"] = pd.to_numeric(
    bubble_df["first_week_audi"], errors="coerce"
)

bubble_df = bubble_df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "genre",
    ]
)

fig = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=55,
    title="개봉일 스크린 수와 총 관객 — 버블 크기는 첫 주 관객",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객",
        "genre": "장르",
    },
)

fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명<br>"
        "첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_area(
    "여섯 번째 그래프 설명",
    placeholder="예: 버블이 클수록 첫 주에 많은 관객을 모은 영화이며, 스크린 수와 총 관객의 관계도 함께 살펴볼 수 있다.",
    label_visibility="collapsed",
)
# --------------------------------------------------
# 7. 제작 국가 → 장르 선버스트
# --------------------------------------------------
st.subheader("7. 제작 국가와 장르별 영화 분포")

sunburst_df = df.copy()

# 제작 국가와 장르의 결측값 처리
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("미상")
    .astype(str)
    .replace("", "미상")
)

sunburst_df["genre"] = (
    sunburst_df["genre"]
    .fillna("미상")
    .astype(str)
    .replace("", "미상")
)

# 국가 → 장르별 영화 편수 집계
sunburst_counts = (
    sunburst_df
    .groupby(["nation", "genre"])
    .size()
    .reset_index(name="영화 편수")
)

fig = px.sunburst(
    sunburst_counts,
    path=["nation", "genre"],
    values="영화 편수",
    title="제작 국가 → 장르별 영화 분포",
)

fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig.update_layout(
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_area(
    "일곱 번째 그래프 설명",
    placeholder="예: 제작 국가별로 영화의 장르 구성이 어떻게 다른지 한눈에 비교할 수 있다.",
    label_visibility="collapsed",
)
# --------------------------------------------------
# 8. 10위권 체류 기간과 총 관객의 관계
# --------------------------------------------------
st.subheader("8. 10위권 체류 기간과 총 관객")

scatter_top10_df = df.copy()

scatter_top10_df["days_in_top10"] = pd.to_numeric(
    scatter_top10_df["days_in_top10"],
    errors="coerce"
)

scatter_top10_df["total_audi"] = pd.to_numeric(
    scatter_top10_df["total_audi"],
    errors="coerce"
)

scatter_top10_df = scatter_top10_df.dropna(
    subset=["days_in_top10", "total_audi", "movieNm"]
)

fig = px.scatter(
    scatter_top10_df,
    x="days_in_top10",
    y="total_audi",
    hover_name="movieNm",
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        "days_in_top10": "10위권에 머문 날수",
        "total_audi": "총 관객 수",
    },
)

fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "10위권에 머문 날수: %{x:,.0f}일<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="10위권에 머문 날수",
    yaxis_title="총 관객 수",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_area(
    "여덟 번째 그래프 설명",
    placeholder="예: 10위권에 머문 기간과 총 관객 수 사이에 어떤 관계가 있는지 살펴볼 수 있다.",
    label_visibility="collapsed",
)
