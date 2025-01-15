"""
Classes abstracted to be usable for any 52-card game (I think). Just because.
"""
from random import shuffle as random_shuffle
from warnings import warn

valid_suits = ["hearts","diamonds","spades","clubs","zero","any"]

class Card:
    face_value: int # Numerical value of card (-1 -- 14 for utility reasons)
    game_value: int # Game-specific card value
    suit: str # Card suit

    def __init__(self, face_value: int, suit: str, game_value: int = None) -> None:
        r"""Create a new Card object.

        - `face_value`: actual numerical value of the card (in `range(1, 14)`)
        - `suit`: suit of the card ("hearts", "diamonds", "spades", "clubs")
        - `game_value`: game-specific card value (i.e. aces high or low, etc)
        """
        if type(face_value) not in [int, float]:
            raise TypeError(f"Face value must be an integer! Invalid: {face_value}")
        if type(suit) != str:
            raise TypeError(f"Suit must be a string! Invalid: {suit}")
        #None is of type NoneType but that's not accessible without imports
        if type(game_value) not in [type(None), int, float]:
            raise TypeError(f"Game-specific value must be an integer! Invalid: {game_value}")

        face_value = round(face_value)
        suit = suit.lower()
        game_value = face_value if game_value == None else round(game_value)
        
        if face_value not in range(-1, 15):
            raise ValueError(f"Invalid card value: \"{face_value}\"")
        if suit not in valid_suits:
            raise ValueError(f"Invalid card suit: \"{suit}\"")
        
        if (face_value == 0 and suit != "zero") or (suit == "zero" and face_value != 0):
            warn("If you really\033[3m really\033[23m want to create a zero card? If so, you should make face_value = 0 and suit='zero'")

        self.face_value = face_value
        self.suit = suit
        self.game_value = game_value
    
    def pretty_value(self, value: int = None, short:bool = False) -> str:
        if value == None: value = self.game_value #no `self` or attributes in anno.

        if value in [1,14]:
            value = "A" if short else "Ace"
        elif value > 10:
            #pick which list to look in with short, then look in at (value%10)-1
            value = (["J","Q","K"] if short else ["Jack","Queen","King"]) \
                [(value%10)-1]
        return str(value)

    def __str__(self) -> str:
        value = self.pretty_value(self.face_value)
        suit = self.suit.capitalize()

        return f"{value} of {suit}"
    
    def __repr__(self) -> str:
        #if self.face_value == self.game_value:
        #    return f"Card({self.face_value}, {self.suit})"
        return f"Card({self.face_value}, '{self.suit}', {self.game_value})"
    
    def __add__(self, other) -> int:
        if type(other) != Card:
            raise TypeError("Invalid addition -- adding a Card to something that isn't.")
        return self.game_value+other.game_value

    def __sub__(self, other) -> int:
        if type(other) != Card:
            raise TypeError("Invalid subtraction -- subtracting a Card from something that isn't.")
        return self.game_value-other.game_value
    
    def __eq__(self, other) -> bool:
        r"""Equality comparison -- returns true if face (not game!) values *and* suits match"""
        if type(other) not in [Card, type(None)]:
            raise TypeError("Invalid equality -- comparing a Card to something that isn't.")
        if other == None: return False
        value_match = self.face_value == other.face_value
        suit_match = self.suit == other.suit
        if self.suit == "any" or other.suit == "any":
            suit_match = True
        if self.face_value == -1 or other.face_value == -1:
            value_match = self.game_value == other.game_value
        return value_match and suit_match

    def __ne__(self, other) -> bool:
        r"""Inquality comparison -- returns false if face (not game!) values *and* suits match"""
        if type(other) not in [Card, type(None)]:
            raise TypeError("Invalid inequality -- comparing a Card to something that isn't.")
        if other == None: return False
        return not self == other

    def __lt__(self, other) -> bool:
        r"""Less-than comparison -- ignores suit"""
        if type(other) not in [Card, type(None)]:
            raise TypeError("Invalid less-than -- comparing a Card to something that isn't.")
        if other == None: return False
        return self.face_value < other.face_value

    def __gt__(self, other) -> bool:
        r"""Greater-than comparison -- ignores suit"""
        if type(other) not in [Card, type(None)]:
            raise TypeError("Invalid greater-than -- comparing a Card to something that isn't.")
        if other == None: return False
        return self.face_value > other.face_value

    


class Deck:
    cards: list[Card] #if we don't define it later, all instances of Deck() become magically linked
    rules: dict = {}

    def Full_Deck(jokers: bool = False, rules: dict = {}) -> None: #anno Deck doesn't work in class def
        r"""Returns a new Deck object, with a full 52 (or 54) card deck

        - `jokers`: Whether or not to include Jokers in the deck (default False)
        - `rules`: A dictionary of {face_value:game_value} for special cards
        """
        this_deck = Deck(rules)
        for value in range(1, 14):
            for suit in ["hearts","diamonds","spades","clubs"]: #NOT all `valid_suits`
                this_deck.add_card(value, suit)
        return this_deck


    def __init__(self, rules: dict = {}) -> None:
        r"""Create a new Deck object, to handle a deck of Cards.
        Can be used for a central Deal pile, a player's hand, etc.
        """
        self.cards = []
        self.rules = rules
        pass

    def add_card(self, card: int|Card, suit: str = None) -> None:
        r"""Add a new card to this deck.
        
        - `card`: numerical value of the card (in `range(1, 15)`) OR a Card object
        - `suit`: suit of the card ("hearts", "diamonds", "spades", "clubs")
        [unnecessary if `card` is a Card]

        Returns this Deck so that it can be chained.
        """
        if type(card) == Card:
            self.cards.append(card)
        elif suit == None:
            raise TypeError("If `card` is not a Card, you must provide a `suit`")
        else:
            if card in self.rules.keys():
                game_value = self.rules[card]
            else: game_value = card
            self.cards.append(Card(card, suit, game_value))
        return self

    def remove_card(self, card: int|Card, suit: str = None) -> None:
        r"""Remove a card from this deck.
        
        - `card`: numerical value of the card (in `range(1, 15)`)
        - `suit`: suit of the card ("hearts", "diamonds", "spades", "clubs")
        [unnecessary if `card` is a Card]

        Returns this Deck so that it can be chained.
        """
        if type(card) == Card:
            self.cards.remove(card)
        elif suit == None:
            raise TypeError("If `card` is and int, you must provide a `suit`")
        else:
            # Find instance of the card in the list. There should only be one...
            #Card() will raise errors if the value or suit is wrong.
            """all of this works, but apparently there's simply a better method:"""
            #index = self.cards.index(Card(card, suit))
            #new_cards = self.cards[:index]
            #new_cards.extend(self.cards[index+1:]) #lists are mutable, so this works in-place
            #self.cards = new_cards
            self.cards.remove(Card(card,suit))
        return self

    def add_cards(self, cards: list[Card] = []) -> None:
        r"""Add each card from a list to this deck.

        - `cards`: a list of cards to be removed

        Returns this deck object so that it can be chained.
        """
        for card in cards:
            if type(card) is not Card:
                raise TypeError("You must only add Cards to a Deck.")
            self.add_card(card)
        return self
    
    def remove_cards(self, count: int, value: int|None = None, suit: str|None = None) -> list[Card]:
        r"""Remove a specified number of cards of cards from this deck. If requested number of 

        - `count`: The number of matching cards to remove (required)
        - `value`: The FACE value of the card(s) to match (optional)
        - `suit`:  The suit       of the card(s) to match (optional)

        Returns the list of cards which were removed. Cannot be chained.
        """
        removed_cards = []
        if value == suit == None: #neither given -- return the top #
            for i in range(count):
                try:
                    removed_cards.append(self.pop())
                except: #catch list-too-small
                    pass
        elif value == None: #only suit given
            for card in self.cards:
                if count == 0: break #end the loop
                if card.suit == suit:
                    removed_cards.append(card)
                    count -= 1
            #so that we don't skip in the first loop by removing from the data we're using
            for card in removed_cards:
                self.remove_card(card)
        else: #the value given (and also the suit given?)
            suit = "any" if suit == None else suit
            for card in self.cards:
                if count == 0: break #end the loop
                if card == Card(-1,suit,value):
                    removed_cards.append(card)
                    count -= 1
            #so that we don't skip in the first loop by removing from the data we're using
            for card in removed_cards:
                self.remove_card(card)
        return removed_cards
    
    def top(self) -> Card | None:
        if len(self.cards) < 1: return None
        return self.cards[-1]

    def pop(self) -> Card:
        return self.cards.pop()
    
    def shuffle(self) -> None:
        r"""Shuffle the cards in this Deck, using `random.shuffle`.
        
        Returns this Deck so that it can be chained.
        """
        random_shuffle(self.cards)
        return self

    def sum(self) -> int:
        total = 0
        for card in self.cards:
            total += card.game_value
        return total

    def count_value_matches(self, value: int) -> int:
        if value not in range(-1,15):
            raise ValueError(f"Invalid card value: \"{value}\"")
        count = 0
        for card in self.cards:
            if card.game_value == value:
                count += 1
        return count
    
    def count_suit_matches(self, suit: str) -> int:
        if suit not in valid_suits:
            raise ValueError(f"Invalid suit to count: \"{suit}\"")
        count = 0
        for card in self.cards:
            if card.suit == suit:
                count += 1
        return count
    
    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return f"Deck with {len(self)} card{'' if len(self)==1 else 's'}."
    
    def __iter__(self) -> iter:
        return iter(self.cards)



if __name__ == "__main__":
    asdf = Card(12,"hearts")
    test = Deck()
    test2 = Deck.Full_Deck()
    #print(test2.cards)
    #test.shuffle()
    #print(test2.cards)
