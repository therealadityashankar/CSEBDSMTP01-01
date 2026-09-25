import json, os, random, sys, time, urllib.error, urllib.request

url = os.environ.get("API_URL", "").rstrip("/")
if not url:
    print("Error: API_URL environment variable is not set.\nUsage: API_URL=https://<your-domain-or-ip> python3 test_server.py")
    sys.exit(1)

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
    time.sleep(random.uniform(0.5, 1.0))
