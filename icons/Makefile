.SILENT:

QLTT := $${HOME}/bin/qubes-label-tt -y --ANSI
ALLLABELS := Maroon Olive Navy Lime Cyan Magenta Apricot Mint Lavender \
	     Alpine Archlinux Debian Fedora Gentoo Manjaro LinuxMint NixOS \
	     openSUSE OpenWrt Tor Whonix \
	     Cubist Qubes2 Qubes3 CAD CAM Cubane Cubicle Dice StickyNotes \
	     Axonometric Engraved Impossible1 Impossibles ImpossibleHex \
	     Infinity Isometrics NAS Tesseract OpticalIllusions Webcolors
CUBIST := qube-cfop-0.svg qube-cfop-cross.svg \
	  qube-cfop-oll-2.svg qube-cfop-pll.svg qube-cubist.svg
QUBESTHEME := qube-square2.svg qube-square3.svg
CAD_CAM := qube-cam.svg qube-isometric.svg
REALLIFE := qube-cubane.svg qube-cubicle.svg qube-NAS.svg qube-sticky-notes.svg \
	    qube-dice-1.svg qube-dice-2.svg qube-dice-3.svg qube-dice-4.svg \
	    qube-dice-5.svg qube-dice-6.svg
CONCEPTUAL := qube-axonometric-1.svg qube-engraved-1.svg qube-impossible-cube-1.svg \
	      qube-impossible-cubes.svg qube-impossible-hexagon-2.svg \
	      qube-infinity.svg qube-isometric-shapes.svg qube-tesseract.svg \
	      qube-optical-illusion.svg qube-webcolors-1.svg

.PHONY: info all UIUX DISTROS Cubist QubesTheme CADCAM Conceptual RealLife clean

info:
	$(info Run 'make <target>' to create target category.)
	$(info Available target lables are as follow:)
	$(info <<< UIUX, Cubist, QubesTheme, CADCAM, RealLife, Conceptual >>>)
	$(info or 'make all' to create all of the available labels.)
	$(info 'make clean' removes all unused Tweak Tools labels.)

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
	$(info Qubes-OS theme labels will be created.)
	$(QLTT) create Qubes2 0xEEEEEE --icon allvm=qube-square2.svg
	$(QLTT) create Qubes3 0xAAAAAA --icon allvm=qube-square3.svg

CADCAM: $(CAD_CAM)
	$(info CAD/CAM lables will be created.)
	$(QLTT) create CAM 0xBBBBBB --icon allvm=qube-cam.svg
	$(QLTT) create CAD 0x555555 --icon allvm=qube-isometric.svg

RealLife: $(REALLIFE)
	$(info Real life lables will be created.)
	$(QLTT) create Cubane 0x000000 --icon allvm=qube-cubane.svg
	$(QLTT) create Cubicle 0x000000 --icon allvm=qube-cubicle.svg
	$(QLTT) create Dice 0x000000 \
		--icon appvm=qube-dice-4.svg \
		--icon dispvm=qube-dice-5.svg \
		--icon servicevm=qube-dice-1.svg \
		--icon standalonevm=qube-dice-6.svg \
		--icon templatevm=qube-dice-3.svg
	$(QLTT) create NAS 0x5c7184 --icon allvm=qube-NAS.svg
	$(QLTT) create StickyNotes 0xBBBBBB --icon allvm=qube-sticky-notes.svg

Conceptual: $(CONCEPTUAL)
	$(info Conecptual lables will be created.)
	$(QLTT) create Axonometric 0xFFDD55 \
		--icon appvm=qube-axonometric-1.svg \
		--icon templatevm=qube-axonometric-2.svg \
		--icon servicevm=qube-axonometric-3.svg \
		--icon standalonevm=qube-axonometric-4.svg \
		--icon dispvm=qube-axonometric-5.svg
	$(QLTT) create Engraved 0x555555 \
		--icon appvm=qube-engraved-1.svg \
		--icon templatevm=qube-engraved-2.svg \
		--icon servicevm=qube-engraved-3.svg \
		--icon standalonevm=qube-engraved-4.svg \
		--icon dispvm=qube-engraved-5.svg
	$(QLTT) create Impossible 0x555555 \
		--icon appvm=qube-impossible-cube-1.svg \
		--icon templatevm=qube-impossible-cube-2.svg \
		--icon servicevm=qube-impossible-cube-3.svg \
		--icon standalonevm=qube-impossible-cube-4.svg \
		--icon dispvm=qube-impossible-cube-5.svg
	$(QLTT) create Impossibles 0x555555 --icon allvm=qube-impossible-cubes.svg
	$(QLTT) create ImpossibleHex 0xF57900 --icon allvm=qube-impossible-hexagon-2.svg
	$(QLTT) create Infinity 0x555555 --icon allvm=qube-infinity.svg
	$(QLTT) create Isometrics 0x555555 --icon allvm=qube-isometric-shapes.svg
	$(QLTT) create Tesseract 0x555555 --icon allvm=qube-tesseract.svg
	$(QLTT) create OpticalIllusions 0x555555 --icon allvm=qube-optical-illusion.svg
	$(QLTT) create Webcolors 0xFF00FF \
		--icon appvm=qube-webcolors-1.svg \
		--icon templatevm=qube-webcolors-2.svg \
		--icon servicevm=qube-webcolors-4.svg \
		--icon standalonevm=qube-webcolors-5.svg \
		--icon dispvm=qube-webcolors-5.svg

clean: $(UI_UX) $(CUBIST) $(QUBESTHEME) $(CAD_CAM) $(REALLIFE) $(CONCEPTUAL)
	$(info All unused custom labels will be removed.)
	$(info Non-existing labels will be ignored.)
	$(foreach label,$(ALLLABELS),$(QLTT) remove $(label);)

