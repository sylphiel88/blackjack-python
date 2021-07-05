import pygame
from pygame.locals import *
import random

pygame.init()
pygame.font.init()

pygame.display.set_mode((640, 480))

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Unser erstes Pygame-Spiel")

spielaktiv = True

def repaintCards(*args):
    global button1,button2,button3,button4
    screen.fill((70,150,0))
    for arg in args:
        for i in range(len(arg)):
            arg[i].makeCard()
    
    button1 = rectButton(490,1200,"Rematch")
    button2 = rectButton(800,600,"Hit")
    button3 = rectButton(800,670,"Stand")
    button4 = rectButton(490,1270,"Quit")
    pygame.display.update()

def makeDeck():
    newDeck = []
    for i in range(4):
        for j in range(13):
            newDeck.append(card(50,50, i,j+2, False))
    random.shuffle(newDeck)
    for i in range(52):
        newDeck[i].newPosition(50+2*i,50)
    return newDeck

class player:
    def __init__(self,isPlayer):
        self.score = 0
        self.isPlayer = isPlayer
    def setScore(self,score1):
        self.score=score1

class card:
    def __init__(self,x,y,color, value, isVisible):
        self.x = x
        self.y = y
        self.color = color
        self.value = value
        if value<=10:
            self.score=value
        elif value==11 or value==12 or value==13:
            self.score=10
        else:
            self.score=11
        self.isVisible = isVisible
        if color==0:
            pic = pygame.image.load('pics/herz.png')
            colorC = (216,0,0)
        elif color==1:
            pic = pygame.image.load('pics/karo.png')
            colorC = (216,0,0)
        elif color==2:
            pic = pygame.image.load('pics/kreuz.png')
            colorC = (0,0,0)
        elif color==3:
            pic = pygame.image.load('pics/pik.png')
            colorC = (0,0,0)
        self.pic = pic
        self.colorC = colorC
        self.card = pygame.transform.scale(pygame.image.load('pics/karte.png'), (200, 300))
        if self.value<=10:
            self.cText = str(self.value)
            self.cardBild = pygame.image.load('pics/leer.png')
        elif self.value==11:
            self.cText = 'B'
            self.cardBild = pygame.image.load('pics/buber.png') if self.color<2 else pygame.image.load('pics/bube.png')
        elif self.value==12:
            self.cText = 'D'
            self.cardBild = pygame.image.load('pics/damer.png') if self.color<2 else pygame.image.load('pics/dame.png')
        elif self.value==13:
            self.cText = 'K'
            self.cardBild = pygame.image.load('pics/königr.png') if self.color<2 else pygame.image.load('pics/könig.png')
        else:
            self.cText = 'A'
            self.cardBild = pygame.image.load('pics/leer.png')
        self.cornerPic = pygame.transform.scale(pic,(25,25))
        self.centerPic = pygame.transform.scale(pic,(100,100))
        myfont = pygame.font.SysFont('Bahnschrift', 25,bold=True)
        self.cardText = myfont.render(self.cText, False, colorC)
        self.cardBild = pygame.transform.scale(self.cardBild,(100,50))
    def makeCard(self):
        if self.isVisible == True:
            x = self.x
            y = self.y
            screen.blit(self.card,(x,y))
            screen.blit(self.cornerPic,(x+12,y+12))
            screen.blit(self.cornerPic,(x+163,y+263))
            screen.blit(self.centerPic,(x+50,y+100))
            screen.blit(self.cardText, (x+17,y+37))
            screen.blit(self.cardText, (x+168,y+228))        
            screen.blit(self.cardBild, (x+51,y+50))
        else:
            x=self.x
            y=self.y
            blankC = pygame.transform.scale(pygame.image.load('pics/ruecken.png'), (200, 300))
            screen.blit(blankC,(x,y))
    def newPosition(self,x,y):
        self.x = x
        self.y = y

class rectButton:
    def __init__(self,x,y,str1):
        self.x = x
        self.y = y
        self.text = str1
        self.but = pygame.draw.rect(screen,(200,200,200),(x,y,150,50))
        myfont = pygame.font.SysFont('Bahnschrift', 25,bold=True)
        self.textT = myfont.render(self.text, False, (0,0,0))
        screen.blit(self.textT,(x+10,y+10))
        pygame.display.update()
        

def checkAces(deck,playerA):
    values = []
    for i in range(len(deck)):
        values.append(deck[i].score)
    numAces = values.count(11)
    score1 = 0
    if numAces!=0:
        for i in range(len(deck)):
            score1+=deck[i].score
        for i in range(len(deck)):
            if deck[i].score==11 and score1>21:
                deck[i].score=1
                score1-=10
        playerA.score=score1

    
def takeCard(player):
    global playerReady,win
    if player.isPlayer:
        playerCards.append(cardDeck[len(cardDeck)-1])
        cardDeck.pop(len(cardDeck)-1)
        playerCards[len(playerCards)-1].x=50+50*(len(playerCards))
        playerCards[len(playerCards)-1].y=500
        playerCards[len(playerCards)-1].isVisible = True
        player.score+=playerCards[len(playerCards)-1].score
        checkAces(playerCards,players[0])
    else:
        dealerCards.append(cardDeck[len(cardDeck)-1])
        cardDeck.pop(len(cardDeck)-1)
        dealerCards[len(dealerCards)-1].x=50+50*(len(dealerCards))
        dealerCards[len(dealerCards)-1].y=820
        dealerCards[len(dealerCards)-1].isVisible = playerReady
        player.score+=dealerCards[len(dealerCards)-1].score
        checkAces(dealerCards,players[1])
    repaintCards(playerCards,cardDeck,dealerCards)
    if players[0].score==21:
        scoreT = "BLACKJACK!"
        myfont = pygame.font.SysFont('Bahnschrift', 35,bold=True)
        scoreText = myfont.render(scoreT, False, (255,255,255))
        screen.blit(scoreText, (750,300))
        pygame.display.update()
        win = True
    if players[0].score>21:
        scoreT = "BUST!"
        myfont = pygame.font.SysFont('Bahnschrift', 35,bold=True)
        scoreText = myfont.render(scoreT, False,(255,255,255))
        screen.blit(scoreText, (490,350))
        pygame.display.update()
        win = True

def makeDealerV():
    global playerCards, dealerCards, cardDeck
    for i in range(len(dealerCards)):
        dealerCards[i].isVisible = True
    repaintCards(playerCards,cardDeck,dealerCards)

def getWinner():
    global win
    win = True
    scoreP = players[0].score
    scoreD = players[1].score
    if scoreP==21:
        scoreT="BLACKJACK!"
    elif (scoreP>scoreD or scoreD>21) and (scoreP<=21):
        scoreT="You WIN!"
    elif scoreP==scoreD:
        scoreT="It's a Draw"
    else:   
        scoreT="You Lost!"
    myfont = pygame.font.SysFont('Bahnschrift',35,bold=True)
    scoreText = myfont.render(scoreT, False,(255,255,255))
    screen.blit(scoreText,(490,300))
    pygame.display.update()
    
def newGame():
    global win,cardDeck,button1,button2,button3,button4,players,playerCards,dealerCards,playerReady
    win = False
    cardDeck=makeDeck()
    players = [player(True), player(False)]
    button1 = ''
    button2 = ''
    button3 = ''
    button4 = ''
    repaintCards(cardDeck)
    playerCards=[]
    dealerCards=[]
    playerReady = False
    takeCard(players[1])
    takeCard(players[0])
    takeCard(players[0])
    takeCard(players[1])

newGame()

while spielaktiv:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False
        screen.fill((70,150,0))
        clock = pygame.time.Clock()
        clock.tick(60)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                takeCard(players[0])
                if players[0].score>21:
                    getWinner()
            if event.key == pygame.K_RETURN:
                playerReady = True
                while not win:
                    makeDealerV()
                    if players[1].score<17:
                        takeCard(players[1])
                    else: getWinner()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button1.but.collidepoint(mouse_pos):
                newGame()
            if button2.but.collidepoint(mouse_pos):
                takeCard(players[0])
                if players[0].score>21:
                    getWinner() 
            if button3.but.collidepoint(mouse_pos):
                playerReady = True
                while not win:
                    makeDealerV()
                    if players[1].score<17:
                        takeCard(players[1])
                    else: getWinner()
            if button4.but.collidepoint(mouse_pos):
                spielaktiv = False
                quit()


                

# https://towardsdatascience.com/lets-play-blackjack-with-python-913ec66c732f
# https://www.askpython.com/python/examples/blackjack-game-using-python