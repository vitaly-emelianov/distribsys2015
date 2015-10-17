import requests
import json
import argparse


TOKEN = "d11cb7099fde43408a35ee5badc0a98e"
URL = "https://cloud-api.yandex.net/v1/disk/resources"


def ls(path):
    params = {"path" : path}
    headers = {"Authorization" : "OAuth " + TOKEN}
    r = requests.get(URL, params=params, headers=headers)
    print(r.status_code, r.reason)
    print(r.json())

def rm():
    pass

def mv():
    pass

def cp():
    pass


if __name__ == '__main__':

    choices = {'ls': ls, 'rm': rm, 'mv': mv, 'cp': cp}
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=choices, help='which operation to do')
    args = parser.parse_args()

    if args.operation == 'ls':
        ls("/")
    elif args.operation == 'rm':
        pass
    elif args.operation == 'mv':
        pass
    elif args.operation == 'cp':
        pass
    else:
        print("Bad argument.")