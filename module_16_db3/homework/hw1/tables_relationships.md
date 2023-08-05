## Tables Relationships in "film_database.db" file

1. `director` - `movie`: many-to-many. The table `movie_direction` is an intermediary one. The director can have many movies and the movie can have many directors.
2. `movie` - `actor`: many-to-many. The table `movie_cast` is an intermediary one. The movie can have many actors and the actor can star in many movies.
3. `movie` - `oscar_awarded`: one-to-many. The film can have many awards but the award corresponds to the only one film.
