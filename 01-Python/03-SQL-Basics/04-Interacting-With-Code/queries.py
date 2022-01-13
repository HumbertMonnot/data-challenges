# pylint: disable=missing-docstring, C0103

def directors_count(db):
    # return the number of directors contained in the database
    query = "SELECT COUNT(*) FROM directors"
    db.execute(query)
    count = db.fetchone()
    return count[0]

def directors_list(db):
    # return the list of all the directors sorted in alphabetical order
    query = "SELECT name FROM directors"
    db.execute(query)
    directors_name = db.fetchall()
    list_directors = []
    for k in directors_name:
        list_directors.append(k[0])
    return sorted(list_directors)

def love_movies(db):
    # return the list of all movies which contain the word "love" in
    # their title, sorted in alphabetical order
    query = "SELECT title FROM movies WHERE UPPER(title) LIKE '%LOVE%'"
    db.execute(query)
    love_titles = db.fetchall()
    list_love = []
    for k in love_titles:
        list_love.append(k[0])
    return sorted(list_love)


def directors_named_like_count(db, name):
    # return the number of directors which contain a given word in their name
    query = f"SELECT COUNT(*) FROM directors WHERE UPPER(name) LIKE '%{name}%'"
    db.execute(query)
    count = db.fetchone()
    return count[0]

def movies_longer_than(db, min_length):
    # return this list of all movies which are longer than a given
    # duration, sorted in the alphabetical order
    query = f"SELECT title FROM movies WHERE minutes>{min_length}"
    db.execute(query)
    film_minute = db.fetchall()
    list_film = []
    for k in film_minute:
        list_film.append(k[0])
    return sorted(list_film)
