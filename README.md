## Vulnerability Management API

This is a simple Flask application that fetches the latest vulnerability data from NVD (National Vulnerability Database) and allows users to view, fix and track vulnerabilities. The application has the following API endpoints:

- `/health_check`: A simple health check endpoint that returns a message confirming that the application is up and running.
- `/get_vulns`: An endpoint that fetches the latest vulnerability data from NVD and saves it to a file named `vulns.json`. It also returns the data in JSON format.
- `/sum_vulns`: An endpoint that summarizes the vulnerability data from `vulns.json` by counting the number of vulnerabilities by severity, and saves the summary to a file named `to_fix.json`. It also returns the summary in JSON format.
- `/fix_vulns`: An endpoint that allows users to mark a vulnerability as fixed by specifying the vulnerability ID in the request body. It loads the summary data from `to_fix.json`, updates the status of the specified vulnerability to 'FIXED' and saves the updated summary back to `to_fix.json`.
- `/total_vulns`: An endpoint that summarizes the vulnerability data from `to_fix.json` by counting the number of vulnerabilities by severity, excluding those that have been fixed, and returns the summary in JSON format.

## SECURITY AND INFRASTRUCTURE IMPORTANT STUFF

**This is not a production code, i'm using json files just to simulate the real data and status persistance, a real security solution as this one, should contains a lot of considerations like:**

1.- Own Database to store the data obtained from the NVD endpoint.

2.- All the connection database credentials must be storaged inside a secret tools like GCP Secret Manager or Hashicorp Vault.

3.- The API must be running inside a Cloud Computing infrastructure, as a K8S, functions, Container as a Service or something else.

4.- All the infrastructure must be implemented with IaC (Terraform), and needs to be constantly scanned with BridgeCrew, Checkov, or something else.

5.- API usage must be authenticated using some API gateway like APIGee or Kong.

6.- Docker image should be hardenized, restrincting the non-root users access to only the /app directory and all tha package versions should be analized with a tool like Clair or Trivy, to find any vulnerability on them, and the Docker image layers as well.


## Installation

I am asuming that you have Docker installed in your local machine

1. Clone the repository: `git clone https://github.com/linuxshark/meli-api-challenge.git`
2. Change into the project directory: `cd meli-api-challenge`
3. Build the Docker image: `docker build -t python-api . --no-cache`
4. Run the Docker container on your local to start the API: `docker run -ti --rm -p 8080:5000 python-api` (I like to map my local 8080 port to 5000 inside the Docker container)
5. OPTIONAL - To make a better debug, you can enter inside the running container and take a look over the persistance emulation files: `docker exec -ti ID_OF_THE_RUNNING_CONTAINER /bin/bash`

## Usage

Once the application is running, you can use a tool like Postman (*or your web browser will be usefull as well*) to interact with the API endpoints. Here are some sample requests:

- `GET http://localhost:8080/health_check`: Returns a message confirming that the application is up and running.
- `GET http://localhost:8080/get_vulns`: Fetches the latest vulnerability data from NVD and saves it to a file named `vulns.json` (just to emulate the persistance). It also returns the data in JSON format.
- `GET http://localhost:8080/sum_vulns`: Summarizes the vulnerability data from `vulns.json` by counting the number of vulnerabilities by severity, and saves the summary to a file named `to_fix.json`. It also returns the summary in JSON format.
- `POST http://localhost:8080/fix_vulns` with body `{"ID": "CVE-2021-1234"}`: Marks the vulnerability with ID `CVE-2021-1234` as fixed. It loads the summary data from `to_fix.json`, updates the status of the specified vulnerability to 'FIXED' and saves the updated summary back to `to_fix.json`. Example: `curl -X POST -H "Content-Type: application/json" -d '{"ID": "CVE-2023-27398"}' http://localhost:8080/fix_vulns`
- `GET http://localhost:8080/total_vulns`: Summarizes the vulnerability data from `to_fix.json` by counting the number of vulnerabilities by severity, excluding those that have been fixed, and returns the summary in JSON format.

## Contribution

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-branch-name`
3. Make your changes and commit them: `git commit -m "my commit message"`
4. Push your changes to your forked repository: `git push origin my-branch-name`
5. Create a pull request.

## License

Just testing and learning process