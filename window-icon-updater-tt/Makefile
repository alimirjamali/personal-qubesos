.SILENT:

BINDIR := ~/bin
LIBDIR := `python3 -m site --user-site`
AUTORUNDIR := ~/.config/autostart

info:
	$(info Run 'make install' to replace original icon-receiver daemon with TT version)
	$(info It will copy .destkop files to '~/.config/autorun' and 'icon-receiver-tt')
	$(info to '~/bin' directories. This daemon requires 'qubesimgconvertertt' lib.)

install:
	$(info Reboot for changes to take effect)
	install -v -D -C -m 755 icon-receiver-tt $(BINDIR)
	install -v -D -C -m 644 qubes-icon-receiver.desktop $(AUTORUNDIR)
	install -v -D -C -m 644 qubes-icon-receiver-tt.desktop $(AUTORUNDIR)
