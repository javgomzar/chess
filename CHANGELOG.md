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
