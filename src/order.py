"""orders.py — eenvoudige orderopslag voor proof-of-concept

Slaat bij elke betaling één record op in data/orders.db met:
- id (AUTOINCREMENT) — ordernummer
- created_at (TEXT, ISO 8601)
- items_json (TEXT) — JSON-lijst met {naam, aantal}
- totaal (REAL)

Gebruik: in main.py roep je bij /betalen:
    items = [{"naam": p["naam"], "aantal": p["aantal"]} for p in producten]
    order_id = save_order(items, totaal)
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
    """Maak de tabel 'orders' aan als die er nog niet is."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                items_json TEXT NOT NULL,
                totaal REAL NOT NULL
            )
            """
        )

def save_order(items: List[Dict], totaal: float) -> Optional[int]:
    """Sla een order op en retourneer het ordernummer (id).

    items: lijst met dicts: {naam: str, aantal: int}
    totaal: totaalbedrag (float)

    All-or-nothing via transaction context.
    """
    if not items:
        return None
    created_at = _dt.datetime.now().isoformat(timespec="seconds")
    items_json = json.dumps(items, ensure_ascii=False)
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO orders (created_at, items_json, totaal) VALUES (?, ?, ?)",
            (created_at, items_json, float(totaal) or 0.0),
        )
        return cur.lastrowid