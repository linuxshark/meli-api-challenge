import json
import os
import requests
from flask import Flask, jsonify, make_response, request

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
    # Check if vulns.json exists, if not, call get_vulns() to create it
    if not os.path.isfile('vulns.json'):
        get_vulns()

    with open('vulns.json') as f:
        data = json.load(f)

    # Dictionary to store vulnerability counts by severity
    counts = {
        'CRITICAL': 0,
        'HIGH': 0,
        'MEDIUM': 0,
        'LOW': 0
    }
    # List to store vulnerability info to display
    vulns_list = []
    # Loop through each vulnerability and count by severity
    for vulnerability in data['result']['CVE_Items']:
        try:
            base_severity = vulnerability['impact']['baseMetricV3']['cvssV3']['baseSeverity']
            counts[base_severity] += 1
            vuln_info = {
                'ID': vulnerability['cve']['CVE_data_meta']['ID'],
                'Description': vulnerability['cve']['description']['description_data'][0]['value'],
                'Severity': base_severity
            }
            vulns_list.append(vuln_info)
        except KeyError:
            pass

    # Create final summary dictionary to return
    summary = {
        'Counts by Severity': counts,
        'Vulnerability Info': vulns_list
    }

    # Save the summary to a file
    with open('to_fix.json', 'w') as f:
        json.dump(summary, f, indent=4)

    # Return a readable and summarized response
    response = make_response(jsonify(summary), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'inline; filename=summary.json'
    return response

@app.route('/fix_vulns', methods=['POST'])
def fix_vulns():
    try:
        req_data = request.get_json()

        if not req_data:
            return jsonify({'message': 'No data found in request'}), 400

        if 'vulnerability' not in req_data:
            return jsonify({'message': 'Vulnerability not found in request'}), 400

        vulnerability = req_data['vulnerability']

        if not vulnerability:
            return jsonify({'message': 'No vulnerability found in request'}), 400

        with open('to_fix.json', 'r') as file:
            data = json.load(file)

        for idx, value in enumerate(data['Vulnerability Info']):
            if value['ID'] == vulnerability:
                del data['Vulnerability Info'][idx]
                counts = {
                    'CRITICAL': 0,
                    'HIGH': 0,
                    'MEDIUM': 0,
                    'LOW': 0
                }
                for vuln in data['Vulnerability Info']:
                    counts[vuln['Severity']] += 1
                summary = {
                    'Counts by Severity': counts,
                    'Vulnerability Info': data['Vulnerability Info']
                }
                with open('to_fix.json', 'w') as f:
                    json.dump(summary, f, indent=4)
                return jsonify({'message': f'Vulnerability {vulnerability} removed successfully'}), 200

        return jsonify({'message': f'Vulnerability {vulnerability} not found in list'}), 404

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')