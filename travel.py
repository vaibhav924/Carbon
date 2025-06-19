import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Travel Tracker",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚗 Travel Tracker Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Track your daily travels, costs, and carbon emissions</p>', unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'travel_data' not in st.session_state:
    st.session_state.travel_data = []
if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False

# Sidebar for user information
with st.sidebar:
    st.markdown('<h2 class="sub-header">👤 User Information</h2>', unsafe_allow_html=True)
    
    if not st.session_state.setup_complete:
        with st.form("user_info_form"):
            name = st.text_input("Enter your name:", placeholder="Your full name")
            age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
            vehicle = st.text_input("Enter your vehicle model:", placeholder="e.g., Honda City, Maruti Swift")
            city = st.text_input("Enter city name:", placeholder="Your city")
            
            submitted = st.form_submit_button("🚀 Start Tracking", use_container_width=True)
            
            if submitted:
                if name and vehicle and city:
                    st.session_state.user_data = {
                        'name': name,
                        'age': age,
                        'vehicle': vehicle,
                        'city': city
                    }
                    st.session_state.setup_complete = True
                    st.rerun()
                else:
                    st.error("Please fill in all required fields!")
    else:
        # Display user info
        st.success("✅ Setup Complete!")
        st.info(f"""
        **Name:** {st.session_state.user_data['name']}  
        **Age:** {st.session_state.user_data['age']}  
        **Vehicle:** {st.session_state.user_data['vehicle']}  
        **City:** {st.session_state.user_data['city']}
        """)
        
        if st.button("🔄 Reset Setup", use_container_width=True):
            st.session_state.setup_complete = False
            st.session_state.travel_data = []
            st.rerun()

# Main content
if st.session_state.setup_complete:
    # Days of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Travel tracking section
    st.markdown('<h2 class="sub-header">📅 Weekly Travel Tracking</h2>', unsafe_allow_html=True)
    
    # Create tabs for each day
    day_tabs = st.tabs([f"📅 {day}" for day in days])
    
    for i, (tab, day) in enumerate(zip(day_tabs, days)):
        with tab:
            st.markdown(f"<h3>🗓️ {day}</h3>", unsafe_allow_html=True)
            
            # Check if data already exists for this day
            existing_data = next((item for item in st.session_state.travel_data if item['day'] == day), None)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                traveled = st.radio(
                    f"Did you travel on {day}?",
                    ["Select", "Yes", "No"],
                    key=f"travel_{day}",
                    index=0 if not existing_data else (1 if existing_data['traveled'] else 2)
                )
            
            if traveled == "Yes":
                with col2:
                    with st.form(f"travel_form_{day}"):
                        destination = st.text_input(
                            "Where did you travel?",
                            value=existing_data['destination'] if existing_data else "",
                            placeholder="Enter destination"
                        )
                        distance = st.number_input(
                            "How many KM did you travel?",
                            min_value=0.0,
                            value=float(existing_data['distance']) if existing_data else 0.0,
                            step=0.1
                        )
                        
                        submitted = st.form_submit_button(f"💾 Save {day} Data", use_container_width=True)
                        
                        if submitted and destination and distance > 0:
                            # Calculate cost and emissions
                            cost = distance * 75  # ₹75 per km
                            emission = distance * 125  # 125g per km
                            
                            # Remove existing data for this day
                            st.session_state.travel_data = [
                                item for item in st.session_state.travel_data if item['day'] != day
                            ]
                            
                            # Add new data
                            st.session_state.travel_data.append({
                                'day': day,
                                'traveled': True,
                                'destination': destination,
                                'distance': distance,
                                'cost': cost,
                                'emission': emission
                            })
                            
                            st.success(f"✅ Data saved for {day}!")
                            st.rerun()
                
                # Display results if data exists
                if existing_data and existing_data['traveled']:
                    st.markdown('<div class="success-message">', unsafe_allow_html=True)
                    st.markdown(f"""
                    **📍 Destination:** {existing_data['destination']}  
                    **📏 Distance:** {existing_data['distance']} KM  
                    **💰 Estimated Cost:** ₹{existing_data['cost']:,.0f}  
                    **🏭 Carbon Emission:** {existing_data['emission']:,.0f}g
                    """)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            elif traveled == "No":
                # Remove any existing data for this day
                st.session_state.travel_data = [
                    item for item in st.session_state.travel_data if item['day'] != day
                ]
                st.session_state.travel_data.append({
                    'day': day,
                    'traveled': False,
                    'destination': '',
                    'distance': 0,
                    'cost': 0,
                    'emission': 0
                })
                
                st.markdown('<div class="warning-message">', unsafe_allow_html=True)
                st.markdown(f"🌱 That's great, {st.session_state.user_data['name']}! You preserved money as well as carbon emission on {day}.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Results and Analytics Section
    if st.session_state.travel_data:
        st.markdown("---")
        st.markdown('<h2 class="sub-header">📊 Travel Analytics & Summary</h2>', unsafe_allow_html=True)
        
        # Filter only traveled days
        traveled_days = [item for item in st.session_state.travel_data if item['traveled']]
        
        if traveled_days:
            # Calculate statistics
            total_km = sum(item['distance'] for item in traveled_days)
            total_cost = sum(item['cost'] for item in traveled_days)
            total_emission = sum(item['emission'] for item in traveled_days)
            
            emissions_list = [item['emission'] for item in traveled_days]
            max_emission = max(emissions_list) if emissions_list else 0
            min_emission = min(emissions_list) if emissions_list else 0
            
            # Display key metrics
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                st.metric("🛣️ Total KM", f"{total_km:.1f}")
            with col2:
                st.metric("💰 Total Cost", f"₹{total_cost:,.0f}")
            with col3:
                st.metric("🏭 Total Emissions", f"{total_emission:,.0f}g")
            with col4:
                st.metric("📈 Max Daily Emission", f"{max_emission:,.0f}g")
            with col5:
                st.metric("📉 Min Daily Emission", f"{min_emission:,.0f}g")
            with col6:
                st.metric("📅 Days Traveled", len(traveled_days))
            
            # Create visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Daily distance chart
                df_traveled = pd.DataFrame(traveled_days)
                fig_distance = px.bar(
                    df_traveled, 
                    x='day', 
                    y='distance',
                    title='Daily Distance Traveled (KM)',
                    color='distance',
                    color_continuous_scale='Blues'
                )
                fig_distance.update_layout(showlegend=False)
                st.plotly_chart(fig_distance, use_container_width=True)
            
            with col2:
                # Daily emissions chart
                fig_emission = px.bar(
                    df_traveled, 
                    x='day', 
                    y='emission',
                    title='Daily Carbon Emissions (g)',
                    color='emission',
                    color_continuous_scale='Reds'
                )
                fig_emission.update_layout(showlegend=False)
                st.plotly_chart(fig_emission, use_container_width=True)
            
            # Pie chart for cost distribution
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(
                    df_traveled,
                    values='cost',
                    names='day',
                    title='Cost Distribution by Day'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Summary table
                st.subheader("📋 Detailed Summary")
                summary_df = df_traveled[['day', 'destination', 'distance', 'cost', 'emission']].copy()
                summary_df['cost'] = summary_df['cost'].apply(lambda x: f"₹{x:,.0f}")
                summary_df['emission'] = summary_df['emission'].apply(lambda x: f"{x:,.0f}g")
                summary_df['distance'] = summary_df['distance'].apply(lambda x: f"{x:.1f} KM")
                
                summary_df.columns = ['Day', 'Destination', 'Distance', 'Cost', 'Emissions']
                st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            # Export data button
            csv = df_traveled.to_csv(index=False)
            st.download_button(
                label="📥 Download Travel Data as CSV",
                data=csv,
                file_name=f"travel_data_{st.session_state.user_data['name']}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv',
                use_container_width=True
            )
        
        else:
            st.info("🌱 Great! You didn't travel any day this week. You saved money and reduced carbon emissions!")
    
    else:
        st.info("👆 Please fill in your travel information for each day using the tabs above.")

else:
    # Welcome message when setup is not complete
    st.markdown("""
    ### 🚀 Welcome to Travel Tracker!
    
    This application helps you track your daily travels, calculate costs, and monitor carbon emissions.
    
    **Features:**
    - 📅 Track travel for each day of the week
    - 💰 Calculate travel costs (₹75 per KM)
    - 🏭 Monitor carbon emissions (125g per KM)
    - 📊 Visualize your travel patterns
    - 📥 Export data for further analysis
    
    **Get Started:**
    👈 Fill in your information in the sidebar to begin tracking!
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        🚗 Travel Tracker Dashboard | Built with Streamlit ❤️
    </div>
    """, 
    unsafe_allow_html=True
)