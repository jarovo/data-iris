


LINUX_DIR_PATH = /lib/modules/$(shell uname -r)/build
INSTALL = install
PWD = $(shell pwd)
WORK = overlays
DTS_DEST_DIR = /opt/unipi/os-configurator/overlays
UDEV_DEST_DIR = /opt/unipi/os-configurator/udev
LIB_DEST_DIR = /opt/unipi/os-configurator
DESCRIPTION = description.yaml

#DTC_FLAGS_unipi-iris-unispi-slot12 := -@
templates =  $(wildcard *.template)

#all: $(dtsi) $(templates) $(WORK)/imx8mm-pinfunc.h

all: $(WORK)/imx8mm-pinfunc.h libunipidata.so
	MAKEFLAGS="$(MAKEFLAGS)" $(MAKE) -C $(LINUX_DIR_PATH) M=$(PWD)/$(WORK)

$(WORK)/imx8mm-pinfunc.h:
	@mkdir -p $(WORK)
	@ln -s $(LINUX_DIR_PATH)/arch/arm64/boot/dts/freescale/imx8mm-pinfunc.h $@

$(WORK)/Makefile: $(templates) $(DESCRIPTION)
	@python3 render-slot.py $(DESCRIPTION) -t template -o $(WORK)

unipi-values.c: template/unipi-values.template.c $(DESCRIPTION)
	@python3 render-slot.py $(DESCRIPTION) -t template -o $(WORK)

unipi-values.o: unipi-values.c
	gcc $^ -c -I unipi-hardware-id/include/ -fPIC

libunipidata.so: unipi-values.o
	gcc $^ -shared -o $@

install: install-dtb install-udev
	$(INSTALL) -m 644 unipi_values.py $(DESTDIR)/$(LIB_DEST_DIR)
	@#$(INSTALL) -m 644 libunipidata.so $(DESTDIR)/$(LIB_DEST_DIR)

install-dtb: $(wildcard $(WORK)/*.dtb)
	mkdir -p $(DESTDIR)/$(DTS_DEST_DIR)
	$(INSTALL) -m 644 $^ $(DESTDIR)/$(DTS_DEST_DIR)

install-udev: $(wildcard udev/*.rules)
	mkdir -p $(DESTDIR)/$(UDEV_DEST_DIR)
	$(INSTALL) -m 644 $^ $(DESTDIR)/$(UDEV_DEST_DIR)

clean:
	@touch $(WORK)/Makefile && MAKEFLAGS="$(MAKEFLAGS)" $(MAKE) -C $(LINUX_DIR_PATH) M=$(PWD)/$(WORK) clean
	@rm -f $(WORK)/*.dts
	@rm -f $(WORK)/Makefile
	@rm -f $(WORK)/imx8mm-pinfunc.h
	@rm -f libunipidata.so unipi-values.c unipi-values.o unipi-values.py
	@rm -f udev/* unipi-values.py
