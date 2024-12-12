import random
import time

# Card ASCII Art
suits = ['♠', '♥', '♦', '♣']
card_art = {
    'A': ['┌─────┐', '│A    │', '│     │', '│    A│', '└─────┘'],
    '2': ['┌─────┐', '│2    │', '│     │', '│    2│', '└─────┘'],
    '3': ['┌─────┐', '│3    │', '│     │', '│    3│', '└─────┘'],
    '4': ['┌─────┐', '│4    │', '│     │', '│    4│', '└─────┘'],
    '5': ['┌─────┐', '│5    │', '│     │', '│    5│', '└─────┘'],
    '6': ['┌─────┐', '│6    │', '│     │', '│    6│', '└─────┘'],
    '7': ['┌─────┐', '│7    │', '│     │', '│    7│', '└─────┘'],
    '8': ['┌─────┐', '│8    │', '│     │', '│    8│', '└─────┘'],
    '9': ['┌─────┐', '│9    │', '│     │', '│    9│', '└─────┘'],
    '10': ['┌─────┐', '│10   │', '│     │', '│   10│', '└─────┘'],
    'J': ['┌─────┐', '│J    │', '│     │', '│    J│', '└─────┘'],
    'Q': ['┌─────┐', '│Q    │', '│     │', '│    Q│', '└─────┘'],
    'K': ['┌─────┐', '│K    │', '│     │', '│    K│', '└─────┘']
}

# Card class for cards with ranks and suits
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = 11 if rank == 'A' else 10 if rank in 'JQK' else int(rank)

    def display(self):
        card_lines = card_art[self.rank]
        return [line.replace(' ', self.suit, 1) for line in card_lines]

# Deck of cards
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in suits for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

# Calculate the score and handle Ace values
def calculate_score(cards):
    score = sum(card.value for card in cards)
    aces = sum(1 for card in cards if card.rank == 'A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# Display cards with ASCII art
def display_cards(cards, hidden=False):
    if hidden:
        print("Dealer's hand:")
        print("┌─────┐ ┌─────┐")
        print("│??   │ │{:5}│".format(cards[1].rank))
        print("│  {}  │ │{:5}│".format(cards[1].suit, cards[1].suit))
        print("│   ??│ │{:5}│".format(cards[1].rank))
        print("└─────┘ └─────┘")
    else:
        for line in zip(*[card.display() for card in cards]):
            print(" ".join(line))

# Basic strategy AI advice
def basic_strategy_advice(player_score, dealer_card, has_soft_hand):
    if has_soft_hand:
        return "hit" if player_score <= 17 else "stand"
    else:
        if player_score <= 11:
            return "hit"
        elif 12 <= player_score <= 16 and dealer_card in [7, 8, 9, 10, 11]:
            return "hit"
        elif player_score >= 17:
            return "stand"
        else:
            return "stand"

# Main game function with betting and AI advisory system
def play_blackjack():
    balance = 100
    top_score = balance
    print("Welcome to Blackjack!\n")
    
    while balance > 0:
        print(f"\nCurrent balance: ${balance}")
        
        # Place a bet
        while True:
            try:
                bet = int(input("Enter your bet amount: $"))
                if 1 <= bet <= balance:
                    break
                else:
                    print(f"Invalid bet. You must bet between $1 and ${balance}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        deck = Deck()
        player_cards = [deck.draw_card(), deck.draw_card()]
        dealer_cards = [deck.draw_card(), deck.draw_card()]
        
        # Display initial hands
        print("\nYour hand:")
        display_cards(player_cards)
        print(f"Player's score: {calculate_score(player_cards)}\n")
        display_cards(dealer_cards, hidden=True)

        player_score = calculate_score(player_cards)
        if player_score == 21:
            print("\nBlackjack! You got a natural 21!")
            balance += int(bet * 1.5)
            top_score = max(top_score, balance)
            print(f"You win ${int(bet * 1.5)}. New balance: ${balance}")
            continue

        while calculate_score(player_cards) < 21:
            choice = input("\nDo you want to hit, stand, or use the AI advisor for 10% of your balance? (h/s/ai): ").lower()
            
            if choice == 'ai':
                if balance >= 10:
                    ai_fee = int(0.1 * balance)
                    balance -= ai_fee
                    dealer_upcard_value = dealer_cards[1].value
                    has_soft_hand = any(card.rank == 'A' for card in player_cards)
                    advice = basic_strategy_advice(player_score, dealer_upcard_value, has_soft_hand)
                    print(f"\nAI Advisor suggests you should: {advice.upper()}")
                    print(f"New balance after AI advisor fee of 10% (${ai_fee}): ${balance}")
                    continue
                else:
                    print("Not enough balance for AI advisor.")
            
            elif choice == 'h':
                player_cards.append(deck.draw_card())
                print("\nYour hand:")
                display_cards(player_cards)
                player_score = calculate_score(player_cards)
                print(f"Player's score: {player_score}\n")
            
            elif choice == 's':
                break
            else:
                print("Invalid input, please choose 'h', 's', or 'ai'.")

        if player_score <= 21:
            while calculate_score(dealer_cards) < 17:
                dealer_cards.append(deck.draw_card())
        
        dealer_score = calculate_score(dealer_cards)
        print("\nFinal Hands:")
        print("Your hand:")
        display_cards(player_cards)
        print(f"Player's final score: {player_score}\n")
        print("Dealer's hand:")
        display_cards(dealer_cards)
        print(f"Dealer's final score: {dealer_score}\n")

        if player_score > 21:
            balance -= bet
            print(f"Player busts! You lose ${bet}. New balance: ${balance}.")
        elif dealer_score > 21 or player_score > dealer_score:
            balance += bet
            print(f"You win! You gain ${bet}. New balance: ${balance}.")
        elif player_score == dealer_score:
            print("It's a tie! Your bet is returned.")
        else:
            balance -= bet
            print(f"Dealer wins! You lose ${bet}. New balance: ${balance}.")
        
        top_score = max(top_score, balance)

    print("\nGame over! You're out of money.")
    
    # Save top score to leaderboard
    # Check if a new top score has been achieved and save it if higher
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    leaderboard_path = r"C:\Users\Dudu\pyton\blackjack\leaderboard.txt"

    # Attempt to read the existing top score
    try:
        with open(leaderboard_path, "r") as file:
            contents = file.read()
            existing_score = int(contents.split("Top Score: $")[1].split("\n")[0])
    except (FileNotFoundError, IndexError, ValueError):
        # If the file doesn't exist or is malformed, assume no existing top score
        existing_score = 0

    # Compare and update if the current top score is higher
    if top_score > existing_score:
        with open(leaderboard_path, "w") as file:
            file.write(f"Top Score: ${top_score}\nDate Achieved: {timestamp}\n")
        print(f"New top score of ${top_score} recorded in leaderboard.txt on {timestamp}")
    else:
        print(f"Top score remains ${existing_score}. No update necessary.")


# Run the game
play_blackjack()
