# FitSync 🫀
**A personal health analytics platform that turns daily wellness data into clear, actionable recovery insights.**

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)

## Project Overview
FitSync is a three-page personal health analytics dashboard built with Python and Streamlit. It helps users explore recovery patterns through a clean landing page, a KPI-focused dashboard, and a dedicated trends page. The app analyzes core wellness metrics such as recovery score, sleep hours, steps, calories burned, and resting heart rate to surface meaningful patterns from daily data. For a recruiter, this project shows product thinking, data handling, dashboard design, and visualization skills in a practical analytics application.

## Key Features
- Clean, recruiter-friendly landing page that introduces the product clearly.
- Dashboard page with KPI cards, time filtering, and interactive Plotly visualizations.
- Trends page with monthly recovery trends, summary statistics, and distribution histograms.
- Shared sidebar time filter for consistent navigation across analytics views.
- Cached data processing with `st.cache_data` for faster reruns and a smoother user experience.
- Dark theme support through Streamlit configuration for a polished visual style.

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![GitHub Codespaces](https://img.shields.io/badge/GitHub_Codespaces-181717?style=for-the-badge&logo=github&logoColor=white)

## Project Structure

```text
FitSync/
├── Home.py
├── pages/
│   ├── Dashboard.py
│   └── Trends.py
├── modules/
│   └── processor.py
├── data/
│   └── health_data.csv
└── requirements.txt
```

## How to Run
### Option 1: GitHub Codespaces
1. Open the repository in GitHub Codespaces.
2. Wait for the environment to finish loading.
3. Open the terminal.
4. Run the app:

```bash
streamlit run Home.py
```

### Option 2: Local Setup
1. Clone the repository.
2. Install the dependencies from `requirements.txt`.
3. Run the app from the terminal:

```bash
streamlit run Home.py
```

4. Use the sidebar to navigate between the main page, dashboard, and trends views.