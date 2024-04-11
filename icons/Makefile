.SILENT:
.PHONY: info all clean UIUX Cubist QubesTheme CADCAM Conceptual RealLife

QLTT := $${HOME}/bin/qubes-label-tweak-tool -y --ANSI
UI_UX := Maroon Olive Navy Lime Cyan Magenta Apricot Mint Lavender
CUBIST := qube-cfop-0.svg qube-cfop-cross.svg \
	  qube-cfop-oll-2.svg qube-cfop-pll.svg qube-cubist.svg
QUBESTHEME := qube-square2.svg qube-square3.svg
CAD_CAM := qube-cam.svg qube-isometric.svg
REALLIFE := qube-dice.svg qube-sticky-notes.svg
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

all: UIUX Cubist QubesTheme CADCAM RealLife Conceptual
	$(info Tweak Tools default labels are created successfully.)

# Labels suggested by Ninavizz
UIUX:
	$(QLTT) create Maroon    0x800000
	$(QLTT) create Olive     0x808000
	$(QLTT) create Navy      0x000075
	$(QLTT) create Lime      0xBFEF45
	$(QLTT) create Cyan      0x42d4f4
	$(QLTT) create Magenta   0xF032e6
	$(QLTT) create Apricot   0xFFD8B1
	$(QLTT) create Mint      0xAAFFC3
	$(QLTT) create Lavender  0xDCBEFF
	$(info Ninavizz suggested labels created with Qute Sushi icons.)

Cubist: $(CUBIST)
	$(QLTT) create Cubist 0x73D216 \
		--icon appvm=qube-cubist.svg \
		--icon dispvm=qube-cfop-0.svg \
		--icon servicevm=qube-cfop-oll-2.svg \
		--icon standalonevm=qube-cfop-pll.svg \
		--icon templatevm=qube-cfop-cross.svg
	$(info Rubik's Qubes label created.)

QubesTheme: $(QUBESTHEME) 
	$(QLTT) create Qubes2 0xEEEEEE --icon allvm=qube-square2.svg
	$(QLTT) create Qubes3 0xAAAAAA --icon allvm=qube-square3.svg
	$(info Qubes-OS theme labels created.)

CADCAM: $(CAD_CAM)
	$(QLTT) create CAM 0xBBBBBB --icon allvm=qube-cam.svg
	$(QLTT) create CAD 0x555555 --icon allvm=qube-isometric.svg
	$(info CAD/CAM lables created.)

RealLife: $(REALLIFE)
	$(QLTT) create Dice 0x000000 --icon allvm=qube-dice.svg
	$(QLTT) create StickyNotes 0xBBBBBB --icon allvm=qube-cam.svg
	$(info Real life lables created.)

Conceptual: $(CONCEPTUAL)
	$(QLTT) create Axonometric 0xFFDD55 --icon allvm=qube-axonometric.svg
	$(QLTT) create Engraved 0x555555 --icon allvm=qube-engraved.svg
	$(QLTT) create Impossible1 0x555555 --icon allvm=qube-impossible-cube1.svg
	$(QLTT) create Impossibles 0x555555 --icon allvm=qube-impossible-cubes.svg
	$(QLTT) create ImpossibleHex 0xF57900 --icon allvm=qube-impossible-hexagon.svg
	$(QLTT) create Infinity 0x555555 --icon allvm=qube-infinity.svg
	$(QLTT) create Isometrics 0x555555 --icon allvm=qube-isometric-shapes.svg
	$(QLTT) create Tesseract 0x555555 --icon allvm=qube-tesseract.svg
	$(QLTT) create OpticalIllusions 0x --icon allvm=qube-optical-illusion.svg
	$(QLTT) create Webcolors 0xFF00FF --icon allvm=qube-webcolors.svg
	$(info Conecptual lables created.)

clean: $(CUBIST) $(QUBESTHEME) $(CAD_CAM) $(REALLIFE) $(CONCEPTUAL) $(UI_UX)
	$(info Non-existing or used labels will be ignored.)
	for LABEL in $^; do \
		$(QTLL) remove $${label}; \
	done
	$(info All unused custom labels are removed.)

