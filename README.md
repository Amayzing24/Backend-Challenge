
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

***Sample Output***
```bash
[
    {
        "code": "pppjo",
        "description": "The PPPJO is looking for intense jugglers seeking to juggle their way to the top. Come with your juggling equipment (and business formal attire) to hone your skills in time for recruiting season!",
        "favorited": 0,
        "name": "Penn Pre-Professional Juggling Organization",
        "tags": [
            "Pre-Professional",
            "Athletics",
            "Undergraduate"
        ]
    },
    {
        "code": "lorem-ipsum",
        "description": "Join our club if you're interested in dolor, or sit amet!",
        "favorited": 0,
        "name": "Penn Lorem Ipsum Club",
        "tags": [
            "Undergraduate",
            "Literary"
        ]
    },
    {
        "code": "penn-memes",
        "description": "We love memes!",
        "favorited": 0,
        "name": "Penn Memes Club",
        "tags": [
            "Graduate",
            "Literary"
        ]
    },
    {
        "code": "pppp",
        "description": "Ever considered yourself a possible procrastinator, but never actually were able to get the motivation to determine for sure? Then join PPPP, Penn's premier potential procrastinating society! We are seeking unmotivated individuals who, in theory, are interested in joining our group, but can't quite get themselves to start working on our application. Start applying today so that you can procrastinate on the application and ultimately miss the deadline",
        "favorited": 0,
        "name": "Penn Program for Potential Procrastinators",
        "tags": [
            "Undergraduate",
            "Academic"
        ]
    },
    {
        "code": "locustlabs",
        "description": "The club that makes your favourite software!",
        "favorited": 0,
        "name": "Locust Labs",
        "tags": [
            "Undergraduate",
            "Graduate",
            "Technology"
        ]
    },
    {
        "code": "pmiotmlaac",
        "description": "We do things related with Microservice, Internet of Things, Machine Learning, and Actionable Analytics!",
        "favorited": 0,
        "name": "Penn Microservice Internet of Things Machine Learning Actionable Analytics Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "pbqcaadmc",
        "description": "We do things related with Blockchain, Quantum Computing, Actionable Analytics, and Data Mining!",
        "favorited": 0,
        "name": "Penn Blockchain Quantum Computing Actionable Analytics Data Mining Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "emqciotrc",
        "description": "We do things related with Microservice, Quantum Computing, Internet of Things, and Robotics!",
        "favorited": 0,
        "name": "Engineering Microservice Quantum Computing Internet of Things Robotics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "ndmarmlbdc",
        "description": "We do things related with Data Mining, Augmented Reality, Machine Learning, and Big Data!",
        "favorited": 0,
        "name": "Nursing Data Mining Augmented Reality Machine Learning Big Data Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "eaimarmlc",
        "description": "We do things related with Artificial Intelligence, Microservice, Augmented Reality, and Machine Learning!",
        "favorited": 0,
        "name": "Engineering Artificial Intelligence Microservice Augmented Reality Machine Learning Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pmlqcaiarc",
        "description": "We do things related with Machine Learning, Quantum Computing, Artificial Intelligence, and Augmented Reality!",
        "favorited": 0,
        "name": "Penn Machine Learning Quantum Computing Artificial Intelligence Augmented Reality Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "emvrbdarc",
        "description": "We do things related with Microservice, Virtual Reality, Big Data, and Augmented Reality!",
        "favorited": 0,
        "name": "Engineering Microservice Virtual Reality Big Data Augmented Reality Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "carmiotaac",
        "description": "We do things related with Augmented Reality, Microservice, Internet of Things, and Actionable Analytics!",
        "favorited": 0,
        "name": "College Augmented Reality Microservice Internet of Things Actionable Analytics Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "wdmvrairc",
        "description": "We do things related with Data Mining, Virtual Reality, Artificial Intelligence, and Robotics!",
        "favorited": 0,
        "name": "Wharton Data Mining Virtual Reality Artificial Intelligence Robotics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "paaaibddmc",
        "description": "We do things related with Actionable Analytics, Artificial Intelligence, Big Data, and Data Mining!",
        "favorited": 0,
        "name": "Penn Actionable Analytics Artificial Intelligence Big Data Data Mining Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "wbdbrqcc",
        "description": "We do things related with Big Data, Blockchain, Robotics, and Quantum Computing!",
        "favorited": 0,
        "name": "Wharton Big Data Blockchain Robotics Quantum Computing Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "wiotmldmarc",
        "description": "We do things related with Internet of Things, Machine Learning, Data Mining, and Augmented Reality!",
        "favorited": 0,
        "name": "Wharton Internet of Things Machine Learning Data Mining Augmented Reality Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "nbardmmlc",
        "description": "We do things related with Blockchain, Augmented Reality, Data Mining, and Machine Learning!",
        "favorited": 0,
        "name": "Nursing Blockchain Augmented Reality Data Mining Machine Learning Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "wmlaadmmc",
        "description": "We do things related with Machine Learning, Actionable Analytics, Data Mining, and Microservice!",
        "favorited": 0,
        "name": "Wharton Machine Learning Actionable Analytics Data Mining Microservice Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "emlmaadmc",
        "description": "We do things related with Machine Learning, Microservice, Actionable Analytics, and Data Mining!",
        "favorited": 0,
        "name": "Engineering Machine Learning Microservice Actionable Analytics Data Mining Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "earmlbiotc",
        "description": "We do things related with Augmented Reality, Machine Learning, Blockchain, and Internet of Things!",
        "favorited": 0,
        "name": "Engineering Augmented Reality Machine Learning Blockchain Internet of Things Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "pdmrmaic",
        "description": "We do things related with Data Mining, Robotics, Microservice, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Penn Data Mining Robotics Microservice Artificial Intelligence Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "wiotbdmbc",
        "description": "We do things related with Internet of Things, Big Data, Microservice, and Blockchain!",
        "favorited": 0,
        "name": "Wharton Internet of Things Big Data Microservice Blockchain Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "nvrairaac",
        "description": "We do things related with Virtual Reality, Artificial Intelligence, Robotics, and Actionable Analytics!",
        "favorited": 0,
        "name": "Nursing Virtual Reality Artificial Intelligence Robotics Actionable Analytics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "nbdmmliotc",
        "description": "We do things related with Big Data, Microservice, Machine Learning, and Internet of Things!",
        "favorited": 0,
        "name": "Nursing Big Data Microservice Machine Learning Internet of Things Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "pbdmlqcbc",
        "description": "We do things related with Big Data, Machine Learning, Quantum Computing, and Blockchain!",
        "favorited": 0,
        "name": "Penn Big Data Machine Learning Quantum Computing Blockchain Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wbqcvraic",
        "description": "We do things related with Blockchain, Quantum Computing, Virtual Reality, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Wharton Blockchain Quantum Computing Virtual Reality Artificial Intelligence Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "eiotbqcvrc",
        "description": "We do things related with Internet of Things, Blockchain, Quantum Computing, and Virtual Reality!",
        "favorited": 0,
        "name": "Engineering Internet of Things Blockchain Quantum Computing Virtual Reality Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "cvrmlarmc",
        "description": "We do things related with Virtual Reality, Machine Learning, Augmented Reality, and Microservice!",
        "favorited": 0,
        "name": "College Virtual Reality Machine Learning Augmented Reality Microservice Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "paadmmlbdc",
        "description": "We do things related with Actionable Analytics, Data Mining, Machine Learning, and Big Data!",
        "favorited": 0,
        "name": "Penn Actionable Analytics Data Mining Machine Learning Big Data Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "wvraimbdc",
        "description": "We do things related with Virtual Reality, Artificial Intelligence, Microservice, and Big Data!",
        "favorited": 0,
        "name": "Wharton Virtual Reality Artificial Intelligence Microservice Big Data Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "waaiotdmaic",
        "description": "We do things related with Actionable Analytics, Internet of Things, Data Mining, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Wharton Actionable Analytics Internet of Things Data Mining Artificial Intelligence Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "paidmqcmc",
        "description": "We do things related with Artificial Intelligence, Data Mining, Quantum Computing, and Microservice!",
        "favorited": 0,
        "name": "Penn Artificial Intelligence Data Mining Quantum Computing Microservice Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wiotaaarvrc",
        "description": "We do things related with Internet of Things, Actionable Analytics, Augmented Reality, and Virtual Reality!",
        "favorited": 0,
        "name": "Wharton Internet of Things Actionable Analytics Augmented Reality Virtual Reality Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "eqcbdaraac",
        "description": "We do things related with Quantum Computing, Big Data, Augmented Reality, and Actionable Analytics!",
        "favorited": 0,
        "name": "Engineering Quantum Computing Big Data Augmented Reality Actionable Analytics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "cbarbdiotc",
        "description": "We do things related with Blockchain, Augmented Reality, Big Data, and Internet of Things!",
        "favorited": 0,
        "name": "College Blockchain Augmented Reality Big Data Internet of Things Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wqcbdaiiotc",
        "description": "We do things related with Quantum Computing, Big Data, Artificial Intelligence, and Internet of Things!",
        "favorited": 0,
        "name": "Wharton Quantum Computing Big Data Artificial Intelligence Internet of Things Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "eiotdmbqcc",
        "description": "We do things related with Internet of Things, Data Mining, Blockchain, and Quantum Computing!",
        "favorited": 0,
        "name": "Engineering Internet of Things Data Mining Blockchain Quantum Computing Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "emmlairc",
        "description": "We do things related with Microservice, Machine Learning, Artificial Intelligence, and Robotics!",
        "favorited": 0,
        "name": "Engineering Microservice Machine Learning Artificial Intelligence Robotics Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "emldmmqcc",
        "description": "We do things related with Machine Learning, Data Mining, Microservice, and Quantum Computing!",
        "favorited": 0,
        "name": "Engineering Machine Learning Data Mining Microservice Quantum Computing Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "ebaiqcmc",
        "description": "We do things related with Blockchain, Artificial Intelligence, Quantum Computing, and Microservice!",
        "favorited": 0,
        "name": "Engineering Blockchain Artificial Intelligence Quantum Computing Microservice Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "pdmqcaiaac",
        "description": "We do things related with Data Mining, Quantum Computing, Artificial Intelligence, and Actionable Analytics!",
        "favorited": 0,
        "name": "Penn Data Mining Quantum Computing Artificial Intelligence Actionable Analytics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "ciotbrdmc",
        "description": "We do things related with Internet of Things, Blockchain, Robotics, and Data Mining!",
        "favorited": 0,
        "name": "College Internet of Things Blockchain Robotics Data Mining Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "emlarvrbc",
        "description": "We do things related with Machine Learning, Augmented Reality, Virtual Reality, and Blockchain!",
        "favorited": 0,
        "name": "Engineering Machine Learning Augmented Reality Virtual Reality Blockchain Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "ndmbdaimlc",
        "description": "We do things related with Data Mining, Big Data, Artificial Intelligence, and Machine Learning!",
        "favorited": 0,
        "name": "Nursing Data Mining Big Data Artificial Intelligence Machine Learning Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "pbmdmqcc",
        "description": "We do things related with Blockchain, Microservice, Data Mining, and Quantum Computing!",
        "favorited": 0,
        "name": "Penn Blockchain Microservice Data Mining Quantum Computing Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "ciotrdmvrc",
        "description": "We do things related with Internet of Things, Robotics, Data Mining, and Virtual Reality!",
        "favorited": 0,
        "name": "College Internet of Things Robotics Data Mining Virtual Reality Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "erqcbbdc",
        "description": "We do things related with Robotics, Quantum Computing, Blockchain, and Big Data!",
        "favorited": 0,
        "name": "Engineering Robotics Quantum Computing Blockchain Big Data Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "nrbarbdc",
        "description": "We do things related with Robotics, Blockchain, Augmented Reality, and Big Data!",
        "favorited": 0,
        "name": "Nursing Robotics Blockchain Augmented Reality Big Data Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "naiiotdmrc",
        "description": "We do things related with Artificial Intelligence, Internet of Things, Data Mining, and Robotics!",
        "favorited": 0,
        "name": "Nursing Artificial Intelligence Internet of Things Data Mining Robotics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "piotvrraac",
        "description": "We do things related with Internet of Things, Virtual Reality, Robotics, and Actionable Analytics!",
        "favorited": 0,
        "name": "Penn Internet of Things Virtual Reality Robotics Actionable Analytics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wvrmldmrc",
        "description": "We do things related with Virtual Reality, Machine Learning, Data Mining, and Robotics!",
        "favorited": 0,
        "name": "Wharton Virtual Reality Machine Learning Data Mining Robotics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "cbdvrriotc",
        "description": "We do things related with Big Data, Virtual Reality, Robotics, and Internet of Things!",
        "favorited": 0,
        "name": "College Big Data Virtual Reality Robotics Internet of Things Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "nrariotdmc",
        "description": "We do things related with Robotics, Augmented Reality, Internet of Things, and Data Mining!",
        "favorited": 0,
        "name": "Nursing Robotics Augmented Reality Internet of Things Data Mining Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "eaaqciotmlc",
        "description": "We do things related with Actionable Analytics, Quantum Computing, Internet of Things, and Machine Learning!",
        "favorited": 0,
        "name": "Engineering Actionable Analytics Quantum Computing Internet of Things Machine Learning Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "prbdiotvrc",
        "description": "We do things related with Robotics, Big Data, Internet of Things, and Virtual Reality!",
        "favorited": 0,
        "name": "Penn Robotics Big Data Internet of Things Virtual Reality Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "nbmarbdc",
        "description": "We do things related with Blockchain, Microservice, Augmented Reality, and Big Data!",
        "favorited": 0,
        "name": "Nursing Blockchain Microservice Augmented Reality Big Data Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "parmbdqcc",
        "description": "We do things related with Augmented Reality, Microservice, Big Data, and Quantum Computing!",
        "favorited": 0,
        "name": "Penn Augmented Reality Microservice Big Data Quantum Computing Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "cairqciotc",
        "description": "We do things related with Artificial Intelligence, Robotics, Quantum Computing, and Internet of Things!",
        "favorited": 0,
        "name": "College Artificial Intelligence Robotics Quantum Computing Internet of Things Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "eaabqcdmc",
        "description": "We do things related with Actionable Analytics, Blockchain, Quantum Computing, and Data Mining!",
        "favorited": 0,
        "name": "Engineering Actionable Analytics Blockchain Quantum Computing Data Mining Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "ndmaiqcmc",
        "description": "We do things related with Data Mining, Artificial Intelligence, Quantum Computing, and Microservice!",
        "favorited": 0,
        "name": "Nursing Data Mining Artificial Intelligence Quantum Computing Microservice Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "pbvrmarc",
        "description": "We do things related with Blockchain, Virtual Reality, Microservice, and Augmented Reality!",
        "favorited": 0,
        "name": "Penn Blockchain Virtual Reality Microservice Augmented Reality Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "waimarqcc",
        "description": "We do things related with Artificial Intelligence, Microservice, Augmented Reality, and Quantum Computing!",
        "favorited": 0,
        "name": "Wharton Artificial Intelligence Microservice Augmented Reality Quantum Computing Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "narriotmlc",
        "description": "We do things related with Augmented Reality, Robotics, Internet of Things, and Machine Learning!",
        "favorited": 0,
        "name": "Nursing Augmented Reality Robotics Internet of Things Machine Learning Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "pqcrbarc",
        "description": "We do things related with Quantum Computing, Robotics, Blockchain, and Augmented Reality!",
        "favorited": 0,
        "name": "Penn Quantum Computing Robotics Blockchain Augmented Reality Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "wvrbdaiqcc",
        "description": "We do things related with Virtual Reality, Big Data, Artificial Intelligence, and Quantum Computing!",
        "favorited": 0,
        "name": "Wharton Virtual Reality Big Data Artificial Intelligence Quantum Computing Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "wiotarbaac",
        "description": "We do things related with Internet of Things, Augmented Reality, Blockchain, and Actionable Analytics!",
        "favorited": 0,
        "name": "Wharton Internet of Things Augmented Reality Blockchain Actionable Analytics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "prmaiaac",
        "description": "We do things related with Robotics, Microservice, Artificial Intelligence, and Actionable Analytics!",
        "favorited": 0,
        "name": "Penn Robotics Microservice Artificial Intelligence Actionable Analytics Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "cbrmaic",
        "description": "We do things related with Blockchain, Robotics, Microservice, and Artificial Intelligence!",
        "favorited": 0,
        "name": "College Blockchain Robotics Microservice Artificial Intelligence Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "crvrmlbdc",
        "description": "We do things related with Robotics, Virtual Reality, Machine Learning, and Big Data!",
        "favorited": 0,
        "name": "College Robotics Virtual Reality Machine Learning Big Data Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wriotvraac",
        "description": "We do things related with Robotics, Internet of Things, Virtual Reality, and Actionable Analytics!",
        "favorited": 0,
        "name": "Wharton Robotics Internet of Things Virtual Reality Actionable Analytics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "edmmaarc",
        "description": "We do things related with Data Mining, Microservice, Actionable Analytics, and Robotics!",
        "favorited": 0,
        "name": "Engineering Data Mining Microservice Actionable Analytics Robotics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "wrbiotmc",
        "description": "We do things related with Robotics, Blockchain, Internet of Things, and Microservice!",
        "favorited": 0,
        "name": "Wharton Robotics Blockchain Internet of Things Microservice Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "pmbaabdc",
        "description": "We do things related with Microservice, Blockchain, Actionable Analytics, and Big Data!",
        "favorited": 0,
        "name": "Penn Microservice Blockchain Actionable Analytics Big Data Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "caimbddmc",
        "description": "We do things related with Artificial Intelligence, Microservice, Big Data, and Data Mining!",
        "favorited": 0,
        "name": "College Artificial Intelligence Microservice Big Data Data Mining Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "nmqciotbc",
        "description": "We do things related with Microservice, Quantum Computing, Internet of Things, and Blockchain!",
        "favorited": 0,
        "name": "Nursing Microservice Quantum Computing Internet of Things Blockchain Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pbrmvrc",
        "description": "We do things related with Blockchain, Robotics, Microservice, and Virtual Reality!",
        "favorited": 0,
        "name": "Penn Blockchain Robotics Microservice Virtual Reality Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "wdmiotbdrc",
        "description": "We do things related with Data Mining, Internet of Things, Big Data, and Robotics!",
        "favorited": 0,
        "name": "Wharton Data Mining Internet of Things Big Data Robotics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "wqcvrbaic",
        "description": "We do things related with Quantum Computing, Virtual Reality, Blockchain, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Wharton Quantum Computing Virtual Reality Blockchain Artificial Intelligence Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "paibdaavrc",
        "description": "We do things related with Artificial Intelligence, Big Data, Actionable Analytics, and Virtual Reality!",
        "favorited": 0,
        "name": "Penn Artificial Intelligence Big Data Actionable Analytics Virtual Reality Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "ndmmlaivrc",
        "description": "We do things related with Data Mining, Machine Learning, Artificial Intelligence, and Virtual Reality!",
        "favorited": 0,
        "name": "Nursing Data Mining Machine Learning Artificial Intelligence Virtual Reality Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wdmmlaabdc",
        "description": "We do things related with Data Mining, Machine Learning, Actionable Analytics, and Big Data!",
        "favorited": 0,
        "name": "Wharton Data Mining Machine Learning Actionable Analytics Big Data Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "piotmlbdrc",
        "description": "We do things related with Internet of Things, Machine Learning, Big Data, and Robotics!",
        "favorited": 0,
        "name": "Penn Internet of Things Machine Learning Big Data Robotics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "nqcvrmmlc",
        "description": "We do things related with Quantum Computing, Virtual Reality, Microservice, and Machine Learning!",
        "favorited": 0,
        "name": "Nursing Quantum Computing Virtual Reality Microservice Machine Learning Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "eaarqcvrc",
        "description": "We do things related with Actionable Analytics, Robotics, Quantum Computing, and Virtual Reality!",
        "favorited": 0,
        "name": "Engineering Actionable Analytics Robotics Quantum Computing Virtual Reality Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "waidmqcbc",
        "description": "We do things related with Artificial Intelligence, Data Mining, Quantum Computing, and Blockchain!",
        "favorited": 0,
        "name": "Wharton Artificial Intelligence Data Mining Quantum Computing Blockchain Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "wbdrvrmlc",
        "description": "We do things related with Big Data, Robotics, Virtual Reality, and Machine Learning!",
        "favorited": 0,
        "name": "Wharton Big Data Robotics Virtual Reality Machine Learning Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "paaarrdmc",
        "description": "We do things related with Actionable Analytics, Augmented Reality, Robotics, and Data Mining!",
        "favorited": 0,
        "name": "Penn Actionable Analytics Augmented Reality Robotics Data Mining Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "nqcvriotbc",
        "description": "We do things related with Quantum Computing, Virtual Reality, Internet of Things, and Blockchain!",
        "favorited": 0,
        "name": "Nursing Quantum Computing Virtual Reality Internet of Things Blockchain Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "edmrbdiotc",
        "description": "We do things related with Data Mining, Robotics, Big Data, and Internet of Things!",
        "favorited": 0,
        "name": "Engineering Data Mining Robotics Big Data Internet of Things Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "caiarmliotc",
        "description": "We do things related with Artificial Intelligence, Augmented Reality, Machine Learning, and Internet of Things!",
        "favorited": 0,
        "name": "College Artificial Intelligence Augmented Reality Machine Learning Internet of Things Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "caimliotbc",
        "description": "We do things related with Artificial Intelligence, Machine Learning, Internet of Things, and Blockchain!",
        "favorited": 0,
        "name": "College Artificial Intelligence Machine Learning Internet of Things Blockchain Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "paiaaarrc",
        "description": "We do things related with Artificial Intelligence, Actionable Analytics, Augmented Reality, and Robotics!",
        "favorited": 0,
        "name": "Penn Artificial Intelligence Actionable Analytics Augmented Reality Robotics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "eaarqcmlc",
        "description": "We do things related with Actionable Analytics, Robotics, Quantum Computing, and Machine Learning!",
        "favorited": 0,
        "name": "Engineering Actionable Analytics Robotics Quantum Computing Machine Learning Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "nraaarmlc",
        "description": "We do things related with Robotics, Actionable Analytics, Augmented Reality, and Machine Learning!",
        "favorited": 0,
        "name": "Nursing Robotics Actionable Analytics Augmented Reality Machine Learning Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "naavriotbdc",
        "description": "We do things related with Actionable Analytics, Virtual Reality, Internet of Things, and Big Data!",
        "favorited": 0,
        "name": "Nursing Actionable Analytics Virtual Reality Internet of Things Big Data Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pdmvrairc",
        "description": "We do things related with Data Mining, Virtual Reality, Artificial Intelligence, and Robotics!",
        "favorited": 0,
        "name": "Penn Data Mining Virtual Reality Artificial Intelligence Robotics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "edmmlarqcc",
        "description": "We do things related with Data Mining, Machine Learning, Augmented Reality, and Quantum Computing!",
        "favorited": 0,
        "name": "Engineering Data Mining Machine Learning Augmented Reality Quantum Computing Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "caaarairc",
        "description": "We do things related with Actionable Analytics, Augmented Reality, Artificial Intelligence, and Robotics!",
        "favorited": 0,
        "name": "College Actionable Analytics Augmented Reality Artificial Intelligence Robotics Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "eaidmmlbdc",
        "description": "We do things related with Artificial Intelligence, Data Mining, Machine Learning, and Big Data!",
        "favorited": 0,
        "name": "Engineering Artificial Intelligence Data Mining Machine Learning Big Data Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "earvrqcaac",
        "description": "We do things related with Augmented Reality, Virtual Reality, Quantum Computing, and Actionable Analytics!",
        "favorited": 0,
        "name": "Engineering Augmented Reality Virtual Reality Quantum Computing Actionable Analytics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pbdqcarrc",
        "description": "We do things related with Big Data, Quantum Computing, Augmented Reality, and Robotics!",
        "favorited": 0,
        "name": "Penn Big Data Quantum Computing Augmented Reality Robotics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "piotbrmlc",
        "description": "We do things related with Internet of Things, Blockchain, Robotics, and Machine Learning!",
        "favorited": 0,
        "name": "Penn Internet of Things Blockchain Robotics Machine Learning Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "cvraraaiotc",
        "description": "We do things related with Virtual Reality, Augmented Reality, Actionable Analytics, and Internet of Things!",
        "favorited": 0,
        "name": "College Virtual Reality Augmented Reality Actionable Analytics Internet of Things Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wbdiotvraac",
        "description": "We do things related with Big Data, Internet of Things, Virtual Reality, and Actionable Analytics!",
        "favorited": 0,
        "name": "Wharton Big Data Internet of Things Virtual Reality Actionable Analytics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "piotaabdmc",
        "description": "We do things related with Internet of Things, Actionable Analytics, Blockchain, and Data Mining!",
        "favorited": 0,
        "name": "Penn Internet of Things Actionable Analytics Blockchain Data Mining Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "cmdmqcaac",
        "description": "We do things related with Microservice, Data Mining, Quantum Computing, and Actionable Analytics!",
        "favorited": 0,
        "name": "College Microservice Data Mining Quantum Computing Actionable Analytics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "naadmiotbdc",
        "description": "We do things related with Actionable Analytics, Data Mining, Internet of Things, and Big Data!",
        "favorited": 0,
        "name": "Nursing Actionable Analytics Data Mining Internet of Things Big Data Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pbdmaaarc",
        "description": "We do things related with Blockchain, Data Mining, Actionable Analytics, and Augmented Reality!",
        "favorited": 0,
        "name": "Penn Blockchain Data Mining Actionable Analytics Augmented Reality Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "naimlrvrc",
        "description": "We do things related with Artificial Intelligence, Machine Learning, Robotics, and Virtual Reality!",
        "favorited": 0,
        "name": "Nursing Artificial Intelligence Machine Learning Robotics Virtual Reality Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "eairdmbdc",
        "description": "We do things related with Artificial Intelligence, Robotics, Data Mining, and Big Data!",
        "favorited": 0,
        "name": "Engineering Artificial Intelligence Robotics Data Mining Big Data Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "craavrmlc",
        "description": "We do things related with Robotics, Actionable Analytics, Virtual Reality, and Machine Learning!",
        "favorited": 0,
        "name": "College Robotics Actionable Analytics Virtual Reality Machine Learning Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "naamldmiotc",
        "description": "We do things related with Actionable Analytics, Machine Learning, Data Mining, and Internet of Things!",
        "favorited": 0,
        "name": "Nursing Actionable Analytics Machine Learning Data Mining Internet of Things Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pmlqcarrc",
        "description": "We do things related with Machine Learning, Quantum Computing, Augmented Reality, and Robotics!",
        "favorited": 0,
        "name": "Penn Machine Learning Quantum Computing Augmented Reality Robotics Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "wbrdmvrc",
        "description": "We do things related with Blockchain, Robotics, Data Mining, and Virtual Reality!",
        "favorited": 0,
        "name": "Wharton Blockchain Robotics Data Mining Virtual Reality Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "wvraiqcbdc",
        "description": "We do things related with Virtual Reality, Artificial Intelligence, Quantum Computing, and Big Data!",
        "favorited": 0,
        "name": "Wharton Virtual Reality Artificial Intelligence Quantum Computing Big Data Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "naambbdc",
        "description": "We do things related with Actionable Analytics, Microservice, Blockchain, and Big Data!",
        "favorited": 0,
        "name": "Nursing Actionable Analytics Microservice Blockchain Big Data Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "eaamvraic",
        "description": "We do things related with Actionable Analytics, Microservice, Virtual Reality, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Engineering Actionable Analytics Microservice Virtual Reality Artificial Intelligence Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "wvraaarbc",
        "description": "We do things related with Virtual Reality, Actionable Analytics, Augmented Reality, and Blockchain!",
        "favorited": 0,
        "name": "Wharton Virtual Reality Actionable Analytics Augmented Reality Blockchain Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "cbmldmrc",
        "description": "We do things related with Blockchain, Machine Learning, Data Mining, and Robotics!",
        "favorited": 0,
        "name": "College Blockchain Machine Learning Data Mining Robotics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "narbdaidmc",
        "description": "We do things related with Augmented Reality, Big Data, Artificial Intelligence, and Data Mining!",
        "favorited": 0,
        "name": "Nursing Augmented Reality Big Data Artificial Intelligence Data Mining Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "pbqcmvrc",
        "description": "We do things related with Blockchain, Quantum Computing, Microservice, and Virtual Reality!",
        "favorited": 0,
        "name": "Penn Blockchain Quantum Computing Microservice Virtual Reality Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "ebdbaarc",
        "description": "We do things related with Big Data, Blockchain, Actionable Analytics, and Robotics!",
        "favorited": 0,
        "name": "Engineering Big Data Blockchain Actionable Analytics Robotics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "cbarraac",
        "description": "We do things related with Blockchain, Augmented Reality, Robotics, and Actionable Analytics!",
        "favorited": 0,
        "name": "College Blockchain Augmented Reality Robotics Actionable Analytics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "cqcrarbdc",
        "description": "We do things related with Quantum Computing, Robotics, Augmented Reality, and Big Data!",
        "favorited": 0,
        "name": "College Quantum Computing Robotics Augmented Reality Big Data Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wdmbqcaac",
        "description": "We do things related with Data Mining, Blockchain, Quantum Computing, and Actionable Analytics!",
        "favorited": 0,
        "name": "Wharton Data Mining Blockchain Quantum Computing Actionable Analytics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wardmbiotc",
        "description": "We do things related with Augmented Reality, Data Mining, Blockchain, and Internet of Things!",
        "favorited": 0,
        "name": "Wharton Augmented Reality Data Mining Blockchain Internet of Things Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "cbdaiaamlc",
        "description": "We do things related with Big Data, Artificial Intelligence, Actionable Analytics, and Machine Learning!",
        "favorited": 0,
        "name": "College Big Data Artificial Intelligence Actionable Analytics Machine Learning Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "nrmaimlc",
        "description": "We do things related with Robotics, Microservice, Artificial Intelligence, and Machine Learning!",
        "favorited": 0,
        "name": "Nursing Robotics Microservice Artificial Intelligence Machine Learning Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pdmarbmc",
        "description": "We do things related with Data Mining, Augmented Reality, Blockchain, and Microservice!",
        "favorited": 0,
        "name": "Penn Data Mining Augmented Reality Blockchain Microservice Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "wairvrqcc",
        "description": "We do things related with Artificial Intelligence, Robotics, Virtual Reality, and Quantum Computing!",
        "favorited": 0,
        "name": "Wharton Artificial Intelligence Robotics Virtual Reality Quantum Computing Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "wvraibdmc",
        "description": "We do things related with Virtual Reality, Artificial Intelligence, Big Data, and Microservice!",
        "favorited": 0,
        "name": "Wharton Virtual Reality Artificial Intelligence Big Data Microservice Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pvrqcbdmlc",
        "description": "We do things related with Virtual Reality, Quantum Computing, Big Data, and Machine Learning!",
        "favorited": 0,
        "name": "Penn Virtual Reality Quantum Computing Big Data Machine Learning Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wbdmlbmc",
        "description": "We do things related with Big Data, Machine Learning, Blockchain, and Microservice!",
        "favorited": 0,
        "name": "Wharton Big Data Machine Learning Blockchain Microservice Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "eaaiotarbc",
        "description": "We do things related with Actionable Analytics, Internet of Things, Augmented Reality, and Blockchain!",
        "favorited": 0,
        "name": "Engineering Actionable Analytics Internet of Things Augmented Reality Blockchain Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "emaiqcbc",
        "description": "We do things related with Microservice, Artificial Intelligence, Quantum Computing, and Blockchain!",
        "favorited": 0,
        "name": "Engineering Microservice Artificial Intelligence Quantum Computing Blockchain Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "parvraamc",
        "description": "We do things related with Augmented Reality, Virtual Reality, Actionable Analytics, and Microservice!",
        "favorited": 0,
        "name": "Penn Augmented Reality Virtual Reality Actionable Analytics Microservice Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "evrdmiotmlc",
        "description": "We do things related with Virtual Reality, Data Mining, Internet of Things, and Machine Learning!",
        "favorited": 0,
        "name": "Engineering Virtual Reality Data Mining Internet of Things Machine Learning Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "waaqciotbc",
        "description": "We do things related with Actionable Analytics, Quantum Computing, Internet of Things, and Blockchain!",
        "favorited": 0,
        "name": "Wharton Actionable Analytics Quantum Computing Internet of Things Blockchain Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "pdmmvraic",
        "description": "We do things related with Data Mining, Microservice, Virtual Reality, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Penn Data Mining Microservice Virtual Reality Artificial Intelligence Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "waabqcmlc",
        "description": "We do things related with Actionable Analytics, Blockchain, Quantum Computing, and Machine Learning!",
        "favorited": 0,
        "name": "Wharton Actionable Analytics Blockchain Quantum Computing Machine Learning Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "caimaabc",
        "description": "We do things related with Artificial Intelligence, Microservice, Actionable Analytics, and Blockchain!",
        "favorited": 0,
        "name": "College Artificial Intelligence Microservice Actionable Analytics Blockchain Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "waimmlbc",
        "description": "We do things related with Artificial Intelligence, Microservice, Machine Learning, and Blockchain!",
        "favorited": 0,
        "name": "Wharton Artificial Intelligence Microservice Machine Learning Blockchain Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "naiqciotaac",
        "description": "We do things related with Artificial Intelligence, Quantum Computing, Internet of Things, and Actionable Analytics!",
        "favorited": 0,
        "name": "Nursing Artificial Intelligence Quantum Computing Internet of Things Actionable Analytics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "emmlaavrc",
        "description": "We do things related with Microservice, Machine Learning, Actionable Analytics, and Virtual Reality!",
        "favorited": 0,
        "name": "Engineering Microservice Machine Learning Actionable Analytics Virtual Reality Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "edmqcaraac",
        "description": "We do things related with Data Mining, Quantum Computing, Augmented Reality, and Actionable Analytics!",
        "favorited": 0,
        "name": "Engineering Data Mining Quantum Computing Augmented Reality Actionable Analytics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "waivrdmmc",
        "description": "We do things related with Artificial Intelligence, Virtual Reality, Data Mining, and Microservice!",
        "favorited": 0,
        "name": "Wharton Artificial Intelligence Virtual Reality Data Mining Microservice Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "edmbiotaic",
        "description": "We do things related with Data Mining, Blockchain, Internet of Things, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Engineering Data Mining Blockchain Internet of Things Artificial Intelligence Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "ebvrdmmlc",
        "description": "We do things related with Blockchain, Virtual Reality, Data Mining, and Machine Learning!",
        "favorited": 0,
        "name": "Engineering Blockchain Virtual Reality Data Mining Machine Learning Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "pqcbdmldmc",
        "description": "We do things related with Quantum Computing, Big Data, Machine Learning, and Data Mining!",
        "favorited": 0,
        "name": "Penn Quantum Computing Big Data Machine Learning Data Mining Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "nqcbdmlaic",
        "description": "We do things related with Quantum Computing, Big Data, Machine Learning, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Nursing Quantum Computing Big Data Machine Learning Artificial Intelligence Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "nmbiotmlc",
        "description": "We do things related with Microservice, Blockchain, Internet of Things, and Machine Learning!",
        "favorited": 0,
        "name": "Nursing Microservice Blockchain Internet of Things Machine Learning Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "eiotbdvrdmc",
        "description": "We do things related with Internet of Things, Big Data, Virtual Reality, and Data Mining!",
        "favorited": 0,
        "name": "Engineering Internet of Things Big Data Virtual Reality Data Mining Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "waivrmaac",
        "description": "We do things related with Artificial Intelligence, Virtual Reality, Microservice, and Actionable Analytics!",
        "favorited": 0,
        "name": "Wharton Artificial Intelligence Virtual Reality Microservice Actionable Analytics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "wriotaaaic",
        "description": "We do things related with Robotics, Internet of Things, Actionable Analytics, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Wharton Robotics Internet of Things Actionable Analytics Artificial Intelligence Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "caavrrmc",
        "description": "We do things related with Actionable Analytics, Virtual Reality, Robotics, and Microservice!",
        "favorited": 0,
        "name": "College Actionable Analytics Virtual Reality Robotics Microservice Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "niotbdqcbc",
        "description": "We do things related with Internet of Things, Big Data, Quantum Computing, and Blockchain!",
        "favorited": 0,
        "name": "Nursing Internet of Things Big Data Quantum Computing Blockchain Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "wiotvrarqcc",
        "description": "We do things related with Internet of Things, Virtual Reality, Augmented Reality, and Quantum Computing!",
        "favorited": 0,
        "name": "Wharton Internet of Things Virtual Reality Augmented Reality Quantum Computing Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "parmlbdrc",
        "description": "We do things related with Augmented Reality, Machine Learning, Big Data, and Robotics!",
        "favorited": 0,
        "name": "Penn Augmented Reality Machine Learning Big Data Robotics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "piotvrardmc",
        "description": "We do things related with Internet of Things, Virtual Reality, Augmented Reality, and Data Mining!",
        "favorited": 0,
        "name": "Penn Internet of Things Virtual Reality Augmented Reality Data Mining Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "nmldmaraac",
        "description": "We do things related with Machine Learning, Data Mining, Augmented Reality, and Actionable Analytics!",
        "favorited": 0,
        "name": "Nursing Machine Learning Data Mining Augmented Reality Actionable Analytics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wvrariotaac",
        "description": "We do things related with Virtual Reality, Augmented Reality, Internet of Things, and Actionable Analytics!",
        "favorited": 0,
        "name": "Wharton Virtual Reality Augmented Reality Internet of Things Actionable Analytics Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "nbdvriotqcc",
        "description": "We do things related with Big Data, Virtual Reality, Internet of Things, and Quantum Computing!",
        "favorited": 0,
        "name": "Nursing Big Data Virtual Reality Internet of Things Quantum Computing Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "nbarbdvrc",
        "description": "We do things related with Blockchain, Augmented Reality, Big Data, and Virtual Reality!",
        "favorited": 0,
        "name": "Nursing Blockchain Augmented Reality Big Data Virtual Reality Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "eaaqcbdrc",
        "description": "We do things related with Actionable Analytics, Quantum Computing, Big Data, and Robotics!",
        "favorited": 0,
        "name": "Engineering Actionable Analytics Quantum Computing Big Data Robotics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "eraamliotc",
        "description": "We do things related with Robotics, Actionable Analytics, Machine Learning, and Internet of Things!",
        "favorited": 0,
        "name": "Engineering Robotics Actionable Analytics Machine Learning Internet of Things Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "nvrmlaibc",
        "description": "We do things related with Virtual Reality, Machine Learning, Artificial Intelligence, and Blockchain!",
        "favorited": 0,
        "name": "Nursing Virtual Reality Machine Learning Artificial Intelligence Blockchain Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "earaivrmlc",
        "description": "We do things related with Augmented Reality, Artificial Intelligence, Virtual Reality, and Machine Learning!",
        "favorited": 0,
        "name": "Engineering Augmented Reality Artificial Intelligence Virtual Reality Machine Learning Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "nbdqcbmc",
        "description": "We do things related with Big Data, Quantum Computing, Blockchain, and Microservice!",
        "favorited": 0,
        "name": "Nursing Big Data Quantum Computing Blockchain Microservice Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "wvrdmiotmc",
        "description": "We do things related with Virtual Reality, Data Mining, Internet of Things, and Microservice!",
        "favorited": 0,
        "name": "Wharton Virtual Reality Data Mining Internet of Things Microservice Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "emdmaarc",
        "description": "We do things related with Microservice, Data Mining, Actionable Analytics, and Robotics!",
        "favorited": 0,
        "name": "Engineering Microservice Data Mining Actionable Analytics Robotics Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "eiotmlrdmc",
        "description": "We do things related with Internet of Things, Machine Learning, Robotics, and Data Mining!",
        "favorited": 0,
        "name": "Engineering Internet of Things Machine Learning Robotics Data Mining Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "edmaambdc",
        "description": "We do things related with Data Mining, Actionable Analytics, Microservice, and Big Data!",
        "favorited": 0,
        "name": "Engineering Data Mining Actionable Analytics Microservice Big Data Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "wbdqcmlrc",
        "description": "We do things related with Big Data, Quantum Computing, Machine Learning, and Robotics!",
        "favorited": 0,
        "name": "Wharton Big Data Quantum Computing Machine Learning Robotics Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "nqcaabarc",
        "description": "We do things related with Quantum Computing, Actionable Analytics, Blockchain, and Augmented Reality!",
        "favorited": 0,
        "name": "Nursing Quantum Computing Actionable Analytics Blockchain Augmented Reality Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "piotmlvrarc",
        "description": "We do things related with Internet of Things, Machine Learning, Virtual Reality, and Augmented Reality!",
        "favorited": 0,
        "name": "Penn Internet of Things Machine Learning Virtual Reality Augmented Reality Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "cdmairarc",
        "description": "We do things related with Data Mining, Artificial Intelligence, Robotics, and Augmented Reality!",
        "favorited": 0,
        "name": "College Data Mining Artificial Intelligence Robotics Augmented Reality Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "carbdaaqcc",
        "description": "We do things related with Augmented Reality, Big Data, Actionable Analytics, and Quantum Computing!",
        "favorited": 0,
        "name": "College Augmented Reality Big Data Actionable Analytics Quantum Computing Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "ndmaaiotaic",
        "description": "We do things related with Data Mining, Actionable Analytics, Internet of Things, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Nursing Data Mining Actionable Analytics Internet of Things Artificial Intelligence Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "pbmmlaic",
        "description": "We do things related with Blockchain, Microservice, Machine Learning, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Penn Blockchain Microservice Machine Learning Artificial Intelligence Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "naamlqciotc",
        "description": "We do things related with Actionable Analytics, Machine Learning, Quantum Computing, and Internet of Things!",
        "favorited": 0,
        "name": "Nursing Actionable Analytics Machine Learning Quantum Computing Internet of Things Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "cmaadmaic",
        "description": "We do things related with Microservice, Actionable Analytics, Data Mining, and Artificial Intelligence!",
        "favorited": 0,
        "name": "College Microservice Actionable Analytics Data Mining Artificial Intelligence Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pqcarbiotc",
        "description": "We do things related with Quantum Computing, Augmented Reality, Blockchain, and Internet of Things!",
        "favorited": 0,
        "name": "Penn Quantum Computing Augmented Reality Blockchain Internet of Things Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "waiiotarbdc",
        "description": "We do things related with Artificial Intelligence, Internet of Things, Augmented Reality, and Big Data!",
        "favorited": 0,
        "name": "Wharton Artificial Intelligence Internet of Things Augmented Reality Big Data Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "pdmmlqcaic",
        "description": "We do things related with Data Mining, Machine Learning, Quantum Computing, and Artificial Intelligence!",
        "favorited": 0,
        "name": "Penn Data Mining Machine Learning Quantum Computing Artificial Intelligence Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "nqcbmlaac",
        "description": "We do things related with Quantum Computing, Blockchain, Machine Learning, and Actionable Analytics!",
        "favorited": 0,
        "name": "Nursing Quantum Computing Blockchain Machine Learning Actionable Analytics Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "eaiarrqcc",
        "description": "We do things related with Artificial Intelligence, Augmented Reality, Robotics, and Quantum Computing!",
        "favorited": 0,
        "name": "Engineering Artificial Intelligence Augmented Reality Robotics Quantum Computing Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "pmldmbaac",
        "description": "We do things related with Machine Learning, Data Mining, Blockchain, and Actionable Analytics!",
        "favorited": 0,
        "name": "Penn Machine Learning Data Mining Blockchain Actionable Analytics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "pbdmlqcrc",
        "description": "We do things related with Big Data, Machine Learning, Quantum Computing, and Robotics!",
        "favorited": 0,
        "name": "Penn Big Data Machine Learning Quantum Computing Robotics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "emlbdariotc",
        "description": "We do things related with Machine Learning, Big Data, Augmented Reality, and Internet of Things!",
        "favorited": 0,
        "name": "Engineering Machine Learning Big Data Augmented Reality Internet of Things Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "nqcrvrbc",
        "description": "We do things related with Quantum Computing, Robotics, Virtual Reality, and Blockchain!",
        "favorited": 0,
        "name": "Nursing Quantum Computing Robotics Virtual Reality Blockchain Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "waaaidmbc",
        "description": "We do things related with Actionable Analytics, Artificial Intelligence, Data Mining, and Blockchain!",
        "favorited": 0,
        "name": "Wharton Actionable Analytics Artificial Intelligence Data Mining Blockchain Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "cvrqcraic",
        "description": "We do things related with Virtual Reality, Quantum Computing, Robotics, and Artificial Intelligence!",
        "favorited": 0,
        "name": "College Virtual Reality Quantum Computing Robotics Artificial Intelligence Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "eaimvrrc",
        "description": "We do things related with Artificial Intelligence, Microservice, Virtual Reality, and Robotics!",
        "favorited": 0,
        "name": "Engineering Artificial Intelligence Microservice Virtual Reality Robotics Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "embvrbdc",
        "description": "We do things related with Microservice, Blockchain, Virtual Reality, and Big Data!",
        "favorited": 0,
        "name": "Engineering Microservice Blockchain Virtual Reality Big Data Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "erbbdiotc",
        "description": "We do things related with Robotics, Blockchain, Big Data, and Internet of Things!",
        "favorited": 0,
        "name": "Engineering Robotics Blockchain Big Data Internet of Things Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "niotbdmvrc",
        "description": "We do things related with Internet of Things, Big Data, Microservice, and Virtual Reality!",
        "favorited": 0,
        "name": "Nursing Internet of Things Big Data Microservice Virtual Reality Club",
        "tags": [
            "Environmentally Friendly"
        ]
    },
    {
        "code": "wbdrarbc",
        "description": "We do things related with Big Data, Robotics, Augmented Reality, and Blockchain!",
        "favorited": 0,
        "name": "Wharton Big Data Robotics Augmented Reality Blockchain Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "emaamlbc",
        "description": "We do things related with Microservice, Actionable Analytics, Machine Learning, and Blockchain!",
        "favorited": 0,
        "name": "Engineering Microservice Actionable Analytics Machine Learning Blockchain Club",
        "tags": [
            "Meme"
        ]
    },
    {
        "code": "nbdvrmlmc",
        "description": "We do things related with Big Data, Virtual Reality, Machine Learning, and Microservice!",
        "favorited": 0,
        "name": "Nursing Big Data Virtual Reality Machine Learning Microservice Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "waimlariotc",
        "description": "We do things related with Artificial Intelligence, Machine Learning, Augmented Reality, and Internet of Things!",
        "favorited": 0,
        "name": "Wharton Artificial Intelligence Machine Learning Augmented Reality Internet of Things Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "emiotrdmc",
        "description": "We do things related with Microservice, Internet of Things, Robotics, and Data Mining!",
        "favorited": 0,
        "name": "Engineering Microservice Internet of Things Robotics Data Mining Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "niotrmldmc",
        "description": "We do things related with Internet of Things, Robotics, Machine Learning, and Data Mining!",
        "favorited": 0,
        "name": "Nursing Internet of Things Robotics Machine Learning Data Mining Club",
        "tags": [
            "Potato"
        ]
    },
    {
        "code": "cbdqcaidmc",
        "description": "We do things related with Big Data, Quantum Computing, Artificial Intelligence, and Data Mining!",
        "favorited": 0,
        "name": "College Big Data Quantum Computing Artificial Intelligence Data Mining Club",
        "tags": [
            "Social"
        ]
    },
    {
        "code": "nraidmmlc",
        "description": "We do things related with Robotics, Artificial Intelligence, Data Mining, and Machine Learning!",
        "favorited": 0,
        "name": "Nursing Robotics Artificial Intelligence Data Mining Machine Learning Club",
        "tags": [
            "Meme"
        ]
    }
]
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
