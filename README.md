# django-json-api-project

Extending the search functionality of [Breaking-Bad--API](https://github.com/timbiles/Breaking-Bad--API) (i.e. searching multiple characters)

## Endpoints
### Original
```
/api/characters?name=Walter+White
```
Original API only retrives one search result. It also has a search function, e.g. searching ```walt``` will return ```Walter White``` and ```Walter White Jr```.
### Extended
```
/api/characters?names=walt,tod,pinkman
```
Notice I am searching for multiple names. The search names parameter is in the form of comma seperated list of names. My API makes calls to the original and returns a condensed list of the results.

## Why?
Just trying to learn Django and APIs. I could have created a PR on the original API and added my changes but I wanted build something from scratch to really learn.