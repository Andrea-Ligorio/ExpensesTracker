import sqlite3

def inizializzaDb():
    db = sqlite3.connect('spese.db')
    cursoreDb = db.cursor()

    cursoreDb.execute('''
        CREATE TABLE IF NOT EXISTS spesa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prezzo REAL,
            data TEXT,
            nome TEXT,
            note TEXT
        )
    ''')

    cursoreDb.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            tag TEXT,
            spesaId INTEGER,
            FOREIGN KEY (spesaId) REFERENCES spesa(id)
        )
    ''')

    db.commit()
    db.close()

def insertSpesa(name, price, date, note, tags):
    db = sqlite3.connect('spese.db')
    cursoreDb = db.cursor()
