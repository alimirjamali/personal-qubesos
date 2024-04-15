.SILENT:

BINDIR ?= ~/bin
LIBDIR ?= `python3 -m site --user-site`

.PHONY: info install remove

info:
	$(info Run 'make install' to install 'qubesappmenustt' library to your local Python)
	$(info lib dir and 'qvm-appmenus-tt' utility to $(BINDIR). This utility could be used as a)
	$(info drop-in replacement of 'qvm-appmenus' or could be used individually.)
	$(info Please refer to README.md file for more information.)
	$(info Run 'make remove' to remove the library and the utility from yoru system)

install:
	install -v -d $(LIBDIR)
	install -v -C -D __init__.py -t $(LIBDIR)/qubesappmenustt
	install -v -C -D -m 755 qvm-appmenus-tt $(BINDIR)

remove:
	-rm -v $(BINDIR)/qvm-appmenus-tt
	-rm -v $(LIBDIR)/qubesappmenustt/__init__.py
	-rmdir -v $(LIBDIR)/qubesappmenustt

