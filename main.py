import os
import shutil
import json
import logging

"""Identify a file category and move the file."""

logging.basicConfig(
    filename="cleaner.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
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


def save_history(history):
    """Save movement history to a JSON file."""

    with open("history.json", "w") as file:
        json.dump(history, file, indent=4)


def load_history():
    """Load previously saved movement history."""

    if not os.path.exists("history.json"):
        return []

    with open("history.json", "r") as file:
        return json.load(file)


def organize_file(file_path, desktop_path, summary, history):
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
        history.append({"original": file_path, "moved": destination})
        save_history(history)
        summary[category] += 1
        print(f"Moved {filename} -> {category}")
        logging.info(f"Moved {filename} -> {category}")

    except OSError as error:
        print(f"Could not move {filename}: {error}")
        logging.error(f"Could not move {filename}: {error}")


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


def undo_last_operation(history):
    """Restore files to their original locations."""

    if not history:
        print("Nothing to undo.")
        return

    print("\n--- UNDO PREVIEW ---")

    for move in reversed(history):
        print(f"{move['moved']} -> {move['original']}")

    choice = input("\nUndo last operation? (y/n): ").strip().lower()

    if choice != "y":
        print("Undo cancelled.")
        logging.info("Undo operation cancelled by user.")
        return

    remaining_history = []
    for move in reversed(history):
        try:
            if not os.path.exists(move["moved"]):
                print(f"File not found: {move['moved']}")
                remaining_history.append(move)
                continue

            if os.path.exists(move["original"]):
                print(
                    f"Cannot restore: original file already exists: {move['original']}"
                )
                remaining_history.append(move)
                continue

            os.makedirs(os.path.dirname(move["original"]), exist_ok=True)
            shutil.move(move["moved"], move["original"])
            print(f"Restored: {os.path.basename(move['original'])}")
            logging.info(f"Restored: {move['original']}")

        except OSError as error:
            print(f"Could not restore file: {error}")
            logging.error(f"Could not restore file: {error}")
            remaining_history.append(move)

    history[:] = list(reversed(remaining_history))
    save_history(history)
    if history:
        print(f"Undo partially completed. {len(history)} file(s) remain.")
    else:
        print("Undo operation completed.")


def clean_desktop(desktop_path):
    """Preview and organize files in the target folder."""

    summary = {category: 0 for category in categories}
    summary["Others"] = 0
    history = load_history()

    if not os.path.isdir(desktop_path):
        print("Error: Desktop folder does not exist.")
        return

    files = os.listdir(desktop_path)
    planned_moves = []

    print("\n--- DRY RUN: File Organization Preview ---")

    for filename in files:
        file_path = os.path.join(desktop_path, filename)

        if os.path.isfile(file_path):
            extension = os.path.splitext(filename)[1].lower()
            destination_folder = "Others"

            for category, extensions in categories.items():
                if extension in extensions:
                    destination_folder = category
                    break

            print(f"{filename} --> {destination_folder}/")
            planned_moves.append(file_path)

    if not planned_moves:
        print("No new files to organize.")

        if history:
            undo_last_operation(history)

        return

    print(f"\nTotal files to organize: {len(planned_moves)}")

    choice = input("\nProceed with file organization? (y/n): ").strip().lower()

    if choice != "y":
        print("Operation cancelled. No files were moved.")
        logging.info("File organization cancelled by user.")
        return

    for file_path in planned_moves:
        organize_file(file_path, desktop_path, summary, history)

    show_report(summary)
    undo_last_operation(history)


def main():
    print("Desktop Cleaner Started!")

    desktop_path = (
        input("Enter the folder path you want to organize: ").strip().strip('"')
    )

    if not os.path.isdir(desktop_path):
        print("Error: Invalid folder path.")
        logging.error(f"Invalid folder path: {desktop_path}")
        return

    clean_desktop(desktop_path)


if __name__ == "__main__":
    main()
