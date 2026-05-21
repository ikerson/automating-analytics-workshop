# Session 2 — Setting Up the Environment

## Introduction

Before you can write any Python, you need three things working together: a copy of the workshop code on your computer, a conda environment with all the right packages installed, and VS Code configured to use that environment. This session walks through each step hands-on. By the end, you will run your first Python script, see it execute inside the correct environment, and save your work to Git.

Reference: Session 1 — The Problem + Tooling Overview

---

## Before You Begin

Confirm your tools are installed. Open **Command Prompt** on Windows (`Win + R`, type `cmd`, press Enter) or **Terminal** on Mac, and run:

```
conda --version
git --version
```

Both should print a version number. If either command is not found, stop and ask your instructor before continuing.

---

## Step 1 — Clone Your Fork

Cloning downloads a copy of your fork from GitHub to your local machine.

In Command Prompt (Windows) or Terminal (Mac), navigate to the folder where you want to store the project. For example, to put it on your Desktop:

```
cd Desktop
```

Then clone your fork. Replace `YOUR-USERNAME` with your GitHub username:

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

> **Mac:** Use `ls` instead of `dir`.

You should see the top-level repo contents, including the `student_report/` folder.

---

## Step 2 — Open the Repo in VS Code

Open VS Code, then open the repo folder you just cloned:

1. In VS Code: **File → Open Folder**
2. Navigate to and select the `automating-analytics-workshop` folder
3. Click **Select Folder** (Windows) or **Open** (Mac)

The folder will appear in the Explorer pane on the left.

You can also open it from the terminal if VS Code's `code` command is in your PATH:

```
code .
```

> **Mac:** If `code .` is not recognized, open VS Code, press `Ctrl+Shift+P` (or `Cmd+Shift+P`), type **Shell Command: Install 'code' command in PATH**, and press Enter. Then try again.

---

## Step 3 — Set Up the Terminal in VS Code

VS Code has a built-in terminal so you can run commands without leaving the editor. Open it with **Terminal → New Terminal** or the keyboard shortcut `` Ctrl+` ``.

### Windows: Command Prompt (cmd)

VS Code defaults to PowerShell on Windows. This workshop uses **Command Prompt** as the primary terminal because it works reliably with conda on all GSU machines.

To switch:

1. Click the dropdown arrow (`∨`) next to the `+` icon in the terminal panel
2. Select **Command Prompt**

To make Command Prompt the default for all future terminals:

1. Press `Ctrl+Shift+P` to open the Command Palette
2. Type **Terminal: Select Default Profile**
3. Choose **Command Prompt**

### Windows: Git Bash (preferred when available)

Git Bash provides a Unix-style shell on Windows and is the preferred terminal for this workshop. However, it may be restricted on some GSU machines. To check:

1. Press `Ctrl+Shift+P` → **Terminal: Select Default Profile**
2. If **Git Bash** appears in the list, select it

If Git Bash is available, you also need to run this command once so that `conda activate` works inside it:

```
conda init bash
```

Restart VS Code after running this. Then open a new terminal and verify:

```
conda --version
```

If Git Bash is not listed, use Command Prompt as described above.

> **Mac:** Terminal (zsh) is the default and works correctly with no changes needed.

---

## Step 4 — Install the Python Extension

VS Code needs the Python extension to understand `.py` files and find conda environments.

1. Click the **Extensions** icon in the left sidebar (or `Ctrl+Shift+X`)
2. Search for **Python**
3. Install the extension published by **Microsoft** (extension ID: `ms-python.python`)

If the extension is already installed, you will see a gear icon instead of an Install button.

---

## Step 5 — Create the Conda Environment

The repo includes an `environment.yml` file inside `student_report/` that defines all packages this workshop uses. Create the environment from it:

In the VS Code terminal, make sure you are in the repo root (the `automating-analytics-workshop` folder), then run:

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

Your terminal prompt should change to show `(student-report)` at the beginning, confirming the environment is active.

Verify Python is coming from the right place:

```
python --version
```

You should see Python 3.11.x.

> **Troubleshooting — `conda activate` not recognized in CMD:**
> Run `conda init cmd.exe` once, then close and reopen the terminal. Try `conda activate student-report` again.

> **Mac:** The commands are identical. Your prompt will show `(student-report)` in the same way.

---

## Step 6 — Select the Interpreter in VS Code

VS Code needs to know which Python to use. Tell it to use the `student-report` conda environment:

1. Press `Ctrl+Shift+P` to open the Command Palette
2. Type **Python: Select Interpreter** and press Enter
3. Look for an entry that shows **student-report** — it will look something like:
   - Windows: `Python 3.11.x ('student-report': conda)`
   - Mac: `Python 3.11.x ('student-report': conda)`
4. Select it

If `student-report` does not appear in the list, click **Enter interpreter path** and paste the path manually:

- **Windows:** `C:\Users\YOUR-USERNAME\miniconda3\envs\student-report\python.exe`
- **Mac:** `/Users/YOUR-USERNAME/miniconda3/envs/student-report/bin/python`

Replace `YOUR-USERNAME` with your Windows or Mac username.

Once selected, VS Code will show the interpreter name in the bottom-right status bar.

---

## Step 7 — Configure Git

Git needs your name and email to label your commits. This is a one-time setup on each machine.

Run these two commands in the terminal (replace with your own name and the email you used to create your GitHub account):

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Verify the settings saved:

```
git config --list
```

You should see `user.name` and `user.email` in the output.

---

## Step 8 — Your First Commit

You will now create a small Python script, run it, and commit it to your fork. This is the same workflow you will use every session.

### Create a scratch file

In VS Code's Explorer pane, right-click in the file list (outside any folder) and choose **New File**. Name it `scratch.py`.

Add this code:

```python
import pandas as pd

print("Environment is working!")
print(f"pandas version: {pd.__version__}")
```

### Run it

Open the VS Code terminal (make sure `(student-report)` is active) and run:

```
python scratch.py
```

You should see:

```
Environment is working!
pandas version: 2.x.x
```

If you see a `ModuleNotFoundError` for pandas, the wrong Python interpreter is active. Re-check Step 6.

### Check what Git sees

```
git status
```

Git will report that `scratch.py` is an untracked file — it exists on your computer but Git is not tracking it yet.

### Stage the file

```
git add scratch.py
```

Run `git status` again. `scratch.py` is now listed under "Changes to be committed" — it is staged.

### Commit

```
git commit -m "add scratch.py to test environment"
```

Git records a snapshot of the staged file with your message. Run `git log` to see your commit in the history.

### Push to GitHub

```
git push
```

The first time you push, Git Credential Manager will open a browser window asking you to sign in to GitHub. Complete the sign-in, then return to the terminal.

Go to `https://github.com/YOUR-USERNAME/automating-analytics-workshop` in your browser. You should see `scratch.py` in your fork.

---

## What You Have Now

| Tool | Status |
|---|---|
| Fork cloned locally | ✓ |
| `student-report` conda environment created | ✓ |
| VS Code using the correct Python interpreter | ✓ |
| Git configured with your name and email | ✓ |
| First commit and push to GitHub | ✓ |

This setup carries through every remaining session. You will activate `student-report`, open the terminal, write code, and commit — the same loop each time.

---

## Additional Resources

- [Conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
- [Git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [VS Code keyboard shortcuts — Windows](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
- [Windows Command Line cheat sheet](https://drive.google.com/file/d/1qoAbZb0M2Adka2f--JoqIXps_SWZNJX8/view)
- [Downloading and Installing Miniconda3](https://www.youtube.com/watch?v=-H_onyfW9VE) (video)
- [Installing Git on Windows](https://youtu.be/4xqVv2lTo40?si=GVTTywH1x-hzSGE6&t=33) (video)
- [Installing VS Code on Windows](https://www.youtube.com/watch?v=CPmQwlycfGI) (video)
