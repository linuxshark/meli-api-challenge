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
                'Severity': base_severity,
                'Fix': '',
                'Status': ''
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
    # Get the ID of the vulnerability to fix from the request body
    vuln_id = request.json['ID']
    # Load the summary data from the to_fix.json file
    with open('to_fix.json', 'r') as f:
        summary = json.load(f)
    # Find the vulnerability with the matching ID and update the Fix and Status fields
    for vuln in summary['Vulnerability Info']:
        if vuln['ID'] == vuln_id:
            vuln['Fix'] = 'DONE'
            vuln['Status'] = 'FIXED'
    # Save the updated summary data back to the to_fix.json file
    with open('to_fix.json', 'w') as f:
        json.dump(summary, f, indent=4)
    # Return a success response
    return jsonify({'message': 'Vulnerability fixed successfully'})

@app.route('/total_vulns', methods=['GET'])
def total_vulns():
    # Check if to_fix.json exists, if not, call sum_vulns() to create it
    if not os.path.isfile('to_fix.json'):
        sum_vulns()

    with open('to_fix.json') as f:
        data = json.load(f)

    # Dictionary to store vulnerability counts by severity
    counts = {
        'CRITICAL': 0,
        'HIGH': 0,
        'MEDIUM': 0,
        'LOW': 0
    }

    # Loop through each vulnerability and count by severity
    for vulnerability in data['Vulnerability Info']:
        if vulnerability['Status'] != 'FIXED':
            counts[vulnerability['Severity']] += 1

    # Create final summary dictionary to return
    summary = {
        'Counts by Severity (excluding FIXED)': counts,
        'Total Count (excluding FIXED)': sum(counts.values())
    }

    # Return a readable and summarized response
    response = make_response(jsonify(summary), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'inline; filename=total_vulns.json'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')