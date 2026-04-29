import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from modules.processor import process_data


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    layout="wide",
    page_title="FitSync Dashboard",
    page_icon="",
)


# -------------------- CUSTOM STYLING --------------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3, h4, .stMetricLabel, .stMetricValue {
            font-family: 'Segoe UI', sans-serif;
        }
        .subtitle {
            color: #6b7280;
            text-align: center;
        }
        .dashboard-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 1rem 1rem 0.5rem 1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- HEADER --------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 0.75rem;">
        <h1>FitSync</h1>
        <h4 class="subtitle">Your Personal Health Analytics Dashboard by Harshvardhanam</h4>
        <p class="subtitle">Track • Analyze • Improve</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------- SIDEBAR --------------------
st.sidebar.header("Filters")

time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2,
)


# -------------------- LOAD DATA --------------------
@st.cache_data(show_spinner=False)
def load_processed_data():
    return process_data()


with st.spinner("Processing your health data..."):
    df = load_processed_data()


# -------------------- COLUMN HANDLING --------------------
def get_col(dataframe, possible_names):
    for name in possible_names:
        if name in dataframe.columns:
            return name
    return None


date_col = get_col(df, ["date", "Date"])
steps_col = get_col(df, ["steps", "Steps"])
sleep_col = get_col(df, ["sleep_hours", "Sleep_Hours", "Sleep Hours"])
recovery_col = get_col(df, ["Recovery_Score", "Recovery Score"])
heart_rate_col = get_col(df, ["heart_rate_bpm", "Heart_Rate_bpm", "Heart Rate Bpm"])
calories_col = get_col(df, ["calories_burned", "Calories_Burned", "Calories Burned"])


# -------------------- FILTERING --------------------
filtered_df = df.copy()

if date_col:
    filtered_df = filtered_df.sort_values(by=date_col).reset_index(drop=True)

    latest_date = filtered_df[date_col].max()
    if time_range == "Last 7 Days":
        cutoff_date = latest_date - pd.Timedelta(days=6)
        filtered_df = filtered_df[filtered_df[date_col] >= cutoff_date]
    elif time_range == "Last 30 Days":
        cutoff_date = latest_date - pd.Timedelta(days=29)
        filtered_df = filtered_df[filtered_df[date_col] >= cutoff_date]

filtered_df = filtered_df.reset_index(drop=True)


# -------------------- HELPERS --------------------
def build_time_series_figure(dataframe, x_col, y_columns, title, y_axis_title):
    figure = go.Figure()

    for column_name in y_columns:
        figure.add_trace(
            go.Scatter(
                x=dataframe[x_col],
                y=dataframe[column_name],
                mode="lines+markers",
                name=column_name.replace("_", " "),
                line=dict(width=3),
                marker=dict(size=6),
            )
        )

    figure.update_layout(
        title=title,
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        height=380,
        legend_title_text="Metric",
        xaxis_title="Date",
        yaxis_title=y_axis_title,
    )
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(gridcolor="#e5e7eb")
    return figure


def build_scatter_figure(dataframe, x_col, y_col, title, x_title, y_title, color_col=None):
    scatter_kwargs = {
        "data_frame": dataframe,
        "x": x_col,
        "y": y_col,
        "title": title,
        "labels": {
            x_col: x_title,
            y_col: y_title,
        },
    }

    if color_col:
        scatter_kwargs["color"] = color_col
        scatter_kwargs["color_continuous_scale"] = "Viridis"
        scatter_kwargs["labels"][color_col] = color_col.replace("_", " ")

    figure = px.scatter(**scatter_kwargs)

    figure.update_traces(marker=dict(size=10, opacity=0.85, line=dict(width=0.5, color="white")))
    figure.update_layout(
        template="plotly_white",
        height=380,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    if color_col:
        figure.update_layout(coloraxis_colorbar=dict(title=color_col.replace("_", " ")))
    figure.update_xaxes(gridcolor="#e5e7eb")
    figure.update_yaxes(gridcolor="#e5e7eb")
    return figure


# -------------------- METRICS --------------------
st.subheader("Your Health Overview")

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        "Avg Steps",
        f"{filtered_df[steps_col].mean():.0f}" if steps_col and not filtered_df.empty else "N/A",
    )

with metric_col2:
    st.metric(
        "Avg Sleep",
        f"{filtered_df[sleep_col].mean():.1f}" if sleep_col and not filtered_df.empty else "N/A",
    )

with metric_col3:
    st.metric(
        "Avg Recovery Score",
        f"{filtered_df[recovery_col].mean():.1f}" if recovery_col and not filtered_df.empty else "N/A",
    )


# -------------------- VISUALS: ROW 1 --------------------
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
left_col, right_col = st.columns(2, gap="large")

with left_col:
    st.markdown("### Recovery Score & Sleep Trend")
    if date_col and recovery_col and sleep_col and not filtered_df.empty:
        trend_figure = build_time_series_figure(
            filtered_df,
            date_col,
            [recovery_col, sleep_col],
            "Recovery Score & Sleep Trend",
            "Value",
        )
        st.plotly_chart(trend_figure, use_container_width=True)
    else:
        st.info("Recovery and sleep data are not available for this view.")

with right_col:
    st.markdown("### Recovery Score vs Daily Steps")
    if steps_col and recovery_col and sleep_col and not filtered_df.empty:
        scatter_figure = build_scatter_figure(
            filtered_df,
            steps_col,
            recovery_col,
            "Recovery Score vs Daily Steps",
            "Daily Steps",
            "Recovery Score",
            color_col=sleep_col,
        )
        st.plotly_chart(scatter_figure, use_container_width=True)
    else:
        st.info("Steps, recovery, or sleep data are not available for this view.")

st.markdown("</div>", unsafe_allow_html=True)


# -------------------- VISUALS: ROW 2 --------------------
st.markdown('<div class="dashboard-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
bottom_left_col, bottom_right_col = st.columns(2, gap="large")

with bottom_left_col:
    st.markdown("### Recovery Score vs Resting Heart Rate")
    if heart_rate_col and recovery_col and not filtered_df.empty:
        heart_rate_figure = build_scatter_figure(
            filtered_df,
            heart_rate_col,
            recovery_col,
            "Recovery Score vs Resting Heart Rate",
            "Resting Heart Rate (bpm)",
            "Recovery Score",
        )
        st.plotly_chart(heart_rate_figure, use_container_width=True)
    else:
        st.info("Heart rate or recovery data are not available for this view.")

with bottom_right_col:
    st.markdown("### Daily Calories Burned Trend")
    if date_col and calories_col and not filtered_df.empty:
        calories_figure = build_time_series_figure(
            filtered_df,
            date_col,
            [calories_col],
            "Daily Calories Burned Trend",
            "Calories Burned",
        )
        st.plotly_chart(calories_figure, use_container_width=True)
    else:
        st.info("Calories data are not available for this view.")

st.markdown("</div>", unsafe_allow_html=True)


# -------------------- FOOTER --------------------
st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#6b7280;">
        Built by Harshvardhanam <br>
        <b>FitSync</b> © 2026
    </div>
    """,
    unsafe_allow_html=True,
)