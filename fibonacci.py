"""
Complications:
- variable limit to fibonacci list
- putting the list-making into functions so it's reusable
- stats about the lists
- repeat attempts without exiting the program
"""

def find_fib(limit=30):
	if limit < 3:
		print("Limit must be greater than 3!")
		return 1
	fibonacci = [1,1]
	for i in range(limit-2):
		fibonacci.append(fibonacci[i]+fibonacci[i+1])
	return fibonacci

def list_sums(list):
	for i in range(len(list)):
		sum = 0
		for j in str(list[i]):
			sum += int(j)
		list[i] = [list[i],sum]
	return list

limit = 30

while True:
	fibonacci = 0

	while not isinstance(fibonacci, list):
		fibonacci = find_fib(limit)
		continue
	print(fibonacci)
	print(len(fibonacci))
	
	print()
	
	fibonacci_sums = list_sums(fibonacci)
	print(fibonacci_sums)
	print(len(fibonacci))

	total = 0
	for i in range(len(fibonacci_sums)):
		total += fibonacci_sums[i][1]
	average = total/limit
	#i was planning on using a loop, but the editor suggested that this was a viable way
	#to do it. i tested it a number of times, and it works. i then spent a bunch of time 
	#trying to understand *how* it works. i finally figured it out, and it's very cool
	#if in the future you would like me to ignore or disable such recommendations, i will do so
	maximum = max(fibonacci_sums, key=lambda x: x[1])[1]
	print()
	print("The total of the sums is:  ", total)
	print("The average of the sums is:", average)
	print("The highest of the sums is:", maximum)

	print()

	play_again = input("Would you like to use a different limit? (y/N) ")
	if play_again.lower() in ["n", ""]:
		break
	limit = int(input("What should the limit be? "))
print("Thank you! Come back soon!")