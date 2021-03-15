#!/usr/bin/env python3

from argparse import ArgumentParser
import os.path
from pprint import pprint

p = ArgumentParser(
    description="generate dot graph from units' relationships"
)
p.add_argument(
    "-r", "--relationships",
    type=lambda r: set(map(str.upper, r.split(","))),
    help="limit to this list of comma-separated relationships"
)
p.add_argument("-A", "--no-aliases", action="store_true", help="exclude aliases")
p.add_argument("-o", "--only-files", action="store_true", help="include only units named in arguments")
p.add_argument("files", metavar="FILE", nargs="+", help="unit file paths")
options = p.parse_args()

keys = [
    ("Before", "After"),
    ("WantedBy", "Wants"),
    ("RequiredBy", "Requires"),
]

def filter_files(files):
    seen_files = set()
    for f in sorted(files, key=lambda f: os.path.islink(f)):
        stat = os.stat(f)
        stat = stat.st_dev, stat.st_ino
        if stat not in seen_files:
            yield f
        seen_files.add(stat)

if options.no_aliases:
    options.files = list(filter_files(options.files))

if options.relationships:
    keys = [ pair for pair in keys if set(map(str.upper, pair)) & options.relationships ]

kmap = { a: b for a, b in keys }
kmap.update({ b: a for a, b in keys })
keys = { key: fwd for key_pair in keys for key, fwd in zip(key_pair, (False, True)) }

print("digraph g {")
print("node [ shape = box ]")

for fn in options.files:
    with open(fn) as f:
        for line in f:
            key, _, value = line.rstrip().partition("=")
            if key not in keys: continue
            values = value.split()
            fwd = keys[key]
            if not fwd:
                key = kmap[key]
            for value in values:
                if options.only_files and value not in options.files:
                    continue
                if fwd:
                    print(f"\"{value}\" -> \"{fn}\" [ label = {key} ]")
                else:
                    print(f"\"{fn}\" -> \"{value}\" [ label = {key} ]")

print("}")
