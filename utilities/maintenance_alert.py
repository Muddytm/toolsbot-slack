if os.path.exists("data/jobs.json"):
    with open("data/jobs.json") as f:
        jobs = json.load(f)
else:
    jobs = []

jobs.append("MAINTENANCE")

with open("data/jobs.json", "w") as f:
    json.dump(jobs, f)
