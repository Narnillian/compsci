import random 

ties = 0
wins = 0
loss = 0

rock = 0
paper = 0
scissors = 0

box_computer = []
box_user = []
box_result = []



user_name = input('What is your name? ')

while True:
	winner = ''
	
	random_choice = random.randint(0,2)

	if random_choice == 0:
		computer_choice = 'rock'
	elif random_choice == 1:
		computer_choice = 'paper'
	else:
		computer_choice = 'scissors'
	box_computer.append(computer_choice[0].capitalize())
	
	user_choice = ''
	while (user_choice != 'rock' and
		   user_choice != 'paper' and
		   user_choice != 'scissors'):
		user_choice = input('rock, paper or scissors? ')

	if user_choice == 'rock':
		rock +=1
	if user_choice == 'paper':
		paper += 1
	if user_choice == 'scissors':
		scissors += 1
	box_user.append(user_choice[0].capitalize())
	
	if computer_choice == user_choice:
		winner = 'Tie'
		ties += 1
		box_result.append('T')
	elif computer_choice == 'paper' and user_choice == 'rock' or \
			computer_choice == 'rock' and user_choice == 'scissors' or \
			computer_choice == 'scissors' and user_choice == 'paper':
		winner = 'Computer'
		loss +=1
		box_result.append('C')
	else:
		winner = user_name
		wins += 1
		box_result.append(user_name[0])
	
	if winner == 'Tie':
		print('We both chose', computer_choice + ', play again.')
		print()
		continue
	else:
		print(winner, 'won. The computer chose', computer_choice + '.')
		print()

	play_again = input('Play again? (Y/n) ')
	print()
	if play_again and play_again[0].lower() == 'n':
		break

print('Thank you for playing!')
wins_s = ''
loss_s = ''
ties_s = ''
if wins-1: wins_s = 's'
if loss-1: loss_s = 's'
if ties-1: ties_s = 's'
print(f'You won {wins} time{wins_s} ({round(wins/(wins+loss+ties), 2)}%)')
print(f'You lost {loss} time{loss_s} ({round(loss/(wins+loss+ties), 2)}%)')
print(f'You tied {ties} time{ties_s} ({round(ties/(wins+loss+ties), 2)}%)')
print()

rock_s = ''
paper_s = ''
scissors_s = ''
if rock-1: rock_s = 's'
if paper-1: paper_s = 's'
if scissors-1: scissors_s = 's'
print(f'You played rock {rock} time{rock_s} ({round(rock/(rock+paper+scissors), 2)}%)')
print(f'You played paper {paper} time{paper_s} ({round(paper/(rock+paper+scissors), 2)}%)')
print(f'You played scissors {scissors} time{scissors_s} ({round(scissors/(rock+paper+scissors), 2)}%)')
print()

print('Victor:           |', end='')
for i in box_result:
	print(f'{i} |', end='')
print()
print('Computer choice:  |', end='')
for i in box_computer:
	print(f'{i} |', end='')
print()
print('Your choice:      |', end='')
for i in box_user:
	print(f'{i} |', end='')
	