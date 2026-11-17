# 🧹 Desktop Cleaner

A Python-based file organization tool that automatically sorts files into categorized folders, helping keep your desktop and directories clean and organized.

## ✨ Features

- **Automatic Organization:** Sorts files into folders based on their extensions.
- **Category Detection:** Supports Images, Documents, Videos, Audio, Code, and Others.
- **Dry Run Preview:** Preview file movements before confirming.
- **Undo Operation:** Restore files to their original locations.
- **Persistent History:** Saves undo history so it remains available after restarting the program.
- **Duplicate Handling:** Prevents overwriting files by generating unique filenames.
- **Custom Directory:** Choose any folder you want to organize.
- **Error Handling:** Handles file operation errors.
- **Logging:** Records operations and errors in `cleaner.log`.

## 🛠️ Technologies Used

- Python
- `os`
- `shutil`
- `json`
- `logging`

No external Python packages are required.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/s-mahapule/desktop-cleaner.git
```

### 2. Open the project folder

```bash
cd desktop-cleaner
```

### 3. Run the application

```bash
python main.py
```

## 📖 How to Use

1. Run the program.
2. Enter the path of the folder you want to organize.
3. Review the dry-run preview.
4. Confirm the operation to organize your files.
5. Use the undo option if you want to restore moved files.

### Example

Before organization:

```text
test_desktop/
├── sample.py
├── sample.txt
└── sample.xyz
```

After organization:

```text
test_desktop/
├── Code/
│   └── sample.py
├── Documents/
│   └── sample.txt
└── Others/
    └── sample.xyz
```

## 📁 Project Structure

```text
desktop-cleaner/
│
├── main.py
├── README.md
├── .gitignore
└── test_desktop/
    ├── Code/
    ├── Documents/
    ├── Images/
    ├── Videos/
    ├── Others/
    ├── sample.py
    ├── sample.txt
    └── sample.xyz
```

## ⚠️ Safety Notes

- Test the application using sample files or a backup folder first.
- Review the preview before confirming file movements.
- Avoid running it on important directories until you are comfortable with its behavior.
- The undo history is stored locally in `history.json`.

## 🔮 Future Improvements

- Graphical user interface (GUI).
- More file categories and customizable extensions.
- Scheduling automatic cleanup.
- Detailed organization reports.

## 👩‍💻 Author

**Shafia Mahapule**

GitHub: [@s-mahapule](https://github.com/s-mahapule)

---

*Built with Python to make file organization simple and efficient.*
