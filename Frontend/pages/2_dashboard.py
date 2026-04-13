import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="SafeHer - Dashboard", layout="wide")

# -------- AUTH CHECK --------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first in Login page")
    st.stop()

# -------- DATASET NAME MAPPING --------
DATASET_NAMES = {
    "dstrCAW_1.csv": "📍 Crime Against Women by District & Year",
    "dstrCAW.csv": "📍 Crime Against Women (District Level)",
    "CAW_TCI_2018.csv": "📈 Crime Against Women - Trend & Case Index",
    "NCRB CII-2020 Table.No-19B.2.csv": "📊 Crime Against Women (State Level)",
}

def get_display_name(filename):
    """Convert filename to readable dataset name"""
    # First try exact match
    if filename in DATASET_NAMES:
        return DATASET_NAMES[filename]
    
    # Try case-insensitive and partial match for NCRB files
    for key, val in DATASET_NAMES.items():
        if filename.lower() in key.lower() or key.lower() in filename.lower():
            return val
    
    # Fallback: clean up the filename
    return filename.replace("_", " ").replace(".csv", "")

# -------- STYLING --------
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
    margin: 10px 0;
}
.metric-label {
    font-size: 14px;
    opacity: 0.9;
}
.chart-container {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------- DATA LOADING --------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
if not DATA_DIR.exists():
    DATA_DIR = Path(__file__).resolve().parents[2] / "data"

csv_files = sorted(DATA_DIR.glob("*.csv")) if DATA_DIR.exists() else []
if not csv_files:
    st.error("No CSV datasets found. Please upload datasets first.")
    st.stop()

# Create display names for dropdown
file_options = {get_display_name(f.name): f.name for f in csv_files}
selected_display = st.selectbox("📊 Select Dataset", list(file_options.keys()), index=0)
selected_file = file_options[selected_display]
path = DATA_DIR / selected_file

try:
    df = pd.read_csv(path)
except Exception as err:
    st.error(f"Error loading {selected_file}: {err}")
    st.stop()

# -------- TITLE & FILTERS --------
st.title("📊 SafeHer Data Analytics Dashboard")
st.markdown(f"**Dataset:** {selected_display} | **Rows:** {len(df):,} | **Columns:** {len(df.columns)}")

# Sidebar filters
df_filtered = df.copy()
with st.sidebar:
    st.header("🔍 Filters")
    
    year_cols = [c for c in df.columns if 'Year' in c or c == 'Year']
    selected_year = None
    if year_cols:
        years = sorted(df[year_cols[0]].dropna().unique())
        if len(years) > 0:
            selected_year = st.selectbox("Year", ["All Years"] + list(years), index=0)
            if selected_year != "All Years":
                df_filtered = df_filtered[df_filtered[year_cols[0]] == selected_year]
                st.success(f"Filtered by year: {selected_year}")
        else:
            st.warning("No year data available in this dataset")
    else:
        st.info("No year filter available for this dataset")

# Reset to original df for display if no filter applied
if df_filtered.empty and selected_year and selected_year != "All Years":
    st.warning(f"⚠️ No data found for year {selected_year}. Showing all data.")
    df_filtered = df.copy()
elif df_filtered.empty:
    df_filtered = df.copy()


# -------- KEY METRICS --------
st.markdown("### 📈 Key Metrics")

# Define crime columns
crime_cols = [c for c in df_filtered.columns if c in [
    "Rape", "Kidnapping and Abduction", "Dowry Deaths", 
    "Assault on women with intent to outrage her modesty", 
    "Insult to modesty of Women", "Cruelty by Husband or his Relatives", 
    "Importation of Girls"
]]

metric_cols = st.columns(4)
if crime_cols and len(crime_cols) > 0:
    total_crimes = df_filtered[crime_cols].sum().sum()
    with metric_cols[0]:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Total Crimes Recorded</div>
            <div class='metric-value'>{int(total_crimes):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if "Rape" in crime_cols:
        with metric_cols[1]:
            rape_count = df_filtered["Rape"].sum()
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Rape Offences</div>
                <div class='metric-value'>{int(rape_count):,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    if "Cruelty by Husband or his Relatives" in crime_cols:
        with metric_cols[2]:
            cruelty = df_filtered["Cruelty by Husband or his Relatives"].sum()
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Cruelty Cases</div>
                <div class='metric-value'>{int(cruelty):,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    if "Kidnapping and Abduction" in crime_cols:
        with metric_cols[3]:
            kidnap = df_filtered["Kidnapping and Abduction"].sum()
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Kidnapping Cases</div>
                <div class='metric-value'>{int(kidnap):,}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    # Fallback for datasets without standard crime columns
    numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        # Show summary stats for available numeric columns
        for i, col in enumerate(numeric_cols[:4]):
            with metric_cols[i]:
                col_sum = df_filtered[col].sum()
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>{col[:30]}</div>
                    <div class='metric-value'>{int(col_sum):,}</div>
                </div>
                """, unsafe_allow_html=True)

# -------- VISUALIZATIONS --------
st.markdown("---")

# Special handling for NCRB dataset (safer check)
if "NCRB" in selected_file:
    # Skip all visualizations for NCRB dataset
    pass

else:
    if crime_cols and len(crime_cols) > 0:
        # Crime Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Crime Categories Distribution")
            total_by_crime = df_filtered[crime_cols].sum().sort_values(ascending=True)
            fig_dist = go.Figure(data=[
                go.Bar(y=total_by_crime.index, x=total_by_crime.values, orientation='h', 
                       marker=dict(color=total_by_crime.values, colorscale='Reds'))
            ])
            fig_dist.update_layout(height=400, showlegend=False, margin=dict(l=200))
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            st.markdown("### Crime Percentage Breakdown")
            fig_pie = px.pie(values=df_filtered[crime_cols].sum().values, 
                             names=df_filtered[crime_cols].sum().index,
                             title="Crime Type Distribution")
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Regional Analysis
        if "STATE/UT" in df_filtered.columns:
            st.markdown("### Top 10 States/UT by Crime Index")
            state_crimes = df_filtered.groupby("STATE/UT")[crime_cols].sum().sum(axis=1).sort_values(ascending=False).head(10)
            fig_states = px.bar(x=state_crimes.values, y=state_crimes.index, orientation='h',
                               labels={'x': 'Total Crimes', 'y': 'State/UT'},
                               color=state_crimes.values, color_continuous_scale='Oranges')
            fig_states.update_layout(height=400, showlegend=False, margin=dict(l=150))
            st.plotly_chart(fig_states, use_container_width=True)
        
        # Year Trend
        if "Year" in df_filtered.columns:
            st.markdown("### Crime Trend Over Years")
            yearly = df_filtered.groupby("Year")[crime_cols].sum().sum(axis=1)
            fig_trend = px.line(x=yearly.index, y=yearly.values, markers=True,
                               labels={'x': 'Year', 'y': 'Total Crimes'})
            fig_trend.update_traces(line=dict(color='#667eea', width=3), marker=dict(size=8))
            fig_trend.update_layout(height=400)
            st.plotly_chart(fig_trend, use_container_width=True)

    else:
        # Fallback: Generate visualizations for generic datasets
        st.info("📊 Creating dynamic visualizations based on available data...")
        
        numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
        string_cols = df_filtered.select_dtypes(include=['object']).columns.tolist()
        
        # Detect geographic columns for mapping
        geo_cols = [c for c in string_cols if any(x in c.lower() for x in ['state', 'district', 'region', 'region', 'zone', 'area'])]
        
        if numeric_cols and string_cols:
            col1, col2 = st.columns(2)
            
            # Find the best column to group by
            group_col = geo_cols[0] if geo_cols else string_cols[0]
            metric_col = numeric_cols[0] if numeric_cols else None
            
            if group_col and metric_col:
                with col1:
                    st.markdown(f"### Top {group_col} by {metric_col}")
                    grouped = df_filtered.groupby(group_col)[metric_col].sum().sort_values(ascending=True).tail(15)
                    fig_dist = go.Figure(data=[
                        go.Bar(y=grouped.index, x=grouped.values, orientation='h', 
                               marker=dict(color=grouped.values, colorscale='Blues'))
                    ])
                    fig_dist.update_layout(height=450, showlegend=False, margin=dict(l=200))
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                with col2:
                    st.markdown(f"### Distribution by {group_col}")
                    top_10 = df_filtered.groupby(group_col)[metric_col].sum().sort_values(ascending=False).head(10)
                    fig_pie = px.pie(values=top_10.values, names=top_10.index, 
                                     title=f"Top 10 {group_col} by {metric_col}")
                    fig_pie.update_layout(height=450)
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            # Show additional numeric metrics
            if len(numeric_cols) > 1:
                st.markdown("### Additional Metrics")
                for col in numeric_cols[1:4]:
                    c1, c2 = st.columns(2)
                    with c1:
                        fig_hist = px.histogram(df_filtered, x=col, nbins=20, title=f"Distribution of {col}",
                                               color_discrete_sequence=['#667eea'])
                        st.plotly_chart(fig_hist, use_container_width=True)
                    with c2:
                        if group_col:
                            fig_box = px.box(df_filtered, x=group_col, y=col, title=f"{col} by {group_col}")
                            st.plotly_chart(fig_box, use_container_width=True)
                        break
        
        elif numeric_cols:
            # Show histograms for numeric data
            st.markdown("### Data Distribution")
            cols_to_show = min(3, len(numeric_cols))
            for col in numeric_cols[:cols_to_show]:
                fig = px.histogram(df_filtered, x=col, nbins=30, title=f"Distribution of {col}",
                                 color_discrete_sequence=['#667eea'])
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.warning("⚠️ No numeric data found for visualization. Showing table only.")

# -------- DATA TABLE --------
st.markdown("---")
st.markdown("### 📋 Full Dataset Preview")

# Select relevant columns for display
display_cols = [c for c in df_filtered.columns if not c.startswith('Si. No') and not c.startswith('Sl')]
if display_cols:
    st.dataframe(df_filtered[display_cols].head(25), use_container_width=True)
else:
    st.dataframe(df_filtered.head(25), use_container_width=True)

# -------- NAVIGATION --------
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("pages/7_About.py")
with col2:
    if st.button("🗺️ Safety Map", use_container_width=True):
        st.switch_page("pages/5_Safety_Map.py")
with col3:
    if st.button("💬 Global Chat", use_container_width=True):
        st.switch_page("pages/6_GlobalChat.py")

