import streamlit as st

recommendations = {
 "Logo Concepts": [
   "**Design Elements**: A stylized coffee cup with steam forming the shape of friends chatting or laughing. ",
   "**Typography**: Playful, rounded sans-serif font to convey friendliness and approachability.",
   "**Iconography**: Incorporate elements like coffee beans or hearts to symbolize connection and warmth."
 ],
 "Color Palette": [
   "**Primary Colors**: Warm browns (coffee), soft cream (milk), and vibrant teal (friendship).",
   "**Accent Colors**: Light coral and sunny yellow to evoke a cheerful and inviting atmosphere."
 ],
 "Tone of Voice": [
   "**Friendly and Casual**: Use conversational language that feels relatable and warm.",
   "**Playful and Inviting**: Incorporate humor and light-heartedness in messaging to create a welcoming vibe."
 ],
 "One-Line Tagline": [
   "\"Brewed for Friends, Sipped with Joy!\""
 ],
 "Marketing Strategies": [
   "**Social Media Engagement**: Create fun challenges or contests encouraging customers to share their coffee moments with friends using a unique hashtag.",
   "**Loyalty Program**: Implement a \"Friends & Brews\" card where customers earn rewards for bringing friends or visiting in groups.",
   "**Community Events**: Host coffee-tasting nights or \"Friendship Fridays\" with discounts for groups to foster community and connection."
 ],
 "Differentiation from Competitors": [
   "**Focus on Experience**: Emphasize the social aspect of coffee drinking by creating cozy, inviting spaces designed for groups.",
   "**Unique Offerings**: Introduce themed coffee blends or seasonal drinks that celebrate friendship and togetherness.",
   "**Collaborations**: Partner with local artists or musicians for events that enhance the coffee experience and draw in crowds."
 ],
 "Building a Loyal Customer Base": [
   "**Consistent Branding**: Ensure all touchpoints (packaging, social media, in-store experience) reflect the fun and friendly vibe of the brand.",
   "**Customer Feedback Loop**: Regularly engage with customers for feedback on new products or events, making them feel valued and heard.",
   "**Community Involvement**: Participate in local events or sponsor community activities to strengthen ties and build brand loyalty."
 ]
}

def display_recommendations(recommendations):
    st.title("Tips and Recommendations")
    st.write(recommendations.items())

    for category, items in recommendations.items():
        with st.container():
            st.subheader(category)
            
            for item in items:
                st.markdown(f"• {item}")
            
            st.divider()


display_recommendations(recommendations)