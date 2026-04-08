# wechat2obsidian

> Export WeChat articles to Obsidian-compatible Markdown with images.
>
> 将微信公众号文章导出为 Obsidian 兼容的 Markdown 文件（含图片下载）。

[English](#english) | [中文文档](#中文文档)

---

## 中文文档

### 这是什么？

一个 Python CLI 工具，输入微信公众号文章链接，自动将文章正文和图片保存为 Markdown 文件到你的 Obsidian vault。

**一行命令搞定：**

```bash
pip install wechat2obsidian
wx2obsidian https://mp.weixin.qq.com/s/xxxxx
```

### 核心特点

- **Obsidian 原生集成** — 自动生成 YAML frontmatter（标题/作者/日期/标签/原文链接）
- **图片自动下载** — 绕过微信防盗链，图片保存到本地并正确引用
- **批量导入** — 一个文本文件丢进去，逐篇处理，失败不中断
- **零配置** — 首次运行记住 vault 路径，之后一键使用
- **离线运行** — 无需注册、无服务器、数据不离开本机
- **跨平台** — Windows / macOS / Linux
- **仅 2 个依赖** — requests + beautifulsoup4

### 快速开始

```bash
# 安装
pip install wechat2obsidian

# 首次配置（指定你的 Obsidian vault 路径）
wx2obsidian config --vault "D:\My Vault" --attach-dir attachments/wechat

# 导入单篇文章
wx2obsidian https://mp.weixin.qq.com/s/xxxxx

# 导入到指定子文件夹
wx2obsidian https://mp.weixin.qq.com/s/xxxxx --folder "微信收藏"

# 批量导入（从文件读取链接）
wx2obsidian --batch links.txt

# 查看当前配置
wx2obsidian config --show
```

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

![图片](wechat_abc123.png)
```

### 不安装 Python 也能用？

可以。从 [GitHub Releases](https://github.com/yourname/wechat2obsidian/releases) 下载 exe 文件，双击运行即可。

---

### FAQ — 常见问题

#### Q1: 这个工具和 mp2md、wechat2md 有什么区别？

| 对比项 | wechat2obsidian | mp2md | wechat2md | Omnivore |
|--------|----------------|-------|-----------|----------|
| 运行方式 | 本地 CLI | 在线网页 | 在线网页 | 浏览器插件 |
| 图片下载 | ✅ 本地保存 | ✅ | ✅ | ✅ |
| Obsidian frontmatter | ✅ 自动生成 | ❌ | ❌ | ✅（已关停） |
| 离线使用 | ✅ | ❌ | ❌ | ❌ |
| 批量处理 | ✅ | ❌ | ❌ | ✅ |
| 数据隐私 | ✅ 完全本地 | ❌ 经过服务器 | ❌ 经过服务器 | ❌ |

**核心差异**：wechat2obsidian 是唯一一个**本地离线**、**Obsidian 原生集成**、**开源免费**的方案。Omnivore 曾是最佳选择，但已于 2024 年停止服务。

#### Q2: 为什么不用浏览器插件 / 微信小程序 / AI Agent Skill？

| 形态 | 可行性 | 说明 |
|------|--------|------|
| Python CLI 工具 | ✅ **最佳** | 跨平台通用，任何 Agent 都能调用 |
| 浏览器插件 | ⚠️ 可行但成本高 | 体验好但开发和审核成本高，后续可考虑 |
| AI Agent Skill | ⚠️ 可行但碎片化 | WorkBuddy 用 SKILL.md、Claude 用 CLAUDE.md、Cursor 用 .cursorrules……格式互不兼容，做成 Skill 只能一个平台用 |
| 微信小程序 | ❌ 不可行 | 微信生态封闭，小程序无法访问公众号文章页面 |

**结论**：Python CLI 工具是唯一真正通用的方案。底层是独立程序，任何能运行 Python 的环境都能用——无论你是直接在终端跑，还是让 Claude / WorkBuddy / 其他 Agent 调用。

#### Q3: 运行这个工具需要安装 Python 吗？

| 用户类型 | 需要 Python 吗 | 怎么用 |
|---------|---------------|--------|
| 开发者 | 需要 | `pip install wechat2obsidian` |
| 普通用户 | 不需要 | 下载 exe 双击运行（GitHub Release） |
| Agent 用户 | 看情况 | Agent 宿主环境有 Python 就能调用 |

#### Q4: 图片存到哪里？

用户自定义。默认存到 vault 下的 `attachments/wechat/` 目录，你可以通过 `--attach-dir` 参数或配置文件改成任何你喜欢的路径。

#### Q5: 为什么图片引用用标准 Markdown 语法而不是 Obsidian wiki-link？

`![](image.png)` 而不是 `![[image.png]]`，原因很简单：

- 标准 Markdown 更通用，其他编辑器也能打开
- Obsidian 两种格式都支持，不影响使用
- 如果导入的 Markdown 以后要分享给非 Obsidian 用户，wiki-link 格式会失效

#### Q6: 支持哪些 Python 版本？

Python 3.8 及以上。覆盖了绝大多数还在维护的 Python 版本。

#### Q7: 微信文章防盗链怎么绕过的？

请求图片时加上 `Referer: https://mp.weixin.qq.com/` 请求头即可。微信服务器会检查 Referer，不带的话返回 403。

#### Q8: 评论区能抓吗？

不能。微信公众号的评论区是前端 JavaScript 动态加载的，不在 HTML 源码中，技术上不可靠。

#### Q9: 批量导入时失败了怎么办？

失败的链接会记录到当前目录的 `_errors.txt` 文件，不会中断其他文章的处理。修好网络后可以重新把失败的链接丢进去再跑一次。

#### Q10: 配置文件存在哪里？

`~/.wechat2obsidian/config.json`（Windows 下是 `C:\Users\你的用户名\.wechat2obsidian\config.json`）。

### 命令行参考

```
wx2obsidian [URLs...] [OPTIONS]

选项:
  --batch, -b FILE       从文件读取 URL（每行一个，# 开头为注释）
  --folder, -f NAME      保存到 vault 的子文件夹
  --attach-dir, -a PATH  图片附件目录（相对于 vault）
  --overwrite, -o        覆盖已存在的文件
  --version, -v          显示版本号

子命令:
  config                 查看/修改配置
    --vault PATH         设置 vault 路径
    --attach-dir PATH    设置附件目录
    --folder NAME        设置默认子文件夹
    --show               显示当前配置
    --reset              重置配置
```

### 开发

```bash
# 克隆仓库
git clone https://github.com/yourname/wechat2obsidian.git
cd wechat2obsidian

# 安装开发模式
pip install -e .

# 直接运行
python -m wechat2obsidian https://mp.weixin.qq.com/s/xxxxx
```

### 项目结构

```
wechat2obsidian/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── wechat2obsidian/
│       ├── __init__.py      # 版本号
│       ├── cli.py           # CLI 入口
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

A Python CLI tool that exports WeChat articles (mp.weixin.qq.com) to Obsidian-compatible Markdown files with images downloaded locally.

### Install

```bash
pip install wechat2obsidian
```

### Quick Start

```bash
# Configure your Obsidian vault (first time only)
wx2obsidian config --vault "/path/to/your/vault"

# Import a single article
wx2obsidian https://mp.weixin.qq.com/s/xxxxx

# Import to a specific folder
wx2obsidian https://mp.weixin.qq.com/s/xxxxx --folder "WeChat"

# Batch import from file
wx2obsidian --batch links.txt
```

### Features

- **Obsidian native** — YAML frontmatter with title, author, date, tags, source URL
- **Image download** — Bypasses WeChat hotlink protection, saves images locally
- **Batch mode** — Process multiple articles from a text file
- **Zero-config after setup** — Remembers your vault path
- **Offline & private** — No servers, no accounts, data stays on your machine
- **Cross-platform** — Windows / macOS / Linux
- **Minimal dependencies** — Only requests + beautifulsoup4

### License

MIT

---

> by workbot · 2026-04-08
