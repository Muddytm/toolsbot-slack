import json

with open("data/weekly_stats.json") as f:
    data = json.loads(f.read())

with open("data/tls_cache.json") as f:
    cache = json.loads(f.read())

total = 0
for ip in data:
    total += data[ip]

print ("{} total\n".format(str(total)))

for set in cache:
    set_total = 0
    for ip in cache[set]:
        if ip in data:
            set_total += data[ip]

    print ("{} - {}".format(set, str(set_total)))
