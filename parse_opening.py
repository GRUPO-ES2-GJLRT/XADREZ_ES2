openings = {}
with open("opening.txt", 'r') as f:
    family = None
    rule = ""
    new_rule = False
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line[0] == '-':
            family = line[37:40]
            if rule:
                print family + ' ' + rule
                openings[rule[2:]] = family
                rule = ""
            continue
        if not family:
            continue
        if line[:3] == family:
            new_rule = True
            if rule:
                print family + ' ' + rule
                openings[rule[2:]] = family
                rule = ""
            continue
        if line[:2] == '1.' and new_rule:
            rule = line
            new_rule = False
            continue
        if not new_rule:
            rule += " " + line
    if rule:
        print family + ' ' + rule
        openings[rule[2:]] = family
        rule = ""

print openings
print len(openings)