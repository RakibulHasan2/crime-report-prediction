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
    
    city_names = { '0': 'Rangpur', '1': 'Rajshahi', '2': 'Barisal', '3': 'Khulna', '4': 'Mymensingh', '5': 'Chittagong', '6': 'Sylhet', '7': 'Dhaka'}
    
    crimes_names = { '0': 'Crime Committed by Juveniles', '1': 'Crime against Children', '2': 'Crime against Senior Citizen', '3': 'Crime against Women', '4': 'Drug Trafficking', '5': 'Kidnapping', '6': 'Murder', '7': 'Rape', '8': 'Robbery', '9':'Theft'}
    
    population = { '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60, '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00, '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50, '18':45.80}
    
    city_code = request.form["City"] 
    crime_code = request.form['Crime'] 
    year = request.form['Year'] 
    pop = population[city_code] 

    # Here increasing / decreasing the population as per the year.
    # Assuming that the population growth rate is 1% per year.
    year_diff = int(year) - 2011;
    pop = pop + 0.01*year_diff*pop

    
    crime_rate = crime_data.predict ([[year, city_code, pop, crime_code]])[0] 
    
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
    
    cases = math.ceil(crime_rate * pop)
    
    return render_template('result.html', city_name=city_name, crime_type=crime_type, year=year, crime_status=crime_status, crime_rate=crime_rate, cases=cases, population=pop)


if __name__ == '__main__':
    app.run(debug=True)
