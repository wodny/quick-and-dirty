# Quick and dirty solutions to some frustrating problems

## x-paste-htmltable-as-csv

Select a part of a table in a internet browser (e.g. Firefox) using 
the mouse while keeping the Ctrl key down. Copy it to clipboard. Then 
paste the table in the CSV format in another program (e.g. vim,
`:r !x-paste-htmltable-as-csv`).

Without using this kind of a script cells are pasted line by line also 
including the excess whitespace.

It's useful to use the vim [Tabular] plug-in after pasting the CSV 
contents.

[Tabular]: https://github.com/godlygeek/tabular
