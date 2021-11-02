import json
import requests
import unittest

player1 = json.dumps({"name": "Anna"})
player2 = json.dumps({"name": "Bill"})
player3 = json.dumps({"name": "Charlie"})
game1 = json.dumps({"player1": "Anna", "player2": "Bill"})
game2 = json.dumps({"player1": "Anna", "player2": "Charlie"})
play1 = json.dumps({"id": 1})
play2 = json.dumps({"id": 2})


class TestWarAPI(unittest.TestCase):
    def Test_create_player(self):
        response = requests.post("http://localhost:8000/createplayer/", player1)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"message": "Success"})

        response = requests.post("http://localhost:8000/createplayer/", player2)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"message": "Success"})

    def Test_duplicate_player(self):
        response = requests.post("http://localhost:8000/createplayer/", player1)
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"message": "Player Anna already exists"})

    def Test_get_wins_success(self):
        response = requests.post("http://localhost:8000/getwins/", player1)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"wins": 0})

    def Test_get_wins_failure(self):
        response = requests.post("http://localhost:8000/getwins/", player3)
        self.assertEqual(response.status_code, 404)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"message": "Player Charlie not found"})

    def Test_get_games_success(self):
        response = requests.post("http://localhost:8000/getgames/", player1)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"games_played": 0})

    def Test_get_games_failure(self):
        response = requests.post("http://localhost:8000/getgames/", player3)
        self.assertEqual(response.status_code, 404)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"message": "Player Charlie not found"})

    def Test_create_game(self):
        response = requests.post("http://localhost:8000/startgame/", game1)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"id": 1})

    def Test_create_game_new_player(self):
        response = requests.post("http://localhost:8000/startgame/", game2)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"id": 2})

    def Test_create_duplicate_game(self):
        response = requests.post("http://localhost:8000/startgame/", game1)
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_json,
            {"message": "Game between P1: Anna and P2: Bill already exists"},
        )

    def Test_take_turn(self):
        response = requests.post("http://localhost:8000/taketurn/", play1)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            set(response_json.keys()),
            {
                "finished",
                "player1",
                "player2",
                "player1_card",
                "player2_card",
                "pile_size",
                "message",
            },
        )

    def Test_play_game(self):
        response = requests.post("http://localhost:8000/playgame/", play1)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_json.keys(),
            {"finished", "player1", "player2", "player1_score", "player2_score"},
        )

    def Test_take_turn_fail(self):
        response = requests.post("http://localhost:8000/taketurn/", play1)
        self.assertEqual(response.status_code, 404)

    def Test_play_game_fail(self):
        response = requests.post("http://localhost:8000/playgame/", play1)
        self.assertEqual(response.status_code, 404)

    def Test_get_games_success2(self):
        response = requests.post("http://localhost:8000/getgames/", player1)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"games_played": 1})

        response = requests.post("http://localhost:8000/getgames/", player2)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_json, {"games_played": 1})

    def Test_get_wins_success2(self):
        response1 = requests.post("http://localhost:8000/getwins/", player1)
        self.assertEqual(response1.status_code, 200)
        response1_json = json.loads(response1.content.decode("utf-8"))

        response2 = requests.post("http://localhost:8000/getwins/", player2)
        self.assertEqual(response2.status_code, 200)
        response2_json = json.loads(response2.content.decode("utf-8"))

        if response1_json["wins"] == 1:
            self.assertEqual(response2_json, {"wins": 0})
        else:
            self.assertEqual(response1_json, {"wins": 0})
            self.assertEqual(response2_json, {"wins": 1})

    def test_api(self):
        self.Test_create_player()
        self.Test_duplicate_player()
        self.Test_get_wins_success()
        self.Test_get_wins_failure()
        self.Test_get_games_success()
        self.Test_get_games_failure()
        self.Test_create_game()
        self.Test_create_game_new_player()
        self.Test_create_duplicate_game()
        self.Test_take_turn()
        self.Test_play_game()
        self.Test_take_turn_fail()
        self.Test_play_game_fail()
        self.Test_get_games_success2()
        self.Test_get_wins_success2()


if __name__ == "__main__":
    unittest.main()
