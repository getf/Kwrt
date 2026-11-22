# CMCC XR30 256MB NAND（Kwrt / Vantage）构建资料

本目录是 2026-11-22 审计后的最小构建配置、补丁与 overlay。它不包含完整的 OpenWrt / Kwrt 源码树，也不包含 factory / sysupgrade 固件二进制。

## 适用范围

仅适用于已经硬件改装为 **256MB NAND** 的 **CMCC XR30**。eMMC 机型与 RAX3000Z 增强版不在本资料范围内。

## 分区与镜像尺寸

补丁文件：[`patches/0001-cmcc-xr30-256m-ubi-and-image-size.patch`](patches/0001-cmcc-xr30-256m-ubi-and-image-size.patch)。

- UBI 分区起始 `0x580000`，大小 `0xEE00000`（238 MiB）：`reg = <0x580000 0xEE00000>;`
- `IMAGE_SIZE := 243712k`
- 刷机前必须在 U-Boot 中选择与上述分区一致的 **256MB / 238MiB** 布局
- 114MiB 布局不能直接 sysupgrade 到这一镜像。应使用 factory 包，并先确认 U-Boot 布局一致

## 父构建产物

父构建完成时间：上海时间 2026-11-22 09:45:26。下列文件由父构建另行保存，**没有**放进本 Git 树，本次也**没有**创建 GitHub Release 或打上标签。`SHA256SUMS` 只记录这两个文件名及其摘要。

| 文件 | 字节数 | SHA256 |
| --- | ---: | --- |
| `kwrt-mediatek-filogic-cmcc_xr30-squashfs-factory.bin` | 66846720 | `ff66d1f5c757accb179a1204478cbc60c376dca3a448e16435f65f977ebac472` |
| `kwrt-mediatek-filogic-cmcc_xr30-squashfs-sysupgrade.bin` | 63744255 | `0424dc2e30417495c4439f5e7a1e9d2c51f9c8d4866ef7638bf27ab13a74a074` |

候选标签名：`xr30-256m-vantage-20261122`。

## 默认与定制

- 资料记载的默认 LAN 地址是 `10.0.0.1`。本目录的 uci-defaults 没有改写 LAN 地址。`.config` 里的 preinit 地址仍是 `CONFIG_TARGET_PREINIT_IP="192.168.1.1"`，该项是 preinit / failsafe 地址。
- 默认 root 密码为空。本目录没有写入 root 密码或 shadow 哈希。
- 主题为 `luci-theme-vantage 1.1.1-r49`。首次开机脚本 [`files/etc/uci-defaults/99-tkos-custom`](files/etc/uci-defaults/99-tkos-custom) 在检测到主题文件后把它设为默认。
- 未包含 Vantage 中文语言包。`.config` 启用了 LuCI 的 `CONFIG_LUCI_LANG_zh_Hans`，这不等于 Vantage 主题翻译。此前截图里的说明文字裁切，尚未验证是否已经修复。
- 资料列出的六个插件：`luci-app-npc`、`luci-app-wan-mac`、`luci-app-easytier`、`luci-app-zerotier`、`luci-app-frpc`、`luci-app-passwall`。完整勾选项以 [`config/openwrt.config`](config/openwrt.config) 为准，其中还包含 Kwrt 默认包和其他包。
- Web 服务器为 Lighttpd（`luci-lighttpd`）。
- 签名为 Mr.Snail，主机名为 `TKOS-Mr.Snail`。横幅在 [`files/etc/banner`](files/etc/banner)。
- [`scripts/strip-status-links.py`](scripts/strip-status-links.py) 去掉状态页上的作者外链展示。GPL 与上游许可证保留。

## 风险与未验证事项

- 尚未做实机启动、网络和实际可用容量验证。
- Lighttpd 的 `server.pem` 来自上游 kiddin9 `luci-lighttpd` 包自带的公用蛇油证书。该证书材料里含有与证书配对的私钥，属于上游公开默认证书，不是用户私密凭据。证书过期时间为 2026-10-05 19:03:18 UTC，即亚洲/上海时间 2026-10-06 03:03:18。本资料包没有单独附带该私钥文件。对这九个文件的审查没有发现用户私钥、令牌或口令。
- [`config/README.txt`](config/README.txt) 说明当时没有留下可用的 diffconfig，因此原样保留了完整 `.config`。本目录仍缺少上游源码树、feed 检出和完整构建脚本，不能据此保证与父构建逐位一致。
- 版本与 feed 钉扎见 [`VERSIONS.txt`](VERSIONS.txt)。

## 目录内容

| 路径 | 作用 |
| --- | --- |
| `README.md` | 本说明 |
| `VERSIONS.txt` | Kwrt、OpenWrt 与 feed 的提交钉扎 |
| `SHA256SUMS` | 父构建两个固件文件的 SHA256；文件本身不在 Git 中 |
| `config/openwrt.config` | 2026-11-22 09:45 CST Vantage 构建使用的完整 `.config` |
| `config/README.txt` | 为何保留完整 `.config` |
| `patches/0001-cmcc-xr30-256m-ubi-and-image-size.patch` | UBI 238MiB 与 `IMAGE_SIZE := 243712k` |
| `files/etc/banner` | Mr.Snail 横幅 |
| `files/etc/uci-defaults/99-tkos-custom` | 主机名、隐藏作者外链、优先 Lighttpd、默认 Vantage 主题 |
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
