import mysql.connector
from mysql.connector import Error


def pripojeni_db():
    """Připojení k MySQL databázi."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111",
            database="task_manager_db"
        )
        return connection
    except Error as e:
        print(f"Chyba při připojení: {e}")
        return None


def vytvoreni_tabulky():
    """Vytvoří tabulku 'ukoly', pokud neexistuje."""
    connection = pripojeni_db()
    if not connection:
        print("Chyba připojení při vytváření tabulky.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
                datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        connection.commit()
    except Error as e:
        print(f"Chyba při vytváření tabulky: {e}")
    finally:
        cursor.close()
        connection.close()


# --- CRUD funkce, které budeme testovat ---
def pridat_ukol_db(nazev, popis, stav="Nezahájeno"):
    """Vloží nový úkol do databáze."""
    if not nazev or not popis:
        raise ValueError("Název a popis nesmí být prázdné!")

    connection = pripojeni_db()
    cursor = connection.cursor()
    query = "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)"
    cursor.execute(query, (nazev, popis, stav))
    connection.commit()
    cursor.close()
    connection.close()
    return True


def aktualizovat_ukol_db(id_ukolu, novy_stav):
    """Aktualizuje stav úkolu podle ID."""
    if novy_stav not in ("Probíhá", "Hotovo"):
        raise ValueError("Neplatný stav úkolu!")

    connection = pripojeni_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s;", (novy_stav, id_ukolu))
    connection.commit()
    updated = cursor.rowcount
    cursor.close()
    connection.close()
    return updated > 0


def odstranit_ukol_db(id_ukolu):
    """Odstraní úkol podle ID."""
    connection = pripojeni_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ukoly WHERE id = %s;", (id_ukolu,))
    connection.commit()
    deleted = cursor.rowcount
    cursor.close()
    connection.close()
    return deleted > 0
 