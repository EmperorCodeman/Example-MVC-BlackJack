from player import Player
class DealerAI(Player):
    def __init__(self, draw, name):
        self.highestHand = None#Of Players what is the highest hand
        super().__init__(draw, name)
    def LogicHitOrNot(self):
        #True means hit
        #if hand <17 hit if ace in hand and hand<18 hit else hold
        handValue = self.GetHandValue()#updates playing
        if self.playing == False:
            return False
        def Ace():#check if ace in hand
            ace = False
            for card in self.hand:
                if card % 13 == 1:
                    return True
            return ace
        if handValue < 18 and Ace():
            return True
        elif handValue < 17:
            return True
        #must hit if anyones hand is greater then yours and below 22
        elif self.highestHand > handValue:
            return True
        else:
            self.playing = False#TODO Simulator().GetPercentChanceToWinHand()
            return False#TODO Simulator().GetPercentChanceToWinHand()
    def InformDealer(self, highestHand):
        self.highestHand = highestHand
























