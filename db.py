import sqlite3

con = sqlite3.connect("JobHuntDB.db")

cur = con.cursor()

print("executing")

res = cur.execute("SELECT * FROM Resumes")

print(res.fetchone())
