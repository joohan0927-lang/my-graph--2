import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 세로막대(|)로 여러 장르가 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].fillna("미상").astype(str).str.split("|").str[0]

    return df


df = load_data()

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
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)

fig.update_layout(
    legend_title="장르",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_area(
    "한 문장으로 적어 보세요.",
    placeholder="예: 이 기간에는 ○○ 장르의 영화가 가장 많았다.",
    label_visibility="collapsed",
)
import pandas as pd
import plotly.express as px
import streamlit as st

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
