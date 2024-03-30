import os
import dotenv
from flask import Flask, jsonify
from feeder import common, mongoHandler, gnHandler, threatfoxHandler, feodoHandler

dotenv.load_dotenv()

GREYNOISE_API_KEY = os.getenv('GN_API_KEY')
MONGO_URI = os.getenv('MONGO_URI')

app = Flask(__name__)

@app.route('/<string:ip>/')
def add_ip(ip):
    if not common.validate_ip(ip):
        return jsonify({'error': 'Invalid IP address provided.'})

    gnHandler.process_ip(ip)
    threatfoxHandler.put_iocs_from_ip(ip)

    return mongoHandler.get_ip_from_greynoise(ip)


def main():
    app.run(host='0.0.0.0', port=8080, debug=False)


if __name__ == "__main__":
    main()
