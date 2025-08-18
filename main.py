import requests
import pprint

def demo():
    url = 'http://5.63.153.31:5051/v1/account/fc5c9258-0e89-4d18-8f5d-aabbb4d5e05e'
    headers = {'accept': 'text/plain'}
    response = requests.put(url=url, headers=headers)
    print(response.status_code)
    try:
        pprint.pprint(response.json())
    except Exception:
        print(response.text)

if __name__ == "__main__":
    demo()