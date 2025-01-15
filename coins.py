#this isn't a full program because we were just practicing. however, the basic idea is there
sum = 287 #cents
combos = 0

dollars = 0
half_dollars = 0
quarters = 0
dimes = 0
nickels = 0
pennies = 0

#if True:
for dimes in range(0, (sum//10)+1):
	for nickels in range(0, ((sum//5)+1)-(dimes*10)):
		for pennies in range(0, (sum+1)-(nickels*5)-(dimes*10)):
			if dimes*10 + nickels*5 + pennies*1 == sum:
				combos += 1

print(combos)