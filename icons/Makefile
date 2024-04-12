.SILENT:
.PHONY: info all UIUX DISTROS Cubist QubesTheme CADCAM Conceptual RealLife clean

QLTT := $${HOME}/bin/qubes-label-tweak-tool -y --ANSI
ALLLABELS := Maroon Olive Navy Lime Cyan Magenta Apricot Mint Lavender \
	     Alpine Archlinux Debian Fedora Gentoo Manjaro LinuxMint NixOS \
	     openSUSE OpenWrt Tor Whonix \
	     Cubist Qubes2 Qubes3 CAD CAM Cubane Cubicle Dice StickyNotes \
	     Axonometric Engraved Impossible1 Impossibles ImpossibleHex \
	     Infinity Isometrics Tesseract OpticalIllusions Webcolors
CUBIST := qube-cfop-0.svg qube-cfop-cross.svg \
	  qube-cfop-oll-2.svg qube-cfop-pll.svg qube-cubist.svg
QUBESTHEME := qube-square2.svg qube-square3.svg
CAD_CAM := qube-cam.svg qube-isometric.svg
REALLIFE := qube-cubane.svg qube-cubicle.svg qube-dice.svg qube-sticky-notes.svg
CONCEPTUAL := qube-axonometric.svg qube-engraved.svg qube-impossible-cube1.svg \
	      qube-impossible-cubes.svg qube-impossible-hexagon.svg \
	      qube-infinity.svg qube-isometric-shapes.svg qube-tesseract.svg \
	      qube-optical-illusion.svg qube-webcolors.svg

info:
	$(info Run 'make <target>' to create target category.)
	$(info Available target lables are as follow:)
	$(info UIUX, Cubist, QubesTheme, CADCAM, RealLife, Conceptual)
	$(info or 'make all' to create all of the available labels.)
	$(info 'make clean' removes all Tweak Tools labels.)

all: UIUX DISTROS Cubist QubesTheme CADCAM RealLife Conceptual
	$(info Tweak Tools default labels are created successfully.)

# Labels suggested by Ninavizz
UIUX:
	$(info Ninavizz suggested labels will be created with Qute Sushi icons.)
	$(QLTT) create Olive     0x808000
	$(QLTT) create Navy      0x000075
	$(QLTT) create Lime      0xBFEF45
	$(QLTT) create Cyan      0x42d4f4
	$(QLTT) create Magenta   0xF032e6
	$(QLTT) create Mint      0xAAFFC3
	$(QLTT) create Lavender  0xDCBEFF

# Including Distro icons pending approval
DISTROS:
	$(info Creating Distro labels with official color with Qute Sushi icons.)
	$(QLTT) create Alpine    0x0d597f
	$(QLTT) create Archlinux 0x1793d1
	$(QLTT) create Debian    0xDD1155
	$(QLTT) create Fedora    0x3c6eb4
	$(QLTT) create Gentoo    0x54487A
	$(QLTT) create Manjaro   0x34be5b
	$(QLTT) create LinuxMint 0x86BE43
	$(QLTT) create NixOS     0x7EBAE4
	$(QLTT) create openSUSE  0x73ba25
	$(QLTT) create OpenWrt   0x00B5E2
	$(QLTT) create Tor       0x7D4698
	$(QLTT) create Whonix    0x7dcff3

Cubist: $(CUBIST)
	$(info Rubik's Qubes label will be created.)
	$(QLTT) create Cubist 0x73D216 \
		--icon appvm=qube-cubist.svg \
		--icon dispvm=qube-cfop-0.svg \
		--icon servicevm=qube-cfop-oll-2.svg \
		--icon standalonevm=qube-cfop-pll.svg \
		--icon templatevm=qube-cfop-cross.svg

QubesTheme: $(QUBESTHEME) 
	$(QLTT) create Qubes2 0xEEEEEE --icon allvm=qube-square2.svg
	$(QLTT) create Qubes3 0xAAAAAA --icon allvm=qube-square3.svg
	$(info Qubes-OS theme labels will be created.)

CADCAM: $(CAD_CAM)
	$(QLTT) create CAM 0xBBBBBB --icon allvm=qube-cam.svg
	$(QLTT) create CAD 0x555555 --icon allvm=qube-isometric.svg
	$(info CAD/CAM lables will be created.)

RealLife: $(REALLIFE)
	$(QLTT) create Cubane 0x000000 --icon allvm=qube-cubane.svg
	$(QLTT) create Cubicle 0x000000 --icon allvm=qube-cubicle.svg
	$(QLTT) create Dice 0x000000 --icon allvm=qube-dice.svg
	$(QLTT) create StickyNotes 0xBBBBBB --icon allvm=qube-sticky-notes.svg
	$(info Real life lables will be created.)

Conceptual: $(CONCEPTUAL)
	$(QLTT) create Axonometric 0xFFDD55 --icon allvm=qube-axonometric.svg
	$(QLTT) create Engraved 0x555555 --icon allvm=qube-engraved.svg
	$(QLTT) create Impossible1 0x555555 --icon allvm=qube-impossible-cube1.svg
	$(QLTT) create Impossibles 0x555555 --icon allvm=qube-impossible-cubes.svg
	$(QLTT) create ImpossibleHex 0xF57900 --icon allvm=qube-impossible-hexagon.svg
	$(QLTT) create Infinity 0x555555 --icon allvm=qube-infinity.svg
	$(QLTT) create Isometrics 0x555555 --icon allvm=qube-isometric-shapes.svg
	$(QLTT) create Tesseract 0x555555 --icon allvm=qube-tesseract.svg
	$(QLTT) create OpticalIllusions 0x555555 --icon allvm=qube-optical-illusion.svg
	$(QLTT) create Webcolors 0xFF00FF --icon allvm=qube-webcolors.svg
	$(info Conecptual lables will be created.)

clean: $(UI_UX) $(CUBIST) $(QUBESTHEME) $(CAD_CAM) $(REALLIFE) $(CONCEPTUAL)
	$(info All unused custom labels will be removed.)
	$(info Non-existing labels will be ignored.)
	$(foreach label,$(ALLLABELS),$(QLTT) remove $(label);)
