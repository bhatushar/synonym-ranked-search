import os
import pandas as pd
import random
from libs import env


files: list[str] = []
queries: list[str] = []
for doc in os.listdir(env.DOCS_PATH):
    with open(f"{env.DOCS_PATH}/{doc}", "r", encoding="utf-8") as file:
        file_stat = os.stat(f"{env.DOCS_PATH}/{doc}")
        for _ in range(random.randrange(5, 10)):
            query = ""
            offset = random.randint(0, file_stat.st_size - 100)
            file.seek(offset)
            file.readline()  # Ignore partial line
            while len(query) < 20:  # Ignore short lines
                query = file.readline().strip()
            files.append(doc)
            queries.append(query)
df = pd.DataFrame({"Files": files, "Queries": queries})
df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the rows
df.to_csv(env.QUERIES_PATH)
