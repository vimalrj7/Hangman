#-------------------------------------------------------------------------------
# Name:        Hangman
# Version:     1.0
# Author:      vimalrj
# Created:     20/1/2018
#-------------------------------------------------------------------------------

import pygame
from time import sleep
import random
import inputbox
from itertools import cycle

pygame.init()

display_width = 800
display_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
light_red = (220, 0, 0)
green = (0, 220, 0)
light_green = (0, 255, 0)
blue = (0,20,255)
light_blue = (0,100,255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Hangman')
clock = pygame.time.Clock()

# Pictures
h0 = pygame.image.load('hangman1.png')
h1 = pygame.image.load('hangman2.png')
h2 = pygame.image.load('hangman3.png')
h3 = pygame.image.load('hangman4.png')
h4 = pygame.image.load('hangman5.png')
h5 = pygame.image.load('hangman6.png')
h6 = pygame.image.load('hangman7.png')
images = [h1, h2, h3, h4, h5, h6]

# Variables
x = (display_width * 0.3)
y = (display_height * 0.5)
x2 = (display_width * 0.55)
y2 = (display_height * 0.25)
score = 0
player_score = [0,0,0]
player = cycle(range(1, 3))

def draw(img, x, y):
    gameDisplay.blit(img, (x, y))

# Displays all text in the game
def message_display(text, size, color, x, y): 
    font = pygame.font.Font('freesansbold.ttf', size)
    t = font.render(text, True, color)
    text_rect = t.get_rect(center=(x, y))
    gameDisplay.blit(t, text_rect)
    pygame.display.update()

# Makes a button    
def button(msg, x, y, i, a, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+200 > mouse[0] > x and y+50 > mouse[1] > y:
        pygame.draw.rect(gameDisplay, a, (x, y, 200, 50))
        if click[0] == 1 and action == 'rand':
            guess(random_word(), 'rand')
        elif click[0] == 1 and action == 'user':
            guess(user_word(next(player)), 'user')
        elif click[0] == 1 and action == 'menu':
            main_menu()
        elif click[0] == 1 and action == 'quit':
            pygame.quit()
            quit()
    else:
        pygame.draw.rect(gameDisplay, i, (x, y, 200, 50))
        
    message_display(msg, 20, black, x+100, y+25)
    
# Main menu design and buttons    
def main_menu():
    global score, player_score
    player_score = [0,0,0]
    score = 0
    menu = True
    x3 = display_width*0.3
    gameDisplay.fill(white)
    message_display('HANGMAN', 80, black, display_width*0.5, 250) 
      
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        button('vs CPU', 170, 300, green, light_green, 'rand')
        button('Quit', 300, 360, red, light_red, 'quit')
        button('vs PLAYER', 430, 300, green, light_green, 'user')

        pygame.display.update()
        clock.tick(60)

# Randomly generates a category and word
def random_word():
    textFile = open('wordlist.txt','r')
    category = textFile.readline().split()
    wl0 = textFile.readline().split()
    wl1 = textFile.readline().split()
    wl2 = textFile.readline().split()
    wl3 = textFile.readline().split()
    wl4 = textFile.readline().split()
    wl5 = textFile.readline().split()
    wl6 = textFile.readline().split()
    wl7 = textFile.readline().split()
    wl8 = textFile.readline().split()
    words = wl1 + wl2 + wl3 + wl4 + wl5 + wl6 + wl7 + wl8
    words={category[0]:wl0,category[1]:wl1,category[2]:wl2,category[3]:wl3,category[4]:wl4,category[5]:wl5,category[6]:wl6,category[7]:wl7,category[8]:wl8}
    textFile.close()
    cat, word = random.choice(list(words.items()))
    return [cat, random.choice(word)]

# Gets a word from player    
def user_word(player):
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, red, (400-200, 300-45, 400, 90))
    if player == 1:
        message_display('Player 1: Choose a secret word!', 35, black, 400, 200)
        message_display('Player 2: Your turn to guess.', 35, black, 400, 400)
    elif player == 2:
        message_display('Player 2: Choose a secret word!', 35, black, 400, 200)
        message_display('Player 1: Your turn to guess.', 35, black, 400, 400)        
    word = inputbox.ask(gameDisplay, "Word")
    return ['User', word]        
        
# Main game logic for Hangman
def guess(w, mode):
    global score, player_score
    gameDisplay.fill(white)
    message_display('HANGMAN', 80, black, display_width*0.5, 50)
    draw(h0, x2, y2) 
    word = list(w[1])
    blank = list('_'*len(word))
    already_guessed = []
    message_display(' '.join(blank), 30, black, x, y)
    message_display(str(len(blank))+' letters', 20, black, x, y+100)
    
    if mode == 'rand':
        message_display('Score: '+str(score), 20, black, x, y+200)
        message_display('The category is: '+w[0], 20, black, x, y-100)
    else:
        message_display("P1's score: "+str(player_score[2]), 20, black, x-75, y+200)
        message_display("P2's score: "+str(player_score[1]), 20, black, x+75, y+200)
    
    tries = 0
    guesses_x = 780
    guesses_y = 50
    exit = False

    while not exit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
            elif event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key)
                pygame.draw.rect(gameDisplay, white, [x-170, y+20, 400, 50])
                
                if guess in already_guessed:
                    message_display('You have already guessed that.', 20, black, x, y+40)  
                elif guess in word:
                    already_guessed.append(guess)
                    for i, j in enumerate(word):
                        if j == guess:
                            blank[i] = guess
                    pygame.draw.rect(gameDisplay, white, [x-200, y-20, 450, 50])
                    message_display(' '.join(blank), 30, black, x, y)
                    
                    message_display(guess, 30, green, guesses_x, guesses_y)
                    guesses_y += 40                    
                else:
                    try:
                        already_guessed.append(guess)
                        draw(images[tries], x2, y2)
                        tries += 1
                        
                        message_display(guess, 30, red, guesses_x, guesses_y)
                        guesses_y += 40
                    except:
                        outcome(mode, 'loss', w[1])
                        exit = True
                        gameDisplay.fill(white)
                
                if blank == word:
                    outcome(mode, 'win', w)
                    exit = True
                            
        button('Menu', 575, 525, blue, light_blue, 'menu')            
        pygame.display.update() 
        clock.tick(60)

# Controls win/loss screen, score and player turn
def outcome(mode, state, word):
    global score, player_score, player
    
    if state == 'win':
        message_display('WINNER!', 100, green, display_width/2, display_height/2)
        sleep(3)
        gameDisplay.fill(white)
        
        if mode == 'rand':
            score += 1
            guess(random_word(), 'rand')
        elif mode == 'user':
            next(player)
            player_score[next(player)] += 1
            guess(user_word(next(player)), 'user')
            
    elif state == 'loss':
        message_display('LOSER!', 100, red, display_width/2, display_height*0.4)
        message_display('The answer was ', 50, red, display_width/2, display_height*0.5)
        message_display('"'+word+'"', 50, red, display_width/2, display_height*0.6)
        sleep(3)
        gameDisplay.fill(white)
        
        if mode == 'rand':
            score = 0
            guess(random_word(), 'rand')        
        else:
            guess(user_word(next(player)), 'user')        

main_menu()        

