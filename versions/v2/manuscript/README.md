# Hardin's binary arrays and Barker's conjectures

For all heights `h>=2` and widths `w>=2`, the number of labeled binary arrays whose overlapping two-bit windows are nondecreasing in every row and column is

`N(h,w) = 2 + 2*binomial(h+w,h) + binomial(h+w-2,h-1)`.

The note proves this formula by classifying rows and counting their inclusion chains with two independent terminal rows. It proves Hardin's empirical polynomials and Barker's conjectural generating functions and recurrences in OEIS A202330--A202334, both Kotesovec diagonal recurrences in A202329, and both first-column identities in A202335. It also proves the least eventual recurrence order and asymptotic at every fixed width. The classical permutation maximum associated with A110610 is attributed to the Putnam solution literature.

## Files and build

- `note.tex`: complete mathematical note with embedded bibliography.
- `note.pdf`: readable note, distributed separately from the source archive.
- `verify.py`: arbitrary-width exact checks using Python 3.9 or later and its standard library.
- `four_column.py`: exact four-column continuation-polynomial checks, imported by `verify.py`.
- `checks.json`: the complete expected output of the default checker.
- `metadata.json`: creators, license, coverage, and source locator.
- `source-manifest.json`: exact source member sizes and SHA256 hashes.

Build with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, run `pdflatex note.tex` twice. The bibliography is embedded, so no BibTeX invocation is required. Required LaTeX packages are `geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `fontenc`, `lmodern`, and `hyperref`.

Run the checks from the extracted source directory:

```sh
python3 verify.py > computed.json
cmp checks.json computed.json
```

Arithmetic is exact. The checks compare direct row-triple transfer counts at every height 2--14 and width 2--8 with the binomial formula, enumerate every binary array in all nine rectangles with both dimensions 2--4, and certify the coefficient identities for the five source polynomials and generating functions. Both diagonal rational identities are checked as polynomial identities after denominator multiplication. The cyclic-product maximum is independently enumerated for permutation sizes 2--8. Four-column checks also certify the continuation invariant coefficient by coefficient and compare counts through source index 210. These finite ranges are consistency checks accompanying the all-index written proofs.

## Scope of the pinned Lean declarations

The note links both files at commit `79dfe4f731baccd42dd3c56cf6331a0ddd3cafdb`.
`HardinA202330.result` has as its conclusion the native four-column quartic for positive indices, its zero-constant formal generating function, and its signed recurrence from index six. `TransferMatrix.cardMatrix` gives the finite-word count from transition-fiber and initial-fiber identities; its four-column specialization retains all 36 ordered row pairs. The general two-parameter formula, other widths, diagonal, first two columns, minimal-order and asymptotic conclusions have written proofs in the note.

General fixed-width rationality was proved in Dougherty-Bliss, Koutschan, Ter-Saakov and Zeilberger, *The (Symbolic and Numeric) Computational Challenges of Counting 0-1 Balanced Matrices*, Theorem 2.2 (2025; arXiv first version 2024). The note distinguishes that general method from the explicit binomial count.

Creators: Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore). License: Creative Commons Attribution 4.0 International (`cc-by-4.0`). OEIS entries are cited for their mathematical definitions and formulas; their full texts are not redistributed in the source archive.
