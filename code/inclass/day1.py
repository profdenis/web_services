print("Hello")
print('Hello\nWorld!')
msg = """Hello
World!
"""
print(msg)
msg = '<div class="something">asdasdas</div>'
print(msg)
msg = "<div class=\"something\">asdasdas</div>"
print(msg)
name = 'Denis'
msg = f'Name = {name}'
print(msg)
# name = 5
x = 5
msg = f'x = {x}'
# y = int(msg)
y = int("25")
print(y)

if y > 10:
    print('bigger than 10')
elif y < 20:
    print('less than 20')
else:
    print('not bigger than 10')

print('end')

x: int = 0
while x < 5:
    x += 1
    print(x)

for i in range(5):
    print(i)

numbers = [4, 5, 1, 2, 53, 12]
for i in range(1, len(numbers)):
    print(f'numbers[{i}] = {numbers[i]}')

for i in range(1, len(numbers), 2):
    print(f'numbers[{i}] = {numbers[i]}')

print('third loop')
for i in range(len(numbers) - 1, -1, -1):
    print(f'numbers[{i}] = {numbers[i]}')

print('4th loop')
for x in numbers:
    print(x)

print('5th loop')
for x in reversed(numbers):
    print(x)


def f(number: int) -> int:
    return number * number


print(f(6))
print(f('abcd'))
