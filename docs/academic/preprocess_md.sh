#!/bin/bash

INPUT="SCIENTIFIC_PAPER_LATEX.md"
OUTPUT="preprocessed_content.md"

# Remove YAML frontmatter if it exists
sed '1,/^---$/d' "$INPUT" | \
# Fix markdown headers
sed 's/^#\+/\\section*/' | \
# Fix tables by adding proper LaTeX formatting
sed 's/|/ \& /g' | \
# Fix math expressions
sed 's/\^\([0-9-+()]*\)/^\{\1\}/g' | \
# Fix special characters
sed 's/—/---/g' \
> "$OUTPUT"

echo "Preprocessed markdown saved to $OUTPUT"
