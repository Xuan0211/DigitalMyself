

def localSearch(problem: str):
    import os
    import sys
    import pandas as pd
    from pathlib import Path
    from similarities import BertSimilarity
    import globalSetting
    from fileManager import FileManager
    sys.path.append('..')
    
    # 1. Read all csv files in the output folder
    file_manager = FileManager()
    enableFileList = file_manager.getEnableFileList()
    
    csv_files = []
    for file in enableFileList:
        file = list(file)
        csv_files.append(globalSetting.OUTPUT_FOLDER + str(file[0]) + ".csv")
    
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
