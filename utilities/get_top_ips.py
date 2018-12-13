import os


for file in os.listdir("/mnt/TLS"):
    lines = open("/mnt/TLS/" + file).readlines()

data = {}

for line in lines:
    ip = line.split("ClientIP")[1].strip().split()[0]

    if ip not in data:
        data[ip] = 0
    else:
        data[ip] += 1

print (data)
