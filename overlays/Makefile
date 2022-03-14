


LINUX_DIR_PATH = /lib/modules/$(shell uname -r)/build
INSTALL = install
PWD = $(shell pwd)
WORK = dts
DEST_DIR = /opt/unipi/os-configurator/data/overlays


#DTC_FLAGS_unipi-iris-unispi-slot12 := -@
templates =  $(wildcard *.template)
dtsi = $(wildcard *.dtsi)

all: $(dtsi) $(templates) $(WORK)/imx8mm-pinfunc.h
	@python3 expand_template2.py
	@cp *.dtsi $(WORK)
	MAKEFLAGS="$(MAKEFLAGS)" $(MAKE) -C $(LINUX_DIR_PATH) M=$(PWD)/$(WORK)

install: $(wildcard $(WORK)/*.dtb)
	@mkdir -p $(INSTALL_DIR)/${DEST_DIR}
	$(INSTALL) -m 644 $^ $(INSTALL_DIR)/${DEST_DIR}

$(WORK)/imx8mm-pinfunc.h:
	@mkdir -p $(WORK)
	@ln -s $(LINUX_DIR_PATH)/arch/arm64/boot/dts/freescale/imx8mm-pinfunc.h $@

clean:
	MAKEFLAGS="$(MAKEFLAGS)" $(MAKE) -C $(LINUX_DIR_PATH) M=$(PWD)/$(WORK) clean
	rm -rf $(WORK)
