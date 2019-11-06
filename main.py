import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds


class UserProfile:
    valid_genres = ["Fiction", "Young Adult", "Science Fiction", "Dystopia", "Fantasy", "Classics", "Academic", "Romance"]

    def __init__(self, inp_id):
        self.id = inp_id
        self.book_ratings = {}
        self.preferred_genres = []

    def print_info(self):
        print("UserID: " + self.id)
        print(self.preferred_genres)
        print(self.book_ratings)

    def add_book_rating(self, inp_book, inp_rating):
        self.book_ratings[inp_book] = inp_rating

    def add_genre_preference(self, inp_genre):
        self.preferred_genres.append(inp_genre)


def recommend_book():
    # TODO add recommendation function

    # find all books user has already rated
    # if have rated all, return that no new books

    # with unrated books
    # go through and recommend from them

    print("Recommended book is: ")


def add_user():
    # TODO add add_user function
    # get new user details
    # check if user already exists
    # add new user to list of lists?
    # use objects to store users?
    print("blah")


def update_user():
    # TODO add update_user function
    # check user exists
    # update relevant attribute
    print("blah")


def user_profile():
    # TODO add logging in function
    # like logging in??
    # object users are same as table users! or else how does it work
    print("blah")


def main_program():
    test_user = UserProfile("1234")
    test_user.add_genre_preference("Fiction")
    test_user.add_genre_preference("Dystopia")
    test_user.add_book_rating("Little Red Riding Hood", 4)

    print("Would you like to: "
          "\n1.Log in as a specific user"
          "\n2.Create a  new user profile"
          "\n3.Edit a user profile")
    menu_option = str(input("Please enter 1, 2 or 3: "))

    print("menu_choice = " + menu_option)

    if menu_option == "1":
        input_id = str(input("Please enter the userID: "))
        # TODO add input_id validation
        print("Log in successful")
        test_user.print_info()


raw_books = pd.read_csv("data/books.csv")
# print(raw_books.head())
# print("---------------")
# print(raw_books.info())

raw_ratings = pd.read_csv("data/ratings.csv")
# print(raw_ratings.head())
# print("---------------")
# print(raw_ratings.info())

print("---------------")
main_program()



