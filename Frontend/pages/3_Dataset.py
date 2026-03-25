import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="SafeHer - Dataset Explorer", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first in Login page")
    st.stop()

st.title("SafeHer Dataset Explorer")

# locate dataset folder in Frontend/data
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
if not DATA_DIR.exists():
    DATA_DIR = Path(__file__).resolve().parents[2] / "data"

st.markdown(f"**Dataset folder**: `{DATA_DIR}`")

csv_files = sorted(DATA_DIR.glob("*.csv")) if DATA_DIR.exists() else []
if not csv_files:
    st.error("No CSV datasets found in data/ folder.")
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

# clean dataset: drop unnecessary columns and rename for clarity
unnecessary_cols = [c for c in df.columns if c.strip().lower().startswith("si. no") or c.strip().lower().startswith("total cities") or c.strip() == ""]
if unnecessary_cols:
    df = df.drop(columns=unnecessary_cols, errors='ignore')

rename_map = {}
if "STATE/UT" in df.columns:
    rename_map["STATE/UT"] = "State/UT"
if "DISTRICT" in df.columns:
    rename_map["DISTRICT"] = "District"
if "Si. No. (Col. 1)" in df.columns:
    rename_map["Si. No. (Col. 1)"] = "Index"
if "City (Col. 2)" in df.columns:
    rename_map["City (Col. 2)"] = "City"
if rename_map:
    df = df.rename(columns=rename_map)

# define emergency helpline by state (default national 1091)
state_emergency = {
    "Andhra Pradesh": "1091",
    "Arunachal Pradesh": "1091",
    "Assam": "1091",
    "Bihar": "1091",
    "Chhattisgarh": "1091",
    "Goa": "1091",
    "Gujarat": "1091",
    "Haryana": "1091",
    "Himachal Pradesh": "1091",
    "Jharkhand": "1091",
    "Karnataka": "1091",
    "Kerala": "1091",
    "Madhya Pradesh": "1091",
    "Maharashtra": "1091",
    "Manipur": "1091",
    "Meghalaya": "1091",
    "Mizoram": "1091",
    "Nagaland": "1091",
    "Odisha": "1091",
    "Punjab": "1091",
    "Rajasthan": "1091",
    "Sikkim": "1091",
    "Tamil Nadu": "1091",
    "Telangana": "1091",
    "Tripura": "1091",
    "Uttar Pradesh": "1091",
    "Uttarakhand": "1091",
    "West Bengal": "1091",
    "Delhi": "112",  # central emergency
    "Jammu & Kashmir": "1091",
    "Ladakh": "1091",
    "Andaman & Nicobar Islands": "1091",
    "Chandigarh": "1091",
    "Dadra and Nagar Haveli & Daman and Diu": "1091",
    "Lakshadweep": "1091",
    "Puducherry": "1091",
}

# identify crime columns for stats
crime_columns = [c for c in df.columns if c in ["Rape", "Kidnapping and Abduction", "Dowry Deaths", "Assault on women with intent to outrage her modesty", "Insult to modesty of Women", "Cruelty by Husband or his Relatives", "Importation of Girls"]]

# if crime dataset
if crime_columns:
    df_analysis = df.copy()
    if "Year" in df_analysis.columns:
        df_analysis["Year"] = pd.to_numeric(df_analysis["Year"], errors='coerce')

    grouping_col = "State/UT" if "State/UT" in df_analysis.columns else ("City" if "City" in df_analysis.columns else None)
    group_name = "State/UT" if grouping_col == "State/UT" else "City"

    if grouping_col:
        summary = df_analysis.groupby(grouping_col)[crime_columns].sum()
        summary["Total Cases"] = summary.sum(axis=1)
        summary = summary.sort_values("Total Cases", ascending=False)

        total_cases = int(summary["Total Cases"].sum())
        highest_state = summary.index[0]
        highest_total = int(summary.iloc[0]["Total Cases"])
        lowest_state = summary.index[-1]
        lowest_total = int(summary.iloc[-1]["Total Cases"])

        pct_change = None
        if "Year" in df_analysis.columns and df_analysis["Year"].notna().any():
            yearly_total = df_analysis.groupby("Year")[crime_columns].sum().sum(axis=1).sort_index()
            if len(yearly_total) > 1:
                last, prev = yearly_total.iloc[-1], yearly_total.iloc[-2]
                if prev != 0:
                    pct_change = (last - prev) / prev * 100

        st.markdown("## Key Insights")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total cases", f"{total_cases:,}")
        c2.metric("Highest", f"{highest_state} ({highest_total:,})")
        c3.metric("Lowest", f"{lowest_state} ({lowest_total:,})")
        c4.metric("% change (year over year)", f"{pct_change:+.2f}%" if pct_change is not None else "N/A")

        st.markdown("### Emergency call number for women safety")
        if grouping_col == "State/UT":
            selected_state = st.selectbox("Select State/UT", [str(s) for s in summary.index], index=0)
            emergency_number = state_emergency.get(selected_state, "1091")
            st.success(f"{selected_state} women safety helpline: {emergency_number}")

        st.markdown("---")

        display_df = summary.reset_index().rename(columns={grouping_col: group_name})

        # conditional style: high values red, low values green in numeric columns
        numeric_cols = display_df.select_dtypes(include=["number"]).columns.tolist()
        if "Total Cases" in numeric_cols:
            high_threshold = display_df["Total Cases"].quantile(0.9)
            low_threshold = display_df["Total Cases"].quantile(0.1)

            def style_value(v):
                if pd.isna(v) or not isinstance(v, (int, float, complex)):
                    return ""
                if v >= high_threshold:
                    return "background-color: #f8d7da; color: #842029"
                if v <= low_threshold:
                    return "background-color: #d1e7dd; color: #0f5132"
                return ""

            st.subheader(f"{group_name} crime overview (sorted by total cases)")
            st.write(display_df.style.applymap(style_value, subset=numeric_cols))
        else:
            st.subheader(f"{group_name} crime overview (sorted by total cases)")
            st.dataframe(display_df)

        if "Year" in df_analysis.columns:
            st.subheader("Trend by year")
            yearly = df_analysis.groupby("Year")[crime_columns].sum().sort_index()
            st.line_chart(yearly)

    else:
        st.warning("No State/UT or City column found for crimes summary.")

else:
    # fallback for non-crime datasets (arrests)
    total_candidates = [c for c in df.columns if 'Total Persons Arrested' in c and 'age and Sex' in c]
    if total_candidates:
        total_col = total_candidates[0]
        total_arrests = int(df[total_col].sum()) if pd.api.types.is_numeric_dtype(df[total_col]) else 0
        st.metric("Total persons arrested", f"{total_arrests:,}")

        if "City" in df.columns:
            city_summary = df.groupby("City")[total_col].sum().sort_values(ascending=False)
            st.subheader("Top 10 cities by total arrests")
            st.bar_chart(city_summary.head(10))

        st.markdown("---")

st.markdown("---")
st.subheader("Dataset head")
st.dataframe(df.head(20))

if st.button("Back to Home"):
    st.info("Use the sidebar to go back to Home or other pages.")
