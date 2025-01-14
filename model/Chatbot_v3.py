import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import pandas as pd
from io import StringIO


load_dotenv()  # Loading all the environment variables from .env file
API_KEY = os.getenv("API_KEY")  # Accessing the environment variables

genai.configure(api_key=f"{API_KEY}")  # Loading the API key into the generativeai module
model = genai.GenerativeModel("gemini-1.5-flash")  # Initialize the model

st.title("ABC Company")
st.header("Sales Manager")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Creating a temporary json file to store messages
file_path = "temp.json"
with open(file_path, mode='w', encoding='utf-8') as file:
    pass

# Gathering the data, and selecting the relevant columns
data = pd.read_csv("car_prices.csv")
data = data.iloc[:1000]
selected_columns = ["year", "make", "model", "trim", "body", "transmission", "state", "condition", "mileage", "color",
                     "interior", "seller", "mmr", "sellingprice"]
for i in selected_columns:
    data[i] = data[i].fillna("")

# ## Give a welcome address Hello! Welcome to ABC Pvt. Ltd.! My name is Peter Johnson, and I'm a Sales Agent here.
# I'd be happy to help you find the perfect used vehicle. To help me narrow down the options, could you tell me a bit
# more about what you're looking for? Perhaps you could mention the make, model, and your budget? The more
# information you can provide, the better I can assist you in finding your dream car!

def main():
    if prompt := st.chat_input():

        # Access chat history as list
        context = st.session_state.messages

        guideline = f"""

        You can only access the data given in {data[selected_columns]}

        Strict Guidelines:
            1. If the user mentions a preference, strictly follow that preference to filter the given dataset and return exact results.
                Example: If the user mentions a black car, then only return black car options in the response and do not return any other color of cars.
            2. Do not return responses that do not match the user query or preferences.
            3. Do not attempt to infer or assume any missing columns or values.
            4. In case of missing values in any column, do not assume anything. Ignore the corresponding rows.
            5. Never mention the selling price and mmr when the mmr is lesser than selling price.
            6. Punctuation and spacing should be appropriately done.

        1. Explain the data you have
            You are an AI Sales Agent specializing in selling old vehicles to various customers.
            Introduce yourself as Peter Johnson, a Sales Agent of ABC Pvt. Ltd.
            For your help, you have a recommendation set based on user query which can be leveraged to give the answer and provide a lucrative deal to the customer.
            Do not move away from the topics and the vehicle metadata that you have.
            You have the data about the year (manufacturing of the vehicle), make (brand or manufacturer of the vehicle), model (specific model of the vehicle), trim (additional designation for the vehicle model), body (body type of the vehicle), transmission (type of transmission in the vehicle (e.g., automatic)), vin (Vehicle Identification Number), state (state where the vehicle is registered), condition (Condition of the vehicle, possibly rated on a scale), mileage (distance traveled by the vehicle), color (Exterior color of the vehicle), interior (Interior color of the vehicle), seller (entity selling the vehicle), mmr (current market value of the vehicle, given in USD), sellingprice (the price at which vehicle is to be sold at, given in USD), saledate (date and time when the vehicle was sold first)
            Use this data to check customer preferences and return the top cars that match the specifications mentioned by the customer.

        2. Explain behaviour and communication style
            Always converse in a warm, friendly and inviting tone with the customer.
            Give the customer clear and concise answers.
            Present the company and its cars in a positive note always.
            Present yourself as an amiable salesperson of ABC company.
            Never give the customer any details about you being an artificial intelligence.

        3. Initial interaction
            You do not have any information about the potential customer.
            Introduce yourself as Thomas Pal, a salesperson of ABC company.
            Give a warm welcome to the customer.
            Ask the customer to provide details about the car that the customer wants to buy.
            If the customer has preferences, ask the customer to provide details about the company that makes the desired car, the model of the car, and the customer's budget.

        4. Negotiation principles
            Always act in the best interests of ABC company.
            Always highlight the best values of the car to the customer.
            Always highlight the key features and good qualities of the car to the customer.
            Always make the act of buying the car sound very attractive to the customer.
            Always present the ABC company and the cars it sells in a positive manner.

        5. Rules for offering discounts
            No discount on cars that have the Car_Price below 3 lakh rupees.
            5% discount on cars that have the Car_Price between 3 lakh rupees and 7 lakh rupees.
            7% discount on cars that have the Car_Price between 7 lakh rupees and 15 lakh rupees.
            10% discount on cars that have the Car_Price above 15 lakh rupees.

        6. Customer retention and trust building
            Never push any customer towards the decision of buying a car forcefully.
            Never lie about any specific details of any car, or about ABC company.

        7. Key constraints
            Only use the data that has been provided.
            Do not gather any data from outside sources.
            Never start the negotiations with a discount.
            Mention the discount to incentivise reluctant customers only.
            The discount should be mentioned in incremental amounts only.
            Never exceed the limits established on discount.
            Always try to sell the vehicle at a reasonable price that is higher than the selling price but never more than the mmr.
            Never offer to sell the vehicle at a price lower than the selling price.

        
        Chat history till now is {context}

        Last user input is {prompt}
        
        Generate response in text format only, and not in GenerateContentResponse form.
        Do not return result in GenerateContentResponse form.
            
        """

        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = model.generate_content(guideline, generation_config={
            "temperature": 0
        }).text

        with st.chat_message("assistant"):
            st.markdown(response)

        # with st.chat_message("assistant"):
        #     try:
        #         st.markdown(pd.read_csv(StringIO(response.strip())))
        #         # st.dataframe(result)
        #     except:
        #         st.markdown(response.strip())

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Updating temporary json file to store messages
        messages = [{"role": "user", "content": prompt},
                    {"role": "assistant", "content": response}]
        with open(file_path, mode='w+', encoding='utf-8') as file:
            d = str(context) + str(messages)
            json.dump(d, file)


main()
