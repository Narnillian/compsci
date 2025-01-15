def swap(a, b):
	tmp = a
	a = b
	b = tmp
	return a,b

num1 = 1
num2 = 2
print("Before swap: ", num1, num2)
num1, num2 = swap(num1, num2)
print("After swap: ", num1, num2)

str1 = "Hello"
str2 = 2
print("Before swap: ", str1, str2)
str1, str2 = swap(str1, str2)
print("After swap: ", str1, str2)

num3 = 2019
print(num3 % 10)
print(num3 // 10)

print(5/0)