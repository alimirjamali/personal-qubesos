.SILENT:

BINDIR ?= ~/bin
SYSTEMDDIR ?= ~/.config/systemd/user/

.PHONY: install

info:
	$(info 'qubes-update-tt' is a package manager helper for Qubes OS templates.)
	$(info Command help is available at top of the script which should explain the details.)
	$(info Please read the README.md file for more information..)
	$(info run 'make install' in current directory to install it at your '~/bin' directory.)
	$(info run 'make remove' to remove it from your system.)

install: qubes-update-tt
	install -v -d $(BINDIR)
	install -v -D -C -m 755 qubes-update-tt $(BINDIR)
	install -v -D -C -m 644 -t $(SYSTEMDDIR) qubes-update-tt-checkonly.service
	install -v -D -C -m 644 -t $(SYSTEMDDIR) qubes-update-tt-checkonly.timer
	install -v -D -C -m 644 -t $(SYSTEMDDIR) qubes-update-tt-download.service
	install -v -D -C -m 644 -t $(SYSTEMDDIR) qubes-update-tt-download.timer

remove:
	-rm -v $(BINDIR)/qubes-update-tt
	-rm -v $(SYSTEMDDIR)/qubes-update-tt-checkonly.service
	-rm -v $(SYSTEMDDIR)/qubes-update-tt-checkonly.timer
	-rm -v $(SYSTEMDDIR)/qubes-update-tt-download.service
	-rm -v $(SYSTEMDDIR)/qubes-update-tt-download.timer
