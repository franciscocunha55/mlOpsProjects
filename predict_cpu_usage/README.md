# Predict CPU Usage with Prometheus

This project demonstrates how to fetch system metrics using Prometheus, process the data with Python, and store the results in a CSV file for further analysis or machine learning purposes.

## Requirements

1. Prometheus:
   - Installed and running locally or on a server.
   - node_exporter configured to collect system metrics.


2. Python:
    - Python 3.9 or higher.


## Setup Instructions

1. Clone the repository:
   ```
   $ git clone https://github.com/franciscocunha55/mlOpsProjects.git
    ```
   
2. Install the required Python packages:
   ```
   $ python3 -m venv [venvName]
   $ source venv/bin/activate  
   $ pip3 install -r requirements.txt
   ```
   
3. Configure Prometheus:
   - Add the following job to the `prometheus.yml` file:
     ```
     - job_name: 'node_exporter'
       static_configs:
         - targets: ['localhost:9100']
     ```
   - Restart Prometheus to apply the changes.


4. Run the Script
    ```
    $ cd predict-cpu-usage
    $ python3 main.py
    ```