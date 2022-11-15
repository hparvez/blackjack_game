from card_models import Deck, Hand
from player_models import MoneyPot
from typing import Type


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
    if hand.check_if_blackjack():
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


def deal_cards(deck):
    """
    Function to deal cards to player and dealer
    """
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    return player_hand, dealer_hand
