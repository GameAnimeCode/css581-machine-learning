# CSS 581: Machine Learning

Assignments and projects for CSS 581 Machine Learning at the University of Washington Bothell (UWB).

Each assignment is a folder with Python code and a writeup. Writeups are Markdown (Quarto) files that build to PDF. The first-page block, running header, and footer follow the course formatting, and the build script fills in personal details so they stay out of the repository.

## Assignments

<!-- assignments:start -->
No assignments yet.
<!-- assignments:end -->

## Layout

```
.
├── assignments/          # one folder per assignment (created by script)
│   └── a1-example/
│       ├── src/main.py   # code
│       ├── writeup.qmd   # report source
│       └── preamble.tex  # page layout (copied from the template)
├── templates/
│   ├── code/main.py      # Python starter
│   └── writeup/          # writeup.qmd and preamble.tex
├── scripts/
│   ├── setup-python.sh       # create .venv and install requirements
│   ├── new-assignment.sh     # create an assignment from the templates
│   └── build-writeup.sh      # render writeups to PDF
├── requirements.txt      # Python dependencies
└── .devcontainer/        # development container
```

## Setup

### 1. Open the dev container

Open the repository in VS Code and choose **Reopen in Container**. The image includes Python 3, Quarto, and TinyTeX (the LaTeX engine Quarto uses for PDF output).

The container requests an NVIDIA GPU (`--device nvidia.com/gpu=all` in `.devcontainer/devcontainer.json`). If your machine has no GPU configured for containers, remove that line.

To work outside the container, install Python 3 and [Quarto](https://quarto.org), then run `quarto install tinytex`.

### 2. Create the Python environment

```bash
scripts/setup-python.sh
source .venv/bin/activate
```

This creates one virtual environment at `.venv` for the whole course and installs `requirements.txt`. VS Code picks it up as the default interpreter in the container.

To add a package, put it in `requirements.txt` and run `scripts/setup-python.sh` again.

### 3. Add your personal details

Create `.local/student.env` (the `.local/` folder is gitignored, so this file is never committed):

```bash
STUDENT_NAME="First Last"
STUDENT_LAST="Last"
STUDENT_ID="000000000"
STUDENT_EMAIL="netid@uw.edu"
```

The build script reads this file and injects the values into the PDF header. If the file is missing, the build still works and uses placeholder values.

## Working on an assignment

### Create it

```bash
scripts/new-assignment.sh a1-linear-regression
```

This creates `assignments/a1-linear-regression/` with `writeup.qmd`, `preamble.tex`, and `src/main.py`, and refreshes the [Assignments](#assignments) list above from the folders in `assignments/`. The script refuses to overwrite an existing folder.

### Write the code

Edit `assignments/<name>/src/main.py`, then run it from the repository root with the virtual environment active:

```bash
python assignments/a1-linear-regression/src/main.py
```

### Write the report

Open `writeup.qmd` and fill in the macros in the block at the top:

| Macro | Meaning |
|---|---|
| `\courseName` | Course line, top right of page 1 (prefilled) |
| `\dueDate` | Date, second line on the right of page 1 |
| `\asgTitle` | Running header from page 2 onward, for example `Assignment 1: Linear Regression` |
| `\codeRepo` | Link shown in the footer on every page (prefilled) |

`\courseName` and `\codeRepo` come prefilled, so usually only `\dueDate` and `\asgTitle` need editing. Name, last name, ID, and email are not in this file. They come from `.local/student.env` at build time.

Write the report below the title block in regular Markdown. `preamble.tex` controls the page layout and rarely needs changes.

### Build the PDF

```bash
scripts/build-writeup.sh a1-linear-regression   # one assignment
scripts/build-writeup.sh                        # every assignment
```

The PDF is written next to the source as `assignments/<name>/writeup.pdf`.

Built files (`*.pdf`, `writeup.tex`, `*_files/`, `.quarto/`) are gitignored, so the repository holds sources only. The page layout is:

- **Page 1:** name and course on the first line, ID, email, and date on the second. No running header.
- **Page 2 onward:** last name on the left and the assignment title on the right.
- **Every page:** code repository link on the left and "Page X of Y" on the right.
