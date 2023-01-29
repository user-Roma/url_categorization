import json
from pathlib import Path
import random
import requests
import timeit

from settings import TEST_URLS


test_data = {'count_200': 1}
requests_count = 5555

def generate_url_fortiguard(urls: list, attempt: int) -> str:
    random_url = random.choice(urls)
    print(f'Processing url №{attempt} - {random_url}....')
    protocol, domen = random_url.split('://')
    search_url = f'https://www.fortiguard.com/webfilter?q={protocol}%3A%2F%2F{domen}%2F'
    return search_url

def check_fortiguard(url: str) -> dict:
    data = {}
    response = requests.get(url)
    data['status_code'] = response.status_code
    if data['status_code'] != 200:
        raise Exception(f'We have been blocked! - {response.status_code}')
    test_data['count_200'] += 1
    # data['headers'] = response.headers
    # data['content'] = response.content.lower()
    data['elapsed'] = response.elapsed.total_seconds()
    # data['text'] = response.text
    # data['cookies'] = response.cookies
    return data



if __name__ == '__main__':
    test_data['start_time'] = timeit.default_timer()
    for attempt in range(1, requests_count):
        url = generate_url_fortiguard(TEST_URLS, attempt)
        test_data[attempt] = check_fortiguard(url)
    test_data['stop_time'] = timeit.default_timer()
    test_data['runtime'] = test_data['stop_time'] - test_data['start_time']
    with open(Path(__file__).with_name('test_forti_dump'), 'w') as file:
        json.dump(test_data, file)
    print(test_data['runtime'])
