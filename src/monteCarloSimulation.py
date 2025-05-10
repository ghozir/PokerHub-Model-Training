from treys import Card, Deck, Evaluator

def simulate_winrate(hole_cards_str, community_cards_str, num_players=2, simulations=1000):
    evaluator = Evaluator()
    hole_cards = [Card.new(card) for card in hole_cards_str]
    community_cards = [Card.new(card) for card in community_cards_str]
    wins = 0
    ties = 0
    used_cards = hole_cards + community_cards

    for _ in range(simulations):
        deck = Deck()
        for card in used_cards:
            if card in deck.cards:
                deck.cards.remove(card)

        sim_community = community_cards + [deck.draw(1)[0] for _ in range(5 - len(community_cards))]
        opponents = [[deck.draw(1)[0], deck.draw(1)[0]] for _ in range(num_players - 1)]

        my_score = evaluator.evaluate(sim_community, hole_cards)
        opp_scores = [evaluator.evaluate(sim_community, opp) for opp in opponents]

        if all(my_score < score for score in opp_scores):
            wins += 1
        elif any(my_score == score for score in opp_scores):
            ties += 1

    winrate = round(wins / simulations, 4)
    tie_rate = round(ties / simulations, 4)
    lose_rate = round(1 - winrate - tie_rate, 4)
    return {"winrate": winrate, "tie_rate": tie_rate, "lose_rate": lose_rate}


# Contoh pemakaian
result = simulate_winrate(['Ah', 'Kh'], ['7h', '2d', 'Jc'], num_players=2, simulations=1000)
print(result)
