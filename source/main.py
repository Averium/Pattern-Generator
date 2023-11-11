#!/usr/bin/python3
# -*- coding: utf-8 -*-

from windows import MainWindow
from settings import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('windowsvista'))
    app.setFont(FONT)

    window = MainWindow(app, DIM['window'], 'Keresztszemes mintatervező')
    sys.exit(app.exec_())

# TODO -------------------------------------------------------------------------

# aktuális méretek megjelenítése

# megjelemítés kijavítása

# rajzfunkciók programozása
    # kijelölés megjelenítése (kontúrkeresés túl lassú)
    # kijelölés mozgatása, kivágása, másolása
    # mentett minta behívása az aktuálisba

# vonalak és kijelölés hozzáadása a visszavonáshoz

# rács méretének bővítése/csökkentése

# aktív színek megjelenítése
# színválasztás bővítése

# nézet:
    # színek, vonalak, rácsok megjelenítése
    # zoom ablak
    # igazítások magasságra, szélességre, teljes képernyőre
    # scrollbar-ok megjelenítése

# beállítások ablak

# DEBUG ------------------------------------------------------------------------

# Zoom közben crash
# Egér elcsúszik
# Nem lép ki
