
# Backend Challenge

## Contents

* [Quickuse Guide](#quickuse-guide)
* [Implementation Details](#implementation-details)
* [Endpoints](#endpoints)

<!--- If we have only one group/collection, then no need for the "ungrouped" heading -->

## Quickuse Guide
1. Run `bootstrap.py` to populate the database with data from `clubs.json` and webpage
2. Run `app.py` to activate the server running on local host. Make sure to use this local host displayed on console in all requests.
3. See documentation below or `app.py` for how to run GET, PUT, POST requests. Alternatively, use Postman with the button below.  
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/f57a73efe7f391e1b5a3?action=collection%2Fimport)
4. Stop running `app.py` to close the server

## Implementation Details
`models.py`:
- Models the data
- Contains three data types: User, Club, Tag
    - Tags are treated as separate objects to enable access to clubs associated with a tag
- Each class has a method `as_json()` that returns the object in json serializable format
    - This makes GET request implementation easier
- Uses many-to-many relationship with back referencing for (1) clubs and tags and (2) user favorites and clubs
    - Many-to-many relationships enable easy access on both ends

`bootstrap.py`:
- Generates the initial databaase
- [BONUS] Uses webscraping on the html file of the clubs website
    - Uses BeautifulSpoon
    - For each webscraped club, a new code is generated using a simple algorithm in `generate_code(club_name)`

`app.py`:
- Activates the server, and contains the various routes for requests
- For ease of data access, GET requests require no json
- For PUT and POST requests, json is required only for new data
    - For ease of convention, this is why the specific club/user being modified is included in the route, not json
- Everytime a club is created with tags or a club's tags are modified, `process_tags(tag_names)` will add any brand-new tags to the database
- [BONUS] Route caching using `flask-caching` is employed for the following routes:
    - Get all clubs: expensive query that will be called frequently (ex: Penn Labs homepage)
    - Get all tags: this is also an expensive query as it involves iterating through all clubs in each tag
    - Get specific tag: since the number of tags is relatively small, memoizing this information provides speed improvements without using too much memory
    - Routes involving user search and club search are not cached
        - There are a high amount of clubs and users and it is unlikely the exact same query will be used repeatedly in a short span

`auth.py`:
- Handles user authentication, including signup, login, and logout
- Uses `flask-login`
- For user signup, the provided password is hashed and then stored for security purposes
- For user login, the hash of the provided password is compared with the hash of the actual one
    - This makes the process completely secure as the plaintext password is never exposed
- Only the currently logged in user can have its data modified
    - Allowing anyone to alter any user's information would be insecure

## Endpoints

* [Clubs](#clubs)
    1. [Get Clubs](#1-get-clubs)
    1. [Create New Club](#2-create-new-club)
    1. [Search for Club](#3-search-for-club)
    1. [Modify Club](#4-modify-club)
* [Tags](#tags)
    1. [Get Tags](#1-get-tags)
    1. [Get Specific Tag](#2-get-specific-tag)
* [Users](#users)
    1. [Get User](#1-get-user)
    1. [Create New User](#2-create-new-user)
    1. [Login User](#3-login-user)
    1. [Logout Current User](#4-logout-current-user)
    1. [Get Current User](#5-get-current-user)

--------



## Clubs

You can get all clubs, search for a club, and modify a club.



### 1. Get Clubs


Gets a list of all clubs. For each club, the following data is included: club code, name, description, tags associated with the club, and number of users who have favorited the club.


***Endpoint:***

```bash
Method: GET
URL: http://localhost/api/clubs
```



### 2. Create New Club


Creates a new club. Request must include a json file with the format below (note the required fields).


***Endpoint:***

```bash
Method: POST
URL: http://localhost/api/clubs
```



***Body:***

```js        
{
    "code": "code of club (required)",
    "name": "name of club (required)",
    "description": "club description",
    "tags": [
        "tag 1 of club", 
        "tag 2 of club"
    ]
}
```



### 3. Search for Club


Fetches all clubs whose name contains the `<search_text>`, case ignorant. Returns the same data for each club as the Get Clubs request.


***Endpoint:***

```bash
Method: GET
URL: http://localhost/api/clubs/<search_text>
```



### 4. Modify Club


Modifies the club with the `<club_code>`. `<club_code>` must match exactly. If no club with the provided code is found, an error is thrown. Request can contain one or more of the fields in the sample json below.


***Endpoint:***

```bash
Method: PUT
URL: http://localhost/api/clubs/<club_code>
```



***Body:***

```js        
{
    "name": "new name of club",
    "description": "new description of club",
    "tags": [
        "new tag 1 of club",
        "new tag 2 of club"
    ]
}
```



## Tags



### 1. Get Tags


Gets all tags. For each tag, gets the number and names of clubs that are associated with that tag.


***Endpoint:***

```bash
Method: GET
URL: http://localhost/api/tags
```



### 2. Get Specific Tag


Gets the data for tag with name `<tag_name>`. `<tag_name>` must match exactly to the desired tag, case ignorant. If a tag is found, then the number and names of clubs that are associated with that tag are returned.


***Endpoint:***

```bash
Method: GET
URL: http://localhost/api/tags/<tag_name>
```



## Users



### 1. Get User


Gets the data for the user with the exact `<username>` provided, case ignorant. The user's username, name, email, year, and favorited clubs are returned.


***Endpoint:***

```bash
Method: GET
URL: http://localhost/api/users/<username>
```



### 2. Create New User


Creates a brand new user. Request must follow the json format below (note the required fields).


***Endpoint:***

```bash
Method: POST
URL: http://localhost/auth/signup
```



***Body:***

```js        
{
    "user": "username (required)",
    "name": "name of user (required)",
    "password": "user's password (required)",
    "year": 1,
    "email": "user's email"
}
```



### 3. Login User


Logs in the user with the provided username and password. Both the username and password must match exactly.


***Endpoint:***

```bash
Method: POST
URL: http://localhost/auth/login
```



***Body:***

```js        
{
    "user": "username (required and must match exactly)",
    "password": "user password (required and must match exactly)"
}
```



### 4. Logout Current User


Logs out the current user. A user must already be logged in for this to be called.


***Endpoint:***

```bash
Method: POST
URL: http://localhost/auth/logout
```



### 5. Get Current User


Gets the data for the user currently logged in. A user must already be logged in for this to be called. Returns the user's username, name, email, year, and favorited clubs.


***Endpoint:***

```bash
Method: GET
URL: http://localhost/auth/profile
```



---
[Back to top](#backend-challenge)
