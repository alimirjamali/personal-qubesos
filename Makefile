.SILENT:
.PHONY: install install_libs install_executables test


BINDIR := ~/bin
LIBDIR = `python3 -m site --user-site`
BASHSCRIPTS = qubes-template-update qubes-label-tweak-tool
PYTHONEXECUTABLES = qvm-get-filtered-image qvm-appmenus-tweak-tool
EXECUTABLES = $(BASHSCRIPTS) $(PYTHONEXECUTABLES)
PYTHONLIBS = qubesimgconvertertweaks qubesappmenustweaks

install: install_python_libs install_executables

install_python_libs: $(PYTHONLIBS)
	install -v -d $(LIBDIR)
	for file in $^; do \
		install -v -D -t $(LIBDIR)/$${file} $${file}/__init__.py; \
	done

install_executables: $(EXECUTABLES)
	for file in $^; do \
		install -v -C -m 755 $${file} $(BINDIR); \
	done

