import sqlite3

def creaDb():
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
    """
    Inserisce una nuova spesa e i relativi tag nel database.
    """
    db = sqlite3.connect('spese.db')
    cursoreDb = db.cursor()

    try:
        cursoreDb.execute('''
            INSERT INTO spesa (nome, prezzo, data, note)
            VALUES (?, ?, ?, ?)
        ''', (name, price, date, note))
        
        spesa_id = cursoreDb.lastrowid
        
        for tag in tags:
            cursoreDb.execute('''
                INSERT INTO tags (tag, spesaId)
                VALUES (?, ?)
            ''', (tag, spesa_id))
            
        db.commit()
        print(f"Spesa '{name}' inserita con successo!")
        
    except sqlite3.Error as e:
        print(f"Errore durante l'inserimento nel database: {e}")
        db.rollback()
        
    finally:
        db.close()

def getSpese():
    """
    Recupera tutte le spese presenti nel database, inclusi i tag, e le restituisce come lista.
    """
    db = sqlite3.connect('spese.db')
    cursoreDb = db.cursor()
    
    lista_spese = []
    
    try:
        cursoreDb.execute('SELECT * FROM spesa')
        rows = cursoreDb.fetchall()
        
        for row in rows:
            spesa_id = row[0]
            
            # Recupera i tag associati alla spesa corrente
            cursoreDb.execute('SELECT tag FROM tags WHERE spesaId = ?', (spesa_id,))
            tags = [r[0] for r in cursoreDb.fetchall()]
            
            spesa_dict = {
                'id': row[0],
                'prezzo': row[1],
                'data': row[2],
                'nome': row[3],
                'note': row[4],
                'tags': tags
            }
            
            lista_spese.append(spesa_dict)
            
    except sqlite3.Error as e:
        print(f"Errore durante la lettura dal database: {e}")
        
    finally:
        db.close()
        
    return lista_spese

# --- Esempio di utilizzo ---
if __name__ == '__main__':
    # Inizializza il database
    creaDb()
    
    # --- 1. Inseriamo più spese di prova ---
    insertSpesa(
        name="Spesa al supermercato",
        price=45.50,
        date="2026-05-06",
        note="Acquisto generi alimentari",
        tags=["cibo", "spesa", "necessario"]
    )
    
    insertSpesa(
        name="Cena al ristorante",
        price=60.00,
        date="2026-05-05",
        note="Cena con amici",
        tags=["svago", "ristorante"]
    )
    
    insertSpesa(
        name="Abbonamento palestra",
        price=35.00,
        date="2026-05-01",
        note="Rata mensile",
        tags=["sport", "salute"]
    )
    
    # --- 2. Otteniamo la lista delle spese ---
    spese = getSpese()
    
    # --- 3. Stampiamo i risultati ---
    print("\n--- Lista delle spese nel database ---")
    for s in spese:
        print(f"ID: {s['id']} | Nome: {s['nome']} | Prezzo: {s['prezzo']}€ | Data: {s['data']} | Tag: {s['tags']}")