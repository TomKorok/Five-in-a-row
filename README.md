# Five-in-a-row
A simple five in a row game in Python using the minmax algorithm and displayed on the console.
The base project was built to have fun and minmax was applied as a part of a university project.

The default map size is 20x20 or 25x25 which can be expanded to the right and down directions until 99x99.
The player plays against a bot whose steps are calculated with the minmax algorithm.
Unfortunately, the way the game is stored makes the minmax very slow so no bigger than the depth of 5-7 is advised.
Another problem is in the game itself because the branching factor is huge in this game. To solve this issue node ordering is applied.

To run the game copy the files and install the used libraries.
