from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "expenses.db"
)

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS expenses(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
            )"""
        )

init_db()

# FastMCP server instance
expense_tracker_mcp = FastMCP(name='Fast MCP Demo Server')

@expense_tracker_mcp.tool()
def add_expense(date: str, amount: float, category: str, subcategory: str = '', note: str = '') -> str:
    """
    Add an expense to the database.
    """
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note)
        )
    return "Expense added successfully."

@expense_tracker_mcp.tool()
def get_expenses() -> list:
    """
    Retrieve all expenses from the database.
    """
    with sqlite3.connect(DB_PATH) as c:
        c.row_factory = sqlite3.Row
        cursor = c.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

if __name__ == "__main__":
    expense_tracker_mcp.run()