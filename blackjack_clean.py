import random
from typing import Type
import time


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


class MoneyPot(object):
    """
    Class to represent a betters pot of money
    """
    def __init__(self, total):
        self.total = total  # Will be input by user
        self.bet = 0  # Will be input by user

    def __str__(self):
        return f"Your remaining money pot is {self.total}"

    def win_bet(self):
        """
        Function that increases money pot if a bet is won
        """
        self.total += self.bet
        print(f"Your remaining pot is {self.total}")

    def win_bet_with_blackjack(self):
        """
        Function that increases money pot if a bet is won by
        being dealth a blackjack at the initial hand (in which
        case, you win 1.5 times your money)
        """
        self.total += (1.5 * self.bet)
        print(f"Your remaining pot is {self.total}")

    def lose_bet(self):
        """
        Function that decreases money pot if a bet is lost
        """
        self.total -= self.bet
        print(f"Your remaining pot is {self.total}")


def make_bet(money_pot: Type[MoneyPot]):
    """
    Function that asks player to how much they'd like to bet

    Args:
        money (Type): money pot of better
    """
    while True:
        try:
            money_pot.bet = float(input("How much would you like to bet? "))
        except ValueError:
            print("Try again - the bet amount must be a number")
        else:
            if money_pot.bet > money_pot.total:
                print(f"Insufficient funds! You only have {money_pot.total}")
            else:
                break


def hit(deck: Type[Deck], hand: Type[Hand]):
    """
    Function that gives the player an extra card

    Args:
        deck (Type[Deck]): the curret deck of cards
        hand (Type[Hand]): the current hand
    """
    new_card = deck.deal()
    hand.add_card(new_card)
    hand.adjust_for_aces()
    print(f"Card drawn is {new_card}")
    print(hand)


def hit_or_stand(deck: Type[Deck], hand: Type[Hand]) -> bool:
    """
    Function that gives the player a choice of whether to hit or stand
    'Hit' refers to the player asking for another card
    'Stand' refers to the player remaining with their current hand

    Args:
        deck (Type[Deck]): the current deck of cards
        hand (Type[Hand]): the current hand

    Returns:
        bool: True if player chose to hit, False otherwise
    """
    while True:
        h_or_s = input("Enter 'H' to hit or 'S' to stand: ")
        if h_or_s.upper() == "H":
            hit(deck, hand)
            return True
        elif h_or_s.upper() == "S":
            print("You chose to stand. It's the dealers turn now ...")
            print("---------------------")
            return False
        else:
            print("Command not recognised, try again")


def blackjack_or_bust(hand: Type[Hand], money_pot: Type[MoneyPot]) -> bool:
    """
    Function to check if a hand has either blackjack or bust at any
    given point in time

    Args:
        hand (Type[Hand]): the hand of cards being checked
        money_pot (Type[MoneyPot]): the current pot of money

    Returns:
        bool: True if either blackjack or bust is present, False otherwsie
    """
    if hand.check_if_bust():
        print("You went bust!")
        money_pot.lose_bet()
        return True
    if player_hand.check_if_blackjack():
        print("You won!")
        money_pot.win_bet()
        return True


def check_initial_blackjack(player_hand: Type[Hand], dealer_hand: Type[Hand],
                            players_pot: Type[MoneyPot]) -> bool:
    """
    Function to check if the initial hand dealt is a blackjack or not

    Args:
        player_hand (Type[Hand]): hand of cards dealt to player
        dealer_hand (Type[Hand]): hand of cards dealt to dealer
        players_pot (Type[MoneyPot]): player's pot of money

    Returns:
        bool: True if initial hand dealt contains blackjack, False otherwise
    """
    if player_hand.check_if_blackjack():
        print("You were dealt a blackjack!")
        print("Let's see what the dealer has ...")
        print(dealer_hand)
        if dealer_hand.check_if_blackjack():
            print("Dealer also has blackjack! It's a draw")
        else:
            print("You won 1.5x your money!")
            players_pot.win_bet_with_blackjack()
        return True


def deal_cards():
    """
    Function to deal cards to player and dealer
    """
    player_hand = Hand()
    player_hand.add_card(new_deck.deal())
    player_hand.add_card(new_deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(new_deck.deal())
    dealer_hand.add_card(new_deck.deal())

    return player_hand, dealer_hand


if __name__ == "__main__":
    print("""Welcome to to the Pyntheus Blackjack table! We operate
    on a 3-2 basis, meaning that for every £10 you bet, you'll get
    £15 profit for being dealt a blackjack (or £25 total)!
    In addition, we shuffle the cards every half deck.""")

    print("Opening a new deck of cards ...")
    new_deck = Deck()

    # Get the players play - when this runs out, game over
    money = float(input("What's your total pot of money? "))
    players_pot = MoneyPot(money)

    playing_round = True
    while playing_round:
        # Check if we've run out of money
        if players_pot.total <= 0:
            print("You've run out of money!")
            break
        
        print("=====================")
        print("New round ...")
        print("---------------------")
        # Check whether we need a new deck or not
        num_cards_remaining = len(new_deck)
        if num_cards_remaining < 26:
            print(f"Re-filling and re-shuffling the deck, there are only {num_cards_remaining} cards left")
            new_deck = Deck()

        # Ask the player how much they want to stake
        make_bet(players_pot)

        # Deal the cards
        print("Dealing cards ...")
        player_hand, dealer_hand = deal_cards()

        # Show hands
        print(player_hand)
        dealer_hand.show_partial_hand()

        # If blackjakck is dealt, round ends here
        if check_initial_blackjack(player_hand, dealer_hand, players_pot):
            playing_round = False
        # We only move on with the game if no blackjacks were dealt
        else:
            # Players turn
            players_turn = True
            while players_turn:
                # "hit_or_stand" returns "False" if the player stands
                h_or_s = hit_or_stand(new_deck, player_hand)
                if not h_or_s:
                    players_turn = False

                # If player has a blackjack or bust, round ends here
                round_end = blackjack_or_bust(player_hand, players_pot)
                if round_end:
                    players_turn = False
                    playing_round = False

            # The dealer only has a turn if the round isnt over, which can be
            # due to player being bust, or round not being over
            if not player_hand.check_if_bust() and playing_round:
                # Dealers turn
                print(dealer_hand)
                while dealer_hand.value < 17:
                    hit(new_deck, dealer_hand)

                # Check who won
                if dealer_hand.value > 21:
                    print("Dealer went bust! You win")
                    players_pot.win_bet()

                elif dealer_hand.value > player_hand.value:
                    print(f"Dealer wins by {dealer_hand.value} to {player_hand.value}")
                    players_pot.lose_bet()

                elif player_hand.value > dealer_hand.value:
                    print(f"You win by {player_hand.value} to {dealer_hand.value}")
                    players_pot.win_bet()

                else:
                    print(f"Tied game! You both have {player_hand.value}!")

        play_again = input("Press Y to play again, or any other key to stop ")
        if play_again.upper() == "Y":
            playing_round = True
        else:
            print(f"You walked away with a pot of {players_pot.total}")
            playing_round = False
