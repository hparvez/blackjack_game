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

