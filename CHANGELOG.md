# CHESS APP - CHANGELOG (DEV)
In this document we will include all substantial changes to the app.

### The versioning of the app will be done as following:
- **v1.x.x** - Main version of the app
- **v1.1.x** - Important changes
- **v1.1.1** - Minor changes

### There will be the following classification for changes:
- `ADDED`: For new functionalities.
- `MODIFIED`: For changes to existing functionalities.
- `DEPRECATED`: For functionalities that will no longer be available.
- `FIXED`: For fixed errors.
- `SECURITY`: For fixed vulnerabilities.


## [1.1.0] - 2022/05/10
## `ADDED`
- Custom error classes
- `game_modes` folder will support in the future different game modes like anti-chess.
## `MODIFIED`
- Checks will be managed by a separate class.
- Big refactoring of code using design patterns.
- Chain of responsability pattern implemented in order to manage move requests and decide if rules apply.
- Strategy pattern for movements of each piece.
- Board actions are now a separate class `Action`, which can be one of `Move`, `Castle`, `Promote` or `En Passant`.
- Each action has an `undo` and `redo` method.
- `ActionController` manages action history, previous boards and undo/redo functionalities.
- Board class has a new parent class hierarchy involving `PieceManager` and `ActionController`
- `PieceManager` adds, removes and replaces pieces on the board.
- `Game` class now in principle can have a `GameMode`. The standard chess rules are in the class `Standard`. Different game modes have not been tried but code should be ready to implement them.
- Implemented the three-fold repetition tie rule in the class `Repetition`, and the fifty moves tie rule in `FiftyMoves`.
- Started the implementation of the dead position tie rule.
- Simplified `README.md`.
- Added testing.
- Players have now a class to manage input and output. Needs improving in the future.

## [1.0.4] - 2021/11/12
## `ADDED`
- Added media folder with `.png` images for the board and chess pieces.
- Added the `image()` methods to the classes `Board` and `Piece`
## `FIXED`
- Fixed the dates in `CHANGELOG.md`.
## `DELETED`
- Deleted the Jupyter notebook file `interactive_notebook.ipynb`.

## [1.0.3] - 2021/11/01
### `ADDED`
- Added a Jupyter Notebook file called `interactive_notebook.ipynb` to be able to interact with the code without downloading it.

## [1.0.2] - 2021/11/01
### `ADDED`
- First version for `README.md`.
### `MODIFIED`
- Changed the `__str__` method in `Piece.py`.
- `is_finished` is now a class attribute in `Game.py`.

## [1.0.1] - 2021/10/29
### `MODIFIED`
- Minor change to square input.

## [1.0.0] - 2021/10/29
### `ADDED`
- First semi-stable version for a chess game with control over the two players. Thorough testing is needed.
### `DEPRECATED`
- Turn class is not needed.
### `MODIFIED`
- `main.py` location changed.
- `.gitignore` simplified.
