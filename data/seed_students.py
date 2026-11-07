from pathlib import Path
import sqlite3
from faker import Faker

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "students.db"
fake = Faker("en_IN")
Faker.seed(2024)


def seed() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    connection = sqlite3.connect(DB_PATH)
    connection.executescript(
        """
        CREATE TABLE students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            branch TEXT NOT NULL,
            cgpa REAL NOT NULL,
            tenth_percent REAL NOT NULL,
            twelfth_percent REAL NOT NULL,
            graduation_year INTEGER NOT NULL,
            backlogs INTEGER NOT NULL,
            placed BOOLEAN NOT NULL DEFAULT 0,
            phone TEXT NOT NULL
        );
        """
    )
    branches = ("CSE", "IT", "ECE", "Mechanical", "EEE")
    rows = []
    for index in range(200, 280):
        branch = branches[index % len(branches)]
        rows.append(
            (
                f"STU{index}",
                fake.name(),
                f"student{index}@example.edu",
                branch,
                round(fake.random.uniform(6.2, 9.8), 2),
                round(fake.random.uniform(58, 96), 1),
                round(fake.random.uniform(58, 95), 1),
                2026 + (index % 2),
                fake.random_int(min=0, max=2),
                1 if index % 7 == 0 else 0,
                fake.phone_number(),
            )
        )
    connection.executemany(
        """INSERT INTO students
        (student_id, name, email, branch, cgpa, tenth_percent, twelfth_percent,
         graduation_year, backlogs, placed, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    connection.commit()
    connection.close()
    print(f"Created {len(rows)} synthetic students in {DB_PATH}")


if __name__ == "__main__":
    seed()
