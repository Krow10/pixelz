# Pixelz

A pixel fighting game running in the terminal. Inspired by the work of [**Jan Tewes Thede (@jtthede)**](https://pixelsfighting.com/).

## Running the game

Make sure your terminal is maximized for maximum fightingz

`$ python -m pixelz` or `$ python pixelz/__main__.py`

### Controls

- `[SPACE]`: Pause/Unpause simulation. While paused, press any other key to advance to the next step.
- `i/I`: Show the ratio of squares on the grid. Lower number corresponds to initial left-side winning and vice-versa (the color of the text will change according the currently winning color).
- `s/S`: Cycle through pixel sprites to change pixelz appearance. Add you own to the `PIXEL_SPRITES` variable [here](pixelz/__main__.py#L9).
- `q/Q`: Quit the program.

## TODO
- [ ] More / cleaner statistics
- [ ] Better simulation with biais / randomness controls
- [ ] Edit initial setup
- [ ] Keep track of board history
- [ ] Increase number of players
- [ ] Allow for players to team up
- [ ] Add immutable / destroyable walls
- [ ] Add random events
- [ ] Handle empty tiles (allowing player movements !)