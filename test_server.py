import json, os, random, sys, time, urllib.error, urllib.request

url = os.environ.get("API_URL", "").rstrip("/")
if not url:
    print("Error: API_URL environment variable is not set.\nUsage: API_URL=https://<your-domain-or-ip> python3 test_server.py")
    sys.exit(1)

sentences = json.load(open("test_sentences.json"))

latencies = []
successful = 0
failed = 0

def percentile(sorted_data, pct):
    if not sorted_data:
        return 0.0
    k = (len(sorted_data) - 1) * (pct / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_data) - 1)
    return sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)

for s in sentences:
    req = urllib.request.Request(
        f"{url}/correct",
        data=json.dumps({"text": s}).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.perf_counter()
    try:
        res = json.loads(urllib.request.urlopen(req).read())
        elapsed = (time.perf_counter() - t0) * 1000
        latencies.append(elapsed)
        successful += 1
        print(f"{res['original']}\n=> {res['corrected']} ({elapsed:.1f}ms)\n")
    except urllib.error.HTTPError as e:
        elapsed = (time.perf_counter() - t0) * 1000
        latencies.append(elapsed)
        failed += 1
        body = json.loads(e.read())
        print(f"{s}\n=> HTTP {e.code}: {body.get('detail')} ({elapsed:.1f}ms)\n")
    except Exception as e:
        elapsed = (time.perf_counter() - t0) * 1000
        failed += 1
        print(f"{s}\n=> ERROR: {e} ({elapsed:.1f}ms)\n")

    time.sleep(random.uniform(0.5, 1.0))

sorted_lat = sorted(latencies)
avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

print("=" * 40)
print("AGGREGATE STATISTICS")
print("=" * 40)
print(f"Total Requests: {len(sentences)}")
print(f"Successful:     {successful}")
print(f"Failed:         {failed}")
print(f"Average:        {avg_latency:.2f}ms")
print(f"P90:            {percentile(sorted_lat, 90):.2f}ms")
print(f"P95:            {percentile(sorted_lat, 95):.2f}ms")
print(f"P99:            {percentile(sorted_lat, 99):.2f}ms")
