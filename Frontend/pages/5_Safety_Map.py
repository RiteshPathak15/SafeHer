import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from data.helplines import helplines
import sys
sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar_header, sidebar_filter_section

st.set_page_config(page_title="SafeHer - Safety Map", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first")
    st.stop()

st.title("🗺️ Safety Map - Crime Intensity by State/District")

# Load data
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
df = pd.read_csv(DATA_DIR / "dstrCAW_1.csv")

# Calculate total crimes per row
crime_cols = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths', 'Assault on women with intent to outrage her modesty', 'Insult to modesty of Women', 'Cruelty by Husband or his Relatives', 'Importation of Girls']
df['Total Crimes'] = df[crime_cols].sum(axis=1)

# Sidebar layout
with st.sidebar:
    render_sidebar_header()
    sidebar_filter_section("🔍 Filters")
    
    # Sidebar filters
    states = sorted(df['STATE/UT'].unique())
    selected_state = st.selectbox("Select State/UT", ["🇮🇳 India (All States)"] + list(states))
    
    years = sorted(df['Year'].unique())
    selected_year = st.selectbox("Select Year", ["All Years"] + list(years), index=len(years))
    
    crime_types = st.multiselect("Select Crime Types", crime_cols, default=crime_cols)

# Filter data
if selected_state == "🇮🇳 India (All States)":
    state_df = df.copy()
    state_name = "India"
else:
    state_df = df[df['STATE/UT'] == selected_state]
    state_name = selected_state
    
if selected_year != "All Years":
    state_df = state_df[state_df['Year'] == selected_year]
if crime_types:
    state_df['Filtered Crimes'] = state_df[crime_types].sum(axis=1)
else:
    state_df['Filtered Crimes'] = state_df['Total Crimes']

# Aggregate by district
district_crimes = state_df.groupby('DISTRICT')['Filtered Crimes'].sum().reset_index().sort_values('Filtered Crimes', ascending=False)

year_text = "All Years" if selected_year == "All Years" else f"({selected_year})"
st.subheader(f"District Crime Summary in {state_name} {year_text}")

# State total card
total_crimes = district_crimes['Filtered Crimes'].sum()
st.metric(label=f"Total Crimes in {state_name}", value=f"{int(total_crimes):,}")

# Display top districts as cards
top_districts = district_crimes.head(5)
cols = st.columns(len(top_districts))
for i, (_, row) in enumerate(top_districts.iterrows()):
    with cols[i]:
        st.metric(label=row['DISTRICT'], value=f"{int(row['Filtered Crimes']):,}")

# Choropleth map for states (India level)
map_year_text = "All Years" if selected_year == "All Years" else str(selected_year)
st.subheader(f"India State Crime Intensity Map ({map_year_text})")

year_df = df if selected_year == "All Years" else df[df['Year'] == selected_year]
if crime_types:
    year_df['Filtered Crimes'] = year_df[crime_types].sum(axis=1)
else:
    year_df['Filtered Crimes'] = year_df['Total Crimes']
state_totals = year_df.groupby('STATE/UT')['Filtered Crimes'].sum().reset_index()

# Map state names to match geojson
state_mapping = {
    'ANDHRA PRADESH': 'Andhra Pradesh',
    'ARUNACHAL PRADESH': 'Arunachal Pradesh',
    'ASSAM': 'Assam',
    'BIHAR': 'Bihar',
    'CHHATTISGARH': 'Chhattisgarh',
    'GOA': 'Goa',
    'GUJARAT': 'Gujarat',
    'HARYANA': 'Haryana',
    'HIMACHAL PRADESH': 'Himachal Pradesh',
    'JAMMU & KASHMIR': 'Jammu and Kashmir',
    'JHARKHAND': 'Jharkhand',
    'KARNATAKA': 'Karnataka',
    'KERALA': 'Kerala',
    'MADHYA PRADESH': 'Madhya Pradesh',
    'MAHARASHTRA': 'Maharashtra',
    'MANIPUR': 'Manipur',
    'MEGHALAYA': 'Meghalaya',
    'MIZORAM': 'Mizoram',
    'NAGALAND': 'Nagaland',
    'ODISHA': 'Odisha',
    'PUNJAB': 'Punjab',
    'RAJASTHAN': 'Rajasthan',
    'SIKKIM': 'Sikkim',
    'TAMIL NADU': 'Tamil Nadu',
    'TRIPURA': 'Tripura',
    'UTTAR PRADESH': 'Uttar Pradesh',
    'UTTARAKHAND': 'Uttarakhand',
    'WEST BENGAL': 'West Bengal',
    'DELHI': 'Delhi',
    'CHANDIGARH': 'Chandigarh',
    'PUDUCHERRY': 'Puducherry',
    'D & N HAVELI': 'Dadra and Nagar Haveli',
    'DAMAN & DIU': 'Daman and Diu',
    'LAKSHADWEEP': 'Lakshadweep',
    'A & N ISLANDS': 'Andaman and Nicobar Islands'
}
state_totals['State'] = state_totals['STATE/UT'].map(state_mapping).fillna(state_totals['STATE/UT'])

fig_map = px.choropleth(state_totals, geojson="https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson",
                        featureidkey='properties.NAME_1',
                        locations='State', color='Filtered Crimes',
                        color_continuous_scale='Reds',
                        title=f"Crime Intensity by State in India ({map_year_text})",
                        hover_name='State', hover_data=['Filtered Crimes'],
                        projection="mercator")
fig_map.update_geos(fitbounds="locations", visible=False, center=dict(lat=20.5937, lon=78.9629), scope="asia")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# Color legend
st.markdown("**Color Legend:** Red indicates higher crime intensity, lighter colors lower.")

# Helpline section
st.subheader("🚨 Emergency Helplines & Protection Resources")

# Helplines in columns
if selected_state in helplines:
    st.write(f"**{selected_state} Emergency Contacts:**")
    cols = st.columns(len(helplines[selected_state]))
    for i, (key, value) in enumerate(helplines[selected_state].items()):
        with cols[i]:
            st.metric(label=key, value=value)
            if st.button(f"Call {key}", key=f"call_{key}_{i}"):
                st.info(f"Dial {value} for {key}")
else:
    st.write("Helpline data not available for this state. General: Police 100, Women Helpline 181")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Police", value="100")
        if st.button("Call Police"):
            st.info("Dial 100 for Police")
    with col2:
        st.metric(label="Women Helpline", value="181")
        if st.button("Call Women Helpline"):
            st.info("Dial 181 for Women Helpline")

# Protection tips in expander
with st.expander("🛡️ Personal Safety Tips", expanded=True):
    st.markdown("""
    **Daily Safety Practices:**
    - Stay in well-lit and populated areas, especially at night
    - Share your live location with trusted family/friends via apps
    - Use safety apps like SafeHer or emergency SOS features on your phone
    - Know the locations of nearby police stations and hospitals
    - Report any suspicious activity immediately to authorities
    - Carry personal alarms or pepper spray if legal in your area
    - Avoid sharing personal information with strangers online or in person
    - Travel in groups when possible, especially in unfamiliar areas
    - Keep emergency contacts saved and ensure your phone is charged
    - Learn basic self-defense techniques through local classes

    **In Case of Emergency:**
    - Stay calm and assess the situation
    - Move to a safe location if possible
    - Call emergency services immediately
    - Provide clear details: location, what happened, description of suspects
    - Do not confront the perpetrator if it endangers you
    - Seek medical attention if injured
    - Contact support organizations for counseling

    **Digital Safety:**
    - Use strong passwords and two-factor authentication
    - Be cautious with sharing location on social media
    - Report cyber harassment to platforms and authorities
    - Use privacy settings on apps and devices
    """)

# Additional resources
st.subheader("📚 Additional Resources")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**National Commission for Women**")
    st.write("Helpline: 011-26942369")
    st.write("Website: ncw.nic.in")
with col2:
    st.markdown("**Ministry of Women & Child Development**")
    st.write("Helpline: 1098 (Child Helpline)")
    st.write("Website: wcd.nic.in")
with col3:
    st.markdown("**One Stop Centre (OSC)**")
    st.write("For women in distress")
    st.write("Dial 181 for location")

st.markdown("---")
st.caption("Remember: Prevention is key. Stay aware, stay safe.")

if st.button("Back to Dashboard"):
    st.switch_page("pages/2_dashboard.py")
