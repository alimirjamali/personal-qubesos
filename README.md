# Tools, Configs, Customization & Tweaks for Qubes OS

## Tools for DOM0 / ManagementVM
### qubes-template-update
This tool was originally created during my Qubes OS 3.2 days. I had to download
updates for many templates during night to circumvent daily download caps.
I added installation, search and remove functionality at later stages. After
being away from Qubes OS for a long time and returning to Qubes OS 4.2, some
parts of it has become obsolete because of the modern Salt interface or the new
graphical updater and `qvm-vm-update` tool. Yet it is still useful as some of 
its features are not yet implemented via the mentioned tools.

### qubes-label
A simple command line tool to list/create/get/index/remove Qubes `labels`. It is
advisable to add a proper suffix to custom labels. This would prevent probable
conflicts with new official labels (if any). Good examples are 'custom','user', 
etc. Also never delete standard labels.
