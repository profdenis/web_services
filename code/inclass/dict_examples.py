import csv

person_dict = {
    "id": 1,
    "name": "Denis",
    "email": "denis@example.com"
}

print(person_dict)
print(person_dict["id"])
print(person_dict["name"])
print(person_dict["email"])
person_dict["email"] = "denis@aaa.com"
print(person_dict["email"])
print(person_dict)

# print(person_dict["abc"])
print(person_dict.get("abc"))
print(person_dict.get("id"))
print(person_dict.get("abc", 0))
print(person_dict.get("id", 0))

with open("person.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["id"] = int(row["id"])
        print(row)

