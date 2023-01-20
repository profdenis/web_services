new_list = []
with open("data.txt", "r") as f:
    for line in f:
        try:
            x = int(line)
            new_list.append(x)
        except ValueError:
            print(f"'{line[:-1]}' is not an integer")

print(new_list)

with open("data2.txt", "w") as f:
    for x in new_list:
        f.write(str(x) + "\n")
        # f.write("\n")

