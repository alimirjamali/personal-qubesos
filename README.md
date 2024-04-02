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

### qubes-label-tweak-tool
A simple command line tool to list/create/get/index/remove Qubes `labels`. It is
advisable to add a proper suffix to custom labels. This would prevent probable
conflicts with new official labels (if any). Good examples are 'custom','user', 
etc. Also never delete standard labels.

Honorable mention: Willy-JL's
[Qubes-Scripts](https://github.com/Willy-JL/Qubes-Scripts)
has been an inspiration for lots of work in this tool.

### qvm-get-filtered-image
As of March 2024 (Qubes OS 4.2.1), only tinted icons are supported for
application icons. `qvm-get-image` and `qvm-get-tinted-image` are the starting
point of this work. They are available via 
[qubes-app-linux-img-converter](https://github.com/QubesOS/qubes-app-linux-img-converter)
repository. Those tools depend on `qubesimgconverter` library which is a part of
[qubes-linux-utils](https://github.com/QubesOS/qubes-linux-utils.git)
repository. Strangely the current systray effects are not implemented via the
same library.

### qvm-appmenus-tweak-tool
Since `qvm-appmenus(1)` calls qubesimgconverter.tint function directly to
performs the tint effect on the locally stored icons, an alternative is required
if we want custom effects for AppMenu icons. Moreover, other useful actions
such as launching qube apps in their dedicated workspace could be automated with
such a tool. Thus qvm-appmenus-teak-tool is born.
