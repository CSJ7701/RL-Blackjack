import random

class Shoe:
    """
    Class representing a blackjack shoe with multiple decks.
    
    Attributes:
    ----------
    deck : dict
        Dictionary representing the number of each card value left in the shoe.
        
    Methods:
    -------
    createDeck(num_decks: int) -> dict[str, int]:
        Creates a dictionary representing the shoe with the specified number of decks.
    
    drawCard() -> str:
        Randomly draws a card from the shoe, reducing its count by one.
    
    isEmpty() -> bool:
        Checks if the shoe is empty (i.e., no cards left).
    """
    
    def __init__(self, num_decks: int = 1):
        """
        Initializes the Shoe class.
        
        Parameters:
        ----------
        num_decks : int
            The number of decks used to create the shoe. Defaults to 1 deck.
        """
        # Initialize the deck with the specified number of decks
        self.deck = self.createDeck(num_decks)

    def createDeck(self, num_decks: int) -> dict[str, int]:
        """
        Creates a shoe (dictionary) representing the total number of each card value 
        based on the number of decks.
        
        Parameters:
        ----------
        num_decks : int
            Number of decks to include in the shoe.
        
        Returns:
        -------
        dict[str, int]
            A dictionary where keys are card values ('2' to 'A') and values are the 
            number of that card in the shoe.
        """
        # Standard deck: 4 of each card from 2-9, 16 of the '10' (including face cards), and 4 Aces.
        cards_per_deck = {
            '2': 4, '3': 4, '4': 4, '5': 4, 
            '6': 4, '7': 4, '8': 4, '9': 4,
            '10': 16, 'A': 4  # 10 includes ten, jack, queen, king
        }

        # Multiply the number of each card by the number of decks
        shoe = {card: count * num_decks for card, count in cards_per_deck.items()}
        
        return shoe

    def drawCard(self) -> str:
        """
        Draws a random card from the shoe, reducing its count by one.
        
        Returns:
        -------
        str
            The value of the drawn card.
        """
        # Get the list of cards with their current counts (only cards with counts > 0)
        cards, counts = zip(*[(card, count) for card, count in self.deck.items() if count > 0])
        
        # Randomly select a card based on the remaining counts (weighted random selection)
        drawn_card = random.choices(cards, counts)[0]
        
        # Reduce the count of the drawn card in the shoe
        self.deck[drawn_card] -= 1
        
        return drawn_card

    def isEmpty(self) -> bool:
        """
        Checks if the shoe is empty (i.e., no cards left).
        
        Returns:
        -------
        bool
            True if the shoe is empty, False otherwise.
        """
        # Sum the counts of all cards. If the total is greater than zero, the shoe is not empty.
        if sum(self.deck.values()) > 0:
            return False
        return True

    def showShoe(self):
        """
        Displays a text-based bar chart showing the current composition of the shoe.
        """
        print("Current Shoe Composition:")
        # Determine the width for the 'count' column.
        space_between = 40
        for card, count in self.deck.items():
            bar = '█' * count
            print(f"{card:>2}: {bar:<{space_between}} ({count:>{3}})")


if __name__ == "__main__":
    # Example usage
    test = Shoe(num_decks=2)  # Create a shoe with 2 decks
    print(test.deck)          # Print the initial deck
    print(test.drawCard())    # Draw a card and print the drawn card
    test.showShoe()
    
