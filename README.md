

# Book_Review

#### 15/06/2020
#### By **Jorim Midumbi Okong'o Opondo, Rose Kairu, Paul Mburu Njuguna, Ian Mdawida, James Maina Mirara**

## Description
This is a book review website. Users will be able to register here and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. We will also use a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via this website’s API.


You can view the site at:[Heroku]()


## Screenshot
![Personal-dev-Blog]()



## User Stories
These are the behaviours/features that the application implements depending on the selection made by a user.

* *Registration*: Users are be able to register.
* *Login*: Users, once registered, should be able to log in to the website with their username and password.
* *Logout*: Logged in users should be able to log out of the site.
* *Search*: Once a user has logged in, they are taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, the website displays a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, search page should find matches for those as well!
* *Book Page*: When users click on a book details from the results of the search page, they are taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on the website.
* *Review Submission*: On the book page, users are be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users won't be able to submit multiple reviews for the same book.
* *Goodreads Review Data*: On the book details page, users are able to see the average rating and number of ratings the work has received from Goodreads.

# API Access

Reviewer API allows developers access to Book Reviews data in order to help other websites or applications that deal with books be more personalized, social and engaging.

## API methods

`/api/<isbn>` - where `<isbn>` is a 10 digit ISBN number. This GET request returns a JSON response containing the book's title, author, publication date, ISBN number, review count, and average score. Example format:
``` json
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
```


## Specifications

| Behaviour | Input | Output |
| :---------------- | :---------------: | ------------------: |
| Load the page | **On page load** | Get all reviews, Select between signup and login|
| Select SignUp| **Email**,**Username**,**Password** | Redirect to login|
| Select Login | **Username** and **password** | Redirect to page with reviews that have been posted by contributors and be able to subscribe to the blog|
| Select comment button | **Comment** | Form that you input your comment|
| Click on submit |  | Redirect to all comments template with your comment and other comments|
|Subscription | **Email Address**| Flash message "Succesfully subsbribed to Book_Review"|



## Development Installation

To get the code..

1. Cloning the repository:
  ```bash
  https://github.com/JORIM1981/Books_review.git
    ```
2. Move to the folder and install requirements
  ```bash
  cd Book_review
  pip install -r requirements.txt
  ```
3. Exporting Configurations
  ```bash
  export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://{User Name}:{password}@localhost/{database name}
  ```
4. Running the application
  ```bash
  python3.8 manage.py server
  ```
5. Testing the application
  ```bash
  python3.8 manage.py test
  ```
Open the application on your browser `127.0.0.1:5000`.


## Technology used

* [Python3.8](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Heroku](https://heroku.com)


## Known Bugs
* There are no known bugs currently but pull requests are allowed incase you spot a bug

## Contact Information 

If you have any question or contributions, please email us at [okongo.midumbi.opondo@gmail.com, rosekairu@gmail.com, paulmburu08@gmail.com, mdawidamengo@gmail.com, mirarajames29@gmail.com]

## License:

- _MIT License:_[LICENSE MIT](./LICENSE)

- Copyright (c) 2020 **Jorim Midumbi Okongo Opondo**


