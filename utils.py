import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from tavily import TavilyClient
import re

# Initialize API clients
def initialize_apis():
    """Initialize all API clients"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=st.secrets["OPENAI_API_KEY"],
        temperature=0.7
    )
    tavily_client = TavilyClient(api_key=st.secrets.get("TAVILY_API_KEY", ""))
    return llm, tavily_client

# =============================================================================
# SESSION STATE MANAGEMENT
# =============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if 'business_data' not in st.session_state:
        st.session_state.business_data = {
            'business_name': '',
            'business_description': '',
            'business_website': '',
            'business_industry': ''
        }
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'applied_recommendations' not in st.session_state:
        st.session_state.applied_recommendations = {
            'tone_of_voice': '',
            'tagline': '',
            'logo_style': '',
            'color_scheme': '',
            'font': ''
        }
    if 'logo_url' not in st.session_state:
        st.session_state.logo_url = None
    if 'competitors' not in st.session_state:
        st.session_state.competitors = []

# =============================================================================
# BUSINESS INFORMATION EXTRACTION
# =============================================================================

def scrape_website_content(url):
    """Scrape website content"""
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
        
        # Limit content
        content = clean_text[:8000]
        return content
    except Exception as e:
        st.error(f"Error scraping website: {str(e)}")
        return None

def extract_business_info_from_website(website_content, url, llm):
    """Extract business information from website using LangChain"""
    prompt = f"""
    Analyze the following website content and extract key business information.
    Website URL: {url}
    
    Website Content:
    {website_content}
    
    Please extract and provide ONLY the following information in this exact format:
    
    Business Name: [extracted name]
    Business Description: [brief description of what they do]
    Business Industry: [industry/sector]
    
    If any information is not clearly available, write "Not specified" for that field.
    Keep descriptions concise and factual.
    """
    
    try:
        message = HumanMessage(content=prompt)
        response = llm([message])
        extracted_info = response.content
        
        # Parse the response
        business_info = {
            'business_name': '',
            'business_description': '',
            'business_website': url,
            'business_industry': ''
        }
        
        lines = extracted_info.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if 'business name' in key:
                    business_info['business_name'] = value
                elif 'business description' in key:
                    business_info['business_description'] = value
                elif 'business industry' in key:
                    business_info['business_industry'] = value
        
        return business_info
        
    except Exception as e:
        st.error(f"Error extracting business information: {str(e)}")
        return None

# =============================================================================
# RECOMMENDATIONS GENERATION
# =============================================================================

def generate_recommendations(business_data, llm):
    """Generate branding recommendations based on business information"""
    prompt = f"""
    Based on the following business information, generate 5 specific branding recommendations:
    
    Business Name: {business_data.get('business_name', 'N/A')}
    Business Description: {business_data.get('business_description', 'N/A')}
    Business Industry: {business_data.get('business_industry', 'N/A')}
    Business Website: {business_data.get('business_website', 'N/A')}
    
    Provide exactly 5 recommendations in this format:
    
    1. Tone of Voice|[specific tone recommendation]|[brief explanation why this tone fits]
    2. Tagline|[catchy tagline]|[explanation of tagline strategy]
    3. Logo Style|[logo style recommendation]|[why this style works for the business]
    4. Color Scheme|[specific colors with hex codes]|[psychology behind color choices]
    5. Font|[specific font recommendation]|[why this font fits the brand]
    
    Each recommendation should be specific, actionable, and tailored to this business.
    """
    
    try:
        message = HumanMessage(content=prompt)
        response = llm([message])
        recommendations_text = response.content
        
        # Parse recommendations
        recommendations = []
        lines = recommendations_text.split('\n')
        
        for line in lines:
            if '|' in line and any(char.isdigit() for char in line[:3]):
                parts = line.split('|')
                if len(parts) >= 3:
                    # Remove number prefix
                    recommendation_type = parts[0].split('.', 1)[-1].strip()
                    recommendation = parts[1].strip()
                    description = parts[2].strip()
                    
                    recommendations.append({
                        'type': recommendation_type,
                        'recommendation': recommendation,
                        'description': description
                    })
        
        return recommendations
        
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []

def apply_recommendation(rec_type, recommendation):
    """Apply a recommendation to the business data"""
    type_mapping = {
        'Tone of Voice': 'tone_of_voice',
        'Tagline': 'tagline',
        'Logo Style': 'logo_style',
        'Color Scheme': 'color_scheme',
        'Font': 'font'
    }
    
    if rec_type in type_mapping:
        st.session_state.applied_recommendations[type_mapping[rec_type]] = recommendation
        st.success(f"Applied {rec_type}: {recommendation}")
    else:
        st.error("Unknown recommendation type")

# =============================================================================
# LOGO GENERATION
# =============================================================================

def generate_logo_with_dalle(business_data, applied_recommendations, llm):
    """Generate logo using DALL-E based on business info and recommendations"""
    try:
        # Create prompt based on business info and applied recommendations
        business_name = business_data.get('business_name', 'Company')
        industry = business_data.get('business_industry', 'business')
        description = business_data.get('business_description', '')
        
        tone = applied_recommendations.get('tone_of_voice', 'professional')
        tagline = applied_recommendations.get('tagline', '')
        logo_style = applied_recommendations.get('logo_style', 'modern')
        color_scheme = applied_recommendations.get('color_scheme', 'professional colors')
        font_style = applied_recommendations.get('font', 'clean')
        
        prompt = f"""
        Create a professional logo for "{business_name}" in the {industry} industry.
        
        Business Context:
        - Description: {description}
        - Tone of Voice: {tone}
        - Tagline: {tagline}
        
        Design Requirements:
        - Style: {logo_style}
        - Colors: {color_scheme}
        - Typography: {font_style}
        - Professional, scalable, and memorable
        - Suitable for digital and print use
        """
        
        # Note: This would typically use DALL-E API, but for demonstration
        # In a real implementation, you'd use:
        # from openai import OpenAI
        # client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        # response = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024")
        # return response.data[0].url
        
        # For demonstration, return a placeholder
        st.info("Logo generation would use DALL-E API here")
        return "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=Claude+Uplift+Logo"
        
    except Exception as e:
        st.error(f"Error generating logo: {str(e)}")
        return None

# =============================================================================
# COMPETITOR ANALYSIS
# =============================================================================

def search_competitors(business_data, tavily_client):
    """Search for competitors using business information"""
    try:
        business_name = business_data.get('business_name', '')
        industry = business_data.get('business_industry', '')
        
        # Search queries
        queries = [
            f"companies in {industry} industry",
            f"competitors of {business_name}",
            f"{industry} businesses similar to {business_name}"
        ]
        
        competitors = []
        
        for query in queries:
            try:
                results = tavily_client.search(query, max_results=3)
                
                for result in results.get('results', []):
                    title = result.get('title', '')
                    url = result.get('url', '')
                    content = result.get('content', '')
                    
                    # Extract potential business names from title and content
                    potential_names = extract_business_names(title, content)
                    
                    for name in potential_names:
                        if name.lower() != business_name.lower():  # Don't include self
                            competitors.append({
                                'name': name,
                                'website': url,
                                'industry': industry,
                                'description': content[:200] + '...' if len(content) > 200 else content
                            })
            except Exception as e:
                st.warning(f"Error in search query '{query}': {str(e)}")
                continue
        
        # Remove duplicates
        unique_competitors = []
        seen_names = set()
        
        for comp in competitors:
            if comp['name'].lower() not in seen_names:
                seen_names.add(comp['name'].lower())
                unique_competitors.append(comp)
        
        return unique_competitors[:10]  # Limit to top 10
        
    except Exception as e:
        st.error(f"Error searching competitors: {str(e)}")
        return []

def extract_business_names(title, content):
    """Extract potential business names from title and content"""
    names = []
    
    # Extract from title
    if title:
        # Remove common words and patterns
        title_clean = re.sub(r'\b(Inc|LLC|Corp|Company|Ltd|Limited)\b', '', title, flags=re.IGNORECASE)
        title_clean = re.sub(r'[^\w\s]', ' ', title_clean)
        
        # Split and take meaningful parts
        words = title_clean.split()
        if len(words) >= 1:
            # Take first 1-3 words as potential company name
            for i in range(1, min(4, len(words) + 1)):
                potential_name = ' '.join(words[:i]).strip()
                if len(potential_name) > 2 and potential_name.lower() not in ['the', 'and', 'or']:
                    names.append(potential_name)
    
    # Extract from content using patterns
    if content:
        # Look for patterns like "CompanyName is" or "CompanyName provides"
        patterns = [
            r'([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,2})\s+(?:is|provides|offers|specializes)',
            r'([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,2})\s+(?:Inc|LLC|Corp|Company|Ltd)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) > 2:
                    names.append(match.strip())
    
    return list(set(names))  # Remove duplicates

# =============================================================================
# UI HELPER FUNCTIONS
# =============================================================================

def display_business_summary():
    """Display current business information"""
    if any(st.session_state.business_data.values()):
        st.subheader("📄 Current Business Information")
        
        data = st.session_state.business_data
        if data['business_name']:
            st.write(f"**Business Name:** {data['business_name']}")
        if data['business_description']:
            st.write(f"**Description:** {data['business_description']}")
        if data['business_website']:
            st.write(f"**Website:** {data['business_website']}")
        if data['business_industry']:
            st.write(f"**Industry:** {data['business_industry']}")

def display_applied_recommendations():
    """Display currently applied recommendations"""
    applied = st.session_state.applied_recommendations
    if any(applied.values()):
        st.subheader("✅ Applied Recommendations")
        for key, value in applied.items():
            if value:
                display_key = key.replace('_', ' ').title()
                st.write(f"**{display_key}:** {value}")

def validate_url(url):
    """Basic URL validation"""
    import re
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None
