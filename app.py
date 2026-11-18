import argparse
import json
import math
import sqlite3


def vector(text):
    try:
        values = [float(v) for v in text.split(",")]
        norm = math.hypot(*values)
        if not math.isfinite(norm) or norm == 0:
            raise ValueError()
        return [x/norm for x in values]
    except ValueError:
        raise argparse.ArgumentTypeError("Enter finite comma-separated coordinates with nonzero length.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Store vectors and search them by cosine similarity.")
    parser.add_argument("--db", default="vectors.sqlite")
    commands = parser.add_subparsers(dest="action", required=True)
    add = commands.add_parser("put")
    add.add_argument("label")
    add.add_argument("vector", type=vector)
    commands.add_parser("search").add_argument("vector", type=vector)
    args = parser.parse_args()
    with sqlite3.connect(args.db) as db:
        db.execute("CREATE TABLE IF NOT EXISTS vectors(label TEXT PRIMARY KEY, coords TEXT)")
        db.execute("BEGIN IMMEDIATE")
        first = db.execute("SELECT coords FROM vectors LIMIT 1").fetchone()
        if first and len(json.loads(first[0])) != len(args.vector):
            parser.error("Vector dimensions must match this database.")
        if args.action == "put":
            db.execute("INSERT OR REPLACE INTO vectors VALUES (?,?)", (args.label, json.dumps(args.vector)))
        else:
            scores = []
            for label, raw in db.execute("SELECT label,coords FROM vectors ORDER BY label"):
                score = sum(x*y for x, y in zip(args.vector, json.loads(raw)))
                scores.append((score, label))
            for score, label in sorted(scores, key=lambda row: -row[0])[:5]:
                print(f"{score:.4f}\t{label}")
