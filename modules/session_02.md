# Session 2 — Clone, Build, and Run

## Introduction

You have your tools installed and your fork created. This session connects everything: you will clone your fork to your computer, create the conda environment that all remaining sessions depend on, and run your first Python script inside VS Code. By the end, you will have made your first commit and push to GitHub.

Reference: Before You Begin (`session_00.md`)

---

> **Before you start:** Confirm you completed all steps in `session_00.md`. Open Git Bash and run `conda --version`, `git --version`, and `git config --list`. All three should return output with no errors. If any fail, work through `session_00.md` before continuing.

---

## Step 1 — Clone Your Fork

Cloning downloads a copy of your fork from GitHub to your local machine.

Open **Git Bash** from the Windows Start menu. Navigate to the folder where you want to store the project — for example, your Desktop:

```
cd Desktop
```

Clone your fork, replacing `YOUR-USERNAME` with your GitHub username:

```
git clone https://github.com/YOUR-USERNAME/automating-analytics-workshop.git
```

This creates a folder called `automating-analytics-workshop`. Navigate into it:

```
cd automating-analytics-workshop
```

Verify the files are there:

```
dir
```

You should see the top-level repo contents, including the `student_report/` folder.

---

## Step 2 — Open the Repo in VS Code

Open VS Code, then open the repo folder you just cloned:

1. **File → Open Folder**
2. Navigate to and select the `automating-analytics-workshop` folder
3. Click **Select Folder**

The folder will appear in the Explorer pane on the left. You can also open it directly from Git Bash:

```
code .
```

### Confirm Git Bash is your terminal

Open the built-in terminal with `` Ctrl+` ``. Confirm the terminal panel shows **bash** in the upper right corner. If you see PowerShell instead, click the dropdown arrow (`∨`) next to the `+` icon, select **Git Bash**, and set it as the default via `Ctrl+Shift+P` → **Terminal: Select Default Profile** → **Git Bash**.

---

## Step 3 — Create the Conda Environment

The repo includes `student_report/environment.yml`, which defines every package this workshop uses. Create the environment from it:

```
conda env create -f student_report/environment.yml
```

This downloads and installs all dependencies. It will take a few minutes the first time. When it finishes you should see:

```
# To activate this environment, use
#     $ conda activate student-report
```

Activate the environment:

```
conda activate student-report
```

Your terminal prompt should change to show `(student-report)` at the beginning. Verify Python is coming from the right place:

```
python --version
```

You should see Python 3.11.x.

> **Troubleshooting — `conda activate` not recognized:**
> Run `conda init bash` once, then close and reopen the terminal. Try `conda activate student-report` again.

---

## Step 4 — Select the Python Interpreter in VS Code

VS Code needs to know which Python to use:

1. Press `Ctrl+Shift+P` to open the Command Palette
2. Type **Python: Select Interpreter** and press Enter
3. Select the entry that shows **student-report**:
   `Python 3.11.x ('student-report': conda)`

If `student-report` does not appear in the list, click **Enter interpreter path** and paste the path manually:

```
C:\Users\YOUR-USERNAME\miniconda3\envs\student-report\python.exe
```

Replace `YOUR-USERNAME` with your Windows username. Once selected, the interpreter name appears in the VS Code status bar at the bottom right.

---

## Step 5 — Your First Commit

You will create a small Python script, run it, and commit it to your fork. This is the same workflow you will use every session.

### Create a scratch file

In the Explorer pane, right-click in the file list and choose **New File**. Name it `scratch.py` and add:

```python
import pandas as pd

print("Environment is working!")
print(f"pandas version: {pd.__version__}")
```

### Run it

In the VS Code terminal (confirm `(student-report)` is active) and run:

```
python scratch.py
```

You should see:

```
Environment is working!
pandas version: 2.x.x
```

If you see `ModuleNotFoundError: No module named 'pandas'`, the wrong Python interpreter is active. Re-check Step 4.

### Stage, commit, and push

Check what Git sees:

```
git status
```

`scratch.py` is listed as untracked. Stage it:

```
git add scratch.py
```

Commit:

```
git commit -m "add scratch.py to test environment"
```

Push to GitHub:

```
git push
```

The first time you push, Git Credential Manager will open a browser window asking you to sign in to GitHub. Complete the sign-in, then return to the terminal.

Visit `https://github.com/YOUR-USERNAME/automating-analytics-workshop` — you should see `scratch.py` in your fork.

---

## What You Have Now

| | Status |
|---|---|
| Fork cloned locally | ✓ |
| `student-report` conda environment created and active | ✓ |
| VS Code using the correct Python interpreter | ✓ |
| First commit and push to GitHub | ✓ |

This setup carries through every remaining session. You will activate `student-report`, open the terminal in VS Code, write code, and commit — the same loop each time.

---

## Additional Resources

- [Conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
- [Git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf)
