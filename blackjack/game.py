from deck import Deck
from player import  Player
from dealer import DealerAI
class Game:
    def __init__(self, seats, names=None):
        self.isActive = True
        self.deck = Deck()
        self.players = []  # you are players [0]
        self.dealer = DealerAI (self.deck.GetTopCards(2), "dealer")
        for seat in range(seats):
            self.players.append(Player(self.deck.GetTopCards(2)))
        for player in self.players:
            self.GetWinner(player, originalDraw=True)
    def GetWinner(self, player, originalDraw=False):
        if self.isActive is not True:
            return False#for stability
        #This function checks original hands and completed hands
        #Then transacts money based on results of play
        dealerHand = self.dealer.GetHandValue()
        playerHand = player.GetHandValue()
        if not originalDraw:
            if player.playing == True or self.dealer.playing == True:
                raise Exception("Cant Judge Winner Before Game Finish")
            if dealerHand >= playerHand:
                #dealer wins
                if dealerHand == 21 and playerHand == 21:
                    self.dealer.AddPoints(1)
                    player.AddPoints(1)
                elif dealerHand == 21:
                    self.dealer.AddPoints(2)
                    player.SubtractPoints(2)
                else:
                    self.dealer.AddPoints(1)
                    player.SubtractPoints(1)
            else:
                #player only wins
                if playerHand == 21:
                    player.AddPoints(2)
                else:
                    player.AddPoints(1)
        else:#test original cards
            if 21 == dealerHand and 21 == playerHand:
                player.AddPoints(1)
                player.playing = False
                self.dealer.AddPoints(1)
                self.dealer.playing = False
            elif playerHand == 21:
                #automatic win if starting 21 and dealer not starting 21
                player.AddPoints(2)
                player.playing = False
    def RestartGame(self):
        self.isActive = True
        self.dealer.highestHand = None
        self.deck = Deck()
        self.dealer.playing = True
        self.dealer.clearCards()
        self.dealer.AddCardsToHand(self.deck.GetTopCards(2))
        for player in self.players:
            player.playing = True
            player.clearCards()
            player.handValue = 0
            player.AddCardsToHand(self.deck.GetTopCards(2))
            self.GetWinner(player, originalDraw=True)
    def FinishGame(self):
        #dealer must hit if any player has a card higher then him and below 22
        def GetHighestActiveHand(players):
            highest = 0
            for player in players:
                if player.handValue > highest:
                    highest = player.handValue
            return highest
        #Have NPC's play and finish round including dealer
        npcList = []
        for player in self.players:
            if player.ID == "NPC":
                npcList.append(player)
        #append dealer to end of list so that they hit or hold last as instructed
        npcList.append(self.dealer)
        #complete play for each npc
        for npc in npcList:
            if npc.ID == "dealer":
                npc.InformDealer(GetHighestActiveHand(self.players))
            while(npc.playing):
                if npc.LogicHitOrNot():#updates playing
                    #Hit
                    draw = self.deck.GetTopCards(1)
                    npc.AddCardsToHand(draw)
        #Give Chips/points to winners, including dealer
        for player in self.players:
            self.GetWinner(player)
        self.isActive = False
    def Hit(self,player):
        #stable can be used any time
        if player.playing:
            player.AddCardsToHand(self.deck.GetTopCards(1))
            player.GetHandValue()# update playing/handValue to make Hit()safe
    def IsNpcTurn(self):
        npcTurn = True
        for player in self.players:
            #if any none npc's are still playing
            if player.playing is True\
                    and player.ID != "dealer" \
                    and player.ID != "NPC":
                npcTurn = False
        return npcTurn
