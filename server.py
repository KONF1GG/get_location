from flask import Flask, request, jsonify
from Yandex_map_parser import YandexMapParser
import functions

app = Flask(__name__)

@app.route('/get_location', methods=['GET'])
def get_location():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400

    location_from_NOMI = functions.get_location(address)

    if not location_from_NOMI:
        parser = YandexMapParser()
        location = parser.get_location_from_Yandex(address)
        parser.close_browser()

        return jsonify(location)

    else:
        return jsonify(location_from_NOMI)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)