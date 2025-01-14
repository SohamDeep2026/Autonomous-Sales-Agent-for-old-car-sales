from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv

# initializes flask servers
app = Flask(__name__)
CORS(app)

# model initialization
load_dotenv()  
API_KEY = os.getenv("GOOGLE_API_KEY")  

genai.configure(api_key=f"{API_KEY}")  
model = genai.GenerativeModel("gemini-1.5-flash")  

data = pd.read_csv("car_prices.csv")
data = data.iloc[:1000]
selected_columns = ["year", "make", "model", "trim", "body", "transmission", "state", "condition", "color",
                    "interior", "seller", "mmr"]
for i in selected_columns:
    data[i] = data[i].fillna("")

# print(data[selected_columns])

@app.route('/ss', methods=['GET'])
def respond():

        context = request.args.get('context')
        prompt = request.args.get('prompt')

        guideline = f"""You are a car salesman selling second-hand cars. 

        Cars you have access to: {data[selected_columns]}

        You must:
        -give options to the user
        -not say anything repeatedly
        -suggest options as soon as possible
        -finalize a deal with a price quickly.

        Chat history till now is {context}
        Last user input is {prompt}

        Generate response in text format only.
        
"""

        response = model.generate_content(guideline, generation_config={
            "temperature": 0
        }).text
        return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)