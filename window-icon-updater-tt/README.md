# `icon-receiver-tt` notes
This is a tweaked version of the original 
[icon-receiver](https://github.com/QubesOS/qubes-gui-daemon/tree/main/window-icon-updater)
`window-icon-updater` daemon. It will check for 'ttfilter' feature tag of the VM 
and provides alternative effects to the default tint. Available alternative
effects are listed at [qubesimgconvertertt](/qubesimgconvertertt) page. 

### Internals & Features
Original daemon is suppressed via special XDG .desktop file at
`~/.config/autostart` and the tweaked daemon is loaded via another .desktop file.
The daemon itself is installed at `~/bin` directory. It loads the original
`icon-receiver` as a Python library and overloads the tweaks on top of it.
VM restart is necessary after changing the `ttfilter` feature tag of the VM.

### Installation & Removal
To install the tool & .desktop files at your `~/bin` & `~/.config/autostart`
directories, run this command in the current directory:
```
make install
```
To remove them from your system, run this command in the current directory:
```
make remove
```
System restart or login/logoff is necessary to properly reload the daemon.

### Limitations, Issues & ToDo
These are the currently known limitation with the tool & library:
- Daemon does not properly register running VMs after logoff/login. This is a
random behaviour which demands further study.
