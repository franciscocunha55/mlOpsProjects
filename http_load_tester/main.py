import asyncio
import json
import time
from http.client import responses
from typing import Any

import httpx
import requests


async def fn():
    task = asyncio.create_task((fn2()))
    print("one")
    print("four")
    await asyncio.sleep(1)
    print("five")
    await asyncio.sleep(1)

async def fn2():
    print("two")
    await asyncio.sleep(1)
    print("three")


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
        #print(response)
        #print(response[0])
        if response[0] == 200:
             success += 1
    return success / len(tuples_responses) * 100

def check_average_latency(tuples_responses):
    total_latency = 0
    for response in tuples_responses:
        total_latency += response[1]
    return total_latency / len(tuples_responses)


if __name__ == '__main__':
    #request_url("http://httpbin.org/headers")
    #asyncio.run(main())
    # request_httpx("https://www.example.org/")
    # asyncio.run(async_request_httpx("https://www.example.org/"))
    start_time = time.time()
    tuples_responses = asyncio.run(async_run_multiple_requests("https://www.example.org", 5, 3))
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    print(f"Success Rate: {check_success_rate(tuples_responses):.2f} ")
    #print(f"Average Latency: {check_average_latency(tuples_responses)}")
