from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the pickled dataset
with open('model.pkl', 'rb') as file:
    crime_data = pickle.load(file)

@app.route('/')
def home():
    return "Welcome to the Urban Safety API!"

@app.route ('/predict', methods =['POST']) 
def predict_result (): 
    city_names = { '6': 'Rangpur', '5': 'Rajshahi', '0': 'Barisal', '3': 'Khulna', '4': 'Mymensingh', '1': 'Chittagong', '7': 'Sylhet', '2': 'Dhaka'}
    
    crimes_names = { '0': 'Crime Committed by Juveniles', '1': 'Crime against Children', '2': 'Crime against Senior Citizen', '3': 'Crime against Women', '4': 'Drug Trafficking', '5': 'Kidnapping', '6': 'Murder', '7': 'Rape', '8': 'Robbery', '9':'Theft'}
    
    population = { '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60, '6': 77.50, '7': 21.70 }

    data = request.get_json(force=True)
    city_code = data["City"] 
    crime_code = data['Crime'] 
    year = data['Year'] 
    pop = population[city_code]

    crime_rate = crime_data.predict ([[year, city_code, crime_code,pop]])[0] 
    
    city_name = city_names[city_code] 
    
    crime_type =  crimes_names[crime_code] 
    
    if crime_rate <= 1:
        crime_status = "Very Low Crime Area" 
    elif crime_rate <= 5:
        crime_status = "Low Crime Area"
    elif crime_rate <= 15:
        crime_status = "High Crime Area"
    else:
        crime_status = "Very High Crime Area" 
    
  
  return jsonify({
            "City": city_name,
            "Crime_Type": crime_type,
            "Year": year,
            "Crime_Status": crime_status,
            "Predicted_Crime_Rate": crime_rate,
            "Estimated_Cases": cases,
            "Population_Used": pop
        })



if __name__ == '__main__':
    app.run(debug=True)
