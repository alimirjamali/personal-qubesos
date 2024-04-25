.SILENT:
.PHONY: install build

BINDIR ?= ~/bin
LIBDIR ?= `python3 -m site --user-site`
PYTHON ?= python3

info:
	$(info Tweaks and improvements to the humble qubesadmin utilities.)
	$(info Original tools are a sub-part of 'qubes-core-admin-client' repository.)
	$(info Tweaked Tools will have a '-tt' suffix.)
	$(info run 'make install' in current directory to install them at your '~/bin' & '~/.local/lib' directories.)
	$(info run 'make remove' to remove them from your system.)

build:
	$(PYTHON) setup.py build

clean:
	rm -rfv qubesadmintt/*/__pycache__
	rm -rfv build
	rm -rfv *.egg-info

install:
	install -v -d $(BINDIR)
	install -v -d $(LIBDIR)
	$(PYTHON) setup.py install -O1 $(PYTHON_PREFIX_ARG) --user

remove:
	-rm -v $(BINDIR)/qvm-ls-tt
	-rm -vrf $(LIBDIR)/qubesadmintt
