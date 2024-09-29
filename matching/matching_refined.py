import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from concurrent.futures import ThreadPoolExecutor
import psycopg2
import time
import pandas as pd

# Function for advanced text normalization

def normalize_title(article):
    text = article[1].lower()
    text = re.sub(r'[^\w\s]', '', article[1])  # Remove punctuation
    text = re.sub(r'\s+', ' ', article[1])     # Remove extra whitespace
    return text.strip()

# Function to process normalization in parallel
def normalize_texts(articles):
    with ThreadPoolExecutor() as executor:
        normalized_texts = list(executor.map(normalize_title, articles))
    return normalized_texts

def filter_similar_titles_blockwise(articles, threshold=0.9, block_size=10000):
    start = time.time()
    normalized_titles = normalize_texts(articles)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(normalized_titles)

    n = tfidf_matrix.shape[0]
    unique_articles = []
    seen_indices = set()

    for i in range(0, n, block_size):
        print(f"{time.time() - start} ------- {i}")
        # Process the TF-IDF matrix in blocks of 'block_size'
        tfidf_block = tfidf_matrix[i:i + block_size]

        # Compute cosine similarity for the current block against the entire matrix
        cos_sim_block = cosine_similarity(tfidf_block, tfidf_matrix)

        # Iterate over each title in the current block
        for j in range(tfidf_block.shape[0]):
            title_index = i + j  # Actual index in the full dataset
            if title_index in seen_indices:
                continue
            unique_articles.append(articles[title_index])

            # Find similar titles within the block based on threshold
            similar_indices = np.where(cos_sim_block[j] >= threshold)[0]
            if(len(similar_indices) > 1):
                for index in similar_indices:
                    if(index != title_index):
                        title = articles[title_index][1]
                        unique_articles.append((articles[index][0], title, articles[index][2], articles[index][3], articles[index][4], articles[index][5]))
            seen_indices.update(similar_indices)

    return unique_articles

start = time.time()
conn = psycopg2.connect("dbname=Scholars_Updated user=postgres password=root host=localhost port=5432")
cur = conn.cursor()

cur.execute("select * from articles WHERE length(articles.title) > 10 order by articles.title asc limit 100000")
articles = cur.fetchall()

# Filter titles based on similarity threshold
filtered_articles = filter_similar_titles_blockwise(articles)
cur.execute("""CREATE TABLE IF NOT EXISTS articles_refined(
                id integer references scholars,
                title varchar(1000) not null,
                national varchar(600),
                referee varchar(600),
                index varchar(600),
                category varchar(600)
    );""")

for article in filtered_articles:
        cur.execute("INSERT INTO articles_refined (id, title, national, referee, index, category) VALUES (%s, %s, %s, %s, %s, %s)", 
                (article[0], article[1], article[2], article[3], article[4], article[5]))
conn.commit()
cur.close()
conn.close()
print(time.time() - start)