# Qubes OS Tweak Tools
My personal Qubes OS Tweak Tools, configs and related files.

## Icons
Mostly icons for `qubes-label-tt`. Full description in [icons](/icons)
sub-directory.

## Tweak Tools & Libraries
### `qubesappmenustt` Lib & `qvm-appmenus-tt` Utility 
Tweak Tools for Qubes OS AppMenus. Full description is available in
[qubesappmenustt](/qubesappmenustt) sub-directory.

### `qubesimgconvertertt` Lib & `qvm-get-image-tt` Utility
Custom effects for Qubes OS icons & images. Full description is available in
[qubesimgconvertertt](/qubesimgconvertertt) sub-directory.

### `qubes-label-tt` Utility
Label management tool for Qubes OS. Full description is available in
[qubes-label-tt](/qubes-label-tt) sub-directory.

### `qubes-update-tt` Utility
My personal template updater tweak tool. This utility is not installed by 
default as a part of Tweak Tools. More information and background in
[qubes-update-tt](/qubes-update-tt) sub-directory.

### `icon-receiver-tt` Daemon
Custom icon effects for the running VM Apps. Full description is available in
[window-icon-updater-tt](/window-icon-updater-tt) sub-directory.

## Installation & Removal
Individual libraries or tools could be installed via the __Makefiles__ inside
their directories. Each __Makefile__ has its own __install & remove__ targets
as well as a default __info__ target which prints brief explanation of the
operation. __qubesimgconvertertt__ is a dependency for __qubesappmenustt__ &
__icon-receiver-tt__ daemon. All of the tools & libraries with the exception of
__qubes-update-tt__ could be installed in the project root via this command:
```
make install
```
And removed via this command:
```
make remove
```

## References & Links
- The ongoing 
[discussion on Qubes OS forum](https://forum.qubes-os.org/t/programming-approaches-to-alternative-appmenu-icon-effects-setting-default-workspace-per-qube-additional-label-colors/25381)
on icon effects, additional labels, workspace/VM.
