# Build tasks for the Data Management session slides.
# `make` renders presentation.qmd to presentation.pdf with Quarto.

QUARTO ?= quarto

.PHONY: all slides clean help

all: slides

slides:
	$(QUARTO) render presentation.qmd

clean:
	rm -f presentation.pdf presentation.tex

help:
	@echo "make (or make slides)  render presentation.qmd to presentation.pdf"
	@echo "make clean             delete the rendered PDF and the intermediate .tex"
	@echo ""
	@echo "If Quarto is not on your PATH: make QUARTO=/path/to/quarto"
