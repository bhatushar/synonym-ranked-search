import pandas as pd
import time
from libs import env, search, system


if __name__ == "__main__":
    system.mkdirs()
    system.cleanup_deleted()
    system.check_changes()
    system.compute_metadata()
    system.encrypt_docs()
    df = pd.read_csv(env.QUERIES_PATH)
    rank_dev = 0
    duration = 0
    for _, row in df.iterrows():
        file = row["Files"]
        query = row["Queries"]
        start = time.perf_counter()
        results = search.find_docs(query)
        duration += time.perf_counter() - start
        rank = -1
        for search_file, score in results:
            rank += 1
            if search_file == file:
                break
        rank_dev += rank**2
    tests = len(df.index)
    mse = rank_dev / tests
    avg_time = duration / tests
    print("Average search time:", avg_time, "sec")
    print("Mean Squared Error:", mse)
