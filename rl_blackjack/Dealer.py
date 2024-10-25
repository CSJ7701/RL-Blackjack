from Shoe import Shoe

class Dealer:
    def __init__(self, shoe: Shoe):
        """
        Initialize the dealer with an empty hand and a shoe of cards to draw from.

        :param shoe: The Shoe object the dealer will draw cards from.
        """
        self.hand = []  # Dealer's hand starts empty
        self.shoe = shoe  # The shoe is used to draw cards

    def drawInitial(self) -> list[str]:
        """
        Draw two initial cards for the dealer.

        :return: A list containing the dealer's two initial cards.
        """
        self.hand = [self.shoe.drawCard(), self.shoe.drawCard()]  # Dealer starts with two cards
        return self.hand

    def draw(self) -> None:
        """
        Draw a card from the shoe and add it to the dealer's hand.
        """
        card = self.shoe.drawCard()  # Draw a card from the shoe
        self.hand.append(card)  # Add the drawn card to the hand

    def calculateHand(self) -> int:
        """
        Calculate the total value of the dealer's hand, taking into account the flexible value of Aces.

        Aces can be worth 1 or 11, depending on the total hand value. If the hand exceeds 21,
        Aces are treated as 1 to prevent a bust.

        :return: The total value of the dealer's hand.
        """
        value = 0  # Total value of the hand
        aces = 0  # Count of Aces in the hand

        # Calculate the initial hand value and track Aces
        for card in self.hand:
            if card == 'A':  # Ace can be 1 or 11
                aces += 1
                value += 11  # Initially treat Ace as 11
            else:
                value += int(card)  # Convert numbered cards ('2' to '10') directly to integers

        # Adjust for Aces to avoid busting (Ace can be 1 instead of 11)
        while value > 21 and aces > 0:
            value -= 10  # Convert one Ace from 11 to 1
            aces -= 1  # Reduce the count of Aces being treated as 11

        return value

    def checkHand(self, fullHand: bool = False) -> list[str]:
        """
        Return the dealer's hand or only the first card based on the game stage.

        :param fullHand: If True, only show the first card (for initial player view). 
                         If False, return the full hand (for endgame evaluation).
        :return: A list representing either the dealer's full hand or the first card.
        """
        if fullHand:
            return [self.hand[0]]  # Show only the first card (used for initial dealer hand display)
        else:
            return self.hand  # Show the entire hand (used when revealing the dealer's hand)

    def reset(self) -> None:
        """
        Reset the dealer's hand, clearing all cards for the next round.
        """
        self.hand = []  # Empty the dealer's hand to prepare for a new round
 
