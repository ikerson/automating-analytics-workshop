# Session 2 — Clone, Build, and Run

## Introduction

::: {.callout-important}
**Before you start:** Confirm you completed all steps in [Environment Setup](session_00.md). Open Git Bash and run the following commands:

- `conda --version`
- `git --version`
- `git config --list`

All three should return output with no errors. If any fail, work through `session_00.md` before continuing.
:::

You should have your tools installed and your fork created. This session connects everything: you will clone your fork to your computer, create the conda environment that all remaining sessions depend on, and run your first Python script inside VS Code. By the end, you will have made your first commit and push to GitHub.

This session has two parts. **Steps 1–3** set up your environment. Steps 1-3 must be working before any later session, so if you get stuck here, ask for help right away. **Step 4** walks through the Git commit-and-push workflow you will repeat each session; if you run low on time, you can finish it at office hours without falling behind.


## VS Code Orientation

VS Code has four areas you will use in every session.

**Explorer** (left sidebar, `Ctrl+Shift+E`) is the file navigator. It shows every file and folder in your project. Click any file to open it in the editor. Right-click to create, rename, or delete files.

**Editor** (center) is where you read and write code. Clicking a file in the Explorer opens it here. You can have multiple files open as tabs.

**Terminal** (bottom panel, `` Ctrl+` ``) is the built-in command line. This is where you run Python scripts, activate conda environments, and execute Git commands. All terminal commands in this workshop are typed here.

**Source Control** (left sidebar, `Ctrl+Shift+G`) is the Git interface. It shows which files have changed since your last commit. You can stage, commit, and review diffs here, although this workshop will use Git commands in the terminal instead.

## Step 1 — Clone Your Fork

Cloning downloads a copy of your fork from GitHub to your local machine.

:::{.callout-tip collapse=false}
### Option A: Using VS Code

1. Open VS Code.
2. Press `Ctrl+Shift+P` to open the Command Palette.
3. Type **Git: Clone** and press Enter.
4. Paste your fork URL, replacing `YOUR-USERNAME` with your GitHub username:
   ```
   https://github.com/YOUR-USERNAME/automating-analytics-workshop.git
   ```
5. A file picker opens — choose a destination folder, for example your Desktop.
6. When VS Code asks **"Would you like to open the cloned repository?"**, click **Open**.

The `automating-analytics-workshop` folder will appear in the Explorer pane on the left.
:::

:::{.callout-tip collapse=true}
### Option B: Git Bash

1. Open **Git Bash** from the Windows Start menu.
2. Navigate to the folder where you want to store the project — for example, your Desktop:

   ```zsh
   cd Desktop
   ```

3. Clone your fork, replacing `YOUR-USERNAME` with your GitHub username:

   ```zsh
   git clone https://github.com/YOUR-USERNAME/automating-analytics-workshop.git
   ```

4. Navigate into the folder and verify the files are there:

   ```zsh
   cd automating-analytics-workshop
   ls
   ```

   You should see the top-level repo contents, including the `student_report/` folder.

5. Open the folder in VS Code:

   ```zsh
   code .
   ```
6. Confirm Git Bash is your terminal.
   - Open the built-in terminal with `` Ctrl+` ``.
   - Confirm the terminal panel shows **bash** in the upper right corner.
      - If you see PowerShell instead, click the dropdown arrow (`∨`) next to the `+` icon, select **Git Bash**, and set it as the default via `Ctrl+Shift+P` → **Terminal: Select Default Profile** → **Git Bash**.
:::


## Step 2 — Create the Conda Environment

The repo includes `student_report/environment.yml`, which defines every package this workshop uses. Create the environment from it:

```zsh
conda env create -f student_report/environment.yml
```

This downloads and installs all dependencies. It will take a few minutes the first time. When it finishes you should see:

```zsh
# To activate this environment, use
#     $ conda activate student-report
```

Activate the environment:

```zsh
conda activate student-report
```

Your terminal prompt should change to show `(student-report)` at the beginning. Verify Python is coming from the right place:

```zsh
python --version
```

You should see Python 3.11.x.

> **Troubleshooting — `conda activate` not recognized:**
> Run `conda init bash` once, then close and reopen the terminal. Try `conda activate student-report` again.

## Step 3 — Select the Python Interpreter in VS Code

VS Code needs to know which Python to use:

1. Press `Ctrl+Shift+P` to open the Command Palette
2. Type **Python: Select Interpreter** and press Enter
3. Select the entry that shows **student-report**:
   `Python 3.11.x ('student-report': conda)`

If `student-report` does not appear in the list, click **Enter interpreter path** and paste the path manually:

```zsh
C:\Users\YOUR-USERNAME\miniconda3\envs\student-report\python.exe
```

Replace `YOUR-USERNAME` with your Windows username. Once selected, the interpreter name appears in the VS Code status bar at the bottom right.

> **Checkpoint — the essential setup is done.** If Steps 1–3 are working — fork cloned, `(student-report)` shows in your terminal prompt, the VS Code interpreter is set, and `python --version` reports 3.11.x — you are ready for every Phase 1 session. Step 4 below is the Git workflow you will reuse each week. It is important, but if you are short on time or hit a credential snag, you can complete it at office hours. Do not let a Git hiccup stall the rest of the class: flag the instructor and keep moving.

## Step 4 — Your First Commit

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

```zsh
python scratch.py
```

You should see:

```
Environment is working!
pandas version: 2.x.x
```

If you see `ModuleNotFoundError: No module named 'pandas'`, the wrong Python interpreter is active. Re-check Step 3.

### Stage, commit, and push

#### Using VS Code

1. Open the Source Control pane with `Ctrl+Shift+G`. You should see `scratch.py` listed under **Changes**.
2. Click the **+** icon next to `scratch.py` to stage it.
3. Type a commit message in the box at the top — for example: `add scratch.py to test environment`
4. Click **Commit**.
5. Click **Sync Changes** (or the **↑** icon in the status bar) to push to GitHub.

The first time you push, Git Credential Manager will open a browser window asking you to sign in to GitHub. Complete the sign-in, then return to VS Code.

#### Alternative — Git Bash

Check what Git sees:

```zsh
git status
```

`scratch.py` is listed as untracked. Stage it:

```zsh
git add scratch.py
```

Commit:

```zsh
git commit -m "add scratch.py to test environment"
```

Push to GitHub:

```zsh
git push
```

The first time you push, Git Credential Manager will open a browser window asking you to sign in to GitHub. Complete the sign-in, then return to the terminal.

Visit `https://github.com/YOUR-USERNAME/automating-analytics-workshop` — you should see `scratch.py` in your fork.

## What You Have Now

| | Status |
|---|---|
| Fork cloned locally | ✓ |
| `student-report` conda environment created and active | ✓ |
| VS Code using the correct Python interpreter | ✓ |
| First commit and push to GitHub | ✓ |

This setup carries through every remaining session. You will activate `student-report`, open the terminal in VS Code, write code, and commit. This will be the same loop each time.

## Additional Resources

- [Conda cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)
- [Git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf)
