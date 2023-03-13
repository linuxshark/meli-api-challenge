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

@app.route('/sum_vulns', methods=['GET'])
def sum_vulns():
    # Read the vulnerability data from the file
    with open('vulns.json', 'r') as f:
        data = json.load(f)
    # Summarize the vulnerability data by severity
    summary = {
        'CRITICAL': [],
        'HIGH': [],
        'MEDIUM': [],
        'LOW': []
    }
    for vulnerability in data['result']['CVE_Items']:
        base_severity = vulnerability['impact']['baseMetricV3']['severity']
        id = vulnerability['cve']['CVE_data_meta']['ID']
        description = vulnerability['cve']['description']['description_data'][0]['value']
        summary[base_severity].append({
            'id': id,
            'description': description,
            'baseSeverity': base_severity
        })
    # Convert the summary to a JSON response
    return jsonify(summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0')