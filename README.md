# Conway_gol
Conway game of life

This is an unfinished program for Conway's Game Of Life, and variants. 

I first read of Conways celluar automation game in Marin Gardner's Mathematical Games column in *Scientific American* when I was in high school. I soon wrote a program to simulate it in Focal, on my high school's DEC PDP 8/l. I have since occasionally revisited the game with better computers. This is a newer program in Python, using Tkinter for the GUI.

At present it plays. One can create/edit an initial pattern with mouse by clicking on squares in the grid. Selecting 'evolove' under the edit menu will allow the colony to evolve. 'Stop' will stop the process, and 'clear' will clear the grid. When a pattern becomes still, the evolution halts automatically. When stopped, the pattern can at any point be edited.

Features that have been added:
1) Save and load initial patterns to from text files (There are a couple of examples of classic patterns.)
2) Store initial pattern so it can be reverted to
3) Ability to define different rules. Rules are lists with the numbers of neighboring cells, as in the default rules:
  
  birth = (3,)      #an empty cell at time T is 'born' for T_2 iff there are three adjacent live cells at T
  survive = (2, 3)  #a living cell at time T will remain such at T_2 iff it has 2 - 3 live adjacent cells at T
  
  
 https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
 
 https://www.ibiblio.org/lifepatterns/october1970.html

In memorial for mathemetician John Conway, the inventor of this game (1938 - April 11, 2020)
