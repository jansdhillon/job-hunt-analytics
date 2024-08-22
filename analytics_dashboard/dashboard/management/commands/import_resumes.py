import os
import re
from django.core.management.base import BaseCommand
from dashboard.models import Company, Position, Application, CoverLetter, Resume
from django.utils import timezone

class Command(BaseCommand):
    help = 'Import existing resumes and cover letters from the resumes directory'

    def handle(self, *args, **kwargs):
        base_dir = "/Users/imigh/Desktop/resumes"

        for month_dir in os.listdir(base_dir):
            month_path = os.path.join(base_dir, month_dir)
            if os.path.isdir(month_path):
                for file_name in os.listdir(month_path):
                    file_path = os.path.join(month_path, file_name)
                    if os.path.isfile(file_path):
                        # Extract the company name from the filename
                        company_name = file_name.strip().split("_")[-1].split(".")[0]
                        print(f"Processing {file_name} for company {company_name}")

                        # Find or create the company
                        company, created = Company.objects.get_or_create(name=company_name)

                        if re.search(r"^.*CoverLetter.*\.pdf$", file_name):
                            # Get the associated resume by filtering through related models
                            resume = Resume.objects.filter(application__position__company=company).first()

                            if not resume:  # If no resume (and thus no application) exists, create a new one
                                position = Position.objects.create(
                                    title="Unknown",
                                    company=company
                                )
                                application = Application.objects.create(
                                    position=position,
                                    date_applied=timezone.now(),
                                    status="pending"
                                )
                            else:
                                application = resume.application

                            # Create the cover letter
                            CoverLetter.objects.create(
                                application=application,
                                content='',  # Assuming content is to be processed later
                                file_path=file_path  # Corrected field name
                            )
                            print(f"Inserted cover letter {file_name} into the database.")
                        elif re.search(r"^.*Resume.*\.pdf$", file_name):
                            # Create a new position and application for the resume
                            position = Position.objects.create(
                                title="Unknown",
                                company=company
                            )
                            application = Application.objects.create(
                                position=position,
                                date_applied=timezone.now(),
                                status="pending"
                            )
                            Resume.objects.create(
                                application=application,
                                file=file_path  # Corrected field name
                            )
                            print(f"Inserted resume {file_name} into the database.")

        self.stdout.write(self.style.SUCCESS('Successfully imported resumes and cover letters'))
