app description:
has 4 tabs:
tab1: business information
tab2: recommendations
tab3: logo generation
tab4: competitor analysis

tab1: business information
- business name
- business description
- business website
- business industry
information is saved to the session state and displayed in the other tabs

There are 2 options to import business information:
- import from website
- import manually

if import from website is selected, the user is asked to enter the website url
an llm call is used to extract the business information from the website, the llm call is with langchain-openai and the model is gpt-4o-mini

if import manually is selected, the user is asked to enter the business information manually

tab2: recommendations
- recommendations are generated based on the business information
- recommentations include: tone of voice, tagline, logo, color scheme, font'

recommendations are displayed in a list with the following columns:
- recommendation
- description
- action

action is a button that allows the user to add the recommendation to the business information

tab3: logo generation
- logo is generated based on the business recommendations, especially the tone of voice and tagline and logo color /scheme/font and logo style
- logo is displayed in a image
- logo is saved to the session state and displayed in the other tabs

tab4: competitor analysis:
competitors are searched for using the business information gathered in tab1
- competitor analysis is generated based on the business information
- competitor analysis is displayed in a list with the following columns:
- competitor name
- competitor website
- competitor industry