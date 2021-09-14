<h1 align="center">Mizuna</h1>

<div align="center">

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/srodriguez1850/Mizuna?label=version)
![GitHub Actions Build Status](https://github.com/srodriguez1850/Mizuna/actions/workflows/mizuna-btd.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/srodriguez1850/Mizuna/badge.svg?branch=main)](https://coveralls.io/github/srodriguez1850/Mizuna?branch=main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

<div align="center">

https://user-images.githubusercontent.com/9145577/132977027-54ba2d74-3559-438a-b4d5-aba1ab80e25e.mp4

</div>

Mizuna is a Python package meant to automate uploading graphs and visualizations (e.g., matplotlib, Seaborn) to
Overleaf. In reality, it's a small wrapper to invoke a git add/commit/push to a repository on files of your
choice.

### Why?

Data visualizations need constant iteration. I noticed I was spending ~10 seconds every time I needed to upload a new
figure through the Overleaf web UI to verify it looked proper. Mizuna freed cycles by rendering the visualization and
automatically uploading it for me.

The concept is a simplified version of the [gigaleaf](https://github.com/gigantum/gigaleaf) library without needing
to use Gigantum for data analysis. This is a local alternative that works directly with Overleaf (or any git 
repository).

## Installation

Installation is done through [PyPI](https://pypi.org/project/mizuna/):

```
$ pip install mizuna
```

## How to Use

### Quick Start

Brief example workflow:
- Initialize Mizuna
- Create and save a figure with your favorite visualization library (e.g., Seaborn, matplotlib)
- Track the resulting file with Mizuna
- Sync with your remote repository

```python
# Import Mizuna object
import seaborn as sns
import matplotlib.pyplot as plt
from mizuna import Mizuna

# Repository URL
remote = 'https://git.overleaf.com/thisisarandomproject'
# Directory to clone the remote into
repo_dir = 'CloneHere'

# Create Mizuna object
m = Mizuna(remote, repo_dir)

# Generate and save a chart (e.g., Seaborn, matplotlib, etc.)
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
sns.scatterplot(x=x, y=y)
plt.savefig('mychart.png', format='png')

# Track a file
m.track('mychart.png')
# Sync with repository
m.sync()
```

### The `Mizuna` Object

Initialize the Mizuna object with the repository URL, the name of the local directory to clone the remote into,
and (optionally) whether the local directory is within a networked drive (e.g., a Z: drive or Google Drive File Stream).

If the drive is networked, pass `True` into the `networked_drive` parameter for Mizuna to work properly.
See [Limitations](#Limitations).

```python
remote = 'https://git.overleaf.com/thisisarandomproject' # Repository URL
repo_dir = 'CloneHere' # Directory to clone the remote into

m = Mizuna(remote, repo_dir) # Mizuna object
```

```python
remote = 'https://git.overleaf.com/thisisarandomproject' # Repository URL
repo_dir = 'CloneHere' # Directory to clone the remote into

m = Mizuna(remote, repo_dir, networked_drive=True) # Mizuna object (networked drive)
```

### Tracking

Mizuna can track a single file:

```python
m.track('mychart.png') # Track one file
```

A single file renamed on the remote:

```python
m.track('mychart.png', 'figure1.png') # Track one file and rename on remote
```

A list of files:

```python
m.track(['mychart1.png', 'mychart2.png', 'mychart3.png']) # Track multiple files
```

A list of tuples (files renamed on the remote):

```python
f1 = ('mychart1.png', 'figure1.png')
f2 = ('mychart2.png', 'figure2.png')
f3 = ('mychart3.png', 'figure3.png')

m.track([f1, f2, f3]) # Track files as tuples
```

Or a dictionary containing multiple files with their respective renames on the remote:

```python
sync_files = { 'mychart1.png': 'figure1.png',
               'mychart2.png': 'figure2.png' }
m.track(sync_files) # Track multiple files with their renames on remote
```

### Untracking

If you need to untrack a file or all files:

```python
m.untrack('mychart.png') # Untrack a single file
m.untrack_all() # Untrack all files
```

### Checking Tracked Files

If you need to see all the files currently tracked by Mizuna:

```python
m.track_list # List all files tracked
```

### Syncing

And finally, push to Overleaf (or your git repository) when ready:

```python
m.sync() # Pulls changes, replaces changes with the tracked figures, and pushes
```

## Limitations

- Files from networked drives (e.g., Z drive, Google Drive File Stream) may throw an incorrect SameFileError exception.
    - See https://bugs.python.org/issue33935.
    - To circumvent this issue, pass `True` into the `networked_drive` parameter in the Mizuna constructor.
      - This prevents samefile checks from shutil.copy().
- Overleaf git URLs only work with [Premium](https://www.overleaf.com/user/subscription/plans) accounts.
  - [Referring](https://www.overleaf.com/user/bonus) a single user to Overleaf unlocks git URLs.
- Mizuna is currently forced to output verbose. Future updates will curb output.

## License

Usage is provided under the MIT License. See LICENSE for full details.
