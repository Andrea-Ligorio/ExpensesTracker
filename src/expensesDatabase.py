import sqlite3
import Spesa

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

def insertSpesa(spesa):
    db = sqlite3.connect('spese.db')
    cursoreDb = db.cursor()

    try:
        cursoreDb.execute('''
            INSERT INTO spesa (nome, prezzo, data, note)
            VALUES (?, ?, ?, ?)
        ''', (spesa.nome, spesa.prezzo, spesa.data, spesa.note))
        
        spesa_id = cursoreDb.lastrowid
        
        for tag in spesa.tag:
            cursoreDb.execute('''
                INSERT INTO tags (tag, spesaId)
                VALUES (?, ?)
            ''', (tag, spesa_id))
            
        db.commit()
        print(f"Spesa '{spesa.nome}' inserita con successo!")
        
    except sqlite3.Error as e:
        print(f"Errore durante l'inserimento nel database: {e}")
        db.rollback()
        
    finally:
        db.close()

def editSpesa(spesa):
    db = sqlite3.connect('spese.db')
    cursoreDb = db.cursor()

    try:
        cursoreDb.execute('''
            UPDATE spesa
            SET nome = ?, prezzo = ?, data = ?, note = ?
            WHERE id = ?
        ''', (spesa.nome, spesa.prezzo, spesa.data, spesa.note, spesa.id))

        cursoreDb.execute('DELETE FROM tags WHERE spesaId = ?', (spesa.id,))
        for tag in spesa.tag:
            cursoreDb.execute('''
                INSERT INTO tags (tag, spesaId)
                VALUES (?, ?)
            ''', (tag, spesa.id))

        db.commit()
        print(f"Spesa con ID {spesa.id} aggiornata con successo!")
    except sqlite3.Error as e:
        print(f"Errore durante l'aggiornamento del database: {e}")
        db.rollback()
    finally:
        db.close()

def deleteSpesa(spesa_id):
    db = sqlite3.connect('spese.db')
    cursoreDb = db.cursor()

    try:
        cursoreDb.execute('DELETE FROM spesa WHERE id = ?', (spesa_id,))
        cursoreDb.execute('DELETE FROM tags WHERE spesaId = ?', (spesa_id,))
        db.commit()
        print(f"Spesa con ID {spesa_id} eliminata con successo!")
    except sqlite3.Error as e:
        print(f"Errore durante l'eliminazione dal database: {e}")
        db.rollback()
    finally:
        db.close()

def getSpese():
    db = sqlite3.connect('spese.db')
    # Impostiamo il row_factory per accedere ai dati tramite nome colonna
    db.row_factory = sqlite3.Row 
    cursoreDb = db.cursor()
    
    lista_spese = []

    try:
        # 1. Recuperiamo tutte le spese principali
        cursoreDb.execute("SELECT id, nome, prezzo, data, note FROM spesa")
        rows = cursoreDb.fetchall()

        for row in rows:
            # Trasformiamo la riga in un dizionario
            spesa = Spesa.Spesa(
                nome=row['nome'],
                prezzo=row['prezzo'],
                data=row['data'],
                note=row['note'],
                id=row['id']
            )

            # 2. Per ogni spesa, recuperiamo i relativi tag
            cursoreDb.execute("SELECT tag FROM tags WHERE spesaId = ?", (spesa.id,))
            spesa.tag = [t['tag'] for t in cursoreDb.fetchall()]
            
            lista_spese.append(spesa)

    except sqlite3.Error as e:
        print(f"Errore durante la lettura dal database: {e}")
    
    finally:
        db.close()

    return lista_spese

def getTags():
    db = sqlite3.connect('spese.db')
    db.row_factory = sqlite3.Row 
    cursoreDb = db.cursor()
    
    tags = set()

    try:
        cursoreDb.execute("SELECT DISTINCT tag FROM tags")
        rows = cursoreDb.fetchall()
        tags = {row['tag'] for row in rows}

    except sqlite3.Error as e:
        print(f"Errore durante la lettura dei tag dal database: {e}")
    
    finally:
        db.close()

    return tags

# --- Esempio di utilizzo ---
if __name__ == '__main__':
    # Inizializza il database
    creaDb()
    
    # --- 2. Otteniamo la lista delle spese ---
    spese = getSpese()
    
    # --- 3. Stampiamo i risultati ---
    spese = getSpese()

    for s in spese:
        # Stampa: ID - Nome - Prezzo - Data - Note - [Tags]
        print(s.nome, s.prezzo, s.data, s.note, s.tag)