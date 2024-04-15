.SILENT:

BINDIR ?= ~/bin
AUTORUNDIR ?= ~/.config/autostart

info:
	$(info 'icon-receiver-tt' is the tweaked icon receiver daemon for Qubes OS.)
	$(info It will check for 'ttfilter' feature tag of the VM and provides alternative)
	$(info effects to the default tint. Read README.md file for more information.)
	$(info Run 'make install' to replace original icon-receiver daemon with TT version)
	$(info It will copy .destkop files to '~/.config/autorun' and 'icon-receiver-tt')
	$(info to '~/bin' directories. This daemon requires 'qubesimgconvertertt' lib.)
	$(info run 'make remove' to remove it from your system.)

install: icon-receiver-tt qubes-icon-receiver.desktop qubes-icon-receiver-tt.desktop
	$(info Installing icon-receiver Tweak Tool. Reboot for changes to take effect)
	install -v -D -C -m 755 icon-receiver-tt $(BINDIR)
	install -v -D -C -m 644 qubes-icon-receiver.desktop $(AUTORUNDIR)
	install -v -D -C -m 644 qubes-icon-receiver-tt.desktop $(AUTORUNDIR)

remove:
	$(info Removing icon-receiver Tweak Tool. Reboot for changes to take effect)
	-rm -v $(BINDIR)/icon-receiver-tt
	-rm -v $(AUTORUNDIR)/qubes-icon-receiver.desktop
	-rm -v $(AUTORUNDIR)/qubes-icon-receiver-tt.desktop
