import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds


def recommend_book():
    print("Recommended book is: ")


raw_books = pd.read_csv("data/books.csv")
print(raw_books.head())
print("---------------")
print(raw_books.info())

raw_ratings = pd.read_csv("data/ratings.csv")
print(raw_ratings.head())
print("---------------")
print(raw_ratings.info())

recommend_book()
