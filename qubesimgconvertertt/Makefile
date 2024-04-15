.SILENT:

BINDIR ?= ~/bin
LIBDIR ?= `python3 -m site --user-site`

.PHONY: info install remove

info:
	$(info Run 'make install' to install 'qubesimgconvertertt' library to your local Python)
	$(info lib dir and 'qvm-get-image-tt' utility to $(BINDIR). 'qvm-get-image-tt' utility)
	$(info could be used exactly like 'qvm-get-image' and 'qvm-get-tinted-image' utilities,)
	$(info but it provides many filter effects in addition to the default tint.)
	$(info Please read README.md file for more information)
	$(info Run 'make remove' to remove the library and the utility from yoru system)

install:
	install -v -d $(LIBDIR)
	install -v -C -D __init__.py -t $(LIBDIR)/qubesimgconverter
	install -v -C -D -m 755 qvm-get-image-tt $(BINDIR)

remove:
	rm -v $(BINDIR)/qvm-get-image-tt
	rm -v $(LIBDIR)/qubesimgconverter/__init__.py
	-rmdir -v $(LIBDIR)/qubesimgconverter

