from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse, Http404
from django.core import exceptions
from django.db import IntegrityError
import json
from .models import Player, Game
from . import war


# Create your views here.
def create_player(request):
    data = json.loads(request.body.decode("utf-8"))
    p = data.get("name")
    player_data = {"name": p}
    try:
        Player.objects.create(**player_data)
        return JsonResponse({"message": "Success"}, status=200)
    except IntegrityError as e:
        return JsonResponse(
            {"message": f"Player {p} already exists"},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"exception_type": str(type(e)), "message": f"DB insert failed, {e}"},
            status=400,
        )


def get_wins(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    p = data.get("name")
    print(p)
    try:
        wins = Player.objects.get(name=p).wins
        return JsonResponse({"wins": wins}, status=200)
    except exceptions.ObjectDoesNotExist as e:
        return JsonResponse(
            {"message": f"Player {p} not found"},
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {"exception_type": str(type(e)), "message": f"DB query failed, {e}"},
            status=400,
        )


def get_games(request):
    data = json.loads(request.body.decode("utf-8"))
    p = data.get("name")
    try:
        games = Player.objects.get(name=p).games_played
        return JsonResponse({"games_played": games}, status=200)
    except exceptions.ObjectDoesNotExist as e:
        return JsonResponse(
            {"message": f"Player {p} not found"},
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {"exception_type": str(type(e)), "message": f"DB query failed, {e}"},
            status=400,
        )


def start_game(request):
    data = json.loads(request.body.decode("utf-8"))
    p1 = data.get("player1")
    p2 = data.get("player2")
    game_state = war.Game(p1, p2).to_json()
    game_entry = {
        "player1": Player.objects.get_or_create(name=p1)[0],
        "player2": Player.objects.get_or_create(name=p2)[0],
        "game_state": game_state,
    }
    print(game_entry)

    db_game = None
    try:
        db_game = Game.objects.create(**game_entry)
    except IntegrityError as e:
        return JsonResponse(
            {"message": f"Game between P1: {p1} and P2: {p2} already exists"},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"exception_type": str(type(e)), "message": f"DB insert failed, {e}"},
            status=400,
        )
    return JsonResponse({"id": db_game.id}, status=200)


def play_game(request):
    data = json.loads(request.body.decode("utf-8"))
    game_id = data.get("id")
    game_json = None
    try:
        game_json = Game.objects.get(id=game_id).game_state
    except exceptions.ObjectDoesNotExist as e:
        return JsonResponse(
            {"message": f"Game {game_id} not found"},
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {"exception_type": str(type(e)), "message": f"DB query failed, {e}"},
            status=400,
        )
    g = war.Game.from_json(game_json)
    game_response = g.play_game()

    p1, p2 = game_response["player1"], game_response["player2"]

    db_p1 = None
    try:
        db_p1 = Player.objects.get(name=p1)
    except exceptions.ObjectDoesNotExist as e:
        return JsonResponse(
            {"message": f"Player {p1} not found"},
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {"exception_type": str(type(e)), "message": f"DB query failed, {e}"},
            status=400,
        )
    db_p1.games_played += 1
    db_p1.wins += game_response["player1_score"]
    db_p1.save()

    db_p2 = None
    try:
        db_p2 = Player.objects.get(name=p2)
    except exceptions.ObjectDoesNotExist as e:
        return JsonResponse(
            {"message": f"Player {p1} not found"},
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {"exception_type": str(type(e)), "message": f"DB query failed, {e}"},
            status=400,
        )
    db_p2.games_played += 1
    db_p2.wins += game_response["player2_score"]
    db_p2.save()

    Game.objects.get(id=game_id).delete()

    return JsonResponse(game_response)


def take_turn(request):
    data = json.loads(request.body.decode("utf-8"))
    game_id = data.get("id")

    db_game = None
    try:
        db_game = Game.objects.get(id=game_id)
    except exceptions.ObjectDoesNotExist as e:
        return JsonResponse(
            {"message": f"Game {game_id} not found"},
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {"exception_type": str(type(e)), "message": f"DB query failed, {e}"},
            status=400,
        )
    game_json = db_game.game_state
    g = war.Game.from_json(game_json)
    game_response = g.game_step()
    db_game.game_state = g.to_json()
    db_game.save()

    if game_response["finished"] == True:
        p1, p2 = game_response["player1"], game_response["player2"]

        db_p1 = None
        try:
            db_p1 = Player.objects.get(name=p1)
        except exceptions.ObjectDoesNotExist as e:
            return JsonResponse(
                {"message": f"Player {p1} not found"},
                status=404,
            )
        except Exception as e:
            return JsonResponse(
                {"exception_type": str(type(e)), "message": f"DB query failed, {e}"},
                status=400,
            )
        db_p1.games_played += 1
        db_p1.wins += game_response["player1_score"]
        db_p1.save()

        db_p2 = None
        try:
            db_p2 = Player.objects.get(name=p2)
        except exceptions.ObjectDoesNotExist as e:
            return JsonResponse(
                {"message": f"Player {p2} not found"},
                status=404,
            )
        except Exception as e:
            return JsonResponse(
                {"exception_type": str(type(e)), "message": f"DB query failed, {e}"},
                status=400,
            )
        db_p2.games_played += 1
        db_p2.wins += game_response["player2_score"]
        db_p2.save()

        Game.objects.get(id=game_id).delete()

    return JsonResponse(game_response)
