# Mosaic Legal Pages 部署说明（多语言）

本文档用于把 `docs/product/legal/` 目录内容发布到公开仓库 `mosaic-legal`，供 App 设置页与应用商店使用。

## 1. 背景说明

- 业务代码仓库 `SnapMosaic` 是私有仓库。
- 用户无法访问私有仓库的 Issues/页面，因此法律页和反馈入口必须使用公开仓库 `mosaic-legal`。

## 2. 目录组织（可直接拷贝）

将本目录以下结构拷贝到 `mosaic-legal` 仓库根目录：

- `index.html`（法律文档入口，默认英文）
- `privacy.html`（英文隐私政策）
- `terms.html`（英文服务条款）
- `zh-CN/index.html`（中文入口）
- `zh-CN/privacy.html`（中文隐私政策）
- `zh-CN/terms.html`（中文服务条款）

## 3. 拷贝命令（本地执行）

```bash
# 假设你本地 legal 仓库路径为 /path/to/mosaic-legal
cp /Users/magic/Desktop/reborn/mosaic/docs/product/legal/index.html /path/to/mosaic-legal/
cp /Users/magic/Desktop/reborn/mosaic/docs/product/legal/privacy.html /path/to/mosaic-legal/
cp /Users/magic/Desktop/reborn/mosaic/docs/product/legal/terms.html /path/to/mosaic-legal/
mkdir -p /path/to/mosaic-legal/zh-CN
cp /Users/magic/Desktop/reborn/mosaic/docs/product/legal/zh-CN/index.html /path/to/mosaic-legal/zh-CN/
cp /Users/magic/Desktop/reborn/mosaic/docs/product/legal/zh-CN/privacy.html /path/to/mosaic-legal/zh-CN/
cp /Users/magic/Desktop/reborn/mosaic/docs/product/legal/zh-CN/terms.html /path/to/mosaic-legal/zh-CN/
```

推送：

```bash
cd /path/to/mosaic-legal
git add .
git commit -m "Update legal pages (EN + zh-CN)"
git push origin main
```

### 一键脚本（推荐）

项目内已提供一键同步脚本：

`docs/product/legal/sync-to-legal-repo.sh`

直接执行（默认目标即你的本地 legal 仓库路径）：

```bash
/Users/magic/Desktop/reborn/mosaic/docs/product/legal/sync-to-legal-repo.sh
```

如需传入其他目标路径：

```bash
/Users/magic/Desktop/reborn/mosaic/docs/product/legal/sync-to-legal-repo.sh /absolute/path/to/mosaic-legal
```

## 4. GitHub Pages 配置

在 `mosaic-legal` 仓库：

1. `Settings -> Pages`
2. `Source: Deploy from a branch`
3. `Branch: main / (root)`
4. 保存后等待 1-3 分钟

## 5. 发布后 URL

- 法律入口：`https://magic-xu.github.io/mosaic-legal/`
- 英文隐私政策：`https://magic-xu.github.io/mosaic-legal/privacy.html`
- 英文服务条款：`https://magic-xu.github.io/mosaic-legal/terms.html`
- 中文入口：`https://magic-xu.github.io/mosaic-legal/zh-CN/`
- 中文隐私政策：`https://magic-xu.github.io/mosaic-legal/zh-CN/privacy.html`
- 中文服务条款：`https://magic-xu.github.io/mosaic-legal/zh-CN/terms.html`

## 6. App 与商店接入建议

- 中文系统优先使用 `zh-CN` 链接，其他语言默认英文链接。
- Play Console `Privacy Policy URL` 建议填英文链接，或按主发版地区填对应语言链接。
- 设置页“问题反馈”建议跳转公开地址：  
  `https://github.com/Magic-Xu/mosaic-legal/issues`

## 7. 更新规则

1. 修改任意语言文档时，同时检查另一语言版本是否同步更新。
2. 同步更新页面中的“生效日期”。
3. 推送 `main` 后等待 Pages 自动重建。
