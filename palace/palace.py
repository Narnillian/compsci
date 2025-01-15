"""The Palace card game, of which I have played many a round at summer camp and the like.
I had not known of its "real" name, as displayed proudly in the Wikipedia URL:

https://en.wikipedia.org/wiki/Shithead_(card_game)

The rules are inconsistent within the article itself, so here are the special cards I use:
2: Reset pile
3: Mirror previous
7: Play under
10: Bomb (and you get another turn)

Also, I know that players start with 7+3+3, not 9+3+3
"""
from cardgamebase import *

def print_hand(hand: Deck, upcards: Deck, downcards: Deck, min: int, max: int) -> int:
    r"""Printer for hand &c of Palace card game.

    - `hand`: The player's hand.
    - `upcards`: The player's face-up table cards
    - `downcards`: The player's face-down table cards
    - `min`: The minimum legal value that can be played (to filter the displayed cards)
    - `max`: The maximum legal value that can be played (to filter the displayed cards)

    Returns the number of playable cards from `hand`, for utility. Not very clean code.
    """
    valid_cards = 0
    for card in sorted(hand,key=lambda card: card.game_value): #sort by game_value
        if (card.game_value < min or card.game_value > max) and card.game_value not in [2,3,7,10]: continue
        print(f"[{card.pretty_value(short=True)}]",end="")
        valid_cards += 1
    if valid_cards == 0: print([],end="") #to at least print one. if this is true, it will skip the next block also
    print("\n  ",end="")

    #upcards can only be 3 or 0 because they all get picked up at once and never returned
    if len(upcards) == 0:
        for card in range(3):
            print("[_]",end="")
    else:
        for card in upcards:
            print(f"[{card.pretty_value(short=True)}]",end="")
    print("\n  ",end="")
    
    #downcards can be 3, 2, or 1
    for card in downcards:
        print("[x]",end="")
    for nothing in range(3-len(downcards)):
        print("[_]",end="")
    print()
    return valid_cards

def do_turn(hand: Deck, upcards: Deck, downcards: Deck) -> None:
    r"""Do one turn (usually) of the Palace card game.

    - `hand`: The player's hand.
    - `upcards`: The player's face-up table cards
    - `downcards`: The player's face-down table cards

    No return.
    """
    topcard = play_pile.top()
    if topcard is None:
        topcard = Card(0,"zero") #debating between this vs None ([0] vs [X] in display)
    elif topcard.game_value == 2:
        topcard = Card(0,"zero",2)
    elif topcard.game_value == 3:
        topcard = Card(0,"zero")
        if len(play_pile) > 1:
            topcard = play_pile.cards[-2]
    if topcard.game_value == 7:
        min = 1
        max = 7
    else:
        min = topcard.game_value + 1
        max = 15
    valid_cards = print_hand(hand,upcards,downcards,min,max)
    require_pickup = not valid_cards #bool
    print(f"\033[2A\033[35C[{'X' if topcard == None else topcard.pretty_value(short=True)}]") #\033[1B\033[3D[O]
    print(f"\033[4B\033[0G")
    if len(hand) == 0: #this can only occur if hand and upcards are used up
        input("Play one of your flipped cards! ")
        card = downcards.pop()
        require_pickup = require_pickup or (card.game_value < min or card.game_value > max)
        if require_pickup: print("Oh no, that card's not good!")
        play_pile.add_card(card)
    elif valid_cards:
        card = 0
        count = 1
        while True:
            try:
                card = int(input("Which card would you like to play? "))
            except:
                print("Please input a number")
                continue
            if card not in range(2, 15): #if this card does not exist
                print("That's not a real card...           (aces high)")
                continue
            count_in_hand = hand.count_value_matches(card)
            match count_in_hand:
                case 0:         #if we are not holding this card
                    print("You do not have this card!")
                    continue
                case 1:        #if we are holding 1 of this card (no choice)
                    pass
                case _:         #if we are holding >1 of this card (choose count)
                    while True:
                        try:
                            count = int(input(f"How many would you like to play? ({count_in_hand}) "))
                        except:
                            print("Please input a number")
                            continue
                        if count < 1:
                            print("Well that's just impossible!")
                            continue
                        if count > count_in_hand:
                            print("You don't have that many of this card...")
                            continue
                        break
            if (card < min or card > max) and card not in [2,3,7,10]:
                print("That's against the rules!")
                continue
            else: break
        removed_cards = hand.remove_cards(count, card)
        play_pile.add_cards(removed_cards)
        #replace played cards:
        hand_size = len(hand)
        #yes, the only possible way for a to happen is for b to be true, but we can be safe:
        if hand_size == 0 and len(draw_pile) == 0:
            if len(upcards): #it's not been emptied yet
                hand = upcards
                print("You get to pick up your cards!")
        if hand_size < numof_playerhand:
            picked_up = draw_pile.remove_cards(numof_playerhand-hand_size)
            hand.add_cards(picked_up)
            print("You picked up: ",end="")
            for card in sorted(picked_up,key=lambda card: card.game_value): #sort by game_value
                print(f"[{card.pretty_value(short=True)}]",end="")
    if require_pickup:
        hand.add_cards(play_pile.remove_cards(len(play_pile)))
        print("You have to pick up the pile...")
    if play_pile.top() == Card(10,"any"):
        discard_pile.add_cards(play_pile.remove_cards(len(play_pile)))
        print("It's a bomb!")
        do_turn(hand,upcards,downcards) #if you bomb, you get to have another turn
    if hand.sum() + upcards.sum() + downcards.sum() == 0:
        print("You win!")
        exit()
    print("\n")




numof_playerpiles = 3
numof_playerhand = 7
    
draw_pile: Deck = Deck.Full_Deck(
        rules = {1:14} #aces high
    ).shuffle().shuffle().shuffle() #third time's the charm!
play_pile = Deck()
discard_pile = Deck()

player_one_hand = Deck()
player_two_hand = Deck()
player_one_downcards = Deck()
player_two_downcards = Deck()
player_one_upcards = Deck()
player_two_upcards = Deck()

#dealing
for i in range(numof_playerpiles):
    player_one_downcards.add_card(draw_pile.pop())
    player_two_downcards.add_card(draw_pile.pop())

for i in range(numof_playerpiles):
    player_one_upcards.add_card(draw_pile.pop())
    player_two_upcards.add_card(draw_pile.pop())

for i in range(numof_playerhand):
    player_one_hand.add_card(draw_pile.pop())
    player_two_hand.add_card(draw_pile.pop())

"""Turn is used to decide whose turn it is. Odd = p1, Even = p2.
This allows the main game loop to have some extra calculations, but less repeated code.
Every loop, it is assigned the value of (turn+1)%2, which is essentially just a NOT.
                                                            (0 -> 1; 1 -> 0)
"""
#the player with the larger sum of hand+upcards goes first
turn = 0 if player_one_hand.sum() > player_two_hand.sum() else 1

#pick_upcards

while True:
    print(f"Player {turn+1}:")
    player = [[player_one_hand, player_one_upcards, player_one_downcards],
                [player_two_hand, player_two_upcards, player_two_downcards]][turn]
    do_turn(player[0], player[1], player[2]) #this stuff works i promise
    
    turn = (turn+1)%2 #flip turn in (0,1)
