openwrt.config is the reviewed full .config used for the 2026-11-22 09:45 CST Vantage build.
A compact diffconfig was not kept: scripts/diffconfig.sh emitted recursive Kconfig dependency warnings from upstream/Kwrt feeds, and the temporary output was not persisted.
This file is included as-is so the build can be reproduced without repairing feed Kconfig cycles.
