import pandas as pd
import plotly.express as px
import streamlit as st

from modules.processor import process_data


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
	layout="wide",
	page_title="Trends & Insights",
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
		.insights-card {
			background: linear-gradient(180deg, #ffffff 0%, #f9fafb 100%);
			border: 1px solid #e5e7eb;
			border-radius: 18px;
			padding: 1rem;
			box-shadow: 0 10px 26px rgba(15, 23, 42, 0.05);
		}
	</style>
	""",
	unsafe_allow_html=True,
)


# -------------------- HEADER --------------------
st.markdown(
	"""
	<div style="text-align:center; margin-bottom: 0.75rem;">
		<h1>Trends & Insights</h1>
		<h4 class="subtitle">Explore deeper patterns in recovery, sleep, steps, and calories</h4>
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
def build_histogram(dataframe, column_name, title, x_title):
	figure = px.histogram(
		dataframe,
		x=column_name,
		nbins=24,
		title=title,
		color_discrete_sequence=["#0ea5e9"],
	)
	figure.update_traces(marker_line_color="#ffffff", marker_line_width=1.2)
	figure.update_layout(
		template="plotly_white",
		height=320,
		margin=dict(l=20, r=20, t=60, b=20),
		bargap=0.08,
		xaxis_title=x_title,
		yaxis_title="Count",
	)
	figure.update_xaxes(gridcolor="#e5e7eb")
	figure.update_yaxes(gridcolor="#e5e7eb")
	return figure


def build_monthly_recovery_figure(dataframe, date_column, recovery_column):
	monthly_df = dataframe[[date_column, recovery_column]].dropna().copy()
	monthly_df["Month"] = monthly_df[date_column].dt.to_period("M").dt.to_timestamp()
	monthly_avg = monthly_df.groupby("Month", as_index=False)[recovery_column].mean()

	figure = px.line(
		monthly_avg,
		x="Month",
		y=recovery_column,
		markers=True,
		title="Average Recovery Score Month-wise",
		labels={recovery_column: "Average Recovery Score", "Month": "Month"},
	)
	figure.update_traces(line=dict(width=3, color="#2563eb"), marker=dict(size=8))
	figure.update_layout(
		template="plotly_white",
		height=360,
		margin=dict(l=20, r=20, t=60, b=20),
		xaxis_title="Month",
		yaxis_title="Average Recovery Score",
	)
	figure.update_xaxes(gridcolor="#e5e7eb")
	figure.update_yaxes(gridcolor="#e5e7eb")
	return figure


def build_summary_table(dataframe, columns):
	rows = []
	for label, column_name in columns:
		if column_name and not dataframe.empty:
			series = dataframe[column_name].dropna()
			rows.append(
				{
					"Metric": label,
					"Mean": round(series.mean(), 1),
					"Min": round(series.min(), 1),
					"Max": round(series.max(), 1),
				}
			)
		else:
			rows.append({"Metric": label, "Mean": None, "Min": None, "Max": None})
	return pd.DataFrame(rows)


# -------------------- SUMMARY STATISTICS --------------------
st.markdown('<div class="insights-card">', unsafe_allow_html=True)
st.subheader("Summary Statistics")

summary_columns = [
	("Recovery Score", recovery_col),
	("Sleep Hours", sleep_col),
	("Steps", steps_col),
	("Calories Burned", calories_col),
]

stats_df = build_summary_table(filtered_df, summary_columns)
st.dataframe(stats_df, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)


# -------------------- MONTHLY RECOVERY TREND --------------------
st.markdown('<div class="insights-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
st.subheader("Monthly Recovery Trend")

if date_col and recovery_col and not filtered_df.empty:
	monthly_recovery_figure = build_monthly_recovery_figure(filtered_df, date_col, recovery_col)
	st.plotly_chart(monthly_recovery_figure, use_container_width=True)
else:
	st.info("Recovery trend data is not available for this view.")

st.markdown("</div>", unsafe_allow_html=True)


# -------------------- DISTRIBUTION HISTOGRAMS --------------------
st.markdown('<div class="insights-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
st.subheader("Distributions")

histogram_targets = [
	("Steps", steps_col, "Steps Distribution"),
	("Calories Burned", calories_col, "Calories Burned Distribution"),
	("Recovery Score", recovery_col, "Recovery Score Distribution"),
	("Sleep Hours", sleep_col, "Sleep Hours Distribution"),
]

top_left, top_right = st.columns(2, gap="large")
bottom_left, bottom_right = st.columns(2, gap="large")
histogram_columns = [top_left, top_right, bottom_left, bottom_right]

for container, (label, column_name, chart_title) in zip(histogram_columns, histogram_targets):
	with container:
		if column_name and not filtered_df.empty:
			histogram_figure = build_histogram(filtered_df, column_name, chart_title, label)
			st.plotly_chart(histogram_figure, use_container_width=True)
		else:
			st.info(f"{label} data are not available for this view.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align:center; color:#6b7280;">
        Built by Harshvardhanam <br>
        <b>FitSync</b> © 2026
    </div>
    """,
    unsafe_allow_html=True,
)
