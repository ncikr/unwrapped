import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.io as pio

# st.set_page_config(
#     page_title="Hours Listened",
#     page_icon="🕓",
# )

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/1982px-Spotify_icon.svg.png",
         width = 100)
st.title("Spotify Unwrapped")
st.header("Playtime over the years")
st.subheader("What was your most musical year?")


if "data" not in st.session_state or st.session_state.data is None:
    st.error("Please upload your listening history or check the 'testing' box in the 'Upload your data' tab.")

else:
    data = st.session_state.data

    total['month_label'] = total['period'].dt.strftime('%b')

    n_years = 10

    total_filtered = total[total['year'].astype("int") > max(total['year'].astype("int")) - n_years]

    total_fig = px.line(
        total_filtered,
        x = "month_label",
        y = "playtime_cumulative",
        color = "year",
        line_shape = "spline",
        height = 1000,
    )

    # add year labels
    for i, d in enumerate(total_fig.data):
        total_fig.add_scatter(x=[d.x[-1]], y = [d.y[-1]],
                        mode = 'markers+text',
                        text = d.legendgroup,
                        textfont = dict(color=d.line.color),
                        textposition='middle right',
                        marker = dict(color = d.line.color, size = 12),
                        legendgroup = d.name,
                        showlegend=False)


    total_fig.layout.template = "plotly_dark+presentation+xgridoff"
    total_fig.update_xaxes(title = None)
    total_fig.update_yaxes(title = None)
    total_fig.layout.legend.x = -0.3

    total_fig.show()


