import requests
from bs4 import BeautifulSoup
import re
import psycopg2

# Function to extract Persian sentences from a webpage
def extract_persian_sentences_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Assuming Persian text is in <p> tags with a specific class or id, adjust as per your website structure
    persian_paragraphs = soup.find_all('p', class_='persian-text')  # Adjust class name as needed
    sentences = []
    for p in persian_paragraphs:
        sentences.extend(re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', p.text))
    return sentences

# Function to filter sentences with more than 5 words
def filter_long_sentences(sentences):
    return [sentence for sentence in sentences if len(sentence.split()) > 5]

# Function to store sentences in PostgreSQL
def store_sentences_in_postgres(sentences):
    conn = psycopg2.connect(
        dbname="first_project",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    for sentence in sentences:
        cur.execute("INSERT INTO sentences (sentence) VALUES (%s)", (sentence,))
    conn.commit()
    cur.close()
    conn.close()

# List of Persian websites
website_urls = ['https://snn.ir', 'https://varzesh3.com']

# Container to store all Persian sentences from all websites
all_persian_sentences = []

# Scrape each website and extract Persian sentences
for url in website_urls:
    persian_sentences = extract_persian_sentences_from_website(url)
    all_persian_sentences.extend(persian_sentences)

# Filter sentences with more than 5 words
filtered_sentences = filter_long_sentences(all_persian_sentences)

# Store filtered sentences in PostgreSQL
store_sentences_in_postgres(filtered_sentences)