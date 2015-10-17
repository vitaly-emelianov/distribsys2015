import requests
import json
import argparse


TOKEN = "d11cb7099fde43408a35ee5badc0a98e"
URL = "https://cloud-api.yandex.net/v1/disk/resources"


def ls(path):
    URL = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {"path": path}
    headers = {"Authorization": "OAuth " + TOKEN}
    r = requests.get(URL, params=params, headers=headers)
    for el in r.json()['_embedded']['items']:
        print("{0}  {1}".format(el['name'], el['modified']))


def rm(path):
    URL = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {"path": path}
    headers = {"Authorization": "OAuth " + TOKEN}
    r = requests.delete(URL, params=params, headers=headers)


def cp(path, destination):
    URL = "https://cloud-api.yandex.net/v1/disk/resources/copy"
    params = {"from": path, "path": destination}
    headers = {"Authorization": "OAuth " + TOKEN}
    r = requests.post(URL, params=params, headers=headers)
    print(r.json())


def mv(path, destination):
    URL = "https://cloud-api.yandex.net/v1/disk/resources/move"
    params = {"from": path, "path": destination}
    headers = {"Authorization": "OAuth " + TOKEN}
    r = requests.post(URL, params=params, headers=headers)


if __name__ == '__main__':

    choices = {'ls': ls, 'rm': rm, 'mv': mv, 'cp': cp}
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=choices, help='which operation to do')
    parser.add_argument('path')
    parser.add_argument('destination')
    args = parser.parse_args()

    if args.operation == 'ls':
        ls(args.path)
    elif args.operation == 'rm':
        rm(args.path)
    elif args.operation == 'mv':
        mv(args.path, args.destination)
    elif args.operation == 'cp':
        cp(args.path, args.destination)
