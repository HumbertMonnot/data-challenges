# pylint: disable=C0103, missing-docstring

from statistics import mean

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    db.execute("SELECT movies.title, movies.genres, directors.name FROM movies \
        JOIN directors ON movies.director_id = directors.id")
    return db.fetchall()


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    db.execute("SELECT movies.title FROM movies \
        JOIN directors ON movies.director_id = directors.id \
        WHERE movies.start_year > directors.death_year")
    list_film = []
    for k in db.fetchall():
        list_film.append(k[0])
    return list_film


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query = f'SELECT movies.minutes, movies.rating FROM movies WHERE genres = "{genre_name}"'
    db.execute(query)
    results = db.fetchall()
    mean_time = round(mean([k[0] for k in results]),2)
    number_of_movies = len(results)
    dict_stat = {'genre': genre_name, 'avg_length': mean_time, 'number_of_movies':number_of_movies}
    return dict_stat


def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = f"""SELECT directors.name, COUNT(title) FROM movies JOIN directors ON \
        movies.director_id = directors.id WHERE genres = "{genre_name}" GROUP BY \
            director_id ORDER BY COUNT(title) DESC, directors.name"""
    db.execute(query)
    return db.fetchall()[:5]

def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    list_duration = []
    compteur_film = 0
    for duree in range(30,1021,30):
        query = f"""SELECT count(title) FROM movies WHERE minutes <{duree}"""
        db.execute(query)
        results = db.fetchone()[0]
        results_duree = results - compteur_film
        if results_duree != 0:
            list_duration.append((duree, results_duree))
            compteur_film += results_duree
    return list_duration


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = """SELECT directors.name, movies.start_year - directors.birth_year \
        FROM movies\
        JOIN directors ON movies.director_id = directors.id\
        WHERE movies.start_year-directors.birth_year > 0\
        ORDER BY movies.start_year-directors.birth_year """
    db.execute(query)
    return db.fetchall()[:5]
