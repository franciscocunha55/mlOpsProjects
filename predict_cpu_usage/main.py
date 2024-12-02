import csv
import os.path
from datetime import datetime, timezone
import requests
import json

prometheus_url = 'http://localhost:9090'
csv_file = 'metrics.csv'
queries = {
    'cpu_usage': 'sum by (instance) (rate(node_cpu_seconds_total{mode!="idle"}[1m]))',
    #'memory_usage': 'sum by (instance) (node_memory_MemTotal_bytes - node_memory_MemFree_bytes)',
}


def fetch_metric(query):
    response = requests.get(prometheus_url + '/api/v1/query', params={'query': query})
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=2))
    values = data['data']['result']  # Path here the necessary values are from the json response
    #print(values)
    return values


def iterate_metrics():
    metrics = []  #List to of dictionaries to store the results

    #iterate over a dictionary
    for metric_name, query in queries.items():
        values = fetch_metric(query)
        for metric in values:
            metric = {
                'instance': metric['metric'].get('instance', 'unknown'),
                # get value from instance key, if not found return unknown
                'timestamp': datetime.fromtimestamp(float(metric["value"][0]), timezone.utc).strftime(
                    '%Y-%m-%d %H:%M:%S'),  # convert timestamp from unix format
                'metric_name': metric_name,
                'value': float(metric['value'][1]),
            }
            metrics.append(metric)

    print(metrics)
    metrics_file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["instance", "timestamp", "metric_name", "value"])
        if not metrics_file_exists:
            writer.writeheader()
        writer.writerows(metrics)
    print("Metrics saved to", csv_file)



if __name__ == '__main__':
    iterate_metrics()
