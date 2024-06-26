.SILENT:

MAKE := make --no-print-directory
BINDIR := ~/bin
LIBDIR := `python3 -m site --user-site`

.PHONY: install install_libs install_executables bundle fetch

info:
	$(info Run 'make install' to install all of the Tweak Tools)
	$(info Individual tools and libraries could be installed from their directory)
	$(info Run 'make remove' to remove all of the Tweak Tools)

install:
	install -v -d $(BINDIR)
	install -v -d $(LIBDIR)
	$(MAKE) -C qubesappmenustt install
	$(MAKE) -C qubesimgconvertertt install
	$(MAKE) -C qubes-label-tt install
	# $(MAKE) -C qubes-update-tt install
	$(MAKE) -C window-icon-updater-tt install

remove:
	$(MAKE) -C qubesappmenustt remove
	$(MAKE) -C qubesimgconvertertt remove
	$(MAKE) -C qubes-label-tt remove
	# $(MAKE) -C qubes-update-tt remove
	$(MAKE) -C window-icon-updater-tt remove

bundle:
	git bundle create - --all

fetch:
	$(info Fetching repository from personal domain)
	qvm-run -u user -p personal \
		"make --quiet -C /home/user/Development/personal-qubesos bundle">\
		/tmp/personal-qubesos.bundle
