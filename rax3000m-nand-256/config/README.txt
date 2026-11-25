openwrt.config is the reviewed full .config that matches the 2026-11-25 23:54:08 CST RAX3000M NAND 256MB image.
CONFIG_PACKAGE_frpc was briefly unset after that image was produced, then restored to y at 2026-11-26 00:00 CST so this file matches the delivered image. The user accepted keeping the leftover frpc client.
config.buildinfo is the compact snapshot written into the image output directory at 2026-11-25 23:49 CST; it also has CONFIG_PACKAGE_frpc=y and luci-nginx.
This directory does not include the full OpenWrt or Kwrt checkout, so bit-for-bit reproduction of the parent build is not guaranteed from these files alone.
