from pathlib import Path

#Project Structure
PROJECT_NAME = ""
folders = [
    "templates",
    "static",
    "database"
]
files = [
    "README.md",
    ".gitignore",
    "requirements.txt",
    "app.py",
    "database/__init__.py",
    "utils.py",
    ".env"
]

#Create Project root
root = Path(PROJECT_NAME)
root.mkdir(exist_ok=True)
#print(root)
#create folders
for folder in folders:
    (root/folder).mkdir(parents=True,exist_ok=True) 
#create files
for file in files:
    path = root/file
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():
        path.touch()
print(f"Project Structure Created Successfully:{root.resolve()}")
