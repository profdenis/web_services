numbers = [3, 4, 12, -2, 6, 7, 1]
print(numbers)
print(numbers[2])
print(numbers[0:2])
print(numbers[:2])
print(numbers[2:])
print(numbers[2:5])
print(numbers[2:5:2])
print(numbers[2::2])
print(numbers[::2])
print(numbers[::-1])
print(numbers[::-2])
print(numbers[3:4:-1])

# print(numbers[12])
print(numbers[-2])
# print(numbers[-12])

# new_list = []
# x = int(input("Enter an integer: "))
# while x > 0:
#     new_list.append(x)
#     x = int(input("Enter an integer: "))
# print(new_list)

new_list = []
answer = input("Enter an integer: ")
while answer != "exit":
    try:
        x = int(answer)
        new_list.append(x)
    except ValueError:
        print("not an integer, try again")
    answer = input("Enter an integer: ")
print(new_list)
