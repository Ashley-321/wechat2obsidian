# wechat2obsidian

> Export WeChat articles to Obsidian-compatible Markdown with images.
>
> 将微信公众号文章导出为 Obsidian 兼容的 Markdown 文件（含图片下载）。

[English](#english) | [中文文档](#中文文档)

---

## 中文文档

### 这是什么？

一个命令行工具，输入微信公众号文章链接，自动将文章正文和图片保存为 Markdown 文件到你的 Obsidian 仓库。

**核心特点：**
- **Obsidian 原生集成** — 自动生成 YAML frontmatter（标题/作者/日期/标签/原文链接）
- **图片自动下载** — 绕过微信防盗链，图片保存到本地并正确引用
- **批量导入** — 一个文本文件丢进去，逐篇处理，失败不中断
- **首次引导配置** — 第一次运行自动引导设置，之后一键使用
- **离线运行** — 无需注册、无服务器、数据不离开本机
- **跨平台** — Windows / macOS / Linux
- **仅 2 个依赖** — requests + beautifulsoup4
- **无需 Python** — 提供打包好的 exe，下载即用

---

### 两种使用方式

| 方式 | 适合谁 | 需要 Python 吗 |
|------|--------|---------------|
| **下载 exe**（推荐新手） | 不想折腾环境的普通用户 | 不需要 |
| **pip install** | 开发者 / 命令行用户 | 需要 Python 3.8+ |

---

## 方式一：下载 exe（推荐新手）

### 第 1 步：下载 exe

从 [GitHub Releases](https://github.com/Ashley-321/wechat2obsidian/releases) 下载 `wx2obsidian.exe`。

把 exe 放到任意文件夹（比如桌面、D 盘随便哪里都行），不需要安装。

### 第 2 步：首次运行 — 设置仓库路径

**方法 A：双击 exe（交互式引导）**

1. 双击 `wx2obsidian.exe`
2. 你会看到：
   ```
   ==================================================
   Welcome to wx2obsidian!
   ==================================================
   First-time setup: please provide your Obsidian vault path.
   This is the root folder of your Obsidian notebook.

   Obsidian vault path:
   ```
3. 输入你的 Obsidian 仓库路径（必须是**完整路径**），例如：
   ```
   D:\Obsidian\我的笔记
   ```
4. 如果路径不存在，会问你是否创建，输入 `y` 确认
5. 接着选择图片保存位置：
   ```
   Where do you want to save images?
     1. Same folder as the article (recommended)
     2. Separate subfolder (e.g. attachments/wechat)
     3. Keep default (attachments/wechat)
   Choice [1/2/3]:
   ```
   - 输入 `1`：图片和文章放在同一个文件夹
   - 输入 `2`：自定义图片子文件夹名（相对仓库路径）
   - 输入 `3`：默认保存到 `attachments/wechat/`
6. 看到 `Config saved!` 就配置完成了

**方法 B：命令行设置**

1. 打开命令行：按 `Win + R`，输入 `cmd`，回车
2. 进入 exe 所在目录，例如：
   ```
   cd /d D:\你的文件夹
   ```
3. 设置仓库路径：
   ```
   wx2obsidian.exe config --vault "D:\Obsidian\我的笔记"
   ```
4. 设置图片保存位置：
   ```
   wx2obsidian.exe config --attach-dir "attachments/wechat"
   ```

### 第 3 步：导出文章

**导出单篇文章：**

1. 在浏览器打开一篇微信公众号文章，复制地址栏链接
   - 链接格式：`https://mp.weixin.qq.com/s/xxxxx`
2. 打开命令行，进入 exe 所在目录
3. 输入：
   ```
   wx2obsidian.exe https://mp.weixin.qq.com/s/xxxxx
   ```
4. 看到 `Saved: xxx.md` 就成功了，去 Obsidian 里刷新查看

**导出到指定子文件夹：**

```
wx2obsidian.exe https://mp.weixin.qq.com/s/xxxxx --folder "微信收藏"
```

**批量导出（从文件读取链接）：**

1. 新建一个文本文件 `links.txt`，每行一个链接：
   ```
   https://mp.weixin.qq.com/s/abc123
   https://mp.weixin.qq.com/s/def456
   # 这行是注释，会被忽略
   https://mp.weixin.qq.com/s/ghi789
   ```
2. 运行：
   ```
   wx2obsidian.exe --batch links.txt
   ```
3. 失败的链接会记录到 `_errors.txt`，不影响其他文章处理

---

## 方式二：pip 安装（开发者）

```bash
# 安装
pip install wechat2obsidian

# 首次运行（自动进入引导，设置仓库路径和图片位置）
wx2obsidian

# 或者命令行直接设置
wx2obsidian config --vault "D:\My Vault"
wx2obsidian config --attach-dir "attachments/wechat"

# 导出文章
wx2obsidian https://mp.weixin.qq.com/s/xxxxx

# 批量导出
wx2obsidian --batch links.txt
```

---

## 配置管理（重点）

### 配置文件位置

```
C:\Users\你的用户名\.wechat2obsidian\config.json
```

配置文件是 JSON 格式，内容示例：

```json
{
  "vault_path": "D:\\Obsidian\\我的笔记",
  "attach_dir": "attachments/wechat",
  "default_folder": "",
  "tags": ["wechat"],
  "request_delay": 0.3,
  "timeout": 30
}
```

### 如何查看当前配置

```bash
wx2obsidian.exe config --show
```

输出：
```
Current configuration:
  Vault path: D:\Obsidian\我的笔记
  Attach dir: attachments/wechat
  Default folder: (none)
  Tags: wechat
  Config file: ~/.wechat2obsidian/config.json
```

### 如何更改仓库路径

**方法 1：命令行修改（推荐）**
```bash
wx2obsidian.exe config --vault "D:\新的仓库路径"
```

**方法 2：直接编辑配置文件**
1. 打开 `C:\Users\你的用户名\.wechat2obsidian\config.json`
2. 修改 `vault_path` 的值
3. 保存文件

### 如何更改图片保存位置

**方法 1：命令行修改（推荐）**
```bash
# 图片和文章放在一起
wx2obsidian.exe config --attach-dir ""

# 图片保存到自定义子文件夹
wx2obsidian.exe config --attach-dir "images/wechat"

# 图片保存到默认位置
wx2obsidian.exe config --attach-dir "attachments/wechat"
```

**方法 2：直接编辑配置文件**
1. 打开 `C:\Users\你的用户名\.wechat2obsidian\config.json`
2. 修改 `attach_dir` 的值
3. 保存文件

### 如何设置默认子文件夹

每次导出文章时，默认保存到仓库下的这个子文件夹：

```bash
wx2obsidian.exe config --folder "微信收藏"
```

设置后，导出文章会自动保存到 `D:\Obsidian\我的笔记\微信收藏\` 目录。

你也可以在导出时临时覆盖：
```bash
wx2obsidian.exe <url> --folder "临时文件夹"
```

### 如何重置所有配置

```bash
wx2obsidian.exe config --reset
```

删除配置文件，下次运行会重新进入首次引导流程。

---

### 命令行参考

```
wx2obsidian [URLs...] [OPTIONS]

参数:
  URLs                     微信公众号文章链接（一个或多个）

选项:
  --batch, -b FILE         从文件读取 URL（每行一个，# 开头为注释）
  --folder, -f NAME        保存到仓库的子文件夹（覆盖默认设置）
  --attach-dir, -a PATH    图片附件目录（相对仓库路径，覆盖默认设置）
  --overwrite, -o          覆盖已存在的文件
  --version, -v            显示版本号

子命令:
  config                   查看/修改配置
    --vault PATH           设置仓库路径
    --attach-dir PATH      设置图片附件目录
    --folder NAME          设置默认子文件夹
    --show                 显示当前配置
    --reset                重置所有配置
```

---

### 输出效果

导出的 Markdown 文件长这样：

```markdown
---
title: 文章标题
author: 公众号名称
date: 2026-03-30
source: https://mp.weixin.qq.com/s/xxxxx
tags:
  - wechat
---

# 文章标题

正文内容...

![图片](attachments/wechat/wechat_abc123.png)
```

打开 Obsidian 即可直接查看，图片正常显示。

---

### FAQ — 常见问题

#### Q1: 这个工具和 mp2md、wechat2md 有什么区别？

| 对比项 | wechat2obsidian | mp2md | wechat2md | Omnivore |
|--------|----------------|-------|-----------|----------|
| 运行方式 | 本地 CLI | 在线网页 | 在线网页 | 浏览器插件 |
| 图片下载 | 本地保存 | 支持 | 支持 | 支持 |
| Obsidian frontmatter | 自动生成 | 不支持 | 不支持 | 支持（已关停） |
| 离线使用 | 支持 | 不支持 | 不支持 | 不支持 |
| 批量处理 | 支持 | 不支持 | 不支持 | 支持 |
| 数据隐私 | 完全本地 | 经过服务器 | 经过服务器 | 经过服务器 |
| 无需安装 Python | exe 版本可以 | 不适用 | 不适用 | 不适用 |

**核心差异**：wechat2obsidian 是唯一一个**本地离线**、**Obsidian 原生集成**、**提供 exe 免安装版**、**开源免费**的方案。

#### Q2: exe 双击后闪退怎么办？

- 如果你还没配置过：双击后会进入引导设置，按提示操作即可
- 如果你已经配置过：双击后会显示帮助信息，然后提示 `Press Enter to exit...`，这是正常的，按回车退出即可
- 如果想在命令行中使用：按 `Win + R`，输入 `cmd`，回车，然后 `cd /d exe所在目录`

#### Q3: 图片存到哪里？

用户自定义。默认存到仓库下的 `attachments/wechat/` 目录。你可以通过以下方式修改：

```bash
# 命令行修改
wx2obsidian.exe config --attach-dir "images/wechat"

# 或者导出时临时指定
wx2obsidian.exe <url> --attach-dir "临时图片目录"
```

#### Q4: 为什么图片引用用标准 Markdown 语法而不是 Obsidian wiki-link？

`![](image.png)` 而不是 `![[image.png]]`，原因：

- 标准 Markdown 更通用，其他编辑器也能打开
- Obsidian 两种格式都支持，不影响使用
- 分享给非 Obsidian 用户时不会失效

#### Q5: 支持哪些 Python 版本？

Python 3.8 及以上。

#### Q6: 微信文章防盗链怎么绕过的？

请求图片时加上 `Referer: https://mp.weixin.qq.com/` 请求头。微信服务器会检查 Referer，不带的话返回 403。

#### Q7: 评论区能抓吗？

不能。微信公众号的评论区是前端 JavaScript 动态加载的，不在 HTML 源码中。

#### Q8: 批量导入时失败了怎么办？

失败的链接会记录到 `_errors.txt` 文件，不会中断其他文章的处理。修好网络后可以把失败的链接重新丢进去再跑一次。

#### Q9: 配置文件存在哪里？

`C:\Users\你的用户名\.wechat2obsidian\config.json`

---

### 开发

```bash
# 克隆仓库
git clone https://github.com/Ashley-321/wechat2obsidian.git
cd wechat2obsidian

# 安装开发模式
pip install -e .

# 直接运行
python -m wechat2obsidian https://mp.weixin.qq.com/s/xxxxx

# 打包 exe
pip install pyinstaller
pyinstaller --onefile --name wx2obsidian --console --clean --noconfirm entry_point.py \
  --hidden-import wechat2obsidian --hidden-import wechat2obsidian.config \
  --hidden-import wechat2obsidian.fetcher --hidden-import wechat2obsidian.downloader \
  --hidden-import wechat2obsidian.parser --hidden-import wechat2obsidian.writer \
  --hidden-import wechat2obsidian.cli --collect-all wechat2obsidian
```

### 项目结构

```
wechat2obsidian/
├── pyproject.toml
├── README.md
├── LICENSE
├── entry_point.py         # PyInstaller 打包入口
├── src/
│   └── wechat2obsidian/
│       ├── __init__.py      # 版本号
│       ├── cli.py           # CLI 入口 + 首次引导
│       ├── config.py        # 配置管理
│       ├── fetcher.py       # 文章抓取
│       ├── parser.py        # HTML → Markdown
│       ├── downloader.py    # 图片下载
│       └── writer.py        # Markdown 写入
└── tests/
```

### License

MIT

---

## English

### What is this?

A CLI tool that exports WeChat articles (mp.weixin.qq.com) to Obsidian-compatible Markdown files with images downloaded locally.

### Install

```bash
pip install wechat2obsidian
```

### Quick Start

```bash
# First run — interactive setup wizard
wx2obsidian

# Or set config via command line
wx2obsidian config --vault "/path/to/your/vault"
wx2obsidian config --attach-dir "attachments/wechat"

# Import a single article
wx2obsidian https://mp.weixin.qq.com/s/xxxxx

# Import to a specific folder
wx2obsidian https://mp.weixin.qq.com/s/xxxxx --folder "WeChat"

# Batch import from file
wx2obsidian --batch links.txt

# View current config
wx2obsidian config --show
```

### Features

- **Obsidian native** — YAML frontmatter with title, author, date, tags, source URL
- **Image download** — Bypasses WeChat hotlink protection, saves images locally
- **Batch mode** — Process multiple articles from a text file
- **First-run wizard** — Interactive setup on first use, zero-config after
- **Offline & private** — No servers, no accounts, data stays on your machine
- **Cross-platform** — Windows / macOS / Linux
- **Minimal dependencies** — Only requests + beautifulsoup4
- **No Python needed** — Pre-built exe available in GitHub Releases

### Configuration

Config file: `~/.wechat2obsidian/config.json`

```bash
# View config
wx2obsidian config --show

# Change vault path
wx2obsidian config --vault "/new/vault/path"

# Change image storage location
wx2obsidian config --attach-dir "images/wechat"

# Set default subfolder
wx2obsidian config --folder "WeChat"

# Reset all config
wx2obsidian config --reset
```

### License

MIT

---

> by workbot · 2026-04-08
