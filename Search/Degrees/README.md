# Degrees

A program that determines how many "degrees of separation" apart two hollywood actors are. Each degree consists of a film that two actors both starred in

## Background

According to the [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon) game, anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in

In this problem, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13”

We can frame this as a search problem: our states are people. Our actions are movies, which take us from one actor to another (a movie could take us to multiple different actors, but that’s okay for this problem). Our initial and goal states are defined by the two people we’re trying to connect. By using breadth-first search, we can find the shortest path from one actor to another

## Files

There is a set of data, the `small` folder. That contains three CSV files, `people.csv`, `movies.csv`, and `stars.csv`.<br/>

- `Movies.csv` contains information on each movie's assigned ID, its title and release year
- `People.csv` contains information about each Hollywood movie star's unique ID, corresponding to their ID in the IMDb's database, with their name and birth year
- `Stars.csv` establishes a relationship between the movie stars in the `people.csv` and movies in `movies.csv`, stating which person starred in which movie

The main program is written in the `degrees.py` file, which utilizes some useful classes and functions in the `util.py` file

## How to Use

In the `degrees` directory, run the command

`python degrees.py dataset`

Where dataset is the name of the dataset folder

## Example Output

```shell
$ python degrees.py large
Loading data...
Data loaded.
Name: Emma Watson
Name: Jennifer Lawrence
3 degrees of separation.
1: Emma Watson and Brendan Gleeson starred in Harry Potter and the Order of the Phoenix
2: Brendan Gleeson and Michael Fassbender starred in Trespass Against Us
3: Michael Fassbender and Jennifer Lawrence starred in X-Men: First Class
```

## Acknowledgements

Information courtesy of [IMDb](https://www.imdb.com/). Used with permission.
