import streamlit as st
import google.generativeai as genai
import io
import os
from dotenv import load_dotenv 

# Load environment variables
load_dotenv()

# Set up Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def get_rec(data):
    model = genai.GenerativeModel('gemini-2.0-flash')

    context = '''
    You are a business advisor assisting small and medium-scale business owners with product purchase forecasting in order to avoid overstocking. The owner will provide you with the past 3-6 months of sales data for their products, 
    including product name and quantity sold. Format it as a table.
    The owner will also provide the business's location (city, state/region, and/or country). 
    Fetch the upcoming holidays, festivals, wheather forecasts and any other things relevant to how sales of productt can be affected in that location for the next month.
    Analyze how these events might impact the demand for each product and based on that, provide a forecast for the demand of each product for the next month. 
    Recommend appropriate purchase quantities for each product, and explain your reasoning.

    Response should be 
    1. Data summary and Recomendation in a json format consititing of Product, the Historical months, Trend, Recommended quantity of the requested month, reasoning]
    2. Forecast reasoning
    Make your answer summarised and consice 

    The sales data and location information are provided below: \n
    '''

    data = data
    request = f'{context}{data}'
    response = model.generate_content(request)

    return response.text

# Streamlit UI
st.title("Kola Inventory LLM Recommender")
st.subheader("Input Location, Product and Historical sales for past 3-6 months to get a recommendation")

# User Inputs
location = st.text_input("Enter Location:", placeholder= 'Accra')
sample_text = '''Product1: month1 - 5, month2 - 10, month3 - 0 
Product2: month1 - 4, month2 - 7, month3 - 5 
'''
product_sales = st.text_area("Enter Product Historical Sales:", placeholder = sample_text)

# Recommend Logic
if st.button("Recommend"):
    if location and product_sales:
        data = f'{location}\n{product_sales}'
        result = get_rec(data)
        st.success(result)
    else:
        st.warning("Please enter both Location and Product Historical Sales!")