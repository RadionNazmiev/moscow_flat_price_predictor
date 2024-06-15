from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import util


app = Flask(__name__)
CORS(app)


def start_server():
    print("Starting python flask server...")
    util.load_saved_artifacts()
    app.run(debug=True, host='0.0.0.0', port=5000)



@app.route('/', methods=['GET'])
def get_form_info():
    response = jsonify(util.get_form_info())
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/favicon.ico')
def favicon():
    return make_response('', 200)


@app.route('/predict_apartment_price', methods=['POST'])
def predict_apartment_price():

    apartment_type = request.form['apartment_type']
    metro_station = request.form['metro_station']
    minutes_to_metro = int(request.form['minutes_to_metro'])
    region = request.form['region']
    number_of_rooms = int(request.form['number_of_rooms'])
    area = float(request.form['area'])
    living_area = float(request.form['living_area'])
    kitchen_area = float(request.form['kitchen_area'])
    floor = int(request.form['floor'])
    number_of_floors = int(request.form['number_of_floors'])
    renovation_type = request.form['renovation_type']

    print(request.form)

    observation = [
        apartment_type,
        metro_station,
        minutes_to_metro,
        region,
        number_of_rooms,
        area,
        living_area,
        kitchen_area,
        floor,
        number_of_floors,
        renovation_type
    ]

    response = jsonify({
        'estimated_price': util.get_estimated_price(*observation)
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



if __name__ == '__main__':
    start_server()
