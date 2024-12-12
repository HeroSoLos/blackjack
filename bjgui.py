import random
import time
import tkinter as tk
import os

# Card and Suit Setup
suits = ['♠', '♥', '♦', '♣']
card_art = {
    'A': 'A', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
    '7': '7', '8': '8', '9': '9', '10': '10', 'J': 'J', 'Q': 'Q', 'K': 'K'
}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = 11 if rank == 'A' else 10 if rank in 'JQK' else int(rank)

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in suits for rank in card_art.keys()]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

def calculate_score(cards):
    score = sum(card.value for card in cards)
    aces = sum(1 for card in cards if card.rank == 'A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# Main Blackjack Game GUI
class BlackjackGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack Game")
        self.geometry("600x500")
        self.balance = 100
        self.top_score = self.balance
        self.bet = 0
        self.auto_bet_percent = 0  # Auto-bet percentage (default to 0)
        self.deck = Deck()
        self.player_cards = []
        self.dealer_cards = []
        
        self.setup_ui()
        
    def setup_ui(self):
        self.balance_label = tk.Label(self, text=f"Balance: ${self.balance}", font=("Arial", 14))
        self.balance_label.pack()

        # Bet entry and button
        self.bet_label = tk.Label(self, text="Place your bet:", font=("Arial", 14))
        self.bet_label.pack()

        self.bet_entry = tk.Entry(self)
        self.bet_entry.pack()

        self.bet_button = tk.Button(self, text="Place Bet", command=self.place_bet)
        self.bet_button.pack()

        # Settings Button
        self.settings_button = tk.Button(self, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=10)

        # Player and Dealer Display
        self.player_label = tk.Label(self, text="Player's Hand:", font=("Arial", 14))
        self.player_label.pack()
        self.player_hand_label = tk.Label(self, font=("Arial", 14))
        self.player_hand_label.pack()

        self.dealer_label = tk.Label(self, text="Dealer's Hand:", font=("Arial", 14))
        self.dealer_label.pack()
        self.dealer_hand_label = tk.Label(self, font=("Arial", 14))
        self.dealer_hand_label.pack()

        # Outcome Message
        self.outcome_label = tk.Label(self, font=("Arial", 18, "bold"))
        self.outcome_label.pack(pady=10)

        # Player Action Buttons - Larger Size
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.hit_button = tk.Button(button_frame, text="Hit", command=self.player_hit, state=tk.DISABLED, font=("Arial", 14), width=8)
        self.hit_button.pack(side=tk.LEFT, padx=5)

        self.stand_button = tk.Button(button_frame, text="Stand", command=self.player_stand, state=tk.DISABLED, font=("Arial", 14), width=8)
        self.stand_button.pack(side=tk.LEFT, padx=5)

        self.ai_button = tk.Button(button_frame, text="AI Advisor (-10%)", command=self.ai_advisor, state=tk.DISABLED, font=("Arial", 14), width=13)
        self.ai_button.pack(side=tk.LEFT, padx=5)

    def place_bet(self):
        if self.balance <= 0:
            self.show_outcome("Game Over! No more balance.", "red")
            self.end_game("GAME OVER")
            return

        if self.auto_bet_percent > 0:
            self.bet = int(self.balance * self.auto_bet_percent / 100)
            self.balance -= self.bet
        else:
            try:
                bet = int(self.bet_entry.get())
                if 1 <= bet <= self.balance:
                    self.bet = bet
                    self.balance -= bet
                else:
                    self.show_outcome("Invalid Bet. Try Again.", "orange")
                    return
            except ValueError:
                self.show_outcome("Enter a valid number!", "orange")
                return

        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.start_game()

    def start_game(self):
        self.player_cards = [self.deck.draw_card(), self.deck.draw_card()]
        self.dealer_cards = [self.deck.draw_card(), self.deck.draw_card()]
        self.update_hand_display()
        self.bet_entry.config(state=tk.DISABLED)
        self.bet_button.config(state=tk.DISABLED)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.ai_button.config(state=tk.NORMAL)

    def player_hit(self):
        self.player_cards.append(self.deck.draw_card())
        self.update_hand_display()
        if calculate_score(self.player_cards) > 21:
            self.end_game("LOSS")

    def player_stand(self):
        while calculate_score(self.dealer_cards) < 17:
            self.dealer_cards.append(self.deck.draw_card())
        self.update_hand_display()
        self.check_winner()

    def ai_advisor(self):
        if self.balance >= 10:
            self.balance -= int(0.1 * self.balance)
            self.balance_label.config(text=f"Balance: ${self.balance}")
            dealer_upcard = self.dealer_cards[1].value
            player_score = calculate_score(self.player_cards)
            advice = "HIT" if player_score <= 16 and dealer_upcard >= 7 else "STAND"
            self.show_outcome(f"AI Suggests: {advice}", "blue")
        else:
            self.show_outcome("Not enough balance for AI.", "red")

    def check_winner(self):
        player_score = calculate_score(self.player_cards)
        dealer_score = calculate_score(self.dealer_cards)
        
        if dealer_score > 21 or player_score > dealer_score:
            self.balance += self.bet * 2
            self.end_game("WIN")
        elif player_score == dealer_score:
            self.balance += self.bet
            self.end_game("TIE")
        else:
            self.end_game("LOSS")

    def update_hand_display(self):
        player_text = ' '.join(f"{card.rank}{card.suit}" for card in self.player_cards)
        self.player_hand_label.config(text=player_text)
        
        dealer_text = ' '.join(f"{card.rank}{card.suit}" for card in self.dealer_cards)
        self.dealer_hand_label.config(text=dealer_text)

    def show_outcome(self, message, color):
        self.outcome_label.config(text=message, fg=color)

    def end_game(self, result):
        if result == "WIN":
            self.show_outcome("WIN", "green")
            self.top_score = max(self.top_score, self.balance)
        elif result == "LOSS":
            self.show_outcome("LOSS", "red")
        elif result == "TIE":
            self.show_outcome("TIE", "gray")
        elif result == "GAME OVER":
            self.save_leaderboard()
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.ai_button.config(state=tk.DISABLED)
            self.bet_entry.config(state=tk.DISABLED)
            self.bet_button.config(state=tk.DISABLED)
            return

        self.bet = 0
        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.ai_button.config(state=tk.DISABLED)
        self.bet_entry.config(state=tk.NORMAL)
        self.bet_button.config(state=tk.NORMAL)

        if self.balance <= 0:
            self.end_game("GAME OVER")
    
    def save_leaderboard(self):
        leaderboard_path = r"C:\Users\Dudu\pyton\blackjack\leaderboard.txt"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        # Check existing top score
        try:
            with open(leaderboard_path, "r") as file:
                contents = file.read()
                existing_score = int(contents.split("Top Score: $")[1].split("\n")[0])
        except (FileNotFoundError, IndexError, ValueError):
            existing_score = 0

        # Update if current top score is higher
        if self.top_score > existing_score:
            with open(leaderboard_path, "w") as file:
                file.write(f"Top Score: ${self.top_score}\nDate Achieved: {timestamp}\n")
            self.show_outcome(f"New high score: ${self.top_score} saved!", "green")
        else:
            self.show_outcome(f"Top score remains ${existing_score}.", "orange")
    def open_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("300x150")

        tk.Label(settings_window, text="Auto-Bet Percentage:", font=("Arial", 12)).pack(pady=5)
        
        self.auto_bet_entry = tk.Entry(settings_window)
        self.auto_bet_entry.pack()

        tk.Button(settings_window, text="Set Auto-Bet", command=self.set_auto_bet).pack(pady=10)

    def set_auto_bet(self):
        try:
            percent = int(self.auto_bet_entry.get())
            if 0 <= percent <= 100:
                self.auto_bet_percent = percent
                self.show_outcome(f"Auto-Bet set to {percent}%", "blue")
            else:
                self.show_outcome("Enter a valid percentage (0-100).", "orange")
        except ValueError:
            self.show_outcome("Enter a valid percentage (0-100).", "orange")

if __name__ == "__main__":
    game = BlackjackGame()
    game.mainloop()
