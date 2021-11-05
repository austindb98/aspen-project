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
- Docker

## Running the project
- Navigate to the ```war_service``` directory

- ```./run.sh```

## Running provided tests
**Caution:** ```tests.sh``` flushes the database.

Just run ```./tests.sh```. The tests in the file are order-dependant, so I combined them into one test case.

## JSON Examples
### Input
- createplayer, getwins, getgames  
```{"name": "Anna"}```
- startgame  
```{"player1": "Anna", "player2": "Bill"}```
- taketurn, playgame  
```{"id": 1}```

### Output
- createplayer  
```{"message": "Success or error message}```
- getwins  
```{"wins": 5}```
- getgames  
```{"games_played": 8}```
- getallwins  
```{"Anna": 2, "Bill": 3, "Charlie": 1}```
- startgame  
```{"id": 4}``` or ```{"message": "Error message"}```
- taketurn - response content differs based on whether the game is complete
```
{   
    "finished": False,
    "player1": "Anna",
    "player2": "Charlie",
    "player1_card": "4 of Hearts",
    "player2_card": "4 of Clubs",
    "pile_size": 6,
    "message": "TIE",
}
```
```
{   
    "finished": True,
    "player1": "Anna",
    "player2": "Charlie",
    "player1_score": 1,
    "player2_score": 0,
}
```
- playgame  
```
{   
    "finished": True,
    "player1": "Anna",
    "player2": "Charlie",
    "player1_score": 1,
    "player2_score": 0,
}
```
## Other details
In the spirit of the project, I'd like to add new fields to the players tracking their match history and an endpoint to generate a matplotlib graph of wins over time. While the graphs for war would look roughly the same over a large number of games played, I think it would be interesting to see for any non-predetermined game. I'd also like to explore the use of non-relational databases, as this seems like a good potential use case.

Thank you for this opportunity to branch out and experiment with tools that I had only barely touched previously. I welcome any criticism or feedback.
