# -*- coding: utf-8 -*-
"""Untitled23.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11tgIDgYOSuOf3ucmuphomPUXcBAcSff2
"""

#2 reading

from sklearn.datasets import fetch_20newsgroups
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the dataset
newsgroups = fetch_20newsgroups(subset='all')

# Tokenization
tokens = word_tokenize(newsgroups.data[0])
print("Tokenized Text:\n", tokens)

# Stop Word Removal
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word.lower() not in stop_words and word.isalnum()]
print("\nAfter Stop Word Removal:\n", filtered_tokens)

# Stemming
stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
print("\nAfter Stemming:\n", stemmed_tokens)

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
print("\nAfter Lemmatization:\n", lemmatized_tokens)

#2 ex
import spacy
from nltk.stem.porter import PorterStemmer

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Initialize NLTK stemmer (spaCy doesn't include a stemmer)
stemmer = PorterStemmer()

# Sample text
text = "The striped bats are hanging on their feet for best"

# Process the text with spaCy
doc = nlp(text)

# Tokenization
tokens = [token.text for token in doc]
print("Tokens:", tokens)

# Stop word removal
no_stop_words = [token for token in doc if not token.is_stop]
print("After Stop Word Removal:", [token.text for token in no_stop_words])

# Lemmatization
lemmatized = [token.lemma_ for token in no_stop_words]
print("Lemmatized:", lemmatized)

# Stemming (using NLTK, since spaCy doesn’t provide stemming)
stemmed = [stemmer.stem(token.text) for token in no_stop_words]
print("Stemmed:", stemmed)

#3
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd

# Sample data
corpus = [
    "The quick brown fox jumps over the lazy dog",
    "Never jump over the lazy dog quickly"
]


ohe = OneHotEncoder(sparse_output=False)
char_data = list("quick")  # example word for one-hot encoding
char_encoded = ohe.fit_transform(np.array(char_data).reshape(-1, 1))
print("One-Hot Encoding (char-level example):")
print(pd.DataFrame(char_encoded, columns=ohe.categories_[0]))

vectorizer = CountVectorizer()
bow = vectorizer.fit_transform(corpus)
print("\nBag of Words:")
print(pd.DataFrame(bow.toarray(), columns=vectorizer.get_feature_names_out()))


tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(corpus)
print("\nTF-IDF:")
print(pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out()))

bigram_vectorizer = CountVectorizer(ngram_range=(2, 2))
bigrams = bigram_vectorizer.fit_transform(corpus)
print("\nBigrams (2-grams):")
print(pd.DataFrame(bigrams.toarray(), columns=bigram_vectorizer.get_feature_names_out()))

!pip install gensim



#4
#http://nlp.stanford.edu/data/glove.6B.zip for glove
#alice.txt:- https://www.gutenberg.org/files/11/11-0.txt
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

with open("/content/alice.txt", encoding='utf-8') as file:
    text = file.read()

text = text.replace('\n', ' ')
sentences = sent_tokenize(text)
tokenized_sentences = [[word.lower() for word in word_tokenize(sent)] for sent in sentences]

cbow_model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, sg=0)

sg_model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, sg=1)

print("CBOW similarity (alice vs wonderland):", cbow_model.wv.similarity('alice', 'wonderland'))
print("Skip-Gram similarity (alice vs wonderland):", sg_model.wv.similarity('alice', 'wonderland'))

flat_text = [' '.join(sentence) for sentence in tokenized_sentences]
tokenizer = Tokenizer()
tokenizer.fit_on_texts(flat_text)

word_index = tokenizer.word_index

def load_glove_embeddings(glove_path, word_index, embedding_dim=50):
    embedding_matrix = np.zeros((len(word_index) + 1, embedding_dim))
    with open(glove_path, encoding='utf8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            if word in word_index:
                idx = word_index[word]
                embedding_matrix[idx] = vector
    return embedding_matrix

glove_path = '/content/glove.6B.50d.txt'
embedding_matrix = load_glove_embeddings(glove_path, word_index)

print("GloVe vector for 'alice':", embedding_matrix[word_index['alice']])

#5
import spacy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Sample dataset
data = {
    "text": [
        "I love this product!",
        "This is the worst thing I have ever bought.",
        "Absolutely fantastic experience.",
        "I'm so disappointed with the service.",
        "Highly recommend to everyone.",
        "Terrible. Just terrible.",
        "Great value for money.",
        "Not worth the price.",
        "Amazing quality!",
        "I will never buy this again."
    ],
    "label": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1 = positive, 0 = negative
}
df = pd.DataFrame(data)

# Preprocessing function using spaCy
def preprocess(text):
    doc = nlp(text)
    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and token.is_alpha
    ]
    return " ".join(tokens)

# Apply preprocessing
df["clean_text"] = df["text"].apply(preprocess)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df["clean_text"], df["label"], test_size=0.2, random_state=42)

# TF-IDF vectorization
tfidf = TfidfVectorizer()
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# -------------------------
# Logistic Regression
# -------------------------
lr_model = LogisticRegression()
lr_model.fit(X_train_tfidf, y_train)
lr_preds = lr_model.predict(X_test_tfidf)

print("=== Logistic Regression ===")
print("Classification Report:\n", classification_report(y_test, lr_preds))
print("Confusion Matrix:\n", confusion_matrix(y_test, lr_preds))

# -------------------------
# Random Forest
# -------------------------
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_tfidf, y_train)
rf_preds = rf_model.predict(X_test_tfidf)

print("\n=== Random Forest ===")
print("Classification Report:\n", classification_report(y_test, rf_preds))
print("Confusion Matrix:\n", confusion_matrix(y_test, rf_preds))

#6
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, GRU, Conv1D, GlobalMaxPooling1D, Dense
from sklearn.metrics import classification_report, confusion_matrix

# -------------------------------
# Load IMDb dataset
# -------------------------------
vocab_size = 10000  # Use top 10,000 words
maxlen = 200        # Max length of each review

(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)

# Pad sequences to make them the same length
X_train = pad_sequences(X_train, maxlen=maxlen)
X_test = pad_sequences(X_test, maxlen=maxlen)

# -------------------------------
# LSTM Model
# -------------------------------
def build_lstm_model():
    model = Sequential([
        Embedding(vocab_size, 64, input_length=maxlen),
        LSTM(64),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# -------------------------------
# GRU Model
# -------------------------------
def build_gru_model():
    model = Sequential([
        Embedding(vocab_size, 64, input_length=maxlen),
        GRU(64),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# -------------------------------
# CNN Model
# -------------------------------
def build_cnn_model():
    model = Sequential([
        Embedding(vocab_size, 64, input_length=maxlen),
        Conv1D(64, kernel_size=3, activation='relu'),
        GlobalMaxPooling1D(),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# -------------------------------
# Train and evaluate each model
# -------------------------------
def train_and_evaluate(model_fn, name):
    print(f"\n=== Training {name} ===")
    model = model_fn()
    model.fit(X_train, y_train, epochs=3, batch_size=128, validation_split=0.2, verbose=2)
    preds = (model.predict(X_test) > 0.5).astype("int32")

    print(f"\n{name} Classification Report:")
    print(classification_report(y_test, preds))
    print(f"{name} Confusion Matrix:")
    print(confusion_matrix(y_test, preds))

# Run all 3 models
train_and_evaluate(build_lstm_model, "LSTM")
train_and_evaluate(build_gru_model, "GRU")
train_and_evaluate(build_cnn_model, "CNN")

#7
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, GlobalAveragePooling1D, LayerNormalization, Dropout, MultiHeadAttention, Layer
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# ----------------------------
# Load and preprocess IMDb data
# ----------------------------
vocab_size = 10000
maxlen = 200

(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)
X_train = pad_sequences(X_train, maxlen=maxlen)
X_test = pad_sequences(X_test, maxlen=maxlen)



# ----------------------------
# Build Self-Attention Model
# ----------------------------
def build_self_attention_model():
    inputs = Input(shape=(maxlen,))
    x = Embedding(vocab_size, 64)(inputs)
    x = SelfAttention(64)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(1, activation='sigmoid')(x)
    model = Model(inputs, outputs)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# ----------------------------
# Build Multi-Head Attention Model
# ----------------------------
def build_multi_head_attention_model():
    inputs = Input(shape=(maxlen,))
    x = Embedding(vocab_size, 64)(inputs)
    attn_output = MultiHeadAttention(num_heads=2, key_dim=64)(x, x)
    x = LayerNormalization()(x + attn_output)  # residual connection
    x = GlobalAveragePooling1D()(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(1, activation='sigmoid')(x)
    model = Model(inputs, outputs)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# ----------------------------
# Train and Evaluate
# ----------------------------
def train_and_evaluate(model_fn, name):
    print(f"\n=== Training {name} ===")
    model = model_fn()
    model.fit(X_train, y_train, epochs=3, batch_size=128, validation_split=0.2, verbose=2)
    preds = (model.predict(X_test) > 0.5).astype("int32")

    print(f"\n{name} Classification Report:")
    print(classification_report(y_test, preds))
    print(f"{name} Confusion Matrix:")
    print(confusion_matrix(y_test, preds))

# Run both models
train_and_evaluate(build_self_attention_model, "Self-Attention")
train_and_evaluate(build_multi_head_attention_model, "Multi-Head Attention")

!pip install --upgrade datasets huggingface_hub

#8
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from datasets import load_dataset
import tensorflow as tf
from transformers import pipeline
import numpy as np
from sklearn.model_selection import train_test_split # Added this import
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, GlobalAveragePooling1D, LayerNormalization, Dropout, MultiHeadAttention, Layer


dataset = load_dataset("cnn_dailymail", "3.0.0", split="train[:10%]", download_mode="force_redownload")

maxlen = 300  # Adjust based on your needs
vocab_size = 5000  # Common vocab size for text classification

tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(dataset['article'])
sequences = tokenizer.texts_to_sequences(dataset['article'])
padded = pad_sequences(sequences, padding='post', maxlen=maxlen)


y = [1 if 'breaking' in article.lower() else 0 for article in dataset['article']]

# Train-test split
# The import was added above
X_train, X_test, y_train, y_test = train_test_split(padded, y, test_size=0.2, random_state=42)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Split training data further into training and validation
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

print("\n📘 Training Transformer-based Classifier...\n")

# --- Transformer Model Definition ---
inputs = Input(shape=(maxlen,))
x = Embedding(vocab_size, 64)(inputs)

# Transformer Block
attn_output = MultiHeadAttention(num_heads=2, key_dim=32)(x, x)
x = LayerNormalization()(x + attn_output) # Add and Norm (residual connection)
x_ff = Dense(64, activation='relu')(x) # Feed-Forward Network
x = LayerNormalization()(x + x_ff) # Add and Norm

x = GlobalAveragePooling1D()(x) # Pooling layer after transformer block
x = Dropout(0.1)(x)
outputs = Dense(1, activation='sigmoid')(x) # Output layer

transformer_model = Model(inputs, outputs)

# Compile and Train
transformer_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
transformer_model.fit(X_train, y_train, epochs=1, batch_size=64, validation_data=(X_val, y_val))

from sklearn.metrics import classification_report, confusion_matrix
preds = (transformer_model.predict(X_test) > 0.5).astype("int32")
print("\nTransformer Model Classification Report:")
print(classification_report(y_test, preds))
print("\nTransformer Model Confusion Matrix:")
print(confusion_matrix(y_test, preds))

#9
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from datasets import load_dataset
import tensorflow as tf
from transformers import pipeline

# 📘 Load the CNN/DailyMail Dataset (for both classification and summarization)
dataset = load_dataset("cnn_dailymail", "3.0.0", split="train[:10%]")  # Using a small portion for quick testing

# Preprocessing
maxlen = 300  # Adjust based on your needs
vocab_size = 5000  # Common vocab size for text classification

# Tokenization and Padding for both tasks
tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(dataset['article'])
sequences = tokenizer.texts_to_sequences(dataset['article'])
padded = pad_sequences(sequences, padding='post', maxlen=maxlen)

# Labels for classification (Can be 'topic' or 'category' if available)
# For simplicity, let's use binary classification: spam vs not-spam (just for this example)
y = [1 if 'breaking' in article.lower() else 0 for article in dataset['article']]

# Split into train-test for classification task
X_train, X_test, y_train, y_test = train_test_split(padded, y, test_size=0.2, random_state=42)

# 📘 Summarization Pipeline using Hugging Face
summarizer = pipeline("summarization")

# 📄 Run summarization on articles from the dataset
for i, sample in enumerate(dataset):
    if i > 3:  # Limiting to 4 samples for quick testing
        break
    print(f"\n📰 Article {i+1}:\n")
    print(sample['article'][:300] + "...\n")  # Show first 300 characters

    # Summarizing the article
    summary = summarizer(sample['article'], max_length=40, min_length=15, do_sample=False)

    print("📗 Generated Summary:\n")
    print(summary[0]['summary_text'])

#10
from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

# Generate text from a prompt
prompt = "Once upon a time in a distant future,"
output = generator(prompt, max_length=50, num_return_sequences=1)

print("🔹 Generated Text (GPT-2):\n")
print(output[0]['generated_text'])