# Project Name 
Five-in-a-row

## Description
A simple five in a row game in Python using the minmax algorithm and displayed on the console.
The base project was built to have fun and minmax was implemented later as a part of a university project.

The default map size is 20x20 or 25x25 which can be expanded to the right and down directions until 99x99. This is only a theoritical limit.
The player plays against a bot whose steps are calculated with the minmax algorithm.

## Challenges
Unfortunately, the way the game is stored makes the minmax very slow, as the board is read from left to right multiple times, so no bigger than the depth of 5-7 is advised.
Another problem is in the game itself because the branching factor is huge in this game. To solve this issue node ordering is applied, or the branching factor could be limited at 8-10. This would create in interesting comparison between the importance of the depth and the branching factor. Further testing would yield the optimal values for these parameters.

## Installation
To run the game clone the repo and install the used libraries.
