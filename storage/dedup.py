import sqlite3
import time
from pathlib import Path

def init_db(db_path: Path):
    """Initialize the database table."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id TEXT PRIMARY KEY,
                created_at REAL
            )
        ''')

def is_processed(db_path: Path, link_id: str) -> bool:
    """Check if the link has already been processed."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute('SELECT 1 FROM history WHERE id = ?', (link_id,))
        return cursor.fetchone() is not None

def mark_processed(db_path: Path, link_id: str):
    """Mark link as processed with current timestamp."""
    with sqlite3.connect(db_path) as conn:
        conn.execute('INSERT OR IGNORE INTO history (id, created_at) VALUES (?, ?)', (link_id, time.time()))

def cleanup_old_records(db_path: Path, days_to_retain: int):
    """Delete records older than specified days."""
    cutoff = time.time() - (days_to_retain * 86400)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute('DELETE FROM history WHERE created_at < ?', (cutoff,))
        print(f"[Clean] Cleaned {cursor.rowcount} old records (Retained {days_to_retain} days)")
