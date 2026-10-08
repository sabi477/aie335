"""Lab 01, step 4 - SERVE. Shows the result and exports it for a consumer."""
import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).parent


def main():
    sys.stdout.reconfigure(encoding="utf-8")    # the table borders need UTF-8 (matters on Windows)
    con = duckdb.connect(str(HERE / "aie335.duckdb"), read_only=True)   # serving only reads

    # serving 1: show the result on the screen, for the person who runs the pipeline
    print("serve: revenue by product category (top 10)")
    con.sql("SELECT * FROM revenue_by_category LIMIT 10").show()

    # serving 2: export the whole table as a file, for someone who has no database
    out = HERE / "output"
    out.mkdir(exist_ok=True)                    # create output/ if it is not there yet
    target = out / "revenue_by_category.csv"
    con.execute(f"COPY revenue_by_category TO '{target.as_posix()}' (HEADER)")   # HEADER = column names in line 1
    print(f"serve: wrote output/{target.name}")

    # serving 3: show top products
    print("\nserve: top 10 best-selling products")
    con.sql("SELECT * FROM top_products").show()

    target_top = out / "top_products.csv"
    con.execute(f"COPY top_products TO '{target_top.as_posix()}' (HEADER)")
    print(f"serve: wrote output/{target_top.name}")

    # serving 4: revenue by state
    print("\nserve: revenue by state (top 10)")
    con.sql("SELECT * FROM revenue_by_state LIMIT 10").show()

    target_state = out / "revenue_by_state.csv"
    con.execute(f"COPY revenue_by_state TO '{target_state.as_posix()}' (HEADER)")
    print(f"serve: wrote output/{target_state.name}")


if __name__ == "__main__":
    main()