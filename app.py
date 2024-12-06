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
      

        # Define mappings for district names to district codes and crime types
        district_names ={
    'Bagerhat': '0',
    'Bandarban': '1',
    'Barguna': '2',
    'Barisal': '3',
    'Bhola': '4',
    'Bogra': '5',
    'Brahmanbaria': '6',
    'Chandpur': '7',
    'Chittagong': '8',
    'Chuadanga': '9',
    'Comilla': '10',
    'Cox\'s Bazar': '11',
    'Dhaka': '12',
    'Dinajpur': '13',
    'Faridpur': '14',
    'Feni': '15',
    'Gaibandha': '16',
    'Gazipur': '17',
    'Gopalganj': '18',
    'Habiganj': '19',
    'Jamalpur': '20',
    'Jessore': '21',
    'Jhalokati': '22',
    'Jhenaidah': '23',
    'Joypurhat': '24',
    'Khagrachari': '25',
    'Khulna': '26',
    'Kishoreganj': '27',
    'Kurigram': '28',
    'Kushtia': '29',
    'Lakshmipur': '30',
    'Lalmonirhat': '31',
    'Madaripur': '32',
    'Magura': '33',
    'Manikganj': '34',
    'Meherpur': '35',
    'Moulvibazar': '36',
    'Munshiganj': '37',
    'Mymensingh': '38',
    'Naogaon': '39',
    'Narail': '40',
    'Narayanganj': '41',
    'Narsingdi': '42',
    'Natore': '43',
    'Netrokona': '44',
    'Nilphamari': '45',
    'Noakhali': '46',
    'Pabna': '47',
    'Panchagarh': '48',
    'Patuakhali': '49',
    'Pirojpur': '50',
    'Rajbari': '51',
    'Rajshahi': '52',
    'Rangamati': '53',
    'Rangpur': '54',
    'Satkhira': '55',
    'Shariatpur': '56',
    'Sherpur': '57',
    'Sirajganj': '58',
    'Sunamganj': '59',
    'Sylhet': '60',
    'Tangail': '61',
    'Thakurgaon': '62'
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

        # Get district and crime codes from input data
        district_name = data["district"]
        district_code = district_names[district_name]
        
        crime_name = data["Crime"]
        crime_code = crimes_names[crime_name]

        year = data["Year"]

        # Map the district name to district code
        if district_name not in district_names:
            return jsonify({"error": f"district '{district_name}' not found"}), 400

        # Get population for the district
        pop = population[district_code]

        # Predict the crime rate using the model
        crime_rate = crime_data.predict([[year, district_code, crime_code, pop]])[0]
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
            "district": district_name,
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
