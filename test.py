runtime = "30 min"

if "hr" in runtime:
    runtime_split = runtime.split("hr")
    if len(runtime_split[1]) == 0:
        hours = int(runtime_split[0].strip())
        print(hours * 60)
    else:
        hours = int(runtime_split[0].strip())
        minutes = int(runtime_split[1].replace("min", "").strip())
        print(hours * 60 + minutes)
else:
    print(int(runtime.split()[0]))
