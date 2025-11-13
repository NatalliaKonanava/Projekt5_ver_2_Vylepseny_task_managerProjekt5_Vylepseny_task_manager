from db_functions import (
    vytvoreni_tabulky,
    pridat_ukol_db,
    aktualizovat_ukol_db,
    odstranit_ukol_db,
)


def pridat_ukol():
    nazev = input("Zadej název úkolu: ").strip()
    popis = input("Zadej popis úkolu: ").strip()
    try:
        pridat_ukol_db(nazev, popis)
        print("Úkol byl úspěšně přidán.")
    except ValueError as e:
        print(f"Chyba: {e}")


def hlavni_menu():
    vytvoreni_tabulky()
    while True:
        print("\nHlavní menu:")
        print("1. Přidat úkol")
        print("2. Aktualizovat úkol")
        print("3. Odstranit úkol")
        print("4. Ukončit")

        volba = input("Vyber možnost (1–4): ").strip()
        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            id_ukolu = input("Zadej ID úkolu: ").strip()
            stav = input("Zadej nový stav (Probíhá/Hotovo): ").strip()
            if aktualizovat_ukol_db(id_ukolu, stav):
                print("Úkol byl aktualizován.")
            else:
                print("Úkol s tímto ID neexistuje.")
        elif volba == "3":
            id_ukolu = input("Zadej ID úkolu: ").strip()
            if odstranit_ukol_db(id_ukolu):
                print("Úkol byl odstraněn.")
            else:
                print("Úkol s tímto ID neexistuje.")
        elif volba == "4":
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba.")


if __name__ == "__main__":
    hlavni_menu()

