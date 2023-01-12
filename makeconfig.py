if input("Do you want to create a new config? (y/n) ") == "n":
    exit()

with open("configtemplate.json") as f:
    with open("config.json", "w") as g:
        for line in f.readlines():
            if line.count("{") or line.count("}"):
                g.write(line)
            else:
                one, _ = line.split(": ")
                two: str = '"' + input(line + " <= ") + '",\n'
                g.write(one + ": " + two)
