"""orders.py — eenvoudige orderopslag voor proof-of-concept

Slaat bij elke betaling één record op in data/orders.db met:
- id (AUTOINCREMENT) — ordernummer
- created_at (TEXT, ISO 8601)
- items (TEXT) — komma-gescheiden namen
- co2_info (TEXT) — CO2-equivalent (bijv. "0.63 kg ~1.2 km")
- totaalbedrag (REAL)
"""
from __future__ import annotations

import os
import json
import sqlite3
import datetime as _dt
from typing import List, Dict, Optional

# Pad naar de orders database (relatief t.o.v. src/)
_THIS_DIR = os.path.dirname(__file__)
_DB_PATH = os.path.normpath(os.path.join(_THIS_DIR, "..", "data", "orders.db"))

def _connect() -> sqlite3.Connection:
    # Zorg dat de map bestaat
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_orders_schema() -> None:
    """Maak/upgrade de tabel 'orders' met vaste kolomvolgorde."""
    with _connect() as conn:
        cur = conn.execute("PRAGMA table_info(orders)")
        cols = [row[1] for row in cur.fetchall()]  # [cid, name, ...]
        if not cols:
            # Vers nieuwe tabel aanmaken met juiste volgorde
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    items TEXT NOT NULL,
                    co2_info TEXT NOT NULL,
                    totaalbedrag REAL NOT NULL
                )
                """
            )
            return
        # Bestaande tabel: check of co2_info ontbreekt of volgorde afwijkt
        desired = ["id", "created_at", "items", "co2_info", "totaalbedrag"]
        if cols != desired:
            # Maak nieuwe tabel met juiste schema en kopieer data
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS orders_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    items TEXT NOT NULL,
                    co2_info TEXT NOT NULL,
                    totaalbedrag REAL NOT NULL
                )
                """
            )
            # Bepaal welke kolommen bestaan en kopieer met defaults
            has_items = "items" in cols or "items_json" in cols
            has_total = "totaalbedrag" in cols or "totaal" in cols
            items_col = "items" if "items" in cols else ("items_json" if "items_json" in cols else "''")
            total_col = "totaalbedrag" if "totaalbedrag" in cols else ("totaal" if "totaal" in cols else "0.0")
            # Zet ontbrekende co2_info als lege string
            conn.execute(
                f"INSERT INTO orders_new (id, created_at, items, co2_info, totaalbedrag) "
                f"SELECT id, created_at, {items_col}, '' as co2_info, {total_col} FROM orders"
            )
            conn.execute("DROP TABLE orders")
            conn.execute("ALTER TABLE orders_new RENAME TO orders")

def save_order(items: List[Dict], totaal: float, co2_text: str | None = None) -> Optional[int]:
    """Sla een order op en retourneer het ordernummer (id).

    items: lijst met dicts: {naam: str, aantal: int}
    totaal: totaalbedrag (float)
    co2_text: optionele string met CO2-info

    All-or-nothing via transaction context.
    """
    if not items:
        return None
    created_at = _dt.datetime.now().isoformat(timespec="seconds")
    
    expanded_items = []
    for item in items:
        naam = item.get("naam")
        aantal = int(item.get("aantal", 1))
        for _ in range(aantal):
            expanded_items.append(naam)
    items_text = ", ".join(expanded_items)
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO orders (created_at, items, co2_info, totaalbedrag) VALUES (?, ?, ?, ?)",
            (created_at, items_text, (co2_text or ""), round(float(totaal) or 0.0, 2)),
        )
        return cur.lastrowid