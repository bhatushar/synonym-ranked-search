import pandas as pd
from libs import env, search, system


if __name__ == "__main__":
    system.mkdirs()
    system.cleanup_deleted()
    system.check_changes()
    system.compute_metadata()
    system.encrypt_docs()
    df = pd.read_csv(env.QUERIES_PATH)
    rank_dev = 0
    for _, row in df.iterrows():
        file = row["Files"]
        query = row["Queries"]
        results = search.find_docs(query)

        rank = -1
        for search_file, score in results:
            rank += 1
            if search_file == file:
                break
        rank_dev += rank**2
    tests = len(df.index)
    mse = rank_dev / tests
    print("Mean Squared Error: ", mse)
