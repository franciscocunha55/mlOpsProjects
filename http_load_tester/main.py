import asyncio
import time
import httpx

list_information = []
csv_file = 'information.csv'

async def async_request_httpx(url, request_id, client_id):
    print(f" Client {client_id + 1}, Request {request_id + 1}: Starting")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    print(f"Client {client_id + 1}, Request {request_id + 1}: Completed")

    print("----------------------")
    return response.status_code, response.elapsed.total_seconds()

async def async_run_multiple_requests(url, num_requests, clients):
    tasks = []
    for client_id in range(clients):
        for request_id in range(num_requests):
            tasks.append(async_request_httpx(url, request_id, client_id))
    responses = await asyncio.gather(*tasks)
    print("All requests completed")
    #print(responses)
    return responses

def check_success_rate(tuples_responses):
    success = 0
    for response in tuples_responses:
        if response[0] == 200:
             success += 1

    success_rate = success / len(tuples_responses) * 100
    list_information.append(success_rate)
    return success_rate

def check_average_latency(tuples_responses):
    total_latency = 0
    for response in tuples_responses:
        total_latency += response[1]
    average_latency = total_latency / len(tuples_responses)
    list_information.append(average_latency)
    return average_latency

def check_max_latency(tuples_responses):
    max_latency = 0
    for response in tuples_responses:
        if response[1] > max_latency:
            max_latency = response[1]
    list_information.append(max_latency)
    return max_latency

def check_min_latency(tuples_responses):
    min_latency = 99999
    for response in tuples_responses:
        if response[1] < min_latency:
            min_latency = response[1]
    list_information.append(min_latency)
    return min_latency


# 95th percentile latency is a statistical measure used to capture the experience of the majority of users while ignore extreme cases (outliers)
# 95% of the values in the list are less than or equal to this value
def calculate_percentile_95(tuples_response):
    sorted_latencies = sorted(tuples_response)
    index_95th = int(len(sorted_latencies) * 0.95) - 1   # -1: Adjusts the index for zero-based indexing.
    latency_95th = sorted_latencies[index_95th]
    list_information.append(latency_95th[1])
    return latency_95th[1]

# def store_info_csv(list_information):
#     information_dict = []
#

if __name__ == '__main__':
    start_time = time.time()
    tuples_responses = asyncio.run(async_run_multiple_requests("https://www.example.org", 5, 4))
    end_time = time.time()
    list_information.append(end_time-start_time)
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    print(f"Success Rate: {check_success_rate(tuples_responses):.2f} %")
    print(f"Average Latency: {check_average_latency(tuples_responses):.2f} seconds")
    print(f"Maximum latency: {check_max_latency(tuples_responses):.2f} seconds")
    print(f"Minimum latency: {check_min_latency(tuples_responses):.2f} seconds")
    print(f"95th Percentile latency: {calculate_percentile_95(tuples_responses):.2f} seconds")

    print(list_information)
