# Makefile for LaTeX compilation with BibTeX

# Executables (you can change to xelatex/lualatex if needed)
LATEX = pdflatex
BIBTEX = bibtex

# Main .tex file (without .tex extension)
MAIN = paper

# Output PDF
PDF = $(MAIN).pdf

# Intermediate files to clean
AUX_FILES = $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log \
            $(MAIN).out $(MAIN).toc $(MAIN).lof $(MAIN).lot \
            $(MAIN).fls $(MAIN).fdb_latexmk $(MAIN).synctex.gz \
            $(MAIN).run.xml *.blg *.bbl *.bcf *.run.xml

.PHONY: all clean veryclean

# Default target
all: $(PDF)

# Compile the PDF with proper BibTeX handling
$(PDF): $(MAIN).tex
	$(LATEX) $(MAIN)
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

# Clean auxiliary files (keeps the PDF)
clean:
	rm -f $(AUX_FILES)

# Clean everything including PDF
veryclean: clean
	rm -f $(PDF)