import pandas as pd
import numpy as np
import sqlite3
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds


def recommend_book():
    # TODO add recommendation function

    # find all books user has already rated
    # if have rated all, return that no new books

    # with unrated books
    # go through and recommend from them

    print("Recommended book is: ")


def validate_user_id(inp_id):
    print(inp_id)


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


def generate_rec_table():
    print("Blahh")


def main_program():
    print("Would you like to: "
          "\n1.Log in as a specific user"
          "\n2.Create a  new user profile"
          "\n3.Edit a user profile")
    menu_option = str(input("Please enter 1, 2 or 3: "))
    # TODO add menu validation
    print("menu_choice = " + menu_option)

    if menu_option == "1":
        input_id = str(input("Please enter the userID: "))
        validate_user_id(input_id)
        print("Log in successful")


main_program()