import csv

with open("person.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        for column in row:
            print("     " + column)

with open("person.csv", "a") as f:
    writer = csv.writer(f)
    row = [4, "Sara", "sara@example.com"]
    writer.writerow(row)

