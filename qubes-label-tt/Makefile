.SILENT:

BINDIR ?= ~/bin

.PHONY: install

info:
	$(info 'qubes-label-tt' is a utility to fasilitate Qubes OS label management.)
	$(info It could be used for listing, creating, deleting and other label related tasks.)
	$(info Command help is available at top of the script which should explain the details.)
	$(info run 'make install' in current directory to install it at your '~/bin' directory.)
	$(info run 'make remove' to remove it from your system.)

install: qubes-label-tt
	install -v -D -C -m 755 qubes-label-tt $(BINDIR)

fixupdategui:
	echo "label {color: #000000;}" >> /usr/lib/python3.11/site-packages/qui/styles/qubes-colors-light.css

remove:
	-rm -v $(BINDIR)/qubes-label-tt
