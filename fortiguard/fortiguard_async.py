import asyncio
import json
from pathlib import Path
import random
import requests
import timeit

from settings import TEST_URLS


test_data = {'count_200': 1}
requests_count = {'count': 55}


# def generate_url_fortiguard(urls: list) -> str:
#     random_url = random.choice(urls)
#     print(f'Processing url №{requests_count["count"]} - {random_url}....')
#     protocol, domen = random_url.split('://')
#     search_url = f'https://www.fortiguard.com/webfilter?q={protocol}%3A%2F%2F{domen}%2F'
#     requests_count['count'] -= 1
#     return search_url


async def check_fortiguard(urls: str) -> dict:
    random_url = random.choice(urls)
    print(f'Processing url №{requests_count["count"]} - {random_url}....')
    protocol, domen = random_url.split('://')
    search_url = f'https://www.fortiguard.com/webfilter?q={protocol}%3A%2F%2F{domen}%2F'
    requests_count['count'] -= 1

    response = requests.get(search_url)

    data = {}

    data['status_code'] = response.status_code
    if data['status_code'] not in (200, 503):
        raise Exception(f'We have been blocked! - {response.status_code}')
    test_data['count_200'] += 1
    data['elapsed'] = response.elapsed.total_seconds()
    return data


async def main():
    test_data['start_time'] = timeit.default_timer()
    while requests_count['count'] != 0:
        test_data[requests_count['count']] = main_loop.create_task(check_fortiguard(TEST_URLS))
        test_data[requests_count['count']] = main_loop.create_task(check_fortiguard(TEST_URLS))

        # test_data[requests_count['count']] = asyncio.create_task(check_fortiguard(TEST_URLS))

    test_data['stop_time'] = timeit.default_timer()
    test_data['runtime'] = test_data['stop_time'] - test_data['start_time']

    print(test_data['runtime'])


if __name__ == '__main__':
    main_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(main_loop)
    try:
        asyncio.run(amain(loop=main_loop))
    except KeyboardInterrupt:
        pass

    with open(Path(__file__).with_name('test_forti_dump'), 'w') as file:
        json.dump(test_data, file)
