import random
import csv
import sys
from treys import Card, Deck, Evaluator
from tqdm import tqdm

def generate_random_hole_cards():
    deck = Deck()
    return [deck.draw(1)[0], deck.draw(1)[0]]

def generate_action_history():
    return [random.choice([0, 1, 2]) for _ in range(random.randint(0, 4))]

def simulate_winrate(hole_cards, num_players=2, simulations=1000):
    evaluator = Evaluator()
    wins = ties = 0

    for _ in range(simulations):
        deck = Deck()
        for c in hole_cards:
            if c in deck.cards:
                deck.cards.remove(c)

        community_cards = [deck.draw(1)[0] for _ in range(5)]
        opponents = [[deck.draw(1)[0], deck.draw(1)[0]] for _ in range(num_players - 1)]

        my_score = evaluator.evaluate(community_cards, hole_cards)
        opp_scores = [evaluator.evaluate(community_cards, o) for o in opponents]

        if all(my_score < s for s in opp_scores):
            wins += 1
        elif any(my_score == s for s in opp_scores):
            ties += 1

    winrate = round(wins / simulations, 4)
    tie_rate = round(ties / simulations, 4)
    lose_rate = round(1 - winrate - tie_rate, 4)
    return winrate, tie_rate, lose_rate

def generate_dataset(simulations_per_data, data_per_player_count, output_file="datasets/dataset.csv"):
    fieldnames = [
        "hole_cards", "board", "position", "num_players", "pot_size", "stack",
        "call_amount", "action_history", "stage", "winrate", "label"
    ]
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for num_players in range(2, 9):
            print(f"Generating for {num_players} players...")
            for _ in tqdm(range(data_per_player_count), desc=f"{num_players} players"):
                hole_cards = generate_random_hole_cards()
                board = [0, 0, 0, 0, 0]
                position = random.randint(0, num_players - 1)
                pot_size = random.randint(20, 150)
                stack = random.randint(500, 2000)
                call_amount = random.choice([0, 10, 20, 50])
                action_history = generate_action_history()
                stage = 0

                winrate, tie_rate, lose_rate = simulate_winrate(hole_cards, num_players, simulations_per_data)

                label = 0 if winrate < 0.2 else 1 if winrate < 0.5 else 2

                writer.writerow({
                    "hole_cards": hole_cards,
                    "board": board,
                    "position": position,
                    "num_players": num_players,
                    "pot_size": pot_size,
                    "stack": stack,
                    "call_amount": call_amount,
                    "action_history": action_history,
                    "stage": stage,
                    "winrate": winrate,
                    "label": label
                })

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generator.py <simulations_per_data> <data_per_player_count>")
        sys.exit(1)

    simulations = int(sys.argv[1])
    data_count = int(sys.argv[2])
    generate_dataset(simulations_per_data=simulations, data_per_player_count=data_count)