# `qubes-update-tt` notes
This tool is a package manger helper for Qubes OS templates.
It was originally created during my Qubes OS 3.2 days, when I had to download
updates for a lot of templates during night to circumvent daily download caps.
I've added installation, search, remove and other functionalities at later
stages. After being away from Qubes OS for a long time and returning to Qubes OS 
4.2, some parts of it became obsolete because of the modern Salt interface, the
new graphical updater and `qvm-vm-update` tool. It is still very useful as some
of its features are not available via the mentioned tools.

### Internals & Features
The tool is written entirely in pure bash. Using some coreutils for text and
message processing. It is compatible with apt, dnf, emerge and pacman based
templates which have qrexec installed on them. It could be used to perform
package install, search and removal operations as well as downloading updates
without installation or actual installation of updates (which is discouraged).
Command help is available at top of the file which hopefully should make it
self-explanatory.

### Installation & Removal
To install the tool at your '~/bin' directory, run this in the current dir:
```
make install
```
To remove it from your system run this in the current directory:
```
make remove
```

### Limitations & Issues
Some of the known limitations and issues at the current status of the tool:
- It uses Qubes Admin API calls via `qubesd-query(1)` utility. Currently only
available in dom0.
- Gentoo's emerge does not detect qvm-run/qrexec-client as a valid tty. So --ask
option of the emerge does not work. Thus, automatic update is disabled for
Gentoo as it deserves careful user intervention.
- Currently tested only on Qubes OS 4.2.1
