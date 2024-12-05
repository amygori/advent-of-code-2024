import os
import sys
import shutil


def copy_template_directory(day_number):
    template_dir = "template"
    new_dir_name = f"day{day_number}"
    new_dir_path = os.path.join(os.getcwd(), new_dir_name)

    try:
        # Copy the template directory to the new directory
        shutil.copytree(template_dir, new_dir_path)
    except FileExistsError:
        print("File already exists.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_day.py <day_number>")
        sys.exit(1)

    day_number = sys.argv[1]
    copy_template_directory(day_number)
