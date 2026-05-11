---
name: auto-archive
description: 全局自动存档 - 选目录 → 描述文件 → 确认 → commit → push
trigger: 我要存档
---

# Auto-Archive Skill

当用户输入 "我要存档" 时，按以下流程交互。

## 执行流程

### Step 1: 选择目标目录

扫描 `~/projects/` 下所有子目录，列出让用户选择：

```
找到以下项目目录：
  [1] ~/projects/abcc
  [2] ~/projects/my-project
  ...
  [N] 输入其他路径
  [N+1] 新建目录
```

- **选数字**：进入对应目录，如果不是 git repo 则自动 `git init` + 切到 `claude-auto` 分支
- **选"输入其他路径"**：用户输入完整路径
- **选"新建目录"**：用户在 `~/projects/` 下新建目录，自动 git init

### Step 2: 展示变更概况 + 选择文件

进入目录后，运行 `git status --short` 展示变更：

```
当前变更：
  M  src/main.py
  M  README.md
  ?? tests/test_foo.py
  ?? docs/notes.md

你要存档哪些文件？（自然语言描述即可）
```

用户可用自然语言描述，例如：
- "全部" / "所有文件" → `--auto` 参数
- "所有 .py 和 .c 文件" → 用 Glob 定位匹配文件
- "除了 docs 目录之外的所有文件" → 排除 docs 后传文件列表
- "README.md 和 main.py" → 指定文件
- "src 目录下所有文件" → 用 Glob 定位 `src/**/*`

Claude 解读用户意图 → 用 Glob/Grep 定位文件 → 整理文件列表 → 展示二次确认。

### Step 3: 执行存档

```bash
python ~/.claude/tools/auto_archive.py --root <目录> --files <f1> <f2> ...
```

支持的参数：
| 参数 | 作用 |
|------|------|
| `--root PATH` | 目标 git 仓库路径（必填） |
| `--files f1 f2...` | 指定文件列表 |
| `--all` | 存档全部文件（git add .） |
| `--message "xxx"` | 自定义 commit message（可选） |
| `--dry-run` | 只预览不执行 |

脚本会展示预览（文件列表 + commit message + git 命令），用户确认（y / n / 输入新 commit message）后执行 `git add` → `git commit` → `git push origin claude-auto`。

## 规则

- 每一步都要展示选项让用户选，不要跳过
- 自然语言描述文件时，Claude 负责解读并定位文件
- 定位结果必须二次展示让用户确认再执行
- 推送失败时展示错误信息，提示用户检查 remote 配置
