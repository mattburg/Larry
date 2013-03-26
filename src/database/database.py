import sqlite3
DATA_PATH = "/Users/matthewburgess/Dropbox/redditScraper/mydatabase.db"


class Database():

    def __init__(self):

        self.cursor = sqlite3.connect(DATA_PATH).cursor()

    def query(self,queryString):

        return self.cursor.execute(queryString)
            










def main():
    db = Database()
    db.query("t")



if __name__ == "__main__":
    main()
