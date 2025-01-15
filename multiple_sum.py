counter = 0
sum = 0
while counter-1000:
	if counter % 3 == 0 or counter % 5 == 0:
		sum += counter
		#print(counter)
	counter += 1
print(sum)