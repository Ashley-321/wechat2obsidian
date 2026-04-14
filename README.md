# wechat2obsidian

<p align="center">
  <strong>微信公众号文章 → Obsidian 一键导入工具</strong><br>
  免安装 · 离线运行 · 图片自动保存
</p>

---

## 这是什么？

一个**免费、开源**的小工具。你把微信文章链接丢进去，它自动把文章内容（文字+图片）下载下来，变成 Markdown 文件存到你的 Obsidian 笔记库。

**不需要注册任何账号，数据不会离开你的电脑。**

---

## 谁适合用？

| 你是 | 这个工具对你有用吗 |
|------|-------------------|
| Obsidian 用户，经常看公众号文章 | ✅ **就是为你做的** |
| 不想每次手动复制粘贴 | ✅ 一条命令搞定 |
| 担心文章被删 / 公众号封号 | ✅ 存本地就不怕了 |
| 不懂编程 / 不会用命令行 | ✅ 双击就能用（exe 版） |
| 用 Mac 或 Linux | ✅ 支持 |

---

## 快速开始（3 步上手）

### 第 1 步：下载

去 [GitHub Releases](https://github.com/Ashley-321/wechat2obsidian/releases) 下载 `wx2obsidian.exe`（约 13 MB）。

把 exe 放到一个固定位置：
- 推荐：桌面
- 或者：随便一个文件夹

### 第 2 步：首次配置（只需一次）

双击 `wx2obsidian.exe`，会弹出一个向导：

```
=== wx2obsidian 首次运行配置 ===

请输入你的 Obsidian 仓库路径，例如：
D:\我的笔记\Obsidian Vault
> [在这里输入路径，按回车]

图片保存到哪里？
1. 仓库下的 attachments/wechat/ 文件夹 (推荐)
2. 和文章放在一起
3. 自定义路径

> [选 1 回车即可]

✓ 配置已保存！现在可以使用了。
```

> **什么是 Obsidian 仓库？**
> 就是你用 Obsidian 打开的那整个文件夹。不知道的话，打开 Obsidian → 左下角齿轮图标 → "查看文件" → 复制那个文件夹的路径。

### 第 3 步：导入文章

**最简单的方法 — 双击批处理脚本：**

我们提供了 3 个小工具，双击就能用，不用打命令：

| 双击这个 | 做什么 | 怎么用 |
|---------|--------|--------|
| 📄 **双击导入单篇.bat** | 导入一篇文章 | 双击 → 粘贴链接 → 回车 |
| 📚 **双击批量导入.bat** | 一次性导很多篇 | 双击 → 选 urls.txt 文件 |
| ⚙️ **查看配置.bat** | 看当前设置 | 双击就显示 |

#### 导入单篇文章（详细步骤）

1. 双击 `双击导入单篇.bat`
2. 会弹出一个小窗口，提示你粘贴链接
3. 打开微信/浏览器，找到你想存的文章
4. 复制地址栏的链接（`https://mp.weixin.qq.com/s/xxxxx`）
5. 粘贴到窗口里，回车
6. 等几秒钟，看到"Saved: xxx.md"就说明成功了
7. 打开 Obsidian，在"公众号"文件夹里就能看到这篇文章了

#### 批量导入多篇文章（详细步骤）

1. 新建一个文本文件，命名为 `urls.txt`
2. 每行写一个文章链接（可以写注释，用 `#` 开头）：
   ```
   # 这些是我要保存的文章
   https://mp.weixin.qq.com/s/第一篇文章
   https://mp.weixin.qq.com/s/第二篇文章
   https://mp.weixin.qq.com/s/第三篇文章
   ```
3. 双击 `双击批量导入.bat`
4. 弹出文件选择框，选中你的 `urls.txt`
5. 自动逐篇处理，等它跑完就行

---

## 高级用法（命令行）

如果你熟悉命令行，也可以直接在终端里操作：

```bash
# 导入一篇文章
wx2obsidian.exe https://mp.weixin.qq.com/s/xxxxx

# 一次导入多篇
wx2obsidian.exe https://mp.weixin.qq.com/s/a https://mp.weixin.qq.com/s/b

# 从文件批量导入
wx2obsidian.exe --batch urls.txt

# 导入到指定子文件夹
wx2obsidian.exe https://mp.weixin.qq.com/s/xxxxx --folder "微信收藏"

# 查看当前配置
wx2obsidian.exe config --show

# 修改仓库路径
wx2obsidian.exe config --vault "D:\新的仓库"

# 重置配置（重新来过）
wx2obsidian.exe config --reset
```

完整命令参考：

```
wx2obsidian [URLs...] [选项]

选项:
  --batch, -b 文件路径     从文件读取 URL 列表（每行一个）
  --folder, -f 名称        保存到子文件夹
  --attach-dir, -a 路径    图片存放位置
  --overwrite, -o          覆盖已存在的文件
  --version, -v            显示版本号

子命令:
  config                   配置管理
    --vault 路径           设置仓库位置
    --attach-dir 路径      设置图片目录
    --show                 查看当前配置
    --reset                重置所有配置
```

---

## 导出效果是什么样的？

工具会在你的 Obsidian 仓库下生成这样的 Markdown 文件：

```markdown
---
title: 用好Agent最重要的技巧不是Skills，是这四个字
author: 数字生命卡兹克
date: 2026-04-14
source: https://mp.weixin.qq.com/s/xxxxx
tags:
  - wechat
---

# 用好Agent最重要的技巧不是Skills，是这四个字

正文内容在这里...

![文章配图](attachments/wechat/wechat_abc123.png)
```

- **标题** = 文章原标题
- **作者** = 公众号名称
- **日期** = 发布时间
- **原文链接** = 方便以后回去看
- **图片** = 已下载到本地，不会失效

直接在 Obsidian 里打开就能看，排版和原文基本一致。

---

## 图片怎么处理？

这是很多人关心的问题：

| 问题 | 答案 |
|------|------|
| 图片会消失吗？ | 不会，图片已下载到你电脑上 |
| 图片存哪里？ | 默认在仓库的 `attachments/wechat/` 文件夹 |
| 可以改位置吗？ | 可以，用 `config --attach-dir` 设置 |
| 微信防盗链怎么办？ | 工具自动绕过（加了正确的请求头） |
| 图片格式是什么？ | 保持原样（png/jpg/gif 等） |

---

## 常见问题

<details>
<summary><b>Q1: exe 双击后闪退怎么办？</b></summary>

第一次双击时需要配置，如果闪退了：
1. 按 `Win + R`，输入 `cmd`，回车
2. 把 exe 拖进 cmd 窗口（会自动填入路径）
3. 回车运行，这样能看到报错信息

大多数情况是因为没完成首次配置。跟着提示走一遍就好了。
</details>

<details>
<summary><b>Q2: 提示"需要登录"或 403 错误</b></summary>

某些文章需要微信登录才能查看。这种情况下工具无法抓取。
- 如果是**付费文章**或**仅关注者可见**的文章，无法导入
- 大部分公开文章都可以正常导入
</details>

<details>
<summary><b>Q3: 和其他同类工具比有什么区别？</b></summary>

| 特性 | wechat2obsidian | mp2md（在线版） | Omnivore（插件） |
|------|----------------|----------------|-----------------|
| 需要联网吗？ | 抓文章时要，之后离线可读 | 始终要联网 | 始终要联网 |
| 数据在哪？ | 你的电脑上 | 别人的服务器 | 别人的服务器 |
| 需要 Python 吗？ | 不用（exe 直接用） | 不用 | 不用 |
| 图片能保存吗？ | ✅ 能，已下载到本地 | ❌ 还是远程链接 | 视情况 |
| 批量导入？ | ✅ 支持 | ❌ 不支持 | ✅ 支持 |
| 免费？ | ✅ 完全免费 | ✅ 免费 | ✅ 免费 |
| 开源？ | ✅ MIT 协议 | 不确定 | ✅ Apache |

核心区别：**数据完全在你自己手上**，不经过任何第三方服务器。
</details>

<details>
<summary><b>Q4: 我不用 Obsidian，能用吗？</b></summary>

可以！导出的就是标准 Markdown 文件 + 本地图片。
任何支持 Markdown 的软件都能打开：
- Typora、VS Code、Notion、语石……
甚至直接用记事本看都行。
</details>

<details>
<summary><b>Q5: 配置文件在哪里？我想备份</b></summary>

```
C:\Users\你的用户名\.wechat2obsidian\config.json
```

把这个文件复制一份就行。换电脑后放到同样位置，就不用重新配置了。
</details>

<details>
<summary><b>Q6: 批量导入时部分失败了怎么办？</b></summary>

失败的链接会自动记录到 `_errors.txt` 文件。
不会中断其他文章的处理。

修好网络后，把 `_errors.txt` 里的链接重新导入一遍就行。
</details>

<details>
<summary><b>Q7: 支持 macOS / Linux 吗？</b></summary>

支持！两种方式：

**方式 A（推荐）：** pip 安装
```bash
pip install wechat2obsidian
wx2obsidian https://mp.weixin.qq.com/s/xxx
```

**方式 B：** 从源码运行
```bash
git clone https://github.com/Ashley-321/wechat2obsidian.git
cd wechat2obsidian
pip install -e .
wx2obsidian https://mp.weixin.qq.com/s/xxx
```

需要 Python 3.8+。
</details>

<details>
<summary><b>Q8: 能抓评论区吗？</b></summary>

不能。微信评论是前端动态加载的，不在网页源码里。
目前只能抓取文章正文部分。
</details>

---

## 项目结构

```
wechat2obsidian/
├── README.md                    ← 你正在看的这个文件
├── LICENSE                      ← MIT 开源协议
├── pyproject.toml               ← 项目配置
├── entry_point.py               ← 打包 exe 的入口
├── src/
│   └── wechat2obsidian/
│       ├── __init__.py          ← 版本号
│       ├── cli.py               ← 命令行界面
│       ├── config.py            ← 配置管理
│       ├── fetcher.py           ← 抓取文章 HTML
│       ├── parser.py            ← 解析 HTML → Markdown
│       ├── downloader.py        ← 下载图片到本地
│       └── writer.py            ← 写入 .md 文件
├── dist/                        ← 放 exe 的地方（发布时打包）
│   └── wx2obsidian.exe
├── 双击导入单篇.bat              ← 小白专用：导入一篇
├── 双击批量导入.bat              ← 小白专用：批量导入
└── 查看配置.bat                  ← 小白专用：查看设置
```

技术栈：Python 3.8+ / requests / beautifulsoup4 / PyInstaller

---

## 开发者指南

```bash
# 克隆
git clone https://github.com/Ashley-321/wechat2obsidian.git
cd wechat2obsidian

# 安装开发模式
pip install -e .

# 运行测试
python -m wechat2obsidian https://mp.weixin.qq.com/s/xxxxx

# 打包为 exe
pip install pyinstaller
pyinstaller --onefile --name wx2obsidian --console --clean --noconfirm entry_point.py \
  --hidden-import wechat2obsidian \
  --hidden-import wechat2obsidian.config \
  --hidden-import wechat2obsidian.fetcher \
  --hidden-import wechat2obsidian.downloader \
  --hidden-import wechat2obsidian.parser \
  --hidden-import wechat2obsidian.writer \
  --hidden-import wechat2obsidian.cli \
  --collect-all wechat2obsidian
```

打包后的 exe 在 `dist/wx2obsidian.exe`。

---

## License

[MIT](LICENSE) — 随意使用、修改、分发，保留版权声明即可。

---

## 更新日志

| 版本 | 日期 | 内容 |
|------|------|------|
| 1.0.0 | 2026-04-14 | 首次发布，支持单篇/批量导入、图片下载、YAML frontmatter、首次引导配置、跨平台 |

---

*by WorkBuddy · 2026-04-14*
