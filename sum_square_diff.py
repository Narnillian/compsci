def sum_square_difference(limit):
	squares_sum = 1
	base_sum = 1
	sum_squared = 0
	for i in range(limit+1):
		#print(range(limit))
		print(i)
		squares_sum += i ** 2
		base_sum += i
	sum_squared = base_sum ** 2	
	return squares_sum - sum_squared


difference = sum_square_difference(100)
print()
print(difference)