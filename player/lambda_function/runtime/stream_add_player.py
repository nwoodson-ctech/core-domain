import base64
import json

def handler(event, context):
    print(event[0])

    for payload in event:
        result = {
            "statusCode": 200,
            "headers": {
                "content-type": "application/json"
            },
            "detail": json.loads(base64.b64decode(payload["data"]).decode("utf-8"))

        }

        print(json.dumps(result))

        return result