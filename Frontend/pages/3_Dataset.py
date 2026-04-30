import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar_header
from theme import apply_global_theme

st.set_page_config(page_title="Rakshika-Ai- Data Science Lab", layout="wide", page_icon="🔬")

# Apply global theme
apply_global_theme()

# -------- AUTH CHECK --------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first in Login page")
    st.stop()

# -------- HEADER --------
st.title("Rakshika-Ai Data Science Lab")
st.markdown("**Advanced Analytics & Research Tools for Women's Safety Data**")

# -------- SIDEBAR HEADER --------
with st.sidebar:
    render_sidebar_header()

# -------- DATA DIRECTORY --------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
if not DATA_DIR.exists():
    DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# -------- LOAD DATASETS --------
csv_files = sorted(DATA_DIR.glob("*.csv")) if DATA_DIR.exists() else []
if not csv_files:
    st.error("No datasets found. Please ensure CSV files are in the data/ folder.")
    st.stop()

# Dataset descriptions
DATASET_INFO = {
    "District-Level Crime Against Women.csv": {
        "name": "📍 District-Level Crime Against Women",
        "description": "Comprehensive district-wise crime statistics across India",
        "type": "crime",
        "columns": ["District", "State/UT", "Year", "Rape", "Kidnapping", "Dowry Deaths", "Cruelty"]
    }
}

# -------- DATASET SELECTION --------
st.markdown("### � Select Dataset for Analysis")

# Create cards for each dataset
cols = st.columns(len(csv_files))
for i, file_path in enumerate(csv_files):
    filename = file_path.name
    info = DATASET_INFO.get(filename, {
        "name": filename.replace(".csv", "").replace("_", " "),
        "description": "Dataset analysis and insights",
        "type": "general"
    })

    with cols[i]:
        st.markdown(f"""
        <div class='dataset-card'>
            <div class='dataset-title'>{info['name']}</div>
            <div class='dataset-desc'>{info['description']}</div>
        </div>
        """, unsafe_allow_html=True)

selected_file = st.selectbox("🔍 Select Dataset to Explore", [f.name for f in csv_files], index=0)
path = DATA_DIR / selected_file

# -------- LOAD SELECTED DATASET --------
try:
    df = pd.read_csv(path)
    st.success(f"✅ Loaded {selected_file} successfully!")
except Exception as err:
    st.error(f"❌ Error loading {selected_file}: {err}")
    st.stop()

# -------- DATA PROFILING --------
st.markdown("---")
st.markdown("## 🔍 Data Profiling & Quality Check")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📏 Shape", f"{df.shape[0]} × {df.shape[1]}")
with col2:
    missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    st.metric("❓ Missing Data", f"{missing_pct:.1f}%")
with col3:
    dup_count = df.duplicated().sum()
    st.metric("🔄 Duplicates", dup_count)
with col4:
    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
    st.metric("💾 Memory", f"{memory_mb:.1f} MB")

# Data quality checks
st.markdown("### 📋 Data Quality Report")
quality_cols = st.columns(3)

with quality_cols[0]:
    st.markdown("**Column Types:**")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        st.write(f"- {dtype}: {count}")

with quality_cols[1]:
    st.markdown("**Missing Values by Column:**")
    missing_by_col = df.isnull().sum()
    missing_cols = missing_by_col[missing_by_col > 0]
    if len(missing_cols) > 0:
        for col, count in missing_cols.head(5).items():
            pct = (count / len(df)) * 100
            st.write(f"- {col}: {count} ({pct:.1f}%)")
    else:
        st.write("✅ No missing values!")

with quality_cols[2]:
    st.markdown("**Data Range Check:**")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.write(f"Numeric columns: {len(numeric_cols)}")
        negative_vals = (df[numeric_cols] < 0).sum().sum()
        st.write(f"Negative values: {negative_vals}")
        zero_vals = (df[numeric_cols] == 0).sum().sum()
        st.write(f"Zero values: {zero_vals}")
    else:
        st.write("No numeric columns found")

# -------- EMERGENCY RESOURCES BANNER --------
st.markdown("""
<div class='emergency-banner'>
    <h3>🚨 Women's Safety Emergency Helplines</h3>
    <p><strong>National Helpline:</strong> 1091 | <strong>Police:</strong> 100 | <strong>Women Helpline:</strong> 181</p>
    <p><em>In case of emergency, call immediately!</em></p>
</div>
""", unsafe_allow_html=True)

# -------- ADVANCED ANALYSIS TOOLS --------
st.markdown("---")
st.markdown("## 🛠️ Advanced Analysis Tools")

analysis_tabs = st.tabs(["📊 Statistical Analysis", "🔗 Correlation Analysis", "🔍 Custom Queries"])
# Tab 1: Statistical Analysis
with analysis_tabs[0]:
    st.markdown("### 📊 Statistical Summary")

    if len(df.select_dtypes(include=[np.number]).columns) > 0:
        # Descriptive statistics
        st.markdown("**Descriptive Statistics:**")
        numeric_df = df.select_dtypes(include=[np.number])
        desc_stats = numeric_df.describe().round(2)
        st.dataframe(desc_stats, use_container_width=True)

        # Distribution analysis
        st.markdown("**Distribution Analysis:**")
        selected_col = st.selectbox("Select column for distribution analysis",
                                   numeric_df.columns.tolist(),
                                   key="dist_col")

        if selected_col:
            col1, col2 = st.columns(2)

            with col1:
                fig_hist = px.histogram(df, x=selected_col, nbins=30,
                                       title=f"Distribution of {selected_col}")
                st.plotly_chart(fig_hist, use_container_width=True)

            with col2:
                sorted_data = df[[selected_col]].dropna().sort_values(by=selected_col)
                fig_line = px.line(sorted_data.reset_index(drop=True), y=selected_col,
                                   title=f"Sorted {selected_col} Trend",
                                   labels={selected_col: selected_col, 'index': 'Rank'})
                fig_line.add_hline(y=df[selected_col].mean(), line_dash="dash",
                                   line_color="green", annotation_text="Mean",
                                   annotation_position="top right")
                fig_line.add_hline(y=df[selected_col].median(), line_dash="dot",
                                   line_color="blue", annotation_text="Median",
                                   annotation_position="bottom right")
                st.plotly_chart(fig_line, use_container_width=True)

            # Statistical tests
            st.markdown(f"**Statistical Tests for {selected_col}:**")
            test_cols = st.columns(4)
            with test_cols[0]:
                st.metric("Mean", f"{df[selected_col].mean():.2f}")
            with test_cols[1]:
                st.metric("Median", f"{df[selected_col].median():.2f}")
            with test_cols[2]:
                st.metric("Std Dev", f"{df[selected_col].std():.2f}")
            with test_cols[3]:
                st.metric("Skewness", f"{df[selected_col].skew():.2f}")

    else:
        st.warning("No numeric columns available for statistical analysis.")

# Tab 2: Correlation Analysis
with analysis_tabs[1]:
    st.markdown("### 🔗 Correlation Analysis")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) >= 2:
        # Correlation matrix
        corr_matrix = df[numeric_cols].corr()

        # Heatmap
        fig_corr = px.imshow(corr_matrix,
                           text_auto=True,
                           aspect="auto",
                           title="Correlation Matrix",
                           color_continuous_scale="RdBu_r")
        st.plotly_chart(fig_corr, use_container_width=True)

        corr_pairs = []
        for i in range(len(numeric_cols)):
            for j in range(i+1, len(numeric_cols)):
                corr_val = abs(corr_matrix.iloc[i, j])
                corr_pairs.append((numeric_cols[i], numeric_cols[j], corr_val))

        corr_pairs.sort(key=lambda x: x[2], reverse=True)

    else:
        st.warning("Need at least 2 numeric columns for correlation analysis.")

# Tab 3: Custom Queries
with analysis_tabs[2]:
    st.markdown("### 🔍 Custom Data Queries")

    st.markdown("""
    <div style='background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 8px; font-family: Courier New, monospace; margin: 10px 0;'>
    <strong>Available DataFrame:</strong> df<br>
    <strong>Example queries:</strong><br>
    • df[df['column'] > value]<br>
    • df.groupby('column')['numeric_col'].mean()<br>
    • df['column'].value_counts()<br>
    • df.isnull().sum()
    </div>
    """, unsafe_allow_html=True)

    query_type = st.selectbox("Query Type",
                             ["Filter Rows", "Group By", "Value Counts", "Custom Expression"])

    if query_type == "Filter Rows":
        filter_col = st.selectbox("Column to filter", df.columns.tolist())
        if df[filter_col].dtype in ['int64', 'float64']:
            min_val, max_val = st.slider("Value range",
                                       float(df[filter_col].min()),
                                       float(df[filter_col].max()),
                                       (float(df[filter_col].min()), float(df[filter_col].max())))
            filtered_df = df[(df[filter_col] >= min_val) & (df[filter_col] <= max_val)]
        else:
            unique_vals = df[filter_col].unique()
            selected_vals = st.multiselect("Select values", unique_vals)
            if selected_vals:
                filtered_df = df[df[filter_col].isin(selected_vals)]
            else:
                filtered_df = df

        st.write(f"Filtered results: {len(filtered_df)} rows")
        st.dataframe(filtered_df.head(20), use_container_width=True)

    elif query_type == "Group By":
        group_col = st.selectbox("Group by column", df.columns.tolist())
        agg_col = st.selectbox("Aggregate column",
                              df.select_dtypes(include=[np.number]).columns.tolist())
        agg_func = st.selectbox("Aggregation function", ["mean", "sum", "count", "min", "max"])

        if agg_func == "count":
            result = df.groupby(group_col)[agg_col].count()
        else:
            result = getattr(df.groupby(group_col)[agg_col], agg_func)()

        result_df = result.reset_index().sort_values(agg_col, ascending=False)
        st.dataframe(result_df, use_container_width=True)

        # Visualization
        fig_group = px.bar(result_df.head(10), x=group_col, y=agg_col,
                          title=f"Top 10 {agg_func.upper()} of {agg_col} by {group_col}")
        st.plotly_chart(fig_group, use_container_width=True)

    elif query_type == "Value Counts":
        count_col = st.selectbox("Column for value counts", df.columns.tolist())
        counts = df[count_col].value_counts().head(20)

        st.dataframe(counts.reset_index(), use_container_width=True)

        fig_counts = px.bar(counts, x=counts.index, y=counts.values,
                           title=f"Value Distribution: {count_col}")
        st.plotly_chart(fig_counts, use_container_width=True)

    elif query_type == "Custom Expression":
        st.markdown("**Enter a pandas expression:**")
        st.code("Example: df[df['numeric_col'] > df['numeric_col'].mean()]")
        custom_query = st.text_area("Custom pandas query", height=100)

        if custom_query.strip():
            try:
                result = eval(custom_query)
                if isinstance(result, pd.DataFrame):
                    st.write(f"Result shape: {result.shape}")
                    st.dataframe(result.head(20), use_container_width=True)
                elif isinstance(result, pd.Series):
                    st.write(f"Result length: {len(result)}")
                    st.dataframe(result.head(20).reset_index(), use_container_width=True)
                else:
                    st.write(f"Result: {result}")
            except Exception as e:
                st.error(f"Query error: {e}")

# -------- RAW DATA VIEW --------
st.markdown("---")
st.markdown("### 📄 Raw Data Preview")

# Filters for data view
col1, col2 = st.columns(2)
with col1:
    show_rows = st.slider("Rows to display", 5, 50, 20)
with col2:
    if len(df.columns) > 10:
        show_all_cols = st.checkbox("Show all columns", value=False)
    else:
        show_all_cols = True

if show_all_cols:
    st.dataframe(df.head(show_rows), use_container_width=True)
else:
    # Show only first 10 columns
    st.dataframe(df.iloc[:show_rows, :10], use_container_width=True)
    st.info("ℹ️ Showing first 10 columns only. Check 'Show all columns' to see everything.")

# -------- DOWNLOAD OPTION --------
st.markdown("---")
st.markdown("### 💾 Export Data")
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Download as CSV"):
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="Click to Download",
            data=csv_data,
            file_name=f"{selected_file}",
            mime="text/csv"
        )
with col2:
    if st.button("📊 Download Summary"):
        summary = df.describe(include='all').to_csv()
        st.download_button(
            label="Click to Download",
            data=summary,
            file_name=f"{selected_file.replace('.csv', '')}_summary.csv",
            mime="text/csv"
        )

# -------- NAVIGATION --------
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("pages/7_About.py")
with col2:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/2_dashboard.py")
with col3:
    if st.button("💬 Global Chat", use_container_width=True):
        st.switch_page("pages/6_GlobalChat.py")
