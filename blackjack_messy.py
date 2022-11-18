from typing import List, Tuple
import random


# Create the deck of cards
def create_deck() -> List[Tuple[str, int]]:
    """
    Function that creates a clean deck of cards
    in new card order

    Returns:
        List[Tuple[str, int]]: deck of cards in 
        new card order
    """
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    cards = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9",
            "10", "Jack", "Queen", "King"]
    card_values = {
        "Ace": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10,
        "Queen": 10, "King": 10
        }

    deck = []
    for suit in suits:
        for card in cards:
            deck.append((f"{card} of {suit}", card_values[card]))

    return deck


# Start the game by shuffling cards
def shuffle(deck: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """
    Function which takes in a deck and shuffles it in place

    Returns:
        List: A list with items of the format (card name, card value)
        randomly shuffled
    """
    return random.shuffle(deck)


def deal(deck: List[Tuple[str, int]]) -> Tuple[str, int]:
    """
    Function which removes and returns a single card from a deck

    Args:
        deck (List[Tuple[str, int]]): deck of playing cards

    Returns:
        Tuple[str, int]: the top card of the deck
    """
    return deck.pop()


def calculate_card_total(cards: List[Tuple[str, int]]) -> int:
    """
    Function that calculates the total value of cards in a hand

    Args:
        cards (List[Tuple): list of cards in hand of the forat
        [(card_name, card_value)]

    Returns:
        int: Total value of cards in hand
    """
    card_total = 0
    for card in cards:
        card_total += card[1]

    return card_total


def check_if_bust(card_total: int) -> bool:
    """
    Function that checks if we've gone bust or not

    Args:
        card_total (int): the current sum of card values
        in a hand

    Returns:
        bool: True if the total exceeds 21, False otherwise
    """    
    return card_total > 21


# def check_if_bust(cards: List[Tuple[str, int]]):
#     # Make adjustment for aces
#     pass


def check_if_blackjack(card_total: int) -> bool:
    """
    Function that checks if we've got blackjack or not

    Args:
        card_total (int): the current sum of card values
        in a hand

    Returns:
        bool: True if the total equals 21, False otherwise
    """
    return card_total == 21


if __name__ == "__main__":
    print("""Welcome to to the Pyntheus Blackjack table! We operate
            on a 3-2 basis, meaning that for every £10 you bet, you'll get
            £15 profit for being dealt a blackjack on the first hand (or £25 total)!
            In addition, we shuffle the cards every half deck.""")
    print("Opening a new deck of cards ...")
    
    # Create a deck and shuffle it
    new_deck = create_deck()
    shuffle(new_deck)
    
    # Ask the player what their starting pot is - if this runs out
    # the game will end
    players_pot = float(input("What's your total pot of money? "))

    while players_pot > 0:
        # If we've got less than 26 cards left, re-shuffle
        num_cards_remaining = len(new_deck)
        if num_cards_remaining < 26:
            print(f"Re-filling and re-shuffling the deck, there are only {num_cards_remaining} left")
        # Create a deck and shuffle it
        new_deck = create_deck()
        shuffle(new_deck)

        # See what the player wants to stake - can't be more than their pot
        stake = float(input("How much do you want to stake? "))
        if stake > players_pot:
            print(f"Insufficient funds! You only have {players_pot}.")
            stake = float(input("How much do you want to stake? "))

        # Deal two cards to the player and dealer
        players_cards = [deal(new_deck) for _ in range(2)]
        dealers_cards = [deal(new_deck) for _ in range(2)]

        print(f"Your cards are: {[card[0] for card in players_cards]}")
        print(f"The dealer has a {dealers_cards[0][0]}")

        # Calculat sum of players cards and dealers cards
        players_total = calculate_card_total(players_cards)
        dealers_total = calculate_card_total(dealers_cards)
        
        if check_if_blackjack(players_total):
            # Dealers turn
            print("The dealer is turning over his other card ...")
            print(f"The dealer has {[card[0] for card in dealers_cards]}")
            if check_if_blackjack(dealers_total):
                print("It's a draw!")
            else:
                print("You win! You got 21!")
                players_pot += stake
        else:

            # Players can only make a choice if they have less 
            # than 21 in their hand
            while players_total < 21:
                hit_or_stand = input("Enter H to hit or S to stand: ")

                if hit_or_stand.upper() == "H":
                    new_card = deal(new_deck)
                    players_cards.append(new_card)
                    players_total = calculate_card_total(players_cards)
                    print(f"You drew a {new_card[0]}. Your new total is {players_total}")
                else:
                    break

            # If we've ggot blackhack or bust - game ends here
            if check_if_blackjack(players_total):
                print("You win! You got 21!")
                players_pot += stake
            elif check_if_bust(players_total):
                print("You lose! Your total is more than 21")
                players_pot -= stake
            else:
                # Dealers turn
                print("The dealer is turning over his other card ...")
                print(f"The dealer has {[card[0] for card in dealers_cards]}")

                # If the dealer has less than 17 cards, he must hit
                while dealers_total < 17:
                    new_card = deal(new_deck)
                    dealers_cards.append(new_card)
                    dealers_total = calculate_card_total(dealers_cards)
                    print("The dealer must hit again ...")
                    print(f"The dealer drew {new_card[0]}. Their new total is {dealers_total}")

                # If the dealer is bust, game ends here
                if check_if_bust(dealers_total):
                    print("Dealer went bust, you won!")
                    players_pot += stake
                else:
                    if players_total > dealers_total:
                        print(f"You beat the dealer by {players_total} to {dealers_total}")
                        players_pot += stake
                    elif dealers_total > players_total:
                        print(f"You lose by {dealers_total} to {players_total}")
                        players_pot -= stake
                    else:
                        print(f"It's a draw!")

        print(f"Your new pot is {players_pot}")
        if players_pot <= 0:
            print("You've run out of money, you can't play anymore!")
            break

        play_again = input("Press Y to play again, or any other key to stop ")
        if play_again.upper() != "Y":
            print(f"You walked away with a pot of {players_pot}")
            break
