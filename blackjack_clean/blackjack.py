from card_models import Deck
from player_models import MoneyPot
import betting_functions

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
    betting_functions.make_bet(players_pot)

    # Deal the cards
    print("Dealing cards ...")
    player_hand, dealer_hand = betting_functions.deal_cards(new_deck)

    # Show hands
    print(player_hand)
    dealer_hand.show_partial_hand()

    # If blackjakck is dealt, round ends here
    if betting_functions.check_initial_blackjack(player_hand, dealer_hand,
                                                 players_pot):
        playing_round = False
    # We only move on with the game if no blackjacks were dealt
    else:
        # Players turn
        players_turn = True
        while players_turn:
            # "hit_or_stand" returns "False" if the player stands
            h_or_s = betting_functions.hit_or_stand(new_deck, player_hand)
            if not h_or_s:
                players_turn = False

            # If player has a blackjack or bust, round ends here
            round_end = betting_functions.blackjack_or_bust(player_hand,
                                                            players_pot,
                                                            dealer_hand)
            if round_end:
                players_turn = False
                playing_round = False

        # The dealer only has a turn if the round isnt over, which can be
        # due to player being bust, or round not being over
        if not player_hand.check_if_bust() and playing_round:
            # Dealers turn
            print(dealer_hand)
            while dealer_hand.value < 17:
                betting_functions.hit(new_deck, dealer_hand)

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
