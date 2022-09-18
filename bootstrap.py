import os
from app import db, DB_FILE
import json
from models import *
import codecs
from bs4 import BeautifulSoup
from werkzeug.security import generate_password_hash

def create_user():
    josh = User(user="josh", name="Josh", year=3, email="josh123@gmail.com", password=generate_password_hash("josh123", method='sha256'))
    db.session.add(josh)
    db.session.commit()


def load_data():
    # load in clubs.json data
    f = open('clubs.json')

    data = json.load(f)

    # tag_map keeps tracks of tags already generated
    # if a tag is already generated, use the tag from the map
    # otherwise, create a new tag and add it to the map
    tag_map = {}

    for i in data:
        club = Club(code=i['code'], name=i['name'], description=i['description'])
        for tag_name in i['tags']:
            if tag_name not in tag_map:
                tag = Tag(name=tag_name)
                tag_map[tag_name] = tag
                db.session.add(tag)
            club.tags.append(tag_map[tag_name])

        db.session.add(club)

    # load in clubdata.html (webscraping data)
    f = codecs.open("clubdata.html", 'r')
    soup = BeautifulSoup(f, "html.parser")
    clubs = soup.find_all("div", class_="box")

    # code_map will ensure no two clubs have the same code
    # if this is ever encountered, then append an integer starting at 0
    code_map = {}

    for club in clubs:
        name = club.find("strong", class_="club-name").text
        tag_name = club.find("span", class_="tag is-info is-rounded").text
        description = club.find("em").text
        code = generate_code(name)

        if code in code_map:
            code = code + str(code_map[code])
            code_map[code] = code_map[code] + 1
        else:
            code_map[code] = 0

        if tag_name not in tag_map:
            tag = Tag(name=tag_name)
            tag_map[tag_name] = tag
            db.session.add(tag)

        club = Club(code=code, name=name, description=description, tags=[tag_map[tag_name]])
        db.session.add(club)

    db.session.commit()


# helper function to generate a code for a club name
# code is the first letter of each word in the club name, lowercase
def generate_code(club_name):
    code = ""
    for i in range(len(club_name)):
        if i == 0 or club_name[i - 1] == ' ':
            code = code + str(club_name[i]).lower()
    return code


# No need to modify the below code.
if __name__ == '__main__':
    # Delete any existing database before bootstrapping a new one.
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    db.create_all()
    create_user()
    load_data()
