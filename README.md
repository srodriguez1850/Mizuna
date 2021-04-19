# Mizuna

Mizuna is a package that automates uploading files (e.g., visualizations) to Overleaf projects.

[![Build Status](https://travis-ci.com/srodriguez1850/Mizuna.svg?branch=main)](https://travis-ci.com/srodriguez1850/Mizuna)
[![Coverage Status](https://coveralls.io/repos/github/srodriguez1850/Mizuna/badge.svg?branch=main)](https://coveralls.io/github/srodriguez1850/Mizuna?branch=main)

## Limitations

- Files from networked drives may throw an incorrect SameFileError exception.
    - See https://bugs.python.org/issue33935
    - To circumvent, all samefile checks from shutil.copy() will return False