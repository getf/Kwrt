# CMCC RAX3000M NAND 256MB（Kwrt / Vantage）构建资料

本目录是 2026-11-25 审计后的最小构建配置、补丁与 overlay。它不包含完整的 OpenWrt / Kwrt 源码树，也不包含 factory / sysupgrade 固件二进制。

## 适用范围

仅适用于已经硬件改装为 **256MB NAND** 的 **CMCC RAX3000M NAND**（`DEVICE_cmcc_rax3000m-nand`）。eMMC 机型、官方混合 `cmcc_rax3000m` 配置，以及 XR30 / RAX3000Z 增强版不在本资料范围内。

## 分区与镜像尺寸

补丁文件：[`patches/0001-cmcc-rax3000m-nand-256m-ubi-and-image-size.patch`](patches/0001-cmcc-rax3000m-nand-256m-ubi-and-image-size.patch)。该补丁只改 RAX3000M NAND，不改 XR30 或其他机型。

- UBI 分区起始 `0x580000`，大小 `0xEE00000`（238 MiB）：`reg = <0x580000 0xEE00000>;`
- 原厂 NAND 起始同样是 `0x580000`，原大小为 `0x7200000`
- `IMAGE_SIZE := 243712k`（针对 `Device/cmcc_rax3000m-nand`）
- 官方 `nand.dtso` 与 eMMC DTS 未修改
- 刷机前必须在 U-Boot 中选择与上述分区一致的 **256MB / 238MiB** 布局
- 114MiB 布局不能直接 sysupgrade 到这一镜像。应使用 factory 包，并先确认 U-Boot 布局一致

说明：父构建是在已应用的 `openwrt/target/linux/mediatek/image/filogic.mk` 里把 `cmcc_rax3000m-nand` 的 `IMAGE_SIZE` 改成 `243712k` 的。上游 Kwrt overlay 的 `devices/mediatek_filogic/patches/01-360t7.patch` 里该机型仍是 `116736k`。本目录补丁把这一改动写回 overlay 补丁，以便在干净的 Kwrt 树上复现。

## 父构建产物

父构建完成时间：上海时间 2026-11-25 23:54:08。离线核验通过时间为 2026-11-25 23:56:54，并于 2026-11-26 00:00:39 再次确认。下列文件由父构建另行保存，**没有**放进本 Git 树。`SHA256SUMS` 只记录这两个文件名及其摘要。提交源码分支时若未能上传带固件二进制的 GitHub Release，不要把大镜像提交进 Git 历史。

| 文件 | 字节数 | SHA256 |
| --- | ---: | --- |
| `kwrt-mediatek-filogic-cmcc_rax3000m-nand-squashfs-factory.bin` | 77332480 | `a1c6a80416a565a25fc0862f53bea1055644bbe82ff09598f7cf022b771254ce` |
| `kwrt-mediatek-filogic-cmcc_rax3000m-nand-squashfs-sysupgrade.bin` | 73974033 | `f3a3c5a40a2af14cf6dd08b0363144499f9cc202a5f2d6c9ec331a7d5040ddea` |

候选标签名：`rax3000m-nand-256-20261125`。

提交前已在本机重新计算 SHA256，并与 `/root/Kwrt/openwrt/bin/targets/mediatek/filogic/sha256sums` 以及 `/root/rax3000m-256-build/images/` 中的副本一致。factory.bin 远小于 `IMAGE_SIZE` 243712k（238 MiB / 249561088 字节）。

## 默认与定制

- 本目录的 uci-defaults 没有改写 LAN 地址。`.config` 里的 preinit 地址是 `CONFIG_TARGET_PREINIT_IP="192.168.1.1"`，该项是 preinit / failsafe 地址。
- 默认 root 密码为空。本目录没有写入 root 密码或 shadow 哈希。镜像内 `root` 的 shadow 字段为空。
- 默认主题为 `luci-theme-vantage 1.1.1-r49`，并带 `luci-app-vantage 1.1.1-r40`。首次开机脚本 [`files/etc/uci-defaults/99-tkos-custom`](files/etc/uci-defaults/99-tkos-custom) 在检测到主题文件后把它设为默认。
- `luci-theme-argon 3.1.4-r44` 作为可切换主题一并编入；同一脚本把 `argon.@global[0].mode` 设为 `light`（Argon Light）。`luci-theme-bootstrap` 仍作为可选主题保留。
- 中文翻译：`.config` 启用了 `CONFIG_LUCI_LANG_zh_Hans`。此 Kwrt 的 `luci.mk` 会把 zh-cn `.lmo` 打进主题/应用主包（根文件系统中有 vantage 与 argon 的 zh-cn lmo）。本树没有单独的 `luci-i18n-vantage-theme-zh-cn` ipk。
- 资料列出的插件：`luci-app-npc`、`luci-app-wan-mac`、`luci-app-easytier`、`luci-app-zerotier`、`luci-app-ttyd`、`luci-app-passwall`、`luci-app-openclash`。完整勾选项以 [`config/openwrt.config`](config/openwrt.config) 为准，其中还包含 Kwrt 默认包和其他包。
- Web 服务器为 nginx（`luci-nginx` + `nginx-ssl`）。未包含 Lighttpd、uhttpd。
- 签名为 Mr.Snail，主机名为 `TKOS-Mr.Snail`。横幅在 [`files/etc/banner`](files/etc/banner)。
- [`scripts/strip-status-links.py`](scripts/strip-status-links.py) 去掉状态页上的作者外链展示。GPL 与上游许可证保留。OpenWrt 项目元数据（如 openwrt.org URL）保留。
- 镜像含遗留的 `frpc` 0.71.1-r11 命令行客户端（来自更早的 XR30 `.config`）。用户已同意保留。未包含 `luci-app-frpc`。
- 本轮未包含 `luci-app-quickfile` / `quickfile`（Rust 工具链过慢，已跳过）。为避免再拉 rust/host，可选的 Ruby YJIT 已关闭；ruby 本身未移除。

## 风险与未验证事项

- 尚未做实机启动、网络和实际可用容量验证。
- 本资料包没有附带 nginx 或其他服务的私钥、SSH 密钥或用户口令。对提交文件的审查没有发现用户私钥、令牌或口令。
- [`config/README.txt`](config/README.txt) 说明保留了完整 `.config`，并附带镜像输出中的 `config.buildinfo`。本目录仍缺少上游源码树、feed 检出和完整构建脚本，不能据此保证与父构建逐位一致。
- 版本与 feed 钉扎见 [`VERSIONS.txt`](VERSIONS.txt)。

## 目录内容

| 路径 | 作用 |
| --- | --- |
| `README.md` | 本说明 |
| `VERSIONS.txt` | Kwrt、OpenWrt 与 feed 的提交钉扎 |
| `SHA256SUMS` | 父构建两个固件文件的 SHA256；文件本身不在 Git 中 |
| `config/openwrt.config` | 与 2026-11-25 23:54 CST 镜像一致的完整 `.config`（2026-11-26 00:00 将 `CONFIG_PACKAGE_frpc` 恢复为 `y` 后的版本） |
| `config/config.buildinfo` | 镜像打包输出中的配置快照（2026-11-25 23:49） |
| `config/README.txt` | 配置文件说明 |
| `patches/0001-cmcc-rax3000m-nand-256m-ubi-and-image-size.patch` | UBI 238MiB 与 `IMAGE_SIZE := 243712k`（仅 RAX3000M NAND） |
| `files/etc/banner` | Mr.Snail 横幅 |
| `files/etc/uci-defaults/99-tkos-custom` | 主机名、隐藏作者外链、优先 nginx、默认 Vantage、Argon Light |
| `scripts/strip-status-links.py` | 从 `10_system.js` 去掉作者外链区块 |

## 许可与上游归属

请遵守 GNU GPL，以及 OpenWrt、Kwrt 和各软件包的上游许可证。`VERSIONS.txt` 记录的钉扎如下：

- Kwrt overlay：`3d2d8dab551f8e864f74291706ebf9ad96f1dd96`（2026-11-20 00:44:05 +0800），分支 `25.12`，VERSION/REVISION `11.21.2026`
- OpenWrt：`6ad88cfb335af314dc8d9827882e3b79581be873`（2026-11-19 10:44:18 +0100），分支 `openwrt-25.12`
- packages `70792587c1d0e22d0be73cc64b8fb1e2cd4722c9`
- luci `92d84fc384f61a03313c137f9efd565c3cb013cc`
- routing `625f9d8446807708bab4eef26cdc44692164818a`
- video `094bf58da6682f895255a35a84349a79dab4bf95`
- kiddin9 `cf0251186fe36855d1e8e1ef05532c81203b34f7`（`https://github.com/kiddin9/op-packages.git`，分支 `main`）

OpenWrt 官方 feed 来自 `openwrt-25.12`：packages、luci、routing、video。
