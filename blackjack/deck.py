from random import shuffle
'''
#Not dead code, This shows the card class which is implemented by schema only
class Card: 
    #Cards are logically the range 2- 54, with 14 as Diomonds Ace.
    # diomonds 2-14  ace 14
    # hearts 15-27   ace 27 or 1 because 27%13 = 1
    # spads  28-40   2=28%13
    # clubs  41-53
    None
'''
class Deck:
    def __init__(self):
        self.cards = [i for i in range(2,54)]
        shuffle(self.cards)
    def shuffle(self):
        shuffle(self.cards)
    def GetTopCards(self, numberOfCardsToRetrieve):
        dealCards = []
        if numberOfCardsToRetrieve > len(self.cards):
            leftToDeal = numberOfCardsToRetrieve - len(self.cards)
            dealCards.append(self.cards)
            #deck out of cards, add new deck
            self.cards = [i for i in range(2, 54)]
            shuffle(self.cards)
            for i in range(leftToDeal):
                dealCards.append(self.cards.pop())
            return dealCards
        for count in range(numberOfCardsToRetrieve):
            dealCards.append(self.cards.pop())
        return dealCards
