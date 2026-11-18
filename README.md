# SQLite vector search

The first vector sets the dimension. A second put with the same label replaces its vector. Search scans all rows and prints the closest five.

## Run locally

Use Python 3.8 or newer. Run these commands in the project directory.

```sh
python app.py put roller 1,0
python app.py put handle 0,1
python app.py search 1,0
```

Run `python app.py --help` for options and `python -m unittest -v` to check the command-line workflow.
