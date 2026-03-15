import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="SafeHer - Dashboard", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first in Login page")
    st.stop()

st.title("SafeHer Dashboard")

# locate dataset folder in dashboard/data
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
if not DATA_DIR.exists():
    DATA_DIR = Path(__file__).resolve().parents[2] / "data"

st.markdown(f"**Dataset folder**: `{DATA_DIR}`")

csv_files = sorted(DATA_DIR.glob("*.csv")) if DATA_DIR.exists() else []
if not csv_files:
    st.error("No CSV datasets found in data/ folder. Upload from Dataset Explorer.")
    st.stop()

selected_file = st.selectbox("Choose dataset", [f.name for f in csv_files], index=0)
path = DATA_DIR / selected_file

try:
    df = pd.read_csv(path)
except Exception as err:
    st.error(f"Could not read file {selected_file}: {err}")
    st.stop()

st.markdown(f"### Loaded: {selected_file}")
st.write(f"Rows: {len(df):,}, Columns: {len(df.columns)}")

# Standard metrics by dataset type
col_total_candidates = [c for c in df.columns if 'Total Persons Arrested' in c and 'age and Sex' in c]
if col_total_candidates:
    col_total = col_total_candidates[0]
    total_crime = df[col_total].sum() if pd.api.types.is_numeric_dtype(df[col_total]) else 0
    st.metric("Total persons arrested", f"{int(total_crime):,}")

    if "City" in df.columns:
        st.subheader("Top 10 cities by total arrests")
        df_city = df.groupby("City")[col_total].sum().sort_values(ascending=False).head(10)
        st.bar_chart(df_city)

    # age group totals if available
    age_cols = [c for c in df.columns if c not in ["Si. No. (Col. 1)", "City (Col. 2)", col_total] and any(x in c for x in ['Total -', 'Male', 'Female'])]
    if age_cols:
        st.subheader("Arrests by Age Category")
        age_summary = df[age_cols].sum().reset_index()
        age_summary.columns = ['Age Category', 'Total']
        st.dataframe(age_summary)
        st.bar_chart(age_summary.set_index('Age Category'))
else:
    crime_cols = [c for c in df.columns if c in ["Rape", "Kidnapping and Abduction", "Dowry Deaths", "Assault on women with intent to outrage her modesty", "Insult to modesty of Women", "Cruelty by Husband or his Relatives", "Importation of Girls"]]
    if crime_cols:
        total_by_crime = df[crime_cols].sum().sort_values(ascending=False)
        st.metric("Total crimes in dataset", f"{int(total_by_crime.sum()):,}")
        st.subheader("Crime share (all categories)")
        st.bar_chart(total_by_crime)

        if "Year" in df.columns:
            st.subheader("Trend by year")
            yearly = df.groupby("Year")[crime_cols].sum().sort_index()
            st.line_chart(yearly)

        if "STATE/UT" in df.columns and "Rape" in df.columns:
            st.subheader("Top 10 states/UT by rape offences")
            top_states = df.groupby("STATE/UT")["Rape"].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top_states)

st.markdown("---")
st.subheader("Dataset head")
st.dataframe(df.head(20))

if st.button("Back to Home"):
    st.info("Use the sidebar to go back to Home or other pages.")
