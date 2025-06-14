import openai
import streamlit as st
import re
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from urllib.parse import urljoin, urlparse

# Initialize API clients
def initialize_apis():
    """Initialize all API clients"""
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    tavily_client = TavilyClient(api_key=st.secrets.get("TAVILY_API_KEY", ""))
    return tavily_client

# =============================================================================
# WEBSITE SCRAPING AND BUSINESS EXTRACTION
# =============================================================================

def scrape_website_content(url):
    """Scrape and extract business information from website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract text content
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit content and clean up
        content = clean_text[:8000]  # Limit to 8000 characters
        
        return content
    except Exception as e:
        st.error(f"Error scraping website: {str(e)}")
        return None

def extract_business_info_from_content(website_content, url):
    """Use AI to extract business information from website content"""
    prompt = f"""
    Analyze the following website content and extract key business information. 
    Website URL: {url}
    
    Website Content:
    {website_content}
    
    Please extract and provide the following information in a structured format:
    
    1. Business Name
    2. Industry
    3. Business Values (what the company stands for)
    4. Business Target Audience (who they serve)
    5. Business Description (what they do)
    6. Business Unique Selling Point (what makes them special)
    
    Format your response as:
    Business Name: [extracted name]
    Industry: [extracted industry]
    Business Values: [extracted values]
    Business Target Audience: [extracted target audience]
    Business Description: [extracted description]
    Business Unique Selling Point: [extracted unique selling point]
    
    If any information is not clearly available, write "Not clearly specified on website" for that field.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        extracted_info = response.choices[0].message.content
        
        # Parse the response into a dictionary
        business_info = {}
        lines = extracted_info.split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                
                if key == 'business_name':
                    business_info['business_name'] = value
                elif key == 'industry':
                    business_info['business_industry'] = value
                elif key == 'business_values':
                    business_info['business_values'] = value
                elif key == 'business_target_audience':
                    business_info['business_target_audience'] = value
                elif key == 'business_description':
                    business_info['business_description'] = value
                elif key == 'business_unique_selling_point':
                    business_info['business_unique_selling_point'] = value
        
        return business_info
        
    except Exception as e:
        st.error(f"Error extracting business information: {str(e)}")
        return {}

# =============================================================================
# COMPETITOR ANALYSIS
# =============================================================================

def search_competitors(business_name, industry, tavily_client):
    """Search for competitors using Tavily"""
    try:
        # Search by industry
        industry_query = f"companies in {industry} industry"
        industry_results = tavily_client.search(industry_query, max_results=3)
        
        # Search by business name
        business_query = f"competitors of {business_name}"
        business_results = tavily_client.search(business_query, max_results=3)
        
        competitors = []
        
        # Process industry results
        for result in industry_results.get('results', []):
            competitors.append({
                'name': result.get('title', 'Unknown'),
                'url': result.get('url', ''),
                'description': result.get('content', '')[:300],
                'search_type': 'Industry Search'
            })
        
        # Process business-specific results
        for result in business_results.get('results', []):
            competitors.append({
                'name': result.get('title', 'Unknown'),
                'url': result.get('url', ''),
                'description': result.get('content', '')[:300],
                'search_type': 'Competitor Search'
            })
        
        return competitors
    except Exception as e:
        st.error(f"Error searching competitors: {str(e)}")
        return []

def generate_recommendations(business_data, competitor_data):
    """Generate business recommendations based on collected data"""
    prompt = f"""
    Based on the following business information and competitor analysis, provide strategic recommendations:
    
    Business Information:
    - Name: {business_data.get('business_name', 'N/A')}
    - Industry: {business_data.get('business_industry', 'N/A')}
    - Description: {business_data.get('business_description', 'N/A')}
    - Values: {business_data.get('business_values', 'N/A')}
    - Target Audience: {business_data.get('business_target_audience', 'N/A')}
    - Unique Selling Point: {business_data.get('business_unique_selling_point', 'N/A')}
    
    Competitor Information:
    {competitor_data[:1000] if competitor_data else 'No competitor data available'}
    
    Please provide recommendations in the following categories:
    
    ### Marketing Strategy
    - [3-4 specific marketing recommendations]
    
    ### Competitive Positioning
    - [3-4 recommendations for standing out from competitors]
    
    ### Business Development
    - [3-4 recommendations for growth and improvement]
    
    ### Brand Enhancement
    - [3-4 recommendations for strengthening brand identity]
    
    ### Digital Presence
    - [3-4 recommendations for online presence and digital marketing]
    
    Make each recommendation specific, actionable, and tailored to this business.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return "Unable to generate recommendations at this time."

# =============================================================================
# LOGO GENERATION
# =============================================================================

def generate_logo(business_info, recommendations=None):
    """Generate logo using DALL-E with enhanced prompt based on recommendations"""
    try:
        business_name = business_info.get('business_name', 'Company')
        industry = business_info.get('business_industry', 'business')
        values = business_info.get('business_values', '')
        description = business_info.get('business_description', '')
        unique_selling_point = business_info.get('business_unique_selling_point', '')
        
        # Base prompt
        prompt = f"""
        Create a modern, professional, and distinctive logo for "{business_name}" in the {industry} industry.
        
        Business Context:
        - Description: {description}
        - Values: {values}
        - Unique Selling Point: {unique_selling_point}
        """
        
        # Enhanced prompt with recommendations if available
        if recommendations:
            prompt += f"""
            
            Strategic Branding Insights:
            Based on comprehensive market analysis and competitor research, incorporate these strategic elements:
            
            {recommendations[:1000]}  # Limit to avoid token limits
            
            Logo Design Requirements:
            - Reflect the strategic positioning identified in the analysis
            - Differentiate from competitors while staying industry-appropriate
            - Embody the recommended brand personality and values
            - Support the suggested marketing strategy and target audience
            - Align with recommended brand enhancement strategies
            """
        
        prompt += f"""
        
        Technical Specifications:
        - Modern, clean, and professional aesthetic
        - Scalable vector-style design that works at any size
        - Memorable and distinctive while remaining timeless
        - Suitable for digital and print applications
        - Colors should be strategic and industry-appropriate
        - Must stand out in the {industry} market landscape
        - Should convey trust, professionalism, and the unique value proposition
        
        Style: Contemporary, sophisticated, and market-conscious design that reflects strategic brand positioning.
        """
        
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        return response.data[0].url
    except Exception as e:
        st.error(f"Error generating logo: {str(e)}")
        return None

# =============================================================================
# LEGACY FUNCTIONS (from original utils.py)
# =============================================================================

def get_tone_select_box():
    """Get tone selection for tagline generation"""
    return st.selectbox(
        "Please select the tone of your tagline", 
        [
            "Professional", "Funny", "Inspiring", "Motivational", 
            "Educational", "Engaging", "Entertaining", "Informative", 
            "Persuasive", "Creative", "Unique", "Catchy", "Memorable"
        ]
    )

def generate_tagline(business_info):
    """Generate tagline and branding recommendations"""
    prompt = f"""
    You are a creative branding strategist, specializing in helping small businesses establish a strong and memorable brand identity. When given information about a business's values, target audience, business unique selling point and industry, you generate branding ideas that include logo concepts, color palettes, tone of voice, a one line tagline, and marketing strategies. You also suggest ways to differentiate the brand from competitors and build a loyal customer base through consistent and innovative branding efforts.

    Business Name: {business_info.get("business_name", "")}
    Business Description: {business_info.get("business_description", "")}
    Business Industry: {business_info.get("business_industry", "")}
    Business Unique Selling Point: {business_info.get("business_unique_selling_point", "")}
    Business Target Audience: {business_info.get("business_target_audience", "")}
    Business Values: {business_info.get("business_values", "")}

    Be concise and to the point, and give me all the fields under headings using ### format.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating tagline: {str(e)}")
        return "Unable to generate tagline at this time."

def separating_answer(text):
    """Parse AI response into structured sections"""
    # Split by ### and filter empty sections
    sections = [section.strip() for section in text.split('###') if section.strip()]

    # Convert to dictionary with lists
    result = {}
    for section in sections:
        lines = section.split('\n', 1)
        title = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        
        # Convert bullet points to list
        if content.startswith('-'):
            # Split by lines starting with -
            bullet_items = re.findall(r'^- (.+)$', content, re.MULTILINE)
            result[title] = bullet_items
        else:
            result[title] = content

    return result

def display_recommendations(recommendations):
    """Display recommendations in a structured format"""
    st.title("💡 Tips and Recommendations")

    for category, items in recommendations.items():
        with st.container():
            st.subheader(category)
            
            if isinstance(items, list):
                for item in items:
                    st.markdown(f"• {item}")
            else:
                st.markdown(items)
            
            st.divider()

def format_business_summary(business_data):
    """Format business data for display"""
    summary = ""
    for key, value in business_data.items():
        if value and value != "Not clearly specified on website":
            display_key = key.replace('_', ' ').title()
            summary += f"**{display_key}:** {value}\n\n"
    return summary

def validate_url(url):
    """Basic URL validation"""
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

# =============================================================================
# SESSION STATE MANAGEMENT
# =============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if 'business_data' not in st.session_state:
        st.session_state.business_data = {}
    if 'competitor_data' not in st.session_state:
        st.session_state.competitor_data = []
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'logo_url' not in st.session_state:
        st.session_state.logo_url = None

# =============================================================================
# UI HELPER FUNCTIONS
# =============================================================================

def display_business_summary():
    """Display current business data if available"""
    if st.session_state.business_data:
        st.divider()
        st.subheader("📄 Current Business Information")
        
        for key, value in st.session_state.business_data.items():
            if value and value != "Not clearly specified on website":
                display_key = key.replace('_', ' ').title()
                st.write(f"**{display_key}:** {value}")

def display_competitor_results():
    """Display competitor analysis results"""
    if st.session_state.competitor_data:
        st.subheader("📊 Competitor Analysis Results")
        
        for i, competitor in enumerate(st.session_state.competitor_data, 1):
            with st.expander(f"🏢 {competitor['name']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Description:** {competitor['description']}")
                    if competitor['url']:
                        st.write(f"**Website:** [Visit Website]({competitor['url']})")
                
                with col2:
                    st.badge(competitor['search_type'])

def display_logo_generation_info():
    """Display logo generation mode information"""
    recommendations_available = bool(st.session_state.get('recommendations'))
    
    col1, col2 = st.columns(2)
    with col1:
        if recommendations_available:
            st.success("🎯 **Strategic Mode**: Using competitor analysis & recommendations")
        else:
            st.warning("⚡ **Basic Mode**: No competitor analysis available")
    
    with col2:
        if not recommendations_available:
            st.markdown("💡 *Complete competitor analysis for strategic logo design*")
        else:
            st.markdown("✨ *Logo will reflect market positioning & brand strategy*")
    
    # Explanation of logo generation modes
    with st.expander("📚 How Logo Generation Works", expanded=False):
        st.markdown("""
        **🎯 Strategic Mode** (With Competitor Analysis):
        - Uses comprehensive market research and recommendations from Tab 2
        - Creates logos that differentiate from competitors
        - Reflects strategic brand positioning and market insights
        - Incorporates target audience preferences and competitive landscape
        - Results in more strategic and market-conscious design
        
        **⚡ Basic Mode** (Without Competitor Analysis):
        - Uses only your business information from Tab 1
        - Creates professional logos based on industry and values
        - Good starting point, but less strategic
        
        💡 **Pro Tip**: Complete the competitor analysis in Tab 2 first for strategically-informed, market-aware logo design that stands out from competitors!
        """)

def display_generated_logo():
    """Display the generated logo if available"""
    if st.session_state.logo_url:
        st.divider()
        st.subheader("🖼️ Your Generated Logo")
        
        business_name = st.session_state.business_data.get('business_name', 'Your Business')
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(st.session_state.logo_url, caption=f"Logo for {business_name}", use_column_width=True)
        
        # Download option
        st.markdown("💡 **Tip:** Right-click on the logo image and select 'Save image as...' to download it.")
