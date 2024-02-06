"""BlackJack Game"""

import random, sys

# Set up the constants
HEARTS = chr(9829) # charecter 9823 is for "hearts" symbol
DIAMONDS = chr(9830) # charecter 9830 is for "diamonds" symbol
SPADES = chr(9824) # charecter 9824 is for "spades" symbol
CLUBS = chr(9827) # charecter 9827 is for "clubs" symbol

BACKSIDE = 'backside' # An arbitrary string to represent the back of a card

def main():
    print('Welcome to Blackjack!')

    money = 5000 #starting money
    while True: #main game loop
    #check if the player has run out of money
      if money <= 0:
        print("Game over! You're broke!")
        sys.exit() #terminate the program
      # Let the player bet
      print("Money: money") 
      bet = getBet(money) #calling the getBet function

      #give the dealer and the player their cards
      deck = getDeck()
      dealerHand = [deck.pop(), deck.pop()] #I'm using the pop() method to remove the last card from the deck and add it to the dealer's hand.
      playerHand = [deck.pop(), deck.pop()] #same as above

      # Handle player actions:
      print('Bet:', bet)
      while True: # Keep looping until player stands or busts.
          displayHands(playerHand, dealerHand, False)
          print()
          
          # Check if the player has bust:
          if getHandValue(playerHand) > 21:
              break

          # Get the player's move, either H, S, or D:
          move = getMove(playerHand, money - bet)

          # Handle the player actions:
          if move == 'D':
              # Player is doubling down, they can increase their bet:
              additionalBet = getBet(min(bet, (money - bet)))
              bet += additionalBet
              print('Bet increased to {}.'.format(bet))
              print('Bet:', bet)

          if move in ('H', 'D'):
              # Hit/doubling down takes another card.
              newCard = deck.pop()
              rank, suit = newCard
              print('You drew a {} of {}.'.format(rank, suit))
              playerHand.append(newCard)

              if getHandValue(playerHand) > 21:
                  # The player has busted:
                continue


          if move in ('S', 'D'):
              # Stand/doubling down stops the player's turn.
              break

      # Handle the dealer's actions:
      if getHandValue(playerHand) <= 21:
          while getHandValue(dealerHand) < 17:
              # The dealer hits:
              print('Dealer hits...')
              dealerHand.append(deck.pop())
              displayHands(playerHand, dealerHand, False)


              if getHandValue(dealerHand) > 21:
                  break # The dealer has busted.
              input('Press Enter to continue...')
              print('\n\n')

      # Show the final hands:
      displayHands(playerHand, dealerHand, True)

      playerValue = getHandValue(playerHand)
      dealerValue = getHandValue(dealerHand)
      # Handle whether the player won, lost, or tied:
      if dealerValue > 21:
          print('Dealer busts! You win ${}!'.format(bet))
          money += bet
      elif (playerValue > 21) or (playerValue < dealerValue):
          print('You lost!')
          money -= bet
      elif playerValue > dealerValue:
          print('You won ${}!'.format(bet))
          money += bet
      elif playerValue == dealerValue:
          print('It\'s a tie, the bet is returned to you.')
      
      input('Press Enter to continue...')
      print('\n\n')

def getBet(maxBet): #here the function takes in the maxbet as a parameter
    """Ask the player how much they want to bet this round."""
    while True: #I need to keep asking until the player enters a valid amount.
        print(f'How much do you want to bet? (1-{maxBet}, or quit)') #f-string is used to format the string
        bet = input('> ').lower().strip() #I'm using the lower() and strip() methods to make the input case-insensitive and to remove any leading or trailing whitespace.
        if bet == 'quit':
            print('thanks for playing!')
            sys.exit() #terminate the program
        
        if not bet.isdecimal(): #I'm using the isdecimal() method to check if the string is a number.
            continue #here continue is used to go back to the start of the loop if the input is not a number.
        
        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet
        
def getDeck(): 
    """Return a list of (rank, suit) tuples representing a deck of 52 cards."""
    deck = [] #I start with an empty list and add each card to it.
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS): #already defines above, making a tuple of suits
        for rank in range(2, 11): #first covering numbers 2-10(11 is exclusive)
            deck.append((str(rank), suit)) #I'm using the str() function to convert the integer to a string and then adding the card to the deck.
        for rank in ('J', 'Q', 'K', 'A'): #then covering the face cards and the ace
            deck.append((rank, suit)) #I'm adding the card to the deck.
    random.shuffle(deck) #shuffle the deck
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    """Show the player's and dealer's cards. Hide the dealer's first card if showDealerHand is False."""
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        displayCards([BACKSIDE] + dealerHand[1:]) #I'm using the + operator to concatenate the two lists together.
    
    #show the player's cards
    print('player:', getHandValue(playerHand))
    displayCards(playerHand)


def getHandValue(cards):
    '''returns the value of the hand'''
    value = 0  # Initialize value here
    numberofAces = 0

    # Add the value for the non-ace cards
    for card in cards:
        rank = card[0]  # I'm using the index 0 to get the rank of the card.
        if rank == 'A':
            numberofAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    # Add the value for the aces
    value += numberofAces  # I'm adding the number of aces to the value of the hand.
    for i in range(numberofAces):
        if value + 10 <= 21:
            value += 10

    return value



def displayCards(cards):
    rows = ['','','',''] #I'm using a list of three empty strings to store the rows of text for the cards.
    for i, card in enumerate(cards):
        rows[0] += ' ___ ' #I'm adding the top line of the card to the first row.
        if card == BACKSIDE:
            #this is the back of the card
            rows[1] += '|## |'
            rows[2] += '|###|'
            rows[3] += '| ##|'
        else:
            rank, suit = card #I'm using the tuple unpacking to assign the rank and suit to the variables rank and suit.
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))
    #print each row in the screen.
    for row in rows:
        print(row)

def getMove(playerHand, money):
    """Asks the player for their move, and returns 'H' for hit, 'S' for
    stand, and 'D' for double down."""

    while True:
        # Determine what moves the player can make:
        moves = ['(H)it', '(S)tand']
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # Get the player's move:
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S', 'D') and (move == 'D' or move in moves):
            return move
        else:
            print("Invalid input! Please enter 'H' for Hit, 'S' for Stand, or 'D' for Double Down if available.")



# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()



























