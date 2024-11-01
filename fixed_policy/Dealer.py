from Agent import Agent
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

    def calculateHand(self, hideHand: bool = False) -> int:
        """
        Calculate the total value of the dealer's hand, taking into account the flexible value of Aces.

        Aces can be worth 1 or 11, depending on the total hand value. If the hand exceeds 21,
        Aces are treated as 1 to prevent a bust.

        :param hideHand: If True, only show value for the first card.
                         If False, calculate the full hand value.

        :return: The total value of the dealer's hand.
        """
        value = 0  # Total value of the hand
        aces = 0  # Count of Aces in the hand

        if hideHand:
            hand = self.hand[0]
        else:
            hand = self.hand

        # Calculate the initial hand value and track Aces
        for card in hand:
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

    def showHand(self, hideHand: bool = False) -> list[str]:
        """
        Return the dealer's hand or only the first card based on the game stage.

        :param fullHand: If True, only show the first card (for initial player view). 
                         If False, return the full hand (for endgame evaluation).
        :return: A list representing either the dealer's full hand or the first card.
        """
        if hideHand:
            return [self.hand[0]]  # Show only the first card (used for initial dealer hand display)
        else:
            return self.hand  # Show the entire hand (used when revealing the dealer's hand)

    def reset(self) -> None:
        """
        Reset the dealer's hand, clearing all cards for the next round.
        """
        self.hand = []  # Empty the dealer's hand to prepare for a new round

    def deal(self, agent: Agent) -> None:
        """
        Deal one card to the specified agent.
        """
        card = self.shoe.drawCard()
        agent.receiveCard(card)

    def playTurn(self, debug: bool = False) -> None:
        """
        Dealer plays their turn according to standard Blackjack rules.
        Draws a card while their hand value is less than 17.
        """
        while self.calculateHand() < 17:
            self.draw()
            if debug:
                print(f"Current Hand: {self.showHand()}\nValue: {self.calculateHand()}")
 
if __name__ == "__main__":
    # Initialize a shoe and a dealer
    shoe = Shoe()
    dealer = Dealer(shoe)

    # Draw initial cards and display them
    initial_hand = dealer.drawInitial()
    print("Dealer's initial hand:", initial_hand)
    
    # Calculate hand value after the initial draw
    initial_value = dealer.calculateHand()
    print("Initial hand value:", initial_value)
    
    # Draw another card and display the hand and new value
    dealer.draw()
    print("Dealer's hand after drawing one more card:", dealer.hand)

    new_value = dealer.calculateHand()
    print("Hand value after additional draw:", new_value)
    
    # Check hand (showing only first card, as in the initial display for the player)
    print("Dealer's visible card for player view:", dealer.showHand(hideHand=True))
    print(f"Dealer's visible hand values: {dealer.calculateHand(True)}")
    
    # Check hand (showing full hand, typically for endgame view)
    print("Dealer's full hand for endgame view:", dealer.showHand(hideHand=False))

    # Reset the dealer's hand for a new round
    dealer.reset()
    print("Dealer's hand after reset:", dealer.hand)

    print("\nPlaying a round:")
    dealer.drawInitial()
    print("Initial Hand:", dealer.showHand())
    dealer.playTurn(True)
    if dealer.calculateHand() > 21:
        print("BUST")
    elif dealer.calculateHand() == 21:
        print("WIN")

    
