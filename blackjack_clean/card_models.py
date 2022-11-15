import random
from typing import Type

# Create a deck of cards
suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
cards = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9",
         "10", "Jack", "Queen", "King"]
card_values = {
    "Ace": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10,
    "Queen": 10, "King": 10
    }


class Card(object):
    """
    Class which represents a playing card
    """
    def __init__(self, suit: str, value: str, card: str):
        self.suit = suit
        self.value = value
        self.card = card

    def __str__(self):
        return f"{self.card} of {self.suit}"


class Deck(Card):
    """
    Class which represents a deck of cards
    """
    def __init__(self):
        self.deck = []
        for suit in suits:
            for card in cards:
                self.deck.append(Card(suit=suit, card=card,
                                      value=card_values[card]))

        self.shuffle()

    def __len__(self):
        return len(self.deck)

    def shuffle(self):
        """
        Function to "shuffle" the deck of cards into a random order
        """
        random.shuffle(self.deck)

    def deal(self):
        """
        Function which picks the top card from the deck and returns
        and removes it
        """
        single_card = self.deck.pop()
        return single_card


class Hand(object):
    """
    Class which represents a 'hand' (subset of a deck)
    """
    def __init__(self):
        self.cards = []  # Empty list which will take the cards within the hand
        self.value = 0
        self.aces = 0  # Keep track of aces so we can adjust for them later

    def __str__(self):
        return f"Hand contains {' and '.join([str(card) for card in self.cards])} with a value of {self.value}"

    def show_partial_hand(self):
        """
        Function that shows only the only card - used for the dealer on
        their first go
        """
        print(f"The dealer has {self.cards[1]}")

    def add_card(self, card: Type[Card]):
        """
        Function to add a card to an existing hand

        Args:
            card (Type): the card to hand to the existing hand
        """
        self.cards.append(card)
        self.value += card.value
        # Keep track of aces so they can be adjusted for
        if card.card == "Ace":
            self.aces += 1

    def adjust_for_aces(self):
        """
        Funcion to adjust for aces - if our hand value exceeds 21, we can
        assign our aces a value of 1 instead
        """
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def check_if_blackjack(self) -> bool:
        """
        Function to check if the hand has blackjack

        Returns:
            bool: True if the total equals 21, False otherwise
        """
        return self.value == 21

    def check_if_bust(self) -> bool:
        """
         Function that checks if we've gone bust or not

        Returns:
            bool: True if the total exceeds 21, False otherwise
        """
        return self.value > 21
