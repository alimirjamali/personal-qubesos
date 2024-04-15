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
self-explanatory. Some use cases:

1. Only checking for updates & notifying dom0. If the template is halted, it is
turned on, checked for update and turned off again. A pair of systemd unit &
timer are provided for this purpose to schedule it for 3:00±60m:
```
qubes-update-tt --all check-only
```
2. Downloading updates without installation only for templates tagged for update
availability. And keep the template running after download. A pair of systemd
unit & timer are provided for this purpose to schedule it for 5:00±60m:
```
qubes-update-tt --all --if-updates update --refresh --download-only -y --skip-broken --after-update running
```
3. Installing `htop` on all minimal templates:
```
qubes-update-tt "*-minimal" install htop
```
4. List repos for Fedora templates:
```
qubes-update-tt "*fedora*" repolist
```
5. Search for blender on XFCE & Arch templates:
```
qubes-update-tt "*xfce*,archlinux" search blender
```

### Installation & Removal
To install the tool at your `~/bin` directory and systemd units at 
`~/.config/systemd/user` run this in the current directory:
```
make install
```
To remove them from your system run this in the current directory:
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
