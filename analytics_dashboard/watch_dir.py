import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analytics_dashboard.settings')

django.setup()

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dashboard.models import Company, Application, CoverLetter, Resume
from django.utils import timezone
import time
import re

class Watcher:
    DIRECTORY_TO_WATCH = "/Users/imigh/Desktop/resumes"

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
            name_parts = file_name.strip().split("_")
            company_name = name_parts[-1].split(".")[0]
            application_number_match = re.search(r"\d+", company_name)
            application_number = application_number_match.group(0) if application_number_match else None
            company_name = re.sub(r"\d+", "", company_name)

            print(f"Company Name: {company_name}")
            print(f"Application Number: {application_number}")
            print(f"File created: {file_name}")

            try:
                company, created = Company.objects.get_or_create(name=company_name)

                if re.search(r"^.*CoverLetter.*\.pdf$", file_name):
                    application = Application.objects.create(
                        company=company,
                        application_number=application_number,
                        date_applied=timezone.now(),
                        status="pending"
                    )
                    CoverLetter.objects.create(
                        application=application,
                        content='',
                        file_path=event.src_path
                    )
                    print(f"Inserted cover letter {file_name} into the database.")

                elif re.search(r"^.*Resume.*\.pdf$", file_name):
                    application = Application.objects.create(
                        company=company,
                        application_number=application_number,
                        date_applied=timezone.now(),
                        status="pending"
                    )
                    Resume.objects.create(
                        application=application,
                        file_path=event.src_path
                    )
                    print(f"Inserted resume {file_name} into the database.")

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    w = Watcher()
    w.run()
