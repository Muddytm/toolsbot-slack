import json

with open("data/tls_cache.json") as f:
    cache = json.load(f)

with open("data/weekly_stats.json") as f:
    data = json.load(f)

for org in cache:
    for ip in cache[org]:
        if ip in data:
            del data[ip]

print (data)

for ip in data:
    url = "https://api.ipdata.co/{}?api-key={}".format(ip,
                                                       "68f2e94139b493e155a2c94326e12a6c1cb36a6dd83db6ed0b27a9a9")
    try:
        response = urllib2.urlopen(url)
        ip_data = response.read()
        info = json.loads(ip_data)
    except Exception as e: #placeholder since the specified exception was apparently not defined...?
        #print (e)
        info = {}

    if info["organisation"] not in cache:
        cache[info["organisation"]] = []

    cache[info["organisation"]].append(ip)

print (cache)
