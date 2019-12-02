import pandas as pd
import numpy as np
from scipy.sparse import csc_matrix
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


def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
    # Get and sort the user's predictions
    user_row_number = userID - 1  # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.user_id == (userID)]
    user_full = (user_data.merge(movies_df, how='left', left_on='book_id', right_on='book_id').
                 sort_values(['rating'], ascending=False)
                 )

    print
    'User {0} has already rated {1} movies.'.format(userID, user_full.shape[0])
    print
    'Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations)

    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies_df[~movies_df['book_id'].isin(user_full['book_id'])].
                           merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
                                 left_on='book_id',
                                 right_on='book_id').
                           rename(columns={user_row_number: 'Predictions'}).
                           sort_values('Predictions', ascending=False).
                           iloc[:num_recommendations, :-1]
                           )

    return user_full, recommendations



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

        print("Log in successful")
        test_user.print_info()


df_books = pd.read_csv("data/books.csv")
df_ratings = pd.read_csv("data/ratings.csv")
df_books['book_id'] = df_books['book_id'].apply(pd.to_numeric)

book_data = pd.merge(df_ratings, df_books, on='book_id')

df_books_ratings = book_data.pivot_table(index='user_id', columns='book_title', values='rating').fillna(0)
books_ratings_matrix = df_books_ratings.to_numpy()

books_ratings_mean = np.mean(books_ratings_matrix, axis=1)
ratings_demeaned = books_ratings_matrix - books_ratings_mean.reshape(-1, 1)
u, s, vt = svds(ratings_demeaned, k=50)
s = np.diag(s)

all_predicted_ratings = np.dot(np.dot(u, s), vt) + books_ratings_mean.reshape(-1, 1)
df_predictions = pd.DataFrame(all_predicted_ratings, columns=df_books_ratings.columns)

print(df_predictions.head())
print("---------------")

already_rated, predictions = recommend_movies(df_predictions, 1, df_books, df_ratings, 10)
