import pandas as pd
import numpy as np
import sqlite3
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds


def recommend_book(inp_id):
    df_preds, df_og_ratings, df_og_books = generate_rec_table()
    user_has_rated = already_rated(inp_id)
    user_predictions = df_preds.iloc[inp_id - 1].sort_values(ascending=False)
    merged_predictions = pd.merge(user_has_rated, user_predictions, on='book_title', how='outer')
    predictions_not_rated = merged_predictions[merged_predictions['user_id'] != str(inp_id)]

    top_five = predictions_not_rated.iloc[:5]

    before_genres = top_five.iloc[:3]
    before_genres = before_genres['book_title']
    before_genres = before_genres.tolist()
    for a in before_genres:
        print(a)
    print("")
    print("---------------------")

    titles_to_genres = top_five['book_title']
    titles_to_genres = titles_to_genres.tolist()

    increase = fave_genres(inp_id, titles_to_genres)

    top_five.columns = ['user_id', 'book_id', 'book_title', 'prediction']
    top_five.index = ['a', 'b', 'c', 'd', 'e']

    counter = 0

    for row in ['a', 'b', 'c', 'd', 'e']:
        if increase[counter]:
            top_five.at[row, 'prediction'] = top_five.at[row, 'prediction'] + 1
        counter = counter + 1

    top_five = top_five.sort_values('prediction', ascending=False)

    top_three = top_five.iloc[:3]
    top_three = top_three['book_title']
    top_three = top_three.tolist()
    for book in top_three:
        print(book)
    print("")


def fave_genres(genre_id, books):
    connection = sqlite3.connect('book_recommender.db')
    cursor = connection.cursor()

    all_preferences = pd.read_sql_query("SELECT * FROM Preferences", connection)

    connection.commit()
    connection.close()

    user_preferences = all_preferences.loc[all_preferences['user_id'] == str(genre_id)]
    user_preferences = user_preferences['genres'].tolist()
    user_preferences = user_preferences[0]
    user_preferences = user_preferences.split("|")

    connection = sqlite3.connect('book_recommender.db')
    cursor = connection.cursor()

    all_genres = pd.read_sql_query("SELECT book_title, book_genres FROM Books", connection)
    connection.commit()
    connection.close()

    book_genres = []
    for book in books:
        book_genre = all_genres.loc[all_genres['book_title'] == str(book)]
        book_genre = book_genre['book_genres'].tolist()
        book_genres.append(book_genre[0])

    increase = []
    for x in range(5):
        is_fave = False
        for genre in user_preferences:
            if genre in book_genres[x]:
                is_fave = True

        increase.append(is_fave)

    return(increase)


def already_rated(inp_id):
    connection = sqlite3.connect('book_recommender.db')
    cursor = connection.cursor()

    has_rated = pd.read_sql_query("SELECT user_id, book_id FROM Ratings", connection)
    user_rated = has_rated.loc[has_rated['user_id'] == str(inp_id)]

    connection.commit()
    connection.close()

    connection = sqlite3.connect('book_recommender.db')
    cursor = connection.cursor()

    id_to_title = pd.read_sql_query("SELECT book_id, book_title FROM Books", connection)

    connection.commit()
    connection.close()

    user_rated_ids = pd.merge(user_rated, id_to_title, on='book_id')

    return user_rated_ids


def validate_user_id(inp_id):
    connection = sqlite3.connect('book_recommender.db')
    cursor = connection.cursor()

    user_ids = pd.read_sql_query("SELECT user_id FROM Ratings", connection)

    connection.commit()
    connection.close()

    user_ids = user_ids['user_id'].tolist()
    user_ids = set(user_ids)

    if str(inp_id) in user_ids:
        return True
    else:
        return False


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
    connection = sqlite3.connect('book_recommender.db')
    cursor = connection.cursor()

    df_books = pd.read_sql_query("SELECT * FROM Books", connection)
    df_ratings = pd.read_sql_query("SELECT * FROM Ratings", connection)

    book_data = pd.merge(df_ratings, df_books, on='book_id')

    df_books_ratings = book_data.pivot_table(index='user_id', columns='book_title', values='rating').fillna(0)
    books_ratings_matrix = df_books_ratings.to_numpy()

    books_ratings_mean = np.mean(books_ratings_matrix, axis=1)
    ratings_demeaned = books_ratings_matrix - books_ratings_mean.reshape(-1, 1)
    u, s, vt = svds(ratings_demeaned, k=50)
    s = np.diag(s)

    all_predicted_ratings = np.dot(np.dot(u, s), vt) + books_ratings_mean.reshape(-1, 1)
    df_predictions = pd.DataFrame(all_predicted_ratings, columns=df_books_ratings.columns)

    connection.commit()
    connection.close()

    return df_predictions, df_ratings, df_books


def generic_recommendation():
    connection = sqlite3.connect('book_recommender.db')
    cursor = connection.cursor()

    df_books = pd.read_sql_query("SELECT * FROM Books", connection)
    df_ratings = pd.read_sql_query("SELECT * FROM Ratings", connection)

    book_data = pd.merge(df_ratings, df_books, on='book_id')

    highest_rated = book_data.groupby('book_title')['rating'].agg(['count', 'mean']).reset_index()
    highest_rated = highest_rated.sort_values('mean', ascending=False)
    highest_rated = highest_rated.iloc[:3]
    highest_rated = highest_rated['book_title']

    highest_rated = highest_rated.tolist()
    for book in highest_rated:
        print(book)
    print("")


running = True

while running:

    print("Would you like to: "
          "\n1. Log in as a specific user"
          "\n2. Create a new user profile"
          "\n3. Get a generic recommendation"
          "\n4. Quit")

    menu_option = str(input("\nPlease enter 1, 2, 3 or 4: "))

    if menu_option == "1":
        input_id = input("\nPlease enter the userID: ")
        user_id_valid = validate_user_id(input_id)

        if user_id_valid:
            print("\nVALID USER ID")

            print("\nWould you like to: "
                  "\n1. Get a recommendation"
                  "\n2. Add a favourite genre"
                  "\n3. Rate a book")
            user_option = str(input("\nPlease enter 1, 2 or 3: "))

            if user_option == "1":
                print("\nRECOMMENDATIONS FOR USER " + str(input_id) + " : ")
                recommend_book(int(input_id))

            elif user_option == "2":
                new_genre = str(input("\nPlease enter the genre you would like to add: "))

            elif user_option == "3":
                print("\nRATE A BOOK")

            else:
                print("\nINVALID CHOICE MADE")
        else:
            print("\nINVALID USER ID")

    elif menu_option == "2":
        print("\nCREATE A NEW USER PROFILE")

    elif menu_option == "3":
        print("\nOVERALL HIGHEST RATED/RECOMMENDED: \n")
        generic_recommendation()

    elif menu_option == "4":
        running = False

    else:
        print("\nINVALID MENU CHOICE")
