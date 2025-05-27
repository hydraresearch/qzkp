#!/bin/bash

# Set the output filenames
OUTPUT="paper.pdf"
TEX_OUTPUT="paper.tex"
MARKDOWN="SCIENTIFIC_PAPER_LATEX.md"
TEMP_MD="temp_content.md"

# Clean up previous build files
echo "Cleaning up previous build files..."
rm -f *.aux *.log *.out *.toc *.bbl *.blg *.bcf *.run.xml *.fls *.fdb_latexmk $TEX_OUTPUT $OUTPUT $TEMP_MD

# Remove YAML frontmatter from markdown if it exists
echo "Preprocessing markdown..."
if grep -q '^---' "$MARKDOWN"; then
    # Remove everything between --- and the next ---
    sed '1,/^---$/d' "$MARKDOWN" | sed '/^---$/,$d' > "$TEMP_MD"
else
    cp "$MARKDOWN" "$TEMP_MD"
fi

# Create a complete LaTeX document
echo "Creating LaTeX document..."
cat > $TEX_OUTPUT << 'EOL'
\documentclass[11pt,a4paper]{article}
\input{header.tex}
\begin{document}
\maketitle
\input{abstract.tex}
\input{temp_content.md}
\end{document}
EOL

# Compile with xelatex for better font handling
echo "Compiling with xelatex..."
xelatex -interaction=nonstopmode $TEX_OUTPUT

# Run bibtex if needed
if [ -f "${TEX_OUTPUT%.*}.aux" ]; then
    echo "Running BibTeX..."
    bibtex ${TEX_OUTPUT%.*}.aux
    # Second pass to resolve references
    xelatex -interaction=nonstopmode $TEX_OUTPUT > /dev/null
fi

# Final compilation
xelatex -interaction=nonstopmode $TEX_OUTPUT > /dev/null

# Clean up temporary files
rm -f "$TEMP_MD"

# Check if compilation was successful
if [ -f "$OUTPUT" ]; then
    echo "Compilation successful! Output file: $OUTPUT"
    open "$OUTPUT"  # Open the PDF on macOS
else
    echo "Compilation failed. Check the error messages above."
    exit 1
fi
