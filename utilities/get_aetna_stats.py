import json


with open("data/weekly_stats.json") as f:
    data = json.loads(f.read())

with open("data/tls_cache.json") as f:
    cache = json.loads(f.read())

total = 0
for ip in data:
    total += data[ip]

stats = "Aetna stats:\n"
aetna_total = 0

for ip in cache["Aetna"]:
    aetna_total += data[ip]
    stats += "{}: {}\n".format(ip, data[ip])

percentage = "%.2f" % float((aetna_total/total)*100.)

stats += "\n{} total".format(str(aetna_total))
stats += "\n{}% of all {} TLS 1.0/1.1 calls".format(percentage, str(total))

#print (stats)
