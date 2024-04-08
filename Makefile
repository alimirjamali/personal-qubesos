.SILENT:
.PHONY: install install_libs install_executables bundle fetch


BINDIR := ~/bin
LIBDIR = `python3 -m site --user-site`
BASHSCRIPTS = bin/qubes-update-tweak-tool bin/qubes-label-tweak-tool
PYTHONEXECUTABLES = bin/qvm-get-filtered-image bin/qvm-appmenus-tweak-tool
EXECUTABLES = $(BASHSCRIPTS) $(PYTHONEXECUTABLES)
PYTHONLIBS = qubesimgconvertertweaks qubesappmenustweaks

install: install-python-libs install-executables

install-python-libs: $(PYTHONLIBS)
	install -v -d $(LIBDIR)
	for lib in $^; do \
		install -v -C -D -t $(LIBDIR)/$${lib} $${lib}/*; \
	done

install-executables: $(EXECUTABLES)
	for file in $^; do \
		install -v -C -m 755 $${file} $(BINDIR); \
	done

bundle:
	git bundle create - --all

fetch:
	echo Fetching repository from personal domain
	qvm-run -u user -p personal \
		"make --quiet -C /home/user/Development/personal-qubesos bundle">\
		/tmp/personal-qubesos.bundle
