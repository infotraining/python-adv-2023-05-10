from queue import Queue
import requests
from threading import Thread
from datetime import date, timedelta
import time

def producer(url_q: Queue, content_q: Queue):
    while True:
        url = url_q.get()
        #print(f"Requested {url}")
        result = requests.get(url)
        if result.status_code != 404:
            content_q.put(result.text)
        url_q.task_done()


def consumer(content_q: Queue, result_q: Queue):
    def parse_content(content: str, currency_code: str = 'USD'):
        import json
        json_table = json.loads(content)
        value = [float(entry['mid']) for entry in json_table[0]["rates"] if entry['code'] == currency_code][0]
        date = json_table[0]['effectiveDate']

        return date, value

    while True:
        content = content_q.get()
        date, value = parse_content(content)
        #print(f"Date: {date} - {value} PLN")
        result_q.put((date, value))
        content_q.task_done()


if __name__ == "__main__":
    url = "http://api.nbp.pl/api/exchangerates/tables/a/{}?format=json"
    start_date = date(2023, 1, 1)
    end_date = date(2023, 3, 30)
    delta = end_date - start_date
    urls = [url.format(str(start_date + timedelta(days=i)))
            for i in range(delta.days + 1)]

    no_of_producers = 10
    no_of_consumers = 1

    start = time.perf_counter()

    url_q = Queue()
    content_q = Queue()
    result_q = Queue()

    producers = [Thread(target=producer, args=(url_q, content_q), daemon=True).start()
                 for _ in range(no_of_producers)]
    consumers = [Thread(target=consumer, args=(content_q, result_q), daemon=True).start()
                 for _ in range(no_of_consumers)]

    for url in urls:
        url_q.put(url)

    url_q.join()
    content_q.join()

    end = time.perf_counter()

    print("-"*40)
    print(f"Elapsed time: {end - start}s")
    print("-"*40)

    values = []
    while not result_q.empty():
        date, value = result_q.get()
        values.append(value)
        #print(f"Date: {date} - {value} PLN")
    
    avg = sum(values) / len(values)
    print(f"Avg price of USD: {avg}")