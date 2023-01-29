import json
import os
import random
import timeit

from bs4 import BeautifulSoup
import requests

from settings import TEST_URLS


test_data = {}
requests_count = 2


def generate_url_fortiguard(url: str, attempt: int) -> str:
    print(f'\nProcessing url №{attempt} - {url}....')
    protocol, domen = url.split('://')
    search_url = (
        'https://www.fortiguard.com/webfilter?'
        f'q={protocol}%3A%2F%2F{domen}%2F'
    )
    return search_url


def check_fortiguard(url_final: str, url: str) -> dict:
    data = {}
    response = requests.get(url_final)
    soup = BeautifulSoup(response.text, 'lxml')
    data['url'] = url
    data['status_code'] = response.status_code
    data['category'] = soup.find(class_='info_title').text
    data['elapsed'] = response.elapsed.total_seconds()

    print(
        f"[INFO] {data['url']} - "
        f"{data['category']} - "
        f"{data['elapsed']}"
    )

    return data


def main():
    test_data['start_time'] = timeit.default_timer()
    for attempt in range(1, requests_count):
        url_check = random.choice(TEST_URLS)
        url_final = generate_url_fortiguard(url_check, attempt)
        test_data[attempt] = check_fortiguard(url_final, url_check)
    test_data['stop_time'] = timeit.default_timer()
    test_data['runtime'] = test_data['stop_time'] - test_data['start_time']

    with open(
        os.path.join(
            f'{os.getcwd()}/datasheet',
            f'test_forti_dump_{test_data["runtime"]}'
        ),
        'w'
    ) as file:
        json.dump(test_data, file)

    return test_data['runtime']


if __name__ == '__main__':
    print(main())
