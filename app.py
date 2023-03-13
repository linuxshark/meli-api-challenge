import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({'message': 'up and running'})

@app.route('/get_vulns', methods=['GET'])
def get_vulns():
    url = 'https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=20'
    response = requests.get(url)
    data = response.json()
    
    # Save the vulnerability data to a file
    with open('vulns.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')