import streamlit as st
from utils import (
    initialize_apis, 
    initialize_session_state,
    scrape_website_content,
    extract_business_info_from_content,
    search_competitors,
    generate_recommendations,
    generate_logo,
    display_business_summary,
    display_competitor_results,
    display_logo_generation_info,
    display_generated_logo
)

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Business AI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# INITIALIZATION
# =============================================================================

# Initialize APIs and session state
tavily_client = initialize_apis()
initialize_session_state()

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    st.title("🚀 Business AI Assistant")
    st.markdown("*Comprehensive business analysis and strategic insights*")
    st.divider()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📊 Import Business", "🔍 Competitor Analysis", "🎨 Logo Generation"])
    
    # =============================================================================
    # TAB 1: IMPORT BUSINESS
    # =============================================================================
    
    with tab1:
        st.header("📊 Import Business Information")
        
        # Two main options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌐 Import Business from Website", use_container_width=True, type="primary"):
                st.session_state.import_method = "website"
        
        with col2:
            if st.button("✏️ Import Business Manually", use_container_width=True, type="secondary"):
                st.session_state.import_method = "manual"
        
        st.divider()
        
        # Website Import
        if st.session_state.get('import_method') == "website":
            handle_website_import()
        
        # Manual Import
        elif st.session_state.get('import_method') == "manual":
            handle_manual_import()
        
        # Display current business data
        display_business_summary()
    
    # =============================================================================
    # TAB 2: COMPETITOR ANALYSIS
    # =============================================================================
    
    with tab2:
        st.header("🔍 Competitor Analysis")
        
        if not st.session_state.business_data:
            st.warning("⚠️ Please import business information in the first tab before proceeding with competitor analysis.")
        else:
            handle_competitor_analysis()
    
    # =============================================================================
    # TAB 3: LOGO GENERATION
    # =============================================================================
    
    with tab3:
        st.header("🎨 Logo Generation")
        
        if not st.session_state.business_data:
            st.warning("⚠️ Please import business information in the first tab before generating a logo.")
        else:
            handle_logo_generation()

# =============================================================================
# TAB HANDLERS
# =============================================================================

def handle_website_import():
    """Handle website import functionality"""
    st.subheader("🌐 Import from Website")
    
    website_url = st.text_input(
        "Enter Business Website URL:",
        placeholder="https://example.com",
        help="Enter the full URL including https://"
    )
    
    if website_url and st.button("🔍 Extract Business Information", type="primary"):
        with st.spinner("Scraping website and extracting business information..."):
            # Scrape website content
            content = scrape_website_content(website_url)
            
            if content:
                # Extract business info using AI
                extracted_info = extract_business_info_from_content(content, website_url)
                
                if extracted_info:
                    st.session_state.business_data = extracted_info
                    st.success("✅ Business information extracted successfully!")
                    
                    # Display extracted information
                    st.subheader("📋 Extracted Information")
                    
                    for key, value in extracted_info.items():
                        display_key = key.replace('_', ' ').title()
                        st.write(f"**{display_key}:** {value}")
                else:
                    st.error("Failed to extract business information from the website.")
            else:
                st.error("Failed to scrape website content. Please check the URL and try again.")

def handle_manual_import():
    """Handle manual business information entry"""
    st.subheader("✏️ Manual Business Information Entry")
    
    with st.form("business_form"):
        business_name = st.text_input("Business Name *", placeholder="Enter your business name")
        business_industry = st.text_input("Industry *", placeholder="e.g., Technology, Healthcare, Retail")
        business_values = st.text_area("Business Values", placeholder="What does your business stand for?")
        business_target_audience = st.text_area("Target Audience", placeholder="Who are your customers?")
        business_description = st.text_area("Business Description", placeholder="What does your business do?")
        business_unique_selling_point = st.text_input("Unique Selling Point", placeholder="What makes you special?")
        
        submitted = st.form_submit_button("💾 Save Business Information", type="primary")
        
        if submitted:
            if business_name and business_industry:
                business_data = {
                    'business_name': business_name,
                    'business_industry': business_industry,
                    'business_values': business_values,
                    'business_target_audience': business_target_audience,
                    'business_description': business_description,
                    'business_unique_selling_point': business_unique_selling_point
                }
                st.session_state.business_data = business_data
                st.success("✅ Business information saved successfully!")
            else:
                st.error("Please fill in at least Business Name and Industry.")

def handle_competitor_analysis():
    """Handle competitor analysis functionality"""
    # Display current business info
    business_name = st.session_state.business_data.get('business_name', 'N/A')
    business_industry = st.session_state.business_data.get('business_industry', 'N/A')
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Business:** {business_name}")
    with col2:
        st.info(f"**Industry:** {business_industry}")
    
    st.divider()
    
    # Search for competitors
    if st.button("🔍 Search for Competitors", type="primary", use_container_width=True):
        with st.spinner("Searching for competitors in your industry..."):
            competitors = search_competitors(business_name, business_industry, tavily_client)
            st.session_state.competitor_data = competitors
            
            if competitors:
                st.success(f"✅ Found {len(competitors)} potential competitors!")
            else:
                st.warning("No competitors found. Try adjusting your business information.")
    
    # Display competitor results
    display_competitor_results()
    
    # Generate recommendations
    if st.session_state.competitor_data:
        st.divider()
        if st.button("📋 Generate Recommendations", type="primary", use_container_width=True):
            with st.spinner("Analyzing competitors and generating recommendations..."):
                competitor_summary = ""
                for comp in st.session_state.competitor_data:
                    competitor_summary += f"- {comp['name']}: {comp['description'][:100]}...\n"
                
                recommendations = generate_recommendations(
                    st.session_state.business_data, 
                    competitor_summary
                )
                st.session_state.recommendations = recommendations
                
                st.subheader("📋 Strategic Recommendations")
                st.markdown(recommendations)

def handle_logo_generation():
    """Handle logo generation functionality"""
    # Display business info for context
    business_name = st.session_state.business_data.get('business_name', 'Your Business')
    st.info(f"**Generating logo for:** {business_name}")
    
    # Show recommendations status and information
    display_logo_generation_info()
    
    st.divider()
    
    # Logo generation buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🎨 Generate Logo", type="primary", use_container_width=True):
            recommendations = st.session_state.get('recommendations', None)
            
            if recommendations:
                st.info("🎯 Using strategic recommendations for enhanced logo design")
            else:
                st.info("💡 Tip: Complete competitor analysis first for strategic logo design")
            
            with st.spinner("Creating your custom logo..."):
                logo_url = generate_logo(st.session_state.business_data, recommendations)
                
                if logo_url:
                    st.session_state.logo_url = logo_url
                    st.success("✅ Logo generated successfully!")
                else:
                    st.error("Failed to generate logo. Please try again.")
    
    with col2:
        if st.session_state.logo_url:
            if st.button("🔄 Generate New Logo", type="secondary", use_container_width=True):
                recommendations = st.session_state.get('recommendations', None)
                
                with st.spinner("Creating a new logo..."):
                    logo_url = generate_logo(st.session_state.business_data, recommendations)
                    
                    if logo_url:
                        st.session_state.logo_url = logo_url
                        st.success("✅ New logo generated!")
    
    # Display generated logo
    display_generated_logo()

# =============================================================================
# RUN APPLICATION
# =============================================================================

if __name__ == "__main__":
    main()
