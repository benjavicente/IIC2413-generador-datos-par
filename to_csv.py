import os
import subprocess as sp

DB = "games.db"
OUR_DIR = "data"

def main():
    os.makedirs(OUR_DIR, exist_ok=True)
    tables = sp.check_output(["sqlite3", DB, ".tables"])
    for table in map(bytes.decode, tables.split()):
        sp.run([
            "sqlite3", DB,
            ".mode csv",
            ".headers on",
            f".output {OUR_DIR}/{table}.csv",
            f"SELECT * FROM {table};",
            ".exit"
        ])

if __name__ == "__main__":
    main()
