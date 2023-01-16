#!/usr/bin/bash
pandoc -s --metadata title="420-941-VA Web Services" --mathjax -c github.css "$1".md -o "$1".html

