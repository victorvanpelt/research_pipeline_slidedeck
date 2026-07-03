# Regenerates the deck's code/terminal screenshots (pygments one-dark renders).
# Needs: pip install pygments pillow   (or PYTHONPATH to a dir that has them)
# Usage: python3 materials/render_shots.py [path-to-research_pipeline_example-clone]
import os
import sys

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-1000/research_pipeline_example"
OUT = os.path.join(os.path.dirname(HERE), "images")


def find_font():
    import glob
    for pat in ["/home/victor/.local/share/fonts/nerd/JetBrainsMonoNerdFontMono-Regular.ttf",
                "/home/victor/.local/share/fonts/nerd/JetBrainsMonoNLNerdFontMono-Regular.ttf",
                "/usr/share/fonts/google-noto/NotoSansMono-Regular.ttf"]:
        hits = glob.glob(pat)
        if hits:
            return hits[0]
    return None


FONT_PATH = find_font()
print("font:", FONT_PATH)


def render(code, lexer_name, outfile, title, font_name, line_numbers=True):
    lexer = get_lexer_by_name(lexer_name)
    fmt = ImageFormatter(style="one-dark", font_name=font_name, font_size=22,
                         line_numbers=line_numbers, line_pad=8, image_pad=16,
                         line_number_bg="#282c34", line_number_fg="#5c6370",
                         line_number_pad=12)
    png = highlight(code, lexer, fmt)
    tmp = "/tmp/_code_render.png"
    with open(tmp, "wb") as f:
        f.write(png)
    body = Image.open(tmp).convert("RGB")
    bar_h = 44
    canvas = Image.new("RGB", (body.width, body.height + bar_h), "#21252b")
    canvas.paste(body, (0, bar_h))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT_PATH, 20) if FONT_PATH else ImageFont.load_default()
    d.text((16, (bar_h - 20) // 2 - 2), title, fill="#9da5b4", font=font)
    canvas.save(outfile)
    print("wrote", outfile, canvas.size)


# pygments ImageFormatter resolves fonts via fc-list; try JetBrains, fall back
FONT = "DejaVu Sans Mono"
for candidate in ["JetBrainsMonoNL Nerd Font Mono", "JetBrainsMono Nerd Font Mono",
                  "Noto Sans Mono", "DejaVu Sans Mono"]:
    try:
        ImageFormatter(font_name=candidate)
        FONT = candidate
        break
    except Exception:
        continue
print("pygments font:", FONT)

# --- Repo file renders (regenerate whenever the repo changes) --------------
do_code = open(f"{REPO}/1_code/code.do").read()
render(do_code, "stata", f"{OUT}/paste-4.png", "1_code/code.do", FONT)

mk = open(f"{REPO}/makefile.mak").read().splitlines()
render("\n".join(mk[0:37]), "make", f"{OUT}/paste-19.png", "makefile.mak", FONT)
render("\n".join(mk[38:59]), "make", f"{OUT}/paste-13.png", "makefile.mak  (Quarto targets)", FONT)

gi = open(f"{REPO}/.gitignore").read()
render(gi, "bash", f"{OUT}/paste-5.png", ".gitignore", FONT)

# paste-16: rebuild-everything terminal (plain `make` via the wrapper Makefile)
console = """$ make
Rscript --vanilla 1_code/code.r
quarto render 4_drafts/paper_example.qmd
quarto render 4_drafts/presentation_example.qmd
"""
render(console, "console", f"{OUT}/paste-16.png", "Terminal — research_pipeline_example", FONT)

# --- Chapter 4 assets -------------------------------------------------------
# N1 (paste-21): what an agent session looks like inside the pipeline.
# Illustrative transcript; every command, path, and edit shown is real
# (the edit is the same winsorize robustness change whose git diff is paste-20).
agent_session = """$ claude "Add a robustness check: winsorize scaled
  earnings at the 1st/99th percentiles before
  the main regression."

* Reading 1_code/code.r
* Editing 1_code/code.r (+5 lines)
* Running: make clean && make
    Rscript --vanilla 1_code/code.r
    quarto render 4_drafts/paper_example.qmd
    quarto render 4_drafts/presentation_example.qmd

Done. Review my change with: git diff 1_code/code.r
"""
render(agent_session, "console", f"{OUT}/paste-21.png",
       "Terminal — an agent working in research_pipeline_example", FONT)

# N2 (paste-22): your own rerun. Lines below are captured from a real run.
rerun = """$ make clean
Cleaned 2_process, 3_output, and render artifacts.
$ make
Rscript --vanilla 1_code/code.r
quarto render 4_drafts/paper_example.qmd
Output created: paper_example.pdf
quarto render 4_drafts/presentation_example.qmd
Output created: presentation_example.pdf
"""
render(rerun, "console", f"{OUT}/paste-22.png",
       "Terminal — rerunning the pipeline yourself", FONT)

# AGENTS.md render (paste-23) for the guardrail slide callout
agents_md = open(f"{REPO}/AGENTS.md").read()
render(agents_md, "markdown", f"{OUT}/paste-23.png", "AGENTS.md", FONT)
