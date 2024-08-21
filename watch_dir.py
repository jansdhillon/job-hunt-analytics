import os
import time
import re
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def connect():
    """Connect to the SQLite database."""
    con = sqlite3.connect("JobHuntDB.db")
    return con, con.cursor()


class Watcher:
    DIRECTORY_TO_WATCH = "../../Desktop/resumes"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        print("Listening for files...")
        try:
            while True:
                time.sleep(300)
                print("Looping...")
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            company_name = file_name.strip().split("_")[-1].split(" ")[0]
            print(f"Company Name: {company_name}")
            print(f"File created: {file_name}")

            try:
                con, cur = connect()

                if re.search(r"^.*CoverLetter.*\.pdf$", file_name):
                    cur.execute("SELECT id FROM Resumes WHERE company_name = ?", (company_name,))
                    resume_id = cur.fetchone()
                    resume_id = resume_id[0] if resume_id else None

                    cur.execute(
                        "INSERT INTO CoverLetters (resume_id, content, cover_letter_file_path) VALUES (?, ?, ?)",
                        (resume_id, '', event.src_path)
                    )
                    con.commit()
                    print(f"Inserted cover letter {file_name} into the database.")

                elif re.search(r"^.*Resume.*\.pdf$", file_name):
                    cur.execute(
                        "INSERT INTO Resumes (position_title, applied_on, company_name, status, resume_file_path) VALUES (?, ?, ?, ?, ?)",
                        ("Unknown", time.strftime('%Y-%m-%d'), company_name, "Pending", event.src_path)
                    )
                    con.commit()
                    print(f"Inserted resume {file_name} into the database.")

            except sqlite3.Error as e:
                print(f"SQLite error: {e}")
            finally:
                con.close()


if __name__ == "__main__":
    w = Watcher()
    w.run()
