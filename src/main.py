import pandas as pd
from libs import search, system


if __name__ == "__main__":
    print("Starting server...")
    system.mkdirs()
    print("Computing metadata: TF and IFD")
    system.compute_metadata()
    print("Encrypting documents")
    system.encrypt_docs()

    try:
        while True:
            query = input("Search> ")
            results = search.find_docs(query)
            results_df = pd.DataFrame(results, columns=["Document", "Score"])
            print(results_df)
            while True:
                doc_id = input("Open (q to exit)> ")
                if doc_id == "q":
                    break
                doc = results_df.iloc[int(doc_id)]["Document"]
                # Decrypt document and open with webbrowser
                print("Opening ", doc)
                system.open_doc(doc)
    except KeyboardInterrupt:
        print()
        print("Shutting down server...")
        system.cleanup()
        print("Goodbye!")
