# `qubesappmenustt` & `qvm-appmenus-tt` notes
Custom effects for Qubes OS AppMenu icons. Provided effects are explained at 
[qubesimgconvertertt](/qubesimgconvertertt) page which is a dependency of the
above tool. Screenshots and use cases of effects are included at the bottom of
this page.

### Internals & Features
The `qubesappmenustt` library is derived from the original
[qubesappmenus](https://github.com/QubesOS/qubes-desktop-linux-common/tree/main/qubesappmenus)
library and `Appmenus` class. The only derived function is the `appicons_create`
and the rest are inherited. The library checks for an special `ttfilter` VM
feature and uses it to determine the custom effect per VM. If the `ttfilter` key
is not present or is invalid, the default tint effect will be applied.

`qvm-appmenus-tt` is the front end to the qubesappmenustt library. It is derived
from the original `qubesappmenus` code. It could be used as a drop-in
replacement to qvm-appmenus-tt. Or could be run independently as follow:

```
qvm-features VMNAME ttfilter <tint|overlay|thin-border|thick-border|untouched|invert|mirror|flip>
qvm-appmenus-tt VMNAME --update --force
```

### Installation & Removal
To install the library & tool at your '~/.local/lib' & '~/bin' directories, 
run this command in the current directory:
```
make install
```
To remove them from your system, run this command in the current directory:
```
make remove
```

### Limitations, Issues & ToDo
These are the currently known limitation with the tool & library:
- Every time user updates their template or adds/removes a single App to 
VM's AppMenu, the original `qubesappmenus` & `qvm-appmenus` are invoked,
effectively overwriting our custom icon effects. Proper deep study of AppMenus
service is needed to determine if it would be possible to replace it with our
own service or to use a hook to run our tool after it. Ideally all of this
should happen in user space without any requirement for root privileges or sudo.
- Launching applications in user defined workspace/VM could be implemented. This
could be done via customizing .desktop files `Exec=` and `wmctrl(1)` utility. Or
an alternative to `qvm-run` could be written.

