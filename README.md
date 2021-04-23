# Mizuna

Mizuna is a package that automates uploading files (e.g., visualizations) to Overleaf projects.

|Integration|Status|
|-------|------|
|GitHub Actions|[![GitHub Actions Build Status](https://github.com/srodriguez1850/Mizuna/actions/workflows/mizuna-btd.yml/badge.svg)]()
|TravisCI|[![TravisCI Build Status](https://travis-ci.com/srodriguez1850/Mizuna.svg?branch=main)](https://travis-ci.com/srodriguez1850/Mizuna)|
|CircleCI|[![CircleCI Build Status](https://circleci.com/gh/srodriguez1850/Mizuna.svg?style=shield)](https://app.circleci.com/pipelines/github/srodriguez1850/Mizuna?branch=main)|
|Test Coverage|[![Coverage Status](https://coveralls.io/repos/github/srodriguez1850/Mizuna/badge.svg?branch=main)](https://coveralls.io/github/srodriguez1850/Mizuna?branch=main)|

## Limitations

- Files from networked drives may throw an incorrect SameFileError exception.
    - See https://bugs.python.org/issue33935
    - To circumvent, the option to prevent samefile checks from shutil.copy() is given.
