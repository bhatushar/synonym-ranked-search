import pandas as pd
from libs import startup, search


if __name__ == "__main__":
    print("Starting server...")
    startup.mkdirs()
    print("Computing metadata: TF and IFD")
    startup.compute_metadata()
    print("Encrypting documents")
    startup.encrypt_docs()

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
                startup.open_doc(doc)
    except KeyboardInterrupt:
        print()
        print("Shutting down server...")
        startup.cleanup()
        print("Goodbye!")
