import json

js = '{\"channel\": 26, \"state\": \"OUT\"}'

pinInfo = json.loads(js)

if "value" not in pinInfo:
    pinInfo["value"] = 10
else:
    print("value is not present")

print(pinInfo["channel"])
print(pinInfo["state"])
print( pinInfo["value"])

pinInfoString = json.dumps(pinInfo)
 
print(pinInfoString)