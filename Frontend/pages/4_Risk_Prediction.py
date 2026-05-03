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

st.set_page_config(page_title="Rakshika-Ai - Risk Prediction", layout="wide", page_icon="🎯")

# Apply global theme
apply_global_theme()

# -------- AUTH CHECK --------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first in Login page")
    st.stop()

# -------- HEADER --------
st.title("🎯 Risk Prediction & Analysis")
st.markdown("**AI-Powered Risk Assessment for Women's Safety**")

# -------- SIDEBAR HEADER --------
with st.sidebar:
    render_sidebar_header()

# -------- DATA DIRECTORY --------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
if not DATA_DIR.exists():
    DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# -------- LOAD DATA --------
@st.cache_data
def load_crime_data():
    csv_path = DATA_DIR / "District-Level Crime Against Women.csv"
    if not csv_path.exists():
        st.error("Crime dataset not found.")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    # Calculate total crimes
    crime_cols = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
                  'Assault on women with intent to outrage her modesty',
                  'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
                  'Importation of Girls']
    df['Total Crimes'] = df[crime_cols].sum(axis=1)
    return df

df = load_crime_data()
if df.empty:
    st.stop()

# -------- PREDICTION INTERFACE --------
st.subheader("🔍 Risk Assessment Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    states = ["All States"] + sorted(df['STATE/UT'].unique())
    selected_state = st.selectbox("Select State/UT", states, index=0)

with col2:
    if selected_state == "All States":
        districts = ["All Districts"]
    else:
        districts = ["All Districts"] + sorted(df[df['STATE/UT'] == selected_state]['DISTRICT'].unique())
    selected_district = st.selectbox("Select District", districts, index=0)

with col3:
    years = ["All Years"] + sorted(df['Year'].unique(), reverse=True)
    selected_year = st.selectbox("Select Year", years, index=0)

# Crime type selection
crime_cols = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
              'Assault on women with intent to outrage her modesty',
              'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
              'Importation of Girls']
selected_crime_types = st.multiselect("Select Crime Types for Analysis",
                                      crime_cols, default=crime_cols[:3])

# -------- RISK CALCULATION --------
def calculate_risk_score(data_subset):
    if data_subset.empty:
        return 0, "No Data"

    total_crimes = data_subset['Total Crimes'].sum()
    avg_crimes = data_subset['Total Crimes'].mean()

    # Simple risk scoring based on percentiles
    national_avg = df['Total Crimes'].mean()
    national_std = df['Total Crimes'].std()

    if total_crimes > national_avg + national_std:
        risk_level = "High Risk"
        risk_score = min(100, 75 + (total_crimes - national_avg) / national_std * 10)
    elif total_crimes > national_avg:
        risk_level = "Medium Risk"
        risk_score = 50 + (total_crimes - national_avg) / national_std * 15
    else:
        risk_level = "Low Risk"
        risk_score = max(0, 25 + (total_crimes - national_avg) / national_std * 10)

    return risk_score, risk_level

# Filter data based on selections
filtered_df = df.copy()
if selected_state != "All States":
    filtered_df = filtered_df[filtered_df['STATE/UT'] == selected_state]
if selected_district != "All Districts":
    filtered_df = filtered_df[filtered_df['DISTRICT'] == selected_district]
if selected_year != "All Years":
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]

risk_score, risk_level = calculate_risk_score(filtered_df)

# -------- DISPLAY RESULTS --------
st.subheader("📊 Risk Assessment Results")

# Risk score display
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='card-title'>Risk Score</div>
        <div class='card-value'>{risk_score:.1f}/100</div>
        <div class='card-subtitle'>{risk_level}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Risk gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Safety Risk Level"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkred" if risk_score > 70 else "orange" if risk_score > 40 else "green"},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 70], 'color': "lightyellow"},
                {'range': [70, 100], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': risk_score
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

with col3:
    # Summary stats
    total_crimes = int(filtered_df['Total Crimes'].sum()) if not filtered_df.empty else 0
    num_districts = len(filtered_df['DISTRICT'].unique()) if not filtered_df.empty else 0

    st.markdown(f"""
    <div class='metric-card'>
        <div class='card-title'>Total Crimes</div>
        <div class='card-value'>{total_crimes:,}</div>
        <div class='card-subtitle'>Across {num_districts} districts</div>
    </div>
    """, unsafe_allow_html=True)

# -------- TREND ANALYSIS --------
if not filtered_df.empty and len(filtered_df) > 1:
    st.subheader("📈 Risk Trend Analysis")

    # Group by year for trend
    yearly_trend = df.groupby('Year')['Total Crimes'].mean().reset_index()

    fig_trend = px.line(yearly_trend, x='Year', y='Total Crimes',
                       title="Average Crime Trend Over Years",
                       markers=True)
    fig_trend.update_layout(height=300)
    st.plotly_chart(fig_trend, use_container_width=True)

# -------- AI RISK ASSISTANT --------
st.subheader("🤖 AI Risk Analysis Assistant")

def build_risk_response(query_text: str):
    query = query_text.strip().lower()

    # Calculate additional insights for better responses
    national_avg = df['Total Crimes'].mean()
    national_max = df['Total Crimes'].max()

    # Get top crime types for the selected area
    if not filtered_df.empty and len(selected_crime_types) > 0:
        crime_breakdown = filtered_df[selected_crime_types].sum().sort_values(ascending=False)
        top_crime = crime_breakdown.index[0] if len(crime_breakdown) > 0 else "various crimes"
        top_crime_count = int(crime_breakdown.iloc[0]) if len(crime_breakdown) > 0 else 0
    else:
        top_crime = "various crimes"
        top_crime_count = 0

    # Calculate risk comparison
    risk_comparison = ""
    if risk_score > 75:
        risk_comparison = f"significantly higher than the national average of {national_avg:.0f} crimes"
    elif risk_score > 50:
        risk_comparison = f"above the national average of {national_avg:.0f} crimes"
    else:
        risk_comparison = f"below the national average of {national_avg:.0f} crimes"

    location_text = f"{selected_district}, {selected_state}" if selected_district != "All Districts" else selected_state
    year_text = "across all years" if selected_year == "All Years" else f"in {selected_year}"

    # Enhanced summary with more details
    if query == "" or query in ["summary", "overview", "status", "risk"]:
        summary = f"**Risk Assessment for {location_text} {year_text}:**\n\n"
        summary += f"• **Risk Score:** {risk_score:.1f}/100 ({risk_level})\n"
        summary += f"• **Total Crimes:** {total_crimes:,} reported cases\n"
        summary += f"• **Primary Crime Type:** {top_crime} ({top_crime_count:,} cases)\n"
        summary += f"• **Risk Level:** This area is {risk_comparison}\n\n"

        if risk_level == "High Risk":
            summary += "⚠️ **High Alert:** Extra precautions recommended. "
        elif risk_level == "Medium Risk":
            summary += "⚡ **Caution:** Stay vigilant and informed. "
        else:
            summary += "✅ **Generally Safe:** Maintain awareness. "

        summary += "\n\n💡 *Ask me about specific safety tips, emergency contacts, or prevention strategies.*"
        return summary

    # Enhanced safety recommendations based on crime types and risk level
    if "recommend" in query or "advice" in query or "prevent" in query or "safety" in query:
        advice = f"**Personalized Safety Recommendations for {location_text}:**\n\n"

        # Base recommendations by risk level
        if risk_level == "High Risk":
            advice += "🚨 **High-Risk Area Precautions:**\n"
            advice += "• Avoid isolated areas, especially after dark\n"
            advice += "• Travel with trusted companions when possible\n"
            advice += "• Share real-time location with emergency contacts\n"
            advice += "• Use well-lit, populated routes\n"
            advice += "• Consider personal safety devices\n\n"
        elif risk_level == "Medium Risk":
            advice += "⚠️ **Medium-Risk Area Precautions:**\n"
            advice += "• Be extra cautious during evening/night hours\n"
            advice += "• Stay in groups when commuting\n"
            advice += "• Keep emergency numbers readily accessible\n"
            advice += "• Trust your instincts and avoid risky situations\n\n"
        else:
            advice += "✅ **General Safety Awareness:**\n"
            advice += "• Maintain basic safety habits\n"
            advice += "• Report any suspicious activities\n"
            advice += "• Support local safety initiatives\n\n"

        # Crime-specific recommendations
        if "Rape" in selected_crime_types and top_crime == "Rape":
            advice += "🎯 **Sexual Assault Prevention:**\n"
            advice += "• Avoid walking alone in poorly lit areas\n"
            advice += "• Be cautious with strangers offering help\n"
            advice += "• Learn self-defense techniques\n"
            advice += "• Use ride-sharing services at night\n\n"

        if "Kidnapping and Abduction" in selected_crime_types:
            advice += "🔐 **Abduction Prevention:**\n"
            advice += "• Don't share personal information with strangers\n"
            advice += "• Be wary of unsolicited offers of assistance\n"
            advice += "• Keep children within sight at all times\n\n"

        # Emergency contacts
        advice += "🚑 **Emergency Contacts:**\n"
        advice += "• Police: 100 | Women Helpline: 181\n"
        advice += "• Medical Emergency: 108 | Fire: 101\n"
        advice += f"• Local Police Station in {selected_state}\n\n"

        advice += "💪 **Prevention is Key:** Stay informed, stay connected, stay safe!"
        return advice

    # Detailed risk factor analysis
    if "factor" in query or "why" in query or "cause" in query:
        factors = f"**Risk Factors Analysis for {location_text}:**\n\n"

        factors += f"📊 **Data-Driven Insights:**\n"
        factors += f"• Primary crime type: {top_crime} ({top_crime_count:,} cases)\n"
        factors += f"• Risk score: {risk_score:.1f}/100 ({risk_comparison})\n"
        factors += f"• Crime concentration: {len(filtered_df)} reporting districts\n\n"

        factors += "🔍 **Contributing Factors:**\n"
        factors += "• **Demographic Patterns:** Population density and urbanization levels\n"
        factors += "• **Socioeconomic Conditions:** Economic disparities and social structures\n"
        factors += "• **Law Enforcement:** Police presence and response capabilities\n"
        factors += "• **Community Awareness:** Local safety education and reporting habits\n"
        factors += "• **Infrastructure:** Lighting, transportation, and public spaces\n\n"

        factors += "📈 **Statistical Context:**\n"
        factors += f"• National average crimes: {national_avg:.0f} per district\n"
        factors += f"• This area's total: {total_crimes:,} crimes\n"
        factors += f"• Risk percentile: Top {100-risk_score:.0f}% safest areas\n\n"

        factors += "💡 *Risk factors are complex and interconnected. This analysis is based on reported crime data.*"
        return factors

    # Enhanced trend analysis with actual data
    if "trend" in query or "change" in query or "over time" in query:
        if selected_year == "All Years" and len(df['Year'].unique()) > 1:
            yearly_data = df.groupby('Year')['Total Crimes'].mean().reset_index()
            trend_direction = "stable"
            if len(yearly_data) > 1:
                first_year = yearly_data['Total Crimes'].iloc[0]
                last_year = yearly_data['Total Crimes'].iloc[-1]
                if last_year > first_year * 1.1:
                    trend_direction = "increasing"
                elif last_year < first_year * 0.9:
                    trend_direction = "decreasing"

            trends = f"**Crime Trend Analysis {year_text}:**\n\n"
            trends += f"📈 **Overall Trend:** Crime rates are {trend_direction}\n"
            trends += f"• Latest year average: {last_year:.0f} crimes per district\n"
            trends += f"• Earliest year average: {first_year:.0f} crimes per district\n"
            trends += f"• {len(yearly_data)} years of data analyzed\n\n"

            trends += "📊 **Year-by-Year Breakdown:**\n"
            for _, row in yearly_data.iterrows():
                trends += f"• {int(row['Year'])}: {row['Total Crimes']:.0f} avg crimes\n"
            trends += "\n"

            trends += "🔍 **Trend Insights:**\n"
            if trend_direction == "increasing":
                trends += "• Rising trend suggests need for increased prevention efforts\n"
                trends += "• Monitor specific crime types for targeted interventions\n"
            elif trend_direction == "decreasing":
                trends += "• Positive trend indicates effective safety measures\n"
                trends += "• Continue and expand successful prevention programs\n"
            else:
                trends += "• Stable trend requires consistent safety measures\n"
                trends += "• Focus on maintaining current prevention strategies\n"

            return trends
        else:
            return f"**Trend Analysis:** Select 'All Years' to see crime patterns over time. Currently showing data for {year_text} only."

    # Enhanced help and community action
    if "help" in query or "what can i do" in query or "contribute" in query:
        help_text = f"**How You Can Help Improve Safety in {location_text}:**\n\n"

        help_text += "🏛️ **Individual Actions:**\n"
        help_text += "• Report suspicious activities to police immediately\n"
        help_text += "• Participate in neighborhood watch programs\n"
        help_text += "• Educate family and friends about safety measures\n"
        help_text += "• Support victims and survivors\n\n"

        help_text += "👥 **Community Involvement:**\n"
        help_text += "• Join local women's safety organizations\n"
        help_text += "• Volunteer for awareness campaigns\n"
        help_text += "• Advocate for better street lighting and infrastructure\n"
        help_text += "• Support candidates who prioritize public safety\n\n"

        help_text += "📢 **Awareness & Education:**\n"
        help_text += "• Share safety information on social media\n"
        help_text += "• Organize or attend safety workshops\n"
        help_text += "• Mentor youth about personal safety\n"
        help_text += "• Use this tool to make informed decisions\n\n"

        help_text += "🚔 **Official Channels:**\n"
        help_text += "• File police reports for all incidents\n"
        help_text += "• Contact local authorities about safety concerns\n"
        help_text += "• Support increased police presence in high-risk areas\n"
        help_text += "• Advocate for better emergency response systems\n\n"

        help_text += "💪 **Your Voice Matters:** Every report and every action contributes to safer communities!"
        return help_text

    # Emergency contacts and immediate help
    if "emergency" in query or "contact" in query or "police" in query or "help" in query:
        emergency = f"**Emergency Contacts & Immediate Help for {selected_state}:**\n\n"

        emergency += "🚨 **National Emergency Numbers:**\n"
        emergency += "• **Police:** 100 (All India)\n"
        emergency += "• **Women Helpline:** 181 (24/7)\n"
        emergency += "• **Medical Emergency:** 108 (Ambulance)\n"
        emergency += "• **Fire:** 101\n"
        emergency += "• **Disaster Management:** 1077\n\n"

        emergency += "📞 **State-Specific Contacts:**\n"
        # Add some common state helplines
        state_helplines = {
            "DELHI": "• Delhi Police: 1091 (Women) | 112 (Emergency)",
            "MAHARASHTRA": "• Maharashtra Women Helpline: 181 | Mumbai Police: 100",
            "KARNATAKA": "• Karnataka Women Helpline: 181 | Bangalore Police: 100",
            "TAMIL NADU": "• Tamil Nadu Women Helpline: 181 | Chennai Police: 100",
            "WEST BENGAL": "• West Bengal Women Helpline: 181 | Kolkata Police: 100",
            "GUJARAT": "• Gujarat Women Helpline: 181 | Ahmedabad Police: 100",
            "RAJASTHAN": "• Rajasthan Women Helpline: 181 | Jaipur Police: 100",
            "UTTAR PRADESH": "• UP Women Helpline: 181 | Lucknow Police: 100"
        }

        if selected_state in state_helplines:
            emergency += state_helplines[selected_state] + "\n"
        else:
            emergency += f"• Local Police Station in {selected_state}\n"

        emergency += "\n📱 **Digital Safety Resources:**\n"
        emergency += "• Download emergency apps with GPS tracking\n"
        emergency += "• Save important numbers in speed dial\n"
        emergency += "• Use location sharing with trusted contacts\n\n"

        emergency += "⚡ **Immediate Actions:**\n"
        emergency += "• Move to a safe, public location\n"
        emergency += "• Call emergency services first\n"
        emergency += "• Provide clear location details\n"
        emergency += "• Stay calm and follow dispatcher instructions\n\n"

        emergency += "🛡️ **Remember:** Your safety is the top priority. Don't hesitate to call for help!"
        return emergency

    # Crime type specific analysis
    if "crime" in query or "type" in query:
        crime_analysis = f"**Crime Type Analysis for {location_text} {year_text}:**\n\n"

        if not filtered_df.empty and len(selected_crime_types) > 0:
            crime_analysis += "📊 **Selected Crime Types Breakdown:**\n"
            for crime_type in selected_crime_types:
                if crime_type in filtered_df.columns:
                    count = int(filtered_df[crime_type].sum())
                    percentage = (count / total_crimes * 100) if total_crimes > 0 else 0
                    crime_analysis += f"• {crime_type}: {count:,} cases ({percentage:.1f}%)\n"

            crime_analysis += f"\n🎯 **Primary Concern:** {top_crime} with {top_crime_count:,} reported cases\n\n"

            # Specific insights for different crime types
            if "Rape" in selected_crime_types:
                crime_analysis += "💡 **Rape Prevention Focus:**\n"
                crime_analysis += "• Community education programs\n"
                crime_analysis += "• Improved street lighting\n"
                crime_analysis += "• Self-defense training\n\n"

            if "Dowry Deaths" in selected_crime_types:
                crime_analysis += "💡 **Dowry Violence Prevention:**\n"
                crime_analysis += "• Legal awareness campaigns\n"
                crime_analysis += "• Family counseling services\n"
                crime_analysis += "• Strict enforcement of anti-dowry laws\n\n"
        else:
            crime_analysis += "❌ No crime data available for the current selection.\n"

        crime_analysis += "🔍 **Understanding Crime Patterns:**\n"
        crime_analysis += "Different crime types require different prevention strategies.\n"
        crime_analysis += "Focus prevention efforts on the most prevalent crime categories."

        return crime_analysis

    # Default response with more context
    default_response = f"**AI Analysis for {location_text} {year_text}:**\n\n"
    default_response += f"I'm analyzing safety data showing {risk_level} conditions "
    default_response += f"with a risk score of {risk_score:.1f}/100.\n\n"

    if total_crimes > 0:
        default_response += f"📊 **Key Statistics:**\n"
        default_response += f"• Total reported crimes: {total_crimes:,}\n"
        default_response += f"• Primary crime type: {top_crime} ({top_crime_count:,} cases)\n"
        default_response += f"• Risk compared to national average: {risk_comparison}\n\n"

    default_response += "💡 **Available Analysis:**\n"
    default_response += "• Safety recommendations and prevention tips\n"
    default_response += "• Detailed risk factor analysis\n"
    default_response += "• Crime trend patterns over time\n"
    default_response += "• Emergency contact information\n"
    default_response += "• Community action suggestions\n\n"

    default_response += "🤔 *Try asking: 'safety recommendations', 'risk factors', 'emergency contacts', or 'how can I help'?*"

    return default_response

# AI Chat Interface
col1, col2 = st.columns([1, 1])

with col1:
    user_query = st.text_input("Ask the AI assistant about risk assessment", key='risk_ai_query')
    ask_button = st.button("Ask Risk AI", key='risk_ai_button')

with col2:
    if 'risk_ai_history' not in st.session_state:
        st.session_state['risk_ai_history'] = [
            {
                'role': 'assistant',
                'text': build_risk_response('summary')
            }
        ]
        st.session_state['risk_ai_context'] = {
            'state': selected_state,
            'district': selected_district,
            'year': selected_year,
            'crime_types': tuple(selected_crime_types),
            'risk_score': risk_score,
            'risk_level': risk_level
        }

    current_context = {
        'state': selected_state,
        'district': selected_district,
        'year': selected_year,
        'crime_types': tuple(selected_crime_types),
        'risk_score': risk_score,
        'risk_level': risk_level
    }

    if st.session_state.get('risk_ai_context') != current_context:
        st.session_state['risk_ai_history'] = [
            {
                'role': 'assistant',
                'text': build_risk_response('summary')
            }
        ]
        st.session_state['risk_ai_context'] = current_context

    if ask_button and user_query:
        st.session_state.risk_ai_history.append({'role': 'user', 'text': user_query})
        st.session_state.risk_ai_history.append({'role': 'assistant', 'text': build_risk_response(user_query)})

# Display chat history
st.markdown("### Conversation")
for message in st.session_state.risk_ai_history[-5:]:  # Show last 5 messages
    if message['role'] == 'user':
        st.markdown(f"<div class='chat-message user'><strong>You:</strong> {message['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-message assistant'><strong>AI Assistant:</strong> {message['text']}</div>", unsafe_allow_html=True)