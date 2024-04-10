# Tools, Configs, Customization & Tweaks for Qubes OS

## Icons
Mostly icons for qubes-label-tweak-tool. Full description in [icons](/icons)
sub-directory.

## Tools for DOM0 / ManagementVM
### qubes-update-tweak-tool
This tool was originally created during my Qubes OS 3.2 days. I had to download
updates for many templates during night to circumvent daily download caps.
I've added installation, search, remove and other functionalities at later 
stages. After being away from Qubes OS for a long time and returning to Qubes OS 
4.2, some parts of it became obsolete because of the modern Salt interface, the
new graphical updater and `qvm-vm-update` tool. It is still useful as some of
its features are not available via the mentioned tools.

### qubes-label-tweak-tool
A simple command line tool to list/create/get/index/remove Qubes OS labels. It 
is advisable to add a proper suffix to custom labels. This should prevent
probable conflicts with new official labels (if any). Good examples are 
'custom','user', etc. Also never delete standard labels.

Honorable mention: Willy-JL's
[Qubes-Scripts](https://github.com/Willy-JL/Qubes-Scripts)
has been an inspiration for this tool.

### qvm-get-filtered-image, qubesimgconvertertweaks
As of March 2024 (Qubes OS 4.2.1), only tinted icons are supported for
application icons. `qvm-get-image` and `qvm-get-tinted-image` were the starting
point of this work. Part of 
[qubes-app-linux-img-converter](https://github.com/QubesOS/qubes-app-linux-img-converter)
repository. `qubesimgconverter` which is a part of
[qubes-linux-utils](https://github.com/QubesOS/qubes-linux-utils.git)
repository is the basis of qubesimgconvertertweaks library. 
It should be noted that the current systray effects are not implemented via the
qubesimgconverter library.

### qvm-appmenus-tweak-tool
Since `qvm-appmenus(1)` calls qubesimgconverter.tint function directly to tint 
icons, an alternative was required to perform custom effects on AppMenu icons.
Other useful actions such as launching qube apps in their dedicated workspace
could be automated via this tool. Thus qvm-appmenus-teak-tool was born.
