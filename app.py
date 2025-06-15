import streamlit as st
from utils import (
    initialize_apis,
    initialize_session_state,
    scrape_website_content,
    extract_business_info_from_website,
    generate_recommendations,
    apply_recommendation,
    generate_logo_with_dalle,
    search_competitors,
    display_business_summary,
    display_applied_recommendations,
    validate_url
)

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Business AI Assistant - Claude Uplift",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# INITIALIZATION
# =============================================================================

# Initialize APIs and session state
llm, tavily_client = initialize_apis()
initialize_session_state()

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    st.title("🚀 Business AI Assistant - Claude Uplift")
    st.markdown("*Comprehensive business analysis and strategic insights powered by Claude*")
    st.divider()
    
    # Create 4 tabs as specified
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Business Information", 
        "💡 Recommendations", 
        "🎨 Logo Generation", 
        "🔍 Competitor Analysis"
    ])
    
    # =============================================================================
    # TAB 1: BUSINESS INFORMATION
    # =============================================================================
    
    with tab1:
        handle_business_information()
    
    # =============================================================================
    # TAB 2: RECOMMENDATIONS
    # =============================================================================
    
    with tab2:
        handle_recommendations()
    
    # =============================================================================
    # TAB 3: LOGO GENERATION
    # =============================================================================
    
    with tab3:
        handle_logo_generation()
    
    # =============================================================================
    # TAB 4: COMPETITOR ANALYSIS
    # =============================================================================
    
    with tab4:
        handle_competitor_analysis()

# =============================================================================
# TAB HANDLERS
# =============================================================================

def handle_business_information():
    """Handle business information tab"""
    st.header("📊 Business Information")
    
    # Display current business data if available
    display_business_summary()
    
    st.divider()
    
    # Two import options
    st.subheader("📥 Import Business Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌐 Import from Website", use_container_width=True, type="primary"):
            st.session_state.import_method = "website"
    
    with col2:
        if st.button("✏️ Import Manually", use_container_width=True, type="secondary"):
            st.session_state.import_method = "manual"
    
    st.divider()
    
    # Handle import methods
    if st.session_state.get('import_method') == "website":
        handle_website_import()
    elif st.session_state.get('import_method') == "manual":
        handle_manual_import()

def handle_website_import():
    """Handle website import functionality"""
    st.subheader("🌐 Import from Website")
    
    website_url = st.text_input(
        "Enter Business Website URL:",
        placeholder="https://example.com",
        help="Enter the full URL including https://"
    )
    
    if website_url and st.button("🔍 Extract Business Information", type="primary"):
        if not validate_url(website_url):
            st.error("Please enter a valid URL (including https://)")
            return
        
        with st.spinner("Scraping website and extracting business information..."):
            # Scrape website content
            content = scrape_website_content(website_url)
            
            if content:
                # Extract business info using LangChain
                extracted_info = extract_business_info_from_website(content, website_url, llm)
                
                if extracted_info:
                    st.session_state.business_data = extracted_info
                    st.success("✅ Business information extracted successfully!")
                    
                    # Display extracted information
                    st.subheader("📋 Extracted Information")
                    display_business_summary()
                else:
                    st.error("Failed to extract business information from the website.")
            else:
                st.error("Failed to scrape website content. Please check the URL and try again.")

def handle_manual_import():
    """Handle manual business information entry"""
    st.subheader("✏️ Manual Business Information Entry")
    
    with st.form("business_form"):
        business_name = st.text_input(
            "Business Name *", 
            value=st.session_state.business_data.get('business_name', ''),
            placeholder="Enter your business name"
        )
        business_description = st.text_area(
            "Business Description *", 
            value=st.session_state.business_data.get('business_description', ''),
            placeholder="What does your business do?"
        )
        business_website = st.text_input(
            "Business Website", 
            value=st.session_state.business_data.get('business_website', ''),
            placeholder="https://yourwebsite.com"
        )
        business_industry = st.text_input(
            "Business Industry *", 
            value=st.session_state.business_data.get('business_industry', ''),
            placeholder="e.g., Technology, Healthcare, Retail"
        )
        
        submitted = st.form_submit_button("💾 Save Business Information", type="primary")
        
        if submitted:
            if business_name and business_description and business_industry:
                st.session_state.business_data = {
                    'business_name': business_name,
                    'business_description': business_description,
                    'business_website': business_website,
                    'business_industry': business_industry
                }
                st.success("✅ Business information saved successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *).")

def handle_recommendations():
    """Handle recommendations tab"""
    st.header("💡 Recommendations")
    
    # Check if business data exists
    if not any(st.session_state.business_data.values()):
        st.warning("⚠️ Please enter business information in the first tab before generating recommendations.")
        return
    
    # Display current business context
    st.subheader("📋 Business Context")
    display_business_summary()
    
    st.divider()
    
    # Display applied recommendations
    display_applied_recommendations()
    
    st.divider()
    
    # Generate recommendations button
    if st.button("🎯 Generate Recommendations", type="primary", use_container_width=True):
        with st.spinner("Generating personalized recommendations..."):
            recommendations = generate_recommendations(st.session_state.business_data, llm)
            st.session_state.recommendations = recommendations
    
    # Display recommendations with action buttons
    if st.session_state.recommendations:
        st.subheader("📝 Generated Recommendations")
        
        # Create table-like display
        for i, rec in enumerate(st.session_state.recommendations):
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 1])
                
                with col1:
                    st.write(f"**{rec['type']}**")
                    st.write(rec['recommendation'])
                
                with col2:
                    st.write(rec['description'])
                
                with col3:
                    if st.button(f"Apply", key=f"apply_{i}", type="secondary"):
                        apply_recommendation(rec['type'], rec['recommendation'])
                        st.rerun()
                
                st.divider()

def handle_logo_generation():
    """Handle logo generation tab"""
    st.header("🎨 Logo Generation")
    
    # Check if business data exists
    if not any(st.session_state.business_data.values()):
        st.warning("⚠️ Please enter business information first.")
        return
    
    # Display business context
    st.subheader("📋 Business Context")
    display_business_summary()
    
    st.divider()
    
    # Display applied recommendations that affect logo
    st.subheader("🎯 Design Guidance")
    display_applied_recommendations()
    
    if not any(st.session_state.applied_recommendations.values()):
        st.info("💡 Generate and apply recommendations first for better logo design guidance.")
    
    st.divider()
    
    # Logo generation
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🎨 Generate Logo", type="primary", use_container_width=True):
            with st.spinner("Creating your custom logo..."):
                logo_url = generate_logo_with_dalle(
                    st.session_state.business_data,
                    st.session_state.applied_recommendations,
                    llm
                )
                
                if logo_url:
                    st.session_state.logo_url = logo_url
                    st.success("✅ Logo generated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to generate logo. Please try again.")
    
    with col2:
        if st.session_state.logo_url:
            if st.button("🔄 Generate New Logo", type="secondary", use_container_width=True):
                with st.spinner("Creating a new logo..."):
                    logo_url = generate_logo_with_dalle(
                        st.session_state.business_data,
                        st.session_state.applied_recommendations,
                        llm
                    )
                    
                    if logo_url:
                        st.session_state.logo_url = logo_url
                        st.success("✅ New logo generated!")
                        st.rerun()
    
    # Display generated logo
    if st.session_state.logo_url:
        st.divider()
        st.subheader("🖼️ Your Generated Logo")
        
        business_name = st.session_state.business_data.get('business_name', 'Your Business')
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(st.session_state.logo_url, caption=f"Logo for {business_name}", use_column_width=True)
        
        st.markdown("💡 **Tip:** Right-click on the logo image and select 'Save image as...' to download it.")

def handle_competitor_analysis():
    """Handle competitor analysis tab"""
    st.header("🔍 Competitor Analysis")
    
    # Check if business data exists
    if not any(st.session_state.business_data.values()):
        st.warning("⚠️ Please enter business information first.")
        return
    
    # Display business context
    st.subheader("📋 Business Context")
    display_business_summary()
    
    st.divider()
    
    # Search for competitors
    if st.button("🔍 Search for Competitors", type="primary", use_container_width=True):
        with st.spinner("Searching for competitors..."):
            competitors = search_competitors(st.session_state.business_data, tavily_client)
            st.session_state.competitors = competitors
            
            if competitors:
                st.success(f"✅ Found {len(competitors)} potential competitors!")
            else:
                st.warning("No competitors found. Try adjusting your business information.")
    
    # Display competitor results
    if st.session_state.competitors:
        st.subheader("📊 Competitor Analysis Results")
        
        # Create table header
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            st.write("**Competitor Name**")
        with col2:
            st.write("**Competitor Website**")
        with col3:
            st.write("**Competitor Industry**")
        
        st.divider()
        
        # Display competitors in table format
        for competitor in st.session_state.competitors:
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                st.write(competitor['name'])
            
            with col2:
                if competitor['website']:
                    st.write(f"[Visit Website]({competitor['website']})")
                else:
                    st.write("Not available")
            
            with col3:
                st.write(competitor['industry'])
            
            # Show description if available
            if competitor.get('description'):
                st.caption(competitor['description'])
            
            st.divider()

# =============================================================================
# RUN APPLICATION
# =============================================================================

if __name__ == "__main__":
    main()
