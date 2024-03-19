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

    # format dates
    data_aggregated = data.sort_values(['datetime'], ascending= [True])
    data_aggregated['month_label'] = data_aggregated['datetime'].dt.strftime('%b')
    data_aggregated['month_number'] = data_aggregated['datetime'].dt.strftime('%m').astype("string")

    # group and sum playtime
    data_aggregated = data_aggregated[["month_number", "month_label", "year","hours_played"]].groupby(["month_number", "month_label","year"])["hours_played"].sum().reset_index()

    # sort
    data_aggregated = data_aggregated.sort_values(['year','month_number'], ascending= [True, True])

    # cumulative sum
    data_aggregated['hours_played_cumlative'] = data_aggregated.groupby(["year"])['hours_played'].cumsum()


    # filter
    year_selection = st.checkbox("Select years", data_aggregated.year.unique())

    chart_data = data_aggregated[data_aggregated.year.isin(year_selection)]
    

    # plot
    playtime_figure = px.line(
        chart_data,
        x = "month_label",
        y = "hours_played_cumlative",
        color = "year",
        line_shape = "spline",
        height = 1000,
    )

    # add year labels
    for i, d in enumerate(playtime_figure.data):
        playtime_figure.add_scatter(x=[d.x[-1]], y = [d.y[-1]],
                        mode = 'markers+text',
                        text = d.legendgroup,
                        textfont = dict(color=d.line.color),
                        textposition='middle right',
                        marker = dict(color = d.line.color, size = 12),
                        legendgroup = d.name,
                        showlegend=False)

    # theme
    playtime_figure.layout.template = "plotly_dark+presentation+xgridoff"
    playtime_figure.update_xaxes(title = None)
    playtime_figure.update_yaxes(title = None)
    playtime_figure.layout.legend.x = -0.3

    st.plotly_chart(playtime_figure)


