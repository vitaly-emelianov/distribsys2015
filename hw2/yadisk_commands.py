import requests
import configparser


URL = "https://cloud-api.yandex.net/v1/disk/resources"

"Parsing configuration file with token."
config = configparser.ConfigParser()
config.read("yadisk.cfg")
token = config['USER']['token']
headers = {"Authorization": "OAuth " + token}


def ls(args):
    params = {"path": args.path}
    r = requests.get(URL, params=params, headers=headers)

    if r.status_code == 200:
        for el in r.json()['_embedded']['items']:
            print("{0}  {1}  {2}".format(el['type'], el['modified'], el['name']))
    else:
        print(r.json()['description'])


def rm(args):
    params = {"path": args.path}
    r = requests.delete(URL, params=params, headers=headers)

    if r.status_code not in {202, 204}:
        print(r.json()['description'])


def cp(args):
    params = {"from": args.path, "path": args.destination}
    r = requests.post(URL + "/copy", params=params, headers=headers)

    if r.status_code not in {201, 202}:
        print(r.json()['description'])


def mv(args):
    params = {"from": args.path, "path": args.destination}
    r = requests.post(URL + "/move", params=params, headers=headers)

    if r.status_code not in {201, 202}:
        print(r.json()['description'])


def upload(args):
    params = {"path": args.path}
    r = requests.get(URL + "/upload", params=params, headers=headers)

    if r.status_code == 200:
        link = r.json()['href']
        try:
            with open(args.local_path) as f:
                file_data = f.read()
                put_request = requests.put(
                    link,
                    data=file_data,
                    params={'file': args.local_path})
                if put_request.status_code != 201:
                    print("Cannot load your file now.")
        except FileNotFoundError:
            print("{0} not found.".format(args.local_path))
    else:
        print(r.json()['description'])


def download(args):
    params = {"path": args.path}
    r = requests.get(URL + "/download", params=params, headers=headers)

    if r.status_code == 200:
        link = r.json()['href']
        get_request = requests.get(link)
        if get_request.status_code == 200:
            try:
                with open(args.local_path, 'wb') as f:
                    for chunk in get_request.iter_content(1024):
                        f.write(chunk)
            except IsADirectoryError:
                print("{0} is a directory".format(args.local_path))

        else:
            print("Cannot download this file now.")
    else:
        print(r.json()['description'])
