from copy import deepcopy
class Player:
    def __init__(self, draw, name="NPC"):
        self.playing = True
        self.points = 0#todo load from database
        self.hand = draw
        self.ID = name#default none player character
        self.handValue = 0
    def AddPoints(self,points):
        self.points += points
    def SubtractPoints(self,points):
        #todo if points < wallet raise exception unless debt allowed
        self.points -= points
    def AddCardsToHand(self, cards):
        self.hand.extend(cards)
    def clearCards(self):
        self.hand = []
    def GetHandValue(self):
        #stable, can always call for hand value
        #will only set playing to false never to true
        handValue = None
        def GetUniSuitHand():
            uniSuitHand = []
            for card in self.hand:
                uniSuit = card % 13
                if uniSuit == 0 or uniSuit <= 12 and uniSuit >= 10:
                    uniSuit = 10#10-king = 10
                uniSuitHand.append(uniSuit)
            uniSuitHand.sort()
            # handle ace value
            if uniSuitHand.__contains__(1):
                nonlocal handValue
                handValue = 0
                # ace is physically one card but logically it is two cards 1 & 14
                alternativeUniSuitHand = deepcopy(uniSuitHand)
                for ace in range (uniSuitHand.count(1)):
                    alternativeUniSuitHand.remove(1)
                    alternativeUniSuitHand.append(11)
                return [uniSuitHand,alternativeUniSuitHand]
            return uniSuitHand
        uniSuitHand = GetUniSuitHand()
        if handValue is not None:
            #ace paths
            hands = []
            #if ace then you have two hands, one with ace as 1 one with ace as 11
            for hand in uniSuitHand:
                for card in hand:
                    handValue += card
                if handValue > 21:
                    handValue = 0
                hands.append(handValue)
                handValue = 0
            if hands[0] >= hands[1]:
                if hands[0] == 21 or hands[0] == 0:
                    self.playing = False
                self.handValue = hands[0]
                return hands[0]
            elif hands[0] < hands[1]:
                if hands[1] == 21:
                    self.playing = False
                self.handValue = hands[1]
                return hands[1]
        else:
            #no ace in hand
            handValue = 0
            for card in uniSuitHand:
                handValue += card
            if handValue > 21:
                handValue = 0
                self.playing = False
            self.handValue = handValue
            if handValue == 21:
                self.playing == False
            return handValue
    def LogicHitOrNot(self):
        #true means hit
        #stable can be called at any time
        handValue = self.GetHandValue()#updates playing
        if self.playing:
            return True#TODO simulations
        return False
    def Hold(self):
        self.playing = False
