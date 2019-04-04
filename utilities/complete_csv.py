import json


results = "IP, TLS 1.0/1.1 CNT, Total TLS CNT, TLS 1.0/1.1 CNT to CareWeb, Total CNT to Careweb\n"

with open("data/alldata/all_12_data.json") as f:
    all_12_data = json.load(f)

with open("data/alldata/all_10_11_data.json") as f:
    all_10_11_data = json.load(f)

with open("data/alldata/sea_12_data.json") as f:
    sea_12_data = json.load(f)

with open("data/alldata/sea_10_11_data.json") as f:
    sea_10_11_data = json.load(f)

for ip in all_12_data:
    results += "{}, ".format(ip)

    if ip in all_10_11_data:
        results += "{}, ".format(str(all_10_11_data[ip]))
        results += "{}, ".format(str(all_12_data[ip] + all_10_11_data[ip]))
        results += "{}, ".format(str(sea_10_11_data[ip]))
        results += "{}\n".format(str(sea_12_data[ip] + sea_10_11_data[ip]))
    else:
        results += "0, "
        results += "{}, ".format(str(all_12_data[ip]))
        results += "0, "
        results += "{}\n".format(str(sea_12_data[ip]))

for ip in all_10_11_data:
    if ip in all_12_data:
        continue
    else:
        results += "{}, ".format(ip)

        results += "{}, ".format(str(all_12_data[ip]))
        results += "{}, ".format(str(all_12_data[ip]))
        results += "{}\n".format(str(sea_12_data[ip]))
        results += "{}\n".format(str(sea_12_data[ip]))

with open("data/alldata/tls_report.csv", "w") as f:
    json.dump(results, f)
