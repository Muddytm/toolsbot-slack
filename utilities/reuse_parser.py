import glob
import os

print ("Reading lines...")
file_list = glob.glob("/mnt/TLS/*.txt")
latest = max(file_list, key=os.path.getctime)
lines = open(latest).readlines()

data = {"sea": {"1.0": {"new": {}, "reuse": {}}, "1.1": {"new": {}, "reuse": {}}}, "dfw": {"1.0": {"new": {}, "reuse": {}}, "1.1": {"new": {}, "reuse": {}}}}

for line in lines:
    if "SSL_HANDSHAKE_SUCCESS" in line:
        tokens = line.split()
        loc = tokens[4].split("-")[0].lower()
        ip = tokens[17]
        tls = tokens[29]
        tls_num = tls.split("v")[1]
        session = tokens[38].lower()
        print ("{} {} {} {}".format(loc, ip, tls, session))

        if ip not in data[loc][tls_num][session]:
            data[loc][tls_num][session][ip] = 1
        else:
            data[loc][tls_num][session][ip] += 1

output = "IP, SEA/DFW, TLS, NEW/REUSE, COUNT"

for i in data["sea"]["1.0"]["new"]:
    output += ("{}, {}, {}, {}, {}\n".format(i, "sea", "1.0", "new", data["sea"]["1.0"]["new"][i]))

for i in data["sea"]["1.0"]["reuse"]:
    output += ("{}, {}, {}, {}, {}\n".format(i, "sea", "1.0", "reuse", data["sea"]["1.0"]["reuse"][i]))

for i in data["sea"]["1.1"]["new"]:
    output += ("{}, {}, {}, {}, {}\n".format(i, "sea", "1.1", "new", data["sea"]["1.1"]["new"][i]))

for i in data["sea"]["1.1"]["reuse"]:
    output += ("{}, {}, {}, {}, {}\n".format(i, "sea", "1.1", "reuse", data["sea"]["1.1"]["reuse"][i]))

# --------

for i in data["dfw"]["1.0"]["new"]:
    output += ("{}, {}, {}, {}, {}\n".format(i, "dfw", "1.0", "new", data["dfw"]["1.0"]["new"][i]))

for i in data["dfw"]["1.0"]["reuse"]:
    output += ("{}, {}, {}, {}, {}\n".format(i, "dfw", "1.0", "reuse", data["dfw"]["1.0"]["reuse"][i]))

for i in data["dfw"]["1.1"]["new"]:
    output += ("{}, {}, {}, {}, {}\n".format(i, "dfw", "1.1", "new", data["dfw"]["1.1"]["new"][i]))

for i in data["dfw"]["1.1"]["reuse"]:
    output += ("{}, {}, {}, {}, {}\n".format(i, "dfw", "1.1", "reuse", data["dfw"]["1.1"]["reuse"][i]))

with open("tls_info.csv", "w") as file:
    file.write(output)
