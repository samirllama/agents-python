# agents-python/utils/db.py
import sqlite3
from pathlib import Path
from typing import Dict, Any

class MetadataDB:
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'data' / 'movies_metadata.db'
        self.conn = sqlite3.connect(str(db_path))
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        """Initialize database schema"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            title TEXT PRIMARY KEY,
            year TEXT,
            genre TEXT,
            director TEXT,
            actors TEXT,
            rating TEXT,
            votes TEXT,
            revenue TEXT,
            metascore TEXT
        )
        ''')
        self.conn.commit()

    def insert_metadata(self, metadata: Dict[str, Any]):
        """Insert or update movie metadata"""
        self.cursor.execute('''
        INSERT OR REPLACE INTO metadata
        (title, year, genre, director, actors, rating, votes, revenue, metascore)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metadata['title'],
            metadata['year'],
            metadata['genre'],
            metadata['director'],
            metadata['actors'],
            metadata['rating'],
            metadata['votes'],
            metadata['revenue'],
            metadata['metascore']
        ))
        self.conn.commit()

    def get_metadata(self, title: str) -> Dict[str, Any] | None:
        """Retrieve metadata for a movie"""
        self.cursor.execute('SELECT * FROM metadata WHERE title = ?', (title,))
        row = self.cursor.fetchone()
        if row:
            return {
                'title': row[0],
                'year': row[1],
                'genre': row[2],
                'director': row[3],
                'actors': row[4],
                'rating': row[5],
                'votes': row[6],
                'revenue': row[7],
                'metascore': row[8]
            }
        return None

    def close(self):
        """Close database connection"""
        self.conn.close()
