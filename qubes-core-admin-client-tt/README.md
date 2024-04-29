# `qubesadmintt` notes
The tools provided here are Tweaks to the original _qubesadmin_ part of
[qubes-core-admin-client](https://github.com/QubesOS/qubes-core-admin-client)
repository. Tweaked version of the original tools will have a `-tt` suffix.

## Internals & Features

### Core `qubesadmintt` Tweaks
All of the core classes, methods and properties are inherited from _qubesadmin_
base class with the following exception:
- `QubesArgumentParser`, `VmNameAction` and `VmNameGroup` classes of
`qubesadmin.tools` are overridden to add Unix like Wildcard matching support
to the admin utilities which support more than one VM (i.e. 
_qvm-check-tt, qvm-kill-tt, qvm-pause-tt, qvm-remove-tt, qvm-shutdown-tt,
qvm-start-tt, qvm-unpause-tt, qvm-ls-tt, qvm-remove-tt_ but most importantly
_qvm-ls-tt_). So you could use `qvm-ls-tt fedora*`, `qvm-shutdown-tt *template`,
...
- `qubesadmin.spinner` is modified to allow cool braille alphabet based spinner.
With further funny ones to come (see ToDo).

### `qvm-ls-tt`
Forked from the original
[qvm_ls.py](https://github.com/QubesOS/qubes-core-admin-client/blob/main/qubesadmin/tools/qvm_ls.py)
code, there are additional improvements to it. A _perf_ output format is added.
Run `qvm-ls-tt --help-formats` to see what data it provides. *MAXMEM* column is
now available. Filtering of VMs based on **internal** feature tag is possible
via `--internal <yes|no|both>` option. Similarly, the `--servicevm <yes|no|both>`
option allows filtering based on ServiceVM status. The two `--class` and
`--label` options allow filtering based on VM Class or Label.

## Installation & Removal
To install the tools at your `~/bin` and the libraries at your `~/.local/lib`,
directories, run this command in the current directory.
```
make install
```
To remove them from your system, run this command in the current directory:
```
make remove
```

## Limitations, Issues & ToDo
- Only tested on Qubes OS 4.2.1. Backward compatibility is unknown.
- Sorting of VMs based on their memory usage, storage usage, etc. should be
added to to `qvm-ls-tt`.
- Filtering of VMs based on last access dates should be added to `qvm-ls-tt`
- Cool terminal [spinners](https://github.com/manrajgrover/py-spinners) should
be added with option for user to select their desired one via a _.conf_ file.
