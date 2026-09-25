import json, urllib.error, urllib.request

url = "http://localhost:8000"
sentences = json.load(open("test_sentences.json"))

for s in sentences:
    req = urllib.request.Request(
        f"{url}/correct",
        data=json.dumps({"text": s}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        res = json.loads(urllib.request.urlopen(req).read())
        print(f"{res['original']}\n=> {res['corrected']}\n")
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        print(f"{s}\n=> HTTP {e.code}: {body.get('detail')}\n")
