# Data Management Session

Slides for the Data Management session of the Doctoral Orientation Week at WHU - Otto Beisheim School of Management. The session makes the case for managing research data and code deliberately. A well-organized project lets one command reproduce every result, even years later on a new laptop. The closing chapter turns to AI coding agents, with one rule above all: the agent may write the code, it never does the research.

The deck is one [Quarto](https://quarto.org) file, `presentation.qmd`, which renders to `presentation.pdf` on the WHU beamer template. Many slides show a real companion repository, the [research pipeline example](https://github.com/victorvanpelt/research_pipeline_example), where raw data go in and one command rebuilds the analysis, the paper, and the slides.

## Repository structure

```
data_management_session/
├── presentation.qmd   the deck's source; this is the file to edit
├── presentation.pdf   the rendered slides
├── presentation.tex   intermediate LaTeX from the render (kept for debugging)
├── images/            figures and screenshots shown on the slides
├── materials/         WHU beamer template, fonts, bibliography, LaTeX support files
├── Makefile           build tasks: `make` renders the deck
├── AGENTS.md          rules for AI coding agents working in this repo
├── .gitignore         keeps local agent configuration out of git
├── LICENSE            MIT license
└── README.md          this file
```

## Building the slides

```bash
git clone https://github.com/victorvanpelt/data_management_session.git
cd data_management_session
make
```

`make` runs `quarto render presentation.qmd` and writes `presentation.pdf`. `make clean` deletes the rendered PDF and the intermediate `.tex`, so the next `make` rebuilds them from scratch. If Quarto is not on your `PATH`, point to it with `make QUARTO=/path/to/quarto`.

The deck uses `date: today`, so the title slide shows the render date. Re-render shortly before the talk.

### Requirements

- **Quarto** to render the deck.
- **A LaTeX distribution** for the PDF. [TinyTeX](https://yihui.org/tinytex/) is the easiest (`quarto install tinytex`).
- **GNU Make.** Ships with macOS and Linux; on Windows, run the commands from Git Bash or WSL.

## AI coding agents

`AGENTS.md` states the rules AI coding agents must follow in this repository. Most agentic coding tools read it automatically. In short: edit `presentation.qmd` only, never touch the rendered PDF or the template by hand, verify by rerunning `make`, and leave all changes uncommitted for the maintainer to review.

---

Maintained by [Victor van Pelt](https://www.victorvanpelt.com). Released under the [MIT License](LICENSE): reuse and adapt freely, as long as the copyright and license notice stay with copies. Third-party files in `materials/` (the media9 LaTeX package, the Helvetica Neue fonts) keep their own licenses.
