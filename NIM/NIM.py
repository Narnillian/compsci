import random

sticks_remaining = 10
turn = 0
hat = []
chosen = []

def assemble_hat(sticks, hat, chosen):
	for i in range(len(hat), sticks):
		this_list = []
		if i < 2:
			for j in range(i+1):
				this_list.append(j+1)
		else: this_list = [1,2,3]
		hat.append(this_list)
		chosen.append(0)
	return hat, chosen

def cpu_turn(sticks_remaining, hat, chosen):
	choice = random.choice(hat[sticks_remaining-1])
	chosen[sticks_remaining-1] = choice
	return sticks_remaining - choice, chosen

def cpu_win(hat, chosen):
	for i in range(len(chosen)):
		if (chosen[i] != 0):
			hat[i].append(chosen[i])
	return(hat)

def player_turn(sticks_remaining):
	while True:
		choice = input("How many sticks would you like to choose? ")
		try:
			choice = int(choice)
			if choice > 0 and choice <= 3:
				break
		except:
			print("Please make sure your input is valid")
		print("Please enter either 1, 2, or 3")
	return sticks_remaining - choice

def random_turn(sticks_remaining):
	if sticks_remaining <= 3:
		return random.choice([0, 3])
	return random.choice([0, sticks_remaining])

def train_cpu(sticks_remaining, hat, chosen):
	for i in range(100000):
		sticks = sticks_remaining
		player = random.randint(0,1)
		while sticks:
			if(player):
				sticks = random_turn(sticks)
			else:
				sticks, chosen = cpu_turn(sticks, hat, chosen)
			player = abs(player-1)
		if(not player):
			hat = cpu_win(hat, chosen)
	return hat


#main:
while True:
	while True:
		sticks_remaining = input("How many sticks would you like to play with? ")
		if sticks_remaining == "":
			sticks_remaining = 10
			print("You will be playing with 10 sticks")
			break
		try:
			sticks_remaining = int(sticks_remaining)
			break
		except:
			print("Please enter a valid number.")
	hat, chosen = assemble_hat(sticks_remaining, hat, chosen)
	hat = train_cpu(sticks_remaining, hat, chosen)
	first_player = input("Would you like to go first? [y/N] ").lower()
	player = 0
	if first_player and [0] == "y": player = 1
	while(sticks_remaining):
		if(player):
			sticks_remaining = player_turn(sticks_remaining)
		else:
			previous_sticks = sticks_remaining
			sticks_remaining, chosen = cpu_turn(sticks_remaining, hat, chosen)
			print("The AI chose " + str(previous_sticks - sticks_remaining) + " stick", end = "")
			if previous_sticks - sticks_remaining -1:
				print("s.", end = "")
			print()
		print("There are " + str(sticks_remaining) + " sticks remaining.\n")
		player = abs(player-1)
	print("And the winner is...")
	if(player):
		print("You!")
	else:
		hat = cpu_win(hat, chosen)
		print("The Computer!")
	print()
	play_again = input("Would you like to play again? ").lower()
	if play_again and play_again[0] == "n": break
