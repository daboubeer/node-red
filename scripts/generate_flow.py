#!/usr/bin/python3

import json

with open("./flows/flows.json", "r") as f:
    data = json.load(f)

    for obj in data:
      print("Object: ", obj["id"])

