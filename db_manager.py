import sys, os
import xml.etree.ElementTree as ET
import sqlite3


def create_database():
    #Creates database file
    #Creates pubs and authors table
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pubs
                          (ID INTEGER PRIMARY KEY NOT NULL, JOURNAL TEXT, PAGES TEXT, YEAR INTEGER, TITLE TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS authors
                          (auth_ID INTEGER, AUTHOR TEXT, FOREIGN KEY (auth_ID) REFERENCES pubs (ID) )''')
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        raise e


def parser(inputfile='pubs.txt'):

    #Parses pubs.txt and retrieves relevant data
    #Creates a cursor and executes insert statements into the database depending on the data

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    pubs_storage = []
    auth_storage = []

    tree = ET.parse(inputfile)
    root = tree.getroot()

    for tree in root:
        for branch in tree:
            AUTHORS = []
            if branch.tag == 'ID':
                if branch.text != None:
                    ID = int(branch.text)
                else:
                    ID = None

            if branch.tag == 'title':
                if branch.text != None:
                    TITLE = str(branch.text)
                else:
                    TITLE = None

            if branch.tag == 'year':
                if branch.text != None:
                    YEAR = str(branch.text)
                else:
                    YEAR = None

            if branch.tag == 'booktitle':
                if branch.text != None:
                    JOURNAL = str(branch.text)
                else:
                    JOURNAL = None

            if branch.tag == 'pages':
                if branch.text != None:
                    PAGES = str(branch.text)
                else:
                    PAGES = None

            for leaf in branch:
                AUTHORS.append(leaf.text)

        pubs_tup = (ID, JOURNAL, PAGES, YEAR, TITLE)
        pubs_storage.append(pubs_tup)

        for author in AUTHORS:
            author_tup = (ID, author)
            auth_storage.append(author_tup)

    cursor.executemany('INSERT INTO pubs VALUES (?,?,?,?,?)', pubs_storage)
    cursor.executemany('INSERT INTO authors VALUES (?,?)', auth_storage)

    connection.commit()
    connection.close()


def main():
    if len(sys.argv) != 2:
        raise IOError("Invalid Argument" + "Unexpected error:", sys.exc_info())
    else:
        create_database()
        inputDir = os.path.abspath(os.path.expanduser(sys.argv[1]))
        parser(inputDir)


if __name__ == "__main__": main()
