from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the pickled dataset
# with open('crime_data.pkl', 'rb') as file:
#     crime_data = pickle.load(file)

@app.route('/')
def home():
    return "Welcome to the Urban Safety API!"

# @app.route('/get_data', methods=['GET'])
# def get_data():
#     # Example: Return the first 5 rows of the dataset
#     return jsonify(crime_data.head().to_dict(orient='records'))

# @app.route('/city_data', methods=['GET'])
# def city_data():
#     # Get city from the query string
#     city = request.args.get('city', default=None, type=str)

#     if city:
#         city_data = crime_data[crime_data['City'].str.contains(city, case=False)]
#         if not city_data.empty:
#             return jsonify(city_data.to_dict(orient='records'))
#         else:
#             return jsonify({"message": "No data found for the specified city."}), 404
#     else:
#         return jsonify({"message": "City parameter is required."}), 400

# @app.route('/predict', methods=['GET'])
# def predict():
#     # Example route for a prediction (for now, just returns a filtered set)
#     city = request.args.get('city', default=None, type=str)
#     crime_type = request.args.get('crime_type', default=None, type=str)

#     if city and crime_type:
#         filtered_data = crime_data[(crime_data['City'].str.contains(city, case=False)) & 
#                                    (crime_data['Crime against Women'].notna())]
        
#         if filtered_data.empty:
#             return jsonify({"message": "No data found for the specified city and crime type."}), 404

#         # Simple logic to show filtered results for specific crime types
#         crime_column = 'Crime against Women' if crime_type.lower() == 'women' else 'Theft'
#         result = filtered_data[['City', 'Population', crime_column]]
        
#         return jsonify(result.to_dict(orient='records'))
#     else:
#         return jsonify({"message": "City and crime_type parameters are required."}), 400

if __name__ == '__main__':
    app.run(debug=True)
