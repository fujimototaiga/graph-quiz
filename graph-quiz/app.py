from math import cos, sin, pi
from random import randint, sample
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit import session_state as state


# 画面構成
st.title("グラフ当てクイズ")
controller = st.container()
graph_board = st.container()
answer_board = st.container()


# 関数定義
def generate_params():
    """正解のパラメータの生成"""
    a, b = sample((3, 5, 7, 11, 13), 2)
    d = randint(0, 6)
    return (a, b, d)


@st.experimental_memo
def lissajous(a, b, d, point_num=300):
    """リサージュ曲線の点をパラメータから作成"""
    x = [cos(a * θ) for θ in np.linspace(0, 2 * pi, point_num)]
    y = [sin(b * θ + d * pi / 12) for θ in np.linspace(0, 2 * pi, point_num)]
    return x, y


def create_box_figure():
    """x軸とy軸のスケールが等しくて枠にフィットする図の作成"""
    fig, ax = plt.subplots()
    ax.set_aspect("equal", adjustable="box")
    return fig, ax


@st.experimental_memo
def plot(x, y):
    """点をつなげてプロットした図の作成"""
    fig, ax = create_box_figure()
    ax.plot(x, y)
    return fig


# session stateの初期化
if "params" not in state:
    state.params = generate_params()
if "showing_answer" not in state:
    state.showing_answer = False


# 正解のデータの作成
x_ans, y_ans = lissajous(*state.params)


# 回答のデータの作成
with controller:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Q.リサージュ曲線")
        st.latex(
            r"""
            x = \cos(aθ) \\
            y = \sin(bθ+\frac{d\pi}{12})
            """
        )
        st.write("のパラメータを調整して、お手本と同じグラフを描画してください。")

    with col2:
        st.write("パラメータ")
        st.slider("a", value=1, min_value=1, max_value=13, key="a")
        st.slider("b", value=1, min_value=1, max_value=13, key="b")
        st.slider("d", value=0, min_value=0, max_value=6, key="d")

        params_in_controll = (state.a, state.b, state.d)
        x, y = lissajous(*params_in_controll)


# グラフ描画
fig_ans = plot(x_ans, y_ans)
fig = plot(x, y)
with graph_board:
    col1, col2 = st.columns(2)

    with col1:
        st.text("お手本")
        st.pyplot(fig_ans)

    with col2:
        st.text("回答")
        st.pyplot(fig)


# 正解の表示
if state.params == params_in_controll and not state.showing_answer:
    state.showing_answer = True
    st.balloons()

ans = f"{state.params}"
with answer_board:
    if state.showing_answer:
        st.success("正解! " + ans, icon="✅")
    with st.expander("答えを見る"):
        st.text(ans)
