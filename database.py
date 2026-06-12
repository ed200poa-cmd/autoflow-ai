import aiosqlite
import json
from datetime import datetime

DB_PATH = "leads.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                company TEXT,
                budget INTEGER,
                message TEXT,
                score TEXT,
                reason TEXT,
                email_draft TEXT,
                follow_up_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def save_lead(lead_data: dict, analysis: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO leads (name, email, company, budget, message, score, reason, email_draft, follow_up_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_data.get("name"),
            lead_data.get("email"),
            lead_data.get("company"),
            lead_data.get("budget"),
            lead_data.get("message"),
            analysis.get("score"),
            analysis.get("reason"),
            analysis.get("email_draft"),
            analysis.get("follow_up_date"),
            datetime.utcnow().isoformat(),
        ))
        await db.commit()
        return cursor.lastrowid


async def get_all_leads() -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM leads ORDER BY created_at DESC") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_lead_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) as total FROM leads") as cursor:
            total = (await cursor.fetchone())[0]
        async with db.execute("SELECT score, COUNT(*) as count FROM leads GROUP BY score") as cursor:
            rows = await cursor.fetchall()
            breakdown = {row[0]: row[1] for row in rows}
    return {"total": total, "breakdown": breakdown}
