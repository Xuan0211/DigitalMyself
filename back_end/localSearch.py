

def localSearch(problem: str):
    import sys
    import pandas as pd
    from pathlib import Path
    from similarities import BertSimilarity
    sys.path.append('..')
    LOCAL_PATH = str(Path(__file__).parent)

    # 1. Read all csv files in the output folder
    output_folder = LOCAL_PATH + '/store/databank/output'
    csv_files = Path(output_folder).rglob('*.csv')
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file, header=None)
        dfs.append(df)

    # 2. Concatenate all DataFrames into a single DataFrame
    concatenated_df = pd.concat(dfs)

    # 3. Compute cosine similarity between two sentences
    sentences = [problem]
    corpus = concatenated_df.iloc[:, 0].tolist()
    model = BertSimilarity(model_name_or_path="shibing624/text2vec-base-chinese")
    similarity_scores = model.similarity(sentences, corpus)

    # 4. Semantic Search
    model.add_corpus(corpus)

    res = []
    for i in list(model.search(sentences[0], topn=3)[0].keys()):
        res.append(corpus[i])
    return res

if __name__ == '__main__':
    print(localSearch('参考书是什么'))
