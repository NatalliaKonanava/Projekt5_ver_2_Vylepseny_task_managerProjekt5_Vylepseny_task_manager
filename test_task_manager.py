import pytest
from db_functions import (
    pripojeni_db,
    vytvoreni_tabulky,
    pridat_ukol_db,
    aktualizovat_ukol_db,
    odstranit_ukol_db,
)

@pytest.fixture(autouse=True)
def cleanup():
    """Vyčistí tabulku před a po každém testu."""
    connection = pripojeni_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ukoly;")
    connection.commit()
    yield
    cursor.execute("DELETE FROM ukoly;")
    connection.commit()
    cursor.close()
    connection.close()


def test_pridat_ukol_pozitivni():
    vytvoreni_tabulky()
    result = pridat_ukol_db("Testovací úkol", "Popis testu")
    assert result is True


def test_pridat_ukol_negativni():
    with pytest.raises(ValueError):
        pridat_ukol_db("", "Popis bez názvu")


def test_aktualizovat_ukol_pozitivni():
    vytvoreni_tabulky()
    pridat_ukol_db("Update test", "Testujeme update")
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Update test';")
    id_ukolu = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    result = aktualizovat_ukol_db(id_ukolu, "Hotovo")
    assert result is True


def test_aktualizovat_ukol_negativni():
    with pytest.raises(ValueError):
        aktualizovat_ukol_db(1, "Špatný stav")


def test_odstranit_ukol_pozitivni():
    vytvoreni_tabulky()
    pridat_ukol_db("Smazat test", "Tento úkol bude smazán")
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Smazat test';")
    id_ukolu = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    result = odstranit_ukol_db(id_ukolu)
    assert result is True


def test_odstranit_ukol_negativni():
    result = odstranit_ukol_db(9999)  # neexistující ID
    assert result is False
