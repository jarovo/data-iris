

dtss += unipi-spi-slot11.dts
dtss += unipi-spi-slot12.dts
dtss += unipi-spi-slot21.dts
dtss += unipi-spi-slot22.dts
dtss += unipi-spi-slot32.dts
dtss += unipi-spi-slot42.dts
dtss += unipi-spi-slot52.dts


dtss += unipi-iris-unispi-slot21.dts
dtss += unipi-iris-unispi-slot12.dts

dtss += unipi-ic-0067-slot11.dts
dtss += unipi-ic-0067-slot12.dts
dtss += unipi-ic-0067-slot22.dts
dtss += unipi-ic-006c-slot11.dts
dtss += unipi-ic-006c-slot22.dts
dtss += unipi-ic-006a-slot22.dts

dtbs = $(dtss:.dts=.dtb)


LINUX_DIR_PATH = /lib/modules/$(shell uname -r)/build
INSTALL = install
PWD = $(shell pwd)

DTC_FLAGS_unipi-mfd := -@
DTC_FLAGS_unipi-ic-0067-slot11 := -@
DTC_FLAGS_unipi-ic-0067-slot22 := -@
DTC_FLAGS_unipi-ic-0067-slot12 := -@
DTC_FLAGS_unipi-ic-006c-slot11 := -@
DTC_FLAGS_unipi-ic-006c-slot22 := -@
DTC_FLAGS_unipi-ic-006a-slot22 := -@

DTC_FLAGS_unipi-iris-unispi-slot21 := -@
DTC_FLAGS_unipi-iris-unispi-slot12 := -@


dtb-y   += $(dtbs)
targets  += $(dtb-y)
always-y += $(dtb-y)


all: $(dtss) imx8mm-pinfunc.h
	MAKEFLAGS="$(MAKEFLAGS)" $(MAKE) -C $(LINUX_DIR_PATH) M=$(PWD)

install: $(dtbs)
	@mkdir -p $(INSTALL_DIR)/boot
	$(INSTALL) -m 644 $^ $(INSTALL_DIR)/boot

imx8mm-pinfunc.h:
	ln -s $(LINUX_DIR_PATH)/arch/arm64/boot/dts/freescale/imx8mm-pinfunc.h $@

clean:
	MAKEFLAGS="$(MAKEFLAGS)" $(MAKE) -C $(LINUX_DIR_PATH) M=$(PWD) clean
	rm -f imx8mm-pinfunc.h

