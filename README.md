# Hello Aspen Capital!
---
## Overview

This project is a web service containing 7 endpoints
1. ```createplayer```, which takes a json containing a unique name and inserts a player into the database.
2. ```getwins```, which takes a json containing an existing player name and returns the number of lifetime wins.
3.  ```getallwins```, which returns a json containing each existing player and their lifetime wins.
4. ```getgames```, which takes a json containing an existing player name and returns the number of lifetime games played.
5. ```startgame```, which takes a json containing two player names and inserts a new game into the database.
6. ```taketurn```, which takes a json containing the game ID and simulates one step of the game. It returns a json containing information that a front end may use, like the cards played and the size of the winnings pile.
7. ```playgame```, which takes a json containing the game ID and simulates the game to completion.

Both ```taketurn``` and ```playgame``` automatically update the wins and games played of both participants upon game completion.

## Requirements
- Python 3
- django

## Running the project
- Navigate to the ```war_service``` directory

- ```python manage.py runserver```

## Running provided tests
**Caution:** ```tests.sh``` flushes the database.

Just run ```./tests.sh```. The tests in the file are order-dependant, so I combined them into one test case.

## Other details
In the spirit of the project, I'd like to add new fields to the players tracking their match history and an endpoint to generate a matplotlib graph of wins over time. While the graphs for war would look roughly the same over a large number of games played, I think it would be interesting to see for any non-predetermined game.

Thank you for this opportunity to branch out and learn a technology that I had only barely touched previously. I welcome any criticism or feedback.
