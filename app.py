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

@app.route('/predict', methods=['POST'])
def predict_result():
    try:
        # Get input JSON
        data = request.get_json(force=True)
      

        # Define mappings for city names to city codes and crime types
        city_names = {
            'Rangpur': '6', 'Rajshahi': '5', 'Barisal': '0', 'Khulna': '3',
            'Mymensingh': '4', 'Chittagong': '1', 'Sylhet': '7', 'Dhaka': '2'
        }

        crimes_names = {
        'Crime Committed by Juveniles': '0',
    'Crime against Children': '1',
    'Crime against Senior Citizen': '2',
    'Crime against Women': '3',
    'Drug Trafficking': '4',
    'Kidnapping': '5',
    'Murder': '6',
    'Rape': '7',
    'Robbery': '8',
    'Theft': '9'
        }

        population = {
            '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60, '6': 77.50, '7': 21.70
        }

        # Get city and crime codes from input data
        city_name = data["City"]
        city_code = city_names[city_name]
        
        crime_name = data["Crime"]
        crime_code = crimes_names[crime_name]

        year = data["Year"]

        # Map the city name to city code
        if city_name not in city_names:
            return jsonify({"error": f"City '{city_name}' not found"}), 400

        # Get population for the city
        pop = population[city_code]

        # Predict the crime rate using the model
        crime_rate = crime_data.predict([[year, city_code, crime_code, pop]])[0]
        print(crime_rate)

        # Determine the crime status based on the predicted crime rate
        if crime_rate <= 1:
            crime_status = "Very Low Crime Area"
        elif crime_rate <= 5:
            crime_status = "Low Crime Area"
        elif crime_rate <= 15:
            crime_status = "High Crime Area"
        else:
            crime_status = "Very High Crime Area"

        # Calculate the estimated number of crime cases
        cases = max(1, round(crime_rate * pop))
        print("cases", cases)

        # Return the result as JSON
        return jsonify({
            "City": city_name,
            "Crime_Type": crime_name,
            "Year": year,
            "Crime_Status": crime_status,
            "Predicted_Crime_Rate": crime_rate,
            "Estimated_Cases": cases,
            "Population_Used": pop
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
