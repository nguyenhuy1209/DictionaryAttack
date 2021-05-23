f = open("10-million-combos.txt", "r", encoding = "ISO-8859-1")
g = open("10-million-combos-fixed.txt", "w")

for line in f:
    if line.strip():
        g.write("\t".join(line.split()[1:]) + "\n")

f.close()
g.close()