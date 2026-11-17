import os
import shutil

"""Identify a file category and move the file."""

# File categories
categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Audio": [".mp3", ".wav"],
    "Code": [".py", ".java", ".cpp", ".html", ".css", ".js"],
}


def get_unique_filename(destination):
    """Generate a unique filename to prevent overwriting."""

    if not os.path.exists(destination):
        return destination

    folder = os.path.dirname(destination)
    filename = os.path.basename(destination)
    name, extension = os.path.splitext(filename)

    counter = 1

    while os.path.exists(destination):
        new_filename = f"{name}_{counter}{extension}"
        destination = os.path.join(folder, new_filename)
        counter += 1

    return destination


def organize_file(file_path, desktop_path, summary):
    """Identify a file category and move the file."""

    filename = os.path.basename(file_path)
    extension = os.path.splitext(filename)[1].lower()

    category = "Others"

    for folder, extensions in categories.items():
        if extension in extensions:
            category = folder
            break

    try:
        folder_path = os.path.join(desktop_path, category)
        os.makedirs(folder_path, exist_ok=True)

        destination = os.path.join(folder_path, filename)
        destination = get_unique_filename(destination)

        shutil.move(file_path, destination)

        summary[category] += 1
        print(f"Moved {filename} -> {category}")

    except OSError as error:
        print(f"Could not move {filename}: {error}")


def show_report(summary):
    """Display the cleaning summary."""

    print("\n========== CLEANING REPORT ==========")

    total_files = 0

    for category, count in summary.items():
        print(f"{category}: {count} files")
        total_files += count

    print("-------------------------------------")
    print(f"Total files organized: {total_files}")
    print("Cleaning completed successfully!")


def clean_desktop(desktop_path):
    """Process all files in the target folder."""

    summary = {category: 0 for category in categories}
    summary["Others"] = 0

    if not os.path.isdir(desktop_path):
        print("Error: Desktop folder does not exist.")
        return

    files = os.listdir(desktop_path)

    for filename in files:
        file_path = os.path.join(desktop_path, filename)

        if os.path.isfile(file_path):
            organize_file(file_path, desktop_path, summary)

    show_report(summary)


def main():
    desktop_path = os.path.join(os.getcwd(), "test_desktop")

    print("Desktop Cleaner Started!")

    clean_desktop(desktop_path)


if __name__ == "__main__":
    main()
