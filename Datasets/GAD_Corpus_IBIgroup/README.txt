GAD Corpus Charactersitics
--------------------------------------------------------------------------------

The GAD corpus is distributed within two files:

- GAD_Y_N.csv: describes positives (Y) and negatives (N) relations between genes and diseases.
- GAD_F.csv: describes falses (F) relations between genes and diseases.

The format of both files are as follows with header and tab delimiters:

Column  1: Identification record from GAD.
Column  2: Type of association (Y, N or F).
Column  3: Gene symbol provided by GAD record.
Column  4: Gene name provided by GAD record.
Column  5: EntrezGeneID provided by GAD record.
Column  6: Gene text in the sentence provided by BioNER.
Column  7: Gene text offset in the sentence provided by BioNER at 'sentence level'.
Column  8: Disease name provided by GAD record.
Column  9: Disease text in the sentence provided by BioNER.
Column 10: Disease text offset in the sentence provided by BioNER at 'sentence level'.
Column 11: Sentence provided by GAD record.


--------------------------------------------------------------------------------

If you use this corpus for any publication purposes, you are requested to cite the source article:

À. Bravo, J. Piñero, N. Queralt, M. Rautschka and L.I. Furlong, "Extraction of relations between genes and diseases from text and large-scale data analysis: implications for translational research". (Submitted).

The GAD corpus is made available under the Open Database License whose full text can be found at http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License whose text can be found at http://opendatacommons.org/licenses/odbl/1.0/
