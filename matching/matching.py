from rapidfuzz import fuzz
import psycopg2
import time
import re

def normalize_title(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)     # Remove extra whitespace
    return text.strip()

threshold = 95
conn = psycopg2.connect("dbname=Scholars_Updated user=postgres password=root host=localhost port=5432")
cur = conn.cursor()

cur.execute("select * from articles")
articles = cur.fetchall()

filtered = [articles[0]] 
start = time.time()

for index, article in enumerate(articles):
    normalized_title = normalize_title(article[1])
    is_different = True
    for element in filtered:
        similarity = fuzz.ratio(normalize_title(normalized_title), normalize_title(element[1]))
        if(similarity >= threshold):
            is_different = False
            break
    if(is_different): filtered.append(article)
    print(f"{time.time() - start} ------- {index}")

print(len(filtered))