import json, random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, o):
        return self.rank == o.rank

    def __ne__(self, o):
        return self.rank == o.rank

    def __lt__(self, o):
        return self.rank < o.rank

    def __gt__(self, o):
        return self.rank > o.rank

    def __le__(self, o):
        return self.__eq__(o) or self.__lt__(o)

    def __ge__(self, o):
        return self.__eq__(o) or self.__gt__(o)

    def __repr__(self):
        if self.rank == 11:
            return "Jack of " + self.suit
        elif self.rank == 12:
            return "Queen of " + self.suit
        elif self.rank == 13:
            return "King of " + self.suit
        elif self.rank == 14:
            return "Ace of " + self.suit
        else:
            return str(self.rank) + " of " + self.suit


class Player:
    def __init__(self, name, deck=[]):
        self.name = name
        self.deck = deck

    def __repr__(self):
        return "Player " + self.name


class Game:
    def __init__(
        self,
        player1_name,
        player2_name,
        player1_deck=None,
        player2_deck=None,
        winnings=[],
    ):
        if not player1_deck and not player2_deck:
            deck = []
            for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
                for rank in range(2, 15):
                    deck.append(Card(suit, rank))

            random.shuffle(deck)
            player1_deck = deck[: len(deck) // 2]
            player2_deck = deck[len(deck) // 2 :]

        self.player1 = Player(player1_name, player1_deck)
        self.player2 = Player(player2_name, player2_deck)
        self.winnings = winnings

    # Simulates one card coming off the top of each deck
    def game_step(self):
        if len(self.player2.deck) == 0:
            return {
                "finished": True,
                "player1": self.player1.name,
                "player2": self.player2.name,
                "player1_score": 1,
                "player2_score": 0,
            }
        elif len(self.player1.deck) == 0:
            return {
                "finished": True,
                "player1": self.player1.name,
                "player2": self.player2.name,
                "player1_score": 0,
                "player2_score": 1,
            }

        p1_card = self.player1.deck.pop(0)
        # print(self.player1.name, p1_card)
        p2_card = self.player2.deck.pop(0)
        # print(self.player2.name, p2_card)
        self.winnings.extend([p1_card, p2_card])
        random.shuffle(self.winnings)

        if p1_card == p2_card:
            if len(self.player1.deck) == 0 or len(self.player2.deck) == 0:
                del self.winnings

                if len(self.player2.deck) == 0:
                    return {
                        "finished": True,
                        "player1": self.player1.name,
                        "player2": self.player2.name,
                        "player1_score": 1,
                        "player2_score": 0,
                    }
                elif len(self.player1.deck) == 0:
                    return {
                        "finished": True,
                        "player1": self.player1.name,
                        "player2": self.player2.name,
                        "player1_score": 0,
                        "player2_score": 1,
                    }
            self.winnings.append(self.player1.deck.pop(0))
            self.winnings.append(self.player2.deck.pop(0))
            return {
                "finished": False,
                "player1": self.player1.name,
                "player2": self.player2.name,
                "player1_card": str(p1_card),
                "player2_card": str(p2_card),
                "pile_size": len(self.winnings),
                "message": "TIE",
            }

        elif p1_card > p2_card:
            self.player1.deck.extend(self.winnings)
            self.winnings = []
            return {
                "finished": False,
                "player1": self.player1.name,
                "player2": self.player2.name,
                "player1_card": str(p1_card),
                "player2_card": str(p2_card),
                "pile_size": len(self.winnings),
                "message": self.player1.name + " wins",
            }
        else:
            self.player2.deck.extend(self.winnings)
            self.winnings = []
            return {
                "finished": False,
                "player1": self.player1.name,
                "player2": self.player2.name,
                "player1_card": str(p1_card),
                "player2_card": str(p2_card),
                "pile_size": len(self.winnings),
                "message": self.player1.name + " wins",
            }

        return None

    # Returns dict of player name and scores
    def play_game(self):
        # print(len(self.player1.deck))
        # print(len(self.player2.deck))
        # print(len(self.winnings))
        while len(self.player1.deck) > 0 and len(self.player2.deck) > 0:
            self.game_step()
            # print(
            #    self.player1.name + ":",
            #    str(len(self.player1.deck)),
            #    "\n" + self.player2.name + ":",
            #    str(len(self.player2.deck)),
            # )
        del self.winnings
        if len(self.player2.deck) == 0:
            return {
                "finished": True,
                "player1": self.player1.name,
                "player2": self.player2.name,
                "player1_score": 1,
                "player2_score": 0,
            }
        else:
            return {
                "finished": True,
                "player1": self.player1.name,
                "player2": self.player2.name,
                "player1_score": 0,
                "player2_score": 1,
            }

    def to_json(self):
        json_dict = {
            "player1": self.player1.name,
            "player1_deck": [
                {"suit": c.suit, "rank": c.rank} for c in self.player1.deck
            ],
            "player2": self.player2.name,
            "player2_deck": [
                {"suit": c.suit, "rank": c.rank} for c in self.player2.deck
            ],
            "winnings": self.winnings,
        }
        return json.dumps(json_dict)

    def from_json(j_str):
        j = json.loads(j_str)
        # print(type(j))
        p1_name = j["player1"]
        # print(p1_name)
        p1_deck = [Card(c["suit"], c["rank"]) for c in j["player1_deck"]]
        # print(p1_deck)
        p2_name = j["player2"]
        # print(p2_name)
        p2_deck = [Card(c["suit"], c["rank"]) for c in j["player2_deck"]]
        # print(p2_deck)
        winnings = j["winnings"]
        # print(winnings)

        return Game(p1_name, p2_name, p1_deck, p2_deck, winnings=winnings)
