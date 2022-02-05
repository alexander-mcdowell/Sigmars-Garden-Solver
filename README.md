# Sigmars-Garden-Solver
A python script for solving games of Sigmar's Garden, a solitaire-esque puzzle mini-game from the programming game _Opus Magnum_ by Zachtronics.

Sigmar's Garden is a one-person mini-game in which the goal is to remove all of the atoms on a hexagonal board. To do this, you must perform a sequence of matches where each match between any two revealed atoms removes the matched pair. An atom is "revealed" if it has at least three contiguous empty spaces around it. There are only a few permitted match combinations:
- A primary element (fire, earth, water, air) and another atom of the same element (e.g: fire + fire).
- A primary element (fire, earth, water, air) and a salt atom.
- Two salt atoms.
- Mors (the black element) and Vitae (the pink element).
- Quicksilver and a Metal (lead, tin, iron, copper, silver). However, a metal atom is only revealed if it has three contiguous empty tiles around it _and_ if the metal before it in precedence was already matched. For instance, copper can only be revealed once lead, tin, and iron have all been removed from the board. Lead is the only metal which does not require this precedence condition.
- Gold is the only exception to the rule of metals and the rule of matching. Gold is only revealed once all of the other metals have been revealed, however, it cannot be matched with quicksilver. Once gold is revealed, it can be removed immediately as it cannot match with anything else.

# Requirements
- Python 3.7.x or higher, although I believe Python 3.x should be sufficient.
- termcolor (latest version). For me, this was v1.1.0.
- colorama (latest version). For me, this was v.0.4.4.

# Instructions
To run the solver, you must first start a game of Sigmar's Garden. Next, read each tile of the hex grid starting from the top-left corner and ending at the bottom right, moving from top to bottom, left to right. For each tile, write the following abbrievation for the element on _a single line_ in the text file "puzzle.txt"

Four primary elements:
- 'F' = fire
- 'E' = earth
- 'A' = air
- 'W' = water

Special elements:
- 'S' = salt
- 'Q' = quicksilver
- 'M' = mors
- 'V' = vitae

Metals, listed in order of precedence:
- 'L' = lead
- 'T' = tin
- 'I' = iron
- 'C' = copper
- 'K' = silver
- 'G' = gold

If there is no element on a given tile, write 'N'.

For instance, this game of Sigmar's Garden:
![Example Puzzle](example_puzzle.png)

Would be transcribed _exactly_ as:
`NNNNNNNFMAEANNLSQEEWNNKEAANNQWVNNAQFNGNWEENNEFVNNWQQNNVSWMFAANNVCTMFWNNFMSFENNNNNNN`

After transcribing the puzzle, run solver.py. After at most a minute, a series of hex grids with certain elements highlighted will be printed. These are the move sequences for solving the puzzle. Matching the highlighted elements for each move will solve the puzzle.
