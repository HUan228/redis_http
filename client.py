import sys

import requests


def add(sent, weight=12):
    rsp = requests.post(
        url="http://localhost:8000/add",
        headers={
            "Content-type": "application/json",
        },
        json={
            "sent": sent,
            "weight": weight,
        }
    )
    print(rsp.content.decode('utf-8'))


def query(term):
    rsp = requests.post(
        url="http://localhost:8000/query",
        headers={
            "Content-type": "application/json",
        },
        json={
            "word": term,
        }
    )
    # print(rsp.content.decode('utf-8'))
    print(rsp.json())


if __name__ == '__main__':
    if sys.argv[1] == "add":
        add(sys.argv[2])
        exit(0)
    elif sys.argv[1] == "query":
        query(sys.argv[2])
        exit(0)
    else:
        exit(-1)
##
