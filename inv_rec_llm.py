import streamlit as st
import pandas as pd
import google.generativeai as genai
import io
import os
from dotenv import load_dotenv 



# Load environment variables
load_dotenv()

# Set up Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def get_rec(data, product, month):
    model = genai.GenerativeModel('gemini-2.0-flash')

    context = f'''
        Act as an MSME owner assistant for local small businesses in ghana providing succinct business growth recommendations (stocking, pricing, promotions, etc.) based on provided demand forecast data for {product} product. For the next 3 months from {month}, analyze the 'seasonal_multiplier' to suggest inventory actions (increase/decrease stock and by what percentage relative to average - where 1 is average). Format your output as follows:

        "Hi! [Product Emoji] Your [Month Range] [Product] sales plan is ready:
        \n•\t[Month Abbreviation] – [Demand Trend Emoji] [Brief description of stock action (increase/decrease and percentage)] above/below normal. [1-2 sentence reason based on holidays, seasonality, weather, events]. *Action:* [1 actionable recommendation for stocking/promotion/pricing].
        \n•\t[Month Abbreviation] – [Demand Trend Emoji] [Brief description of stock action (increase/decrease and percentage)] above/below normal. [1-2 sentence reason based on holidays, seasonality, weather, events]. *Action:* [1 actionable recommendation for stocking/promotion/pricing].
        \n•\t[Month Abbreviation] – [Demand Trend Emoji] [Brief description of stock action (increase/decrease and percentage)] above/below normal. [1-2 sentence reason based on holidays, seasonality, weather, events]. *Action:* [1 actionable recommendation for stocking/promotion/pricing].

        [Concluding sentence with a positive outlook and call to action emoji]."

        Ensure the recommendations are specific to the provided data and the 'seasonal_multiplier'. Explore if previous or following month's holidays, seasonality, etc may affect current month

        Use plain and basic english for local business owners. The welcome note can be slightly adjusted not to sound too robotic.

        The forecast data are provided below: \n
    '''

    # context = f'''
    #             You are an MSME owner assistant to recommend actions for business growth onstocking, pricing, promotions, etc.
    #             Given this table containing {product} demand forecast for a region using demand and seasonal multipler as a proxy, 
    #             suggest inventory actions for a business owner for the next 3 months. Use the  seasonal multiplier to determine 
    #             stock change where 1 is the percentage average stock level, meaning 1.17 means an increase by 17% and vice versa. 
    #             recommend actions for the next 3 months from {month}. Make the recommendation succinct to be sent via a whatsapp text. 
    #             Give possible reasons for the raise or dip based on seasonality/ holidays, weather etc all provided in the forecast data. Add a Concluding sentence with 
    #             a positive outlook and call to action emoji

    #         '''

    # context = f'''
    #             You are an assistant helping MSME owners make smart inventory, pricing, and promotion decisions. You are given forecast data for the next 3 months from {month}, including product category for {product}, seasonal multiplier, holidays, weather, school resumption, and tourism.

    #             Use the seasonal multiplier to guide inventory strategy:
    #                 •	1.00 = average demand
    #                 •   >1.00 = stock should increase proportionally (e.g. 1.40 means stock 40% above average)
    #                 •	<1.00 = stock should decrease proportionally

    #             Based on this, write a short, friendly WhatsApp message advising the MSME owner on:
    #                 •	Recommended stock adjustment per month
    #                 •	Key reasons (e.g. holidays, weather, school, tourism)
    #                 •	Suggested actions (e.g. promotions, bundles, discount types)

    #             Make it clear, actionable, and no longer than 120 words. Use bullet points and emojis when helpful.

    #             Input data: \n                
    #             '''

    prod_map = {'rice': 1006, 'oil':1516,'milk':402, 'skincare':3304}

    data = data[(data['prod_code']==prod_map[product.lower()]) & (data['region']=='Central')]
    data = data.to_string()
    print(data)

    request = f'{context}{data}'
    response = model.generate_content(request)

    return response.text


months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

products_cat = ['rice','oil','milk','skincare']


# Streamlit UI
st.title("Kola Inventory Recommender")
st.subheader("Select product category and month to see recommendations for the next 3 months")

# User Inputs
product = st.selectbox("Select a product",products_cat)
month = st.selectbox("Select a month to see suggetions for next 3 months", months)

prod_recs = pd.read_csv('pred_all.csv')


# Recommend Logic
if st.button("Recommend"):
    if product and month:
        res = get_rec(prod_recs, product, month)
        # print(res)
        st.success(res)
    else:
        st.warning("Please enter both Product and Month!")
