# `qubesimgconvertertt` & `qvm-get-image-tt` notes
Custom effects for Qubes OS AppMenu icons. Provided effects are _overlay, 
thin-border, thick-border_ as well as the standard _tint_ which will use the 
label color for their effects. Special effects of _untouched, invert, mirror,
flip_ are also available. The _invert_ mode is very useful for untrusted AppVM.
Screenshot and use case of effects are at the end of this page.

### Internals & Features
The `qubesimgconvertertt` library is derived from the original
[qubesimgconverter](https://github.com/QubesOS/qubes-linux-utils/tree/main/imgconverter/qubesimgconverter)
library and `Image` class. Effects are written as individual methods.

The `qvm-get-image-tt` is an independent utility which could be used as a
drop-in replacement for `qvm-get-image` or `qvm-get-tinted-image`. Based on
[qubes-app-linux-img-converter](https://github.com/QubesOS/qubes-app-linux-img-converter)
utilities with additional `--filter` & `--mirror` options which allows user to
select the desired filter. An extra `--ANSI` function is provided to quickly
check the results directly within the terminal. By default, it checks for an 
special `ttfilter` VM feature and uses it to determine the custom effect.
If the `ttfilter` key is not present or is invalid, the default tint effect will
be applied. To change the default filter of any VM:

```
qvm-features VMNAME ttfilter <tint|overlay|thin-border|thick-border|untouched|invert|mirror|flip>
```

### Installation & Removal
To install the library & tool at your `~/.local/lib` & `~/bin` directories, 
run this command in the current directory:
```
make install
```
To remove them from your system, run this command in the current directory:
```
make remove
```

### Limitations, Issues & ToDo
These are the current known limitation with the tool & library:
- It should be noted that the current systray effects are not implemented via the
qubesimgconverter library but are rather a part of
[qubes-gui-daemon](https://github.com/QubesOS/qubes-gui-daemon/tree/main/gui-daemon)
- Effects are already fast but there is always room for improvements. 
