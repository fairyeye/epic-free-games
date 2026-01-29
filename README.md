# Epic Games 每周免费游戏通知

一个自动获取 Epic Games 每周免费游戏并通过飞书通知你的 GitHub Actions 应用。

## 功能

- 🎮 每周四自动检查 Epic Games 免费游戏
- 📅 显示当前免费和即将免费的游戏
- 📱 通过飞书发送通知（需要配置）
- ⏰ 自动定时运行，也可手动触发

## 快速开始

### 1. Fork 此仓库

点击右上角的 "Fork" 按钮，将仓库复制到你的 GitHub 账号。

### 2. 启用 GitHub Actions

- 进入你的 Fork 仓库
- 点击 "Actions" 标签页
- 点击 "I understand my workflows, go ahead and enable them" 按钮启用 Actions

### 3. 测试运行

手动触发一次来测试：

- 进入 "Actions" 标签页
- 选择 "Epic Games Weekly Free Games Notification" 工作流
- 点击 "Run workflow" 按钮

## 自动通知配置

要自动收到飞书通知，你需要配置飞书集成。以下有两种方式：

### 方式一：使用 Clawdbot 发送（推荐）

如果你使用 Clawdbot，可以创建一个 cron 任务每周从 GitHub Actions 获取结果：

```bash
# 创建一个 cron 任务
clawdbot cron add \
  --name "Epic免费游戏通知" \
  --schedule "0 9 * * 4" \
  --target "main" \
  --text "检查本周Epic免费游戏"
```

然后在 GitHub Actions 中添加一个步骤，将结果保存到文件，Clawdbot 会自动读取。

### 方式二：配置飞书 Webhook

1. 创建飞书机器人
   - 在飞书中创建自定义机器人
   - 获取 Webhook URL

2. 添加 GitHub Secret
   - 进入仓库 Settings > Secrets and variables > Actions
   - 点击 "New repository secret"
   - 添加 `FEISHU_WEBHOOK_URL`

3. 修改 `.github/workflows/epic-weekly.yml`，在 "Send to Feishu" 步骤中添加：

```yaml
- name: Send to Feishu
  if: steps.fetch.outputs.has_games == 'true'
  env:
    FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
  run: |
    MESSAGE=$(cat message.txt)
    curl -X POST "$FEISHU_WEBHOOK_URL" \
      -H "Content-Type: application/json" \
      -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"$MESSAGE\"}}"
```

## 工作原理

### 脚本说明

1. **epic_games.py**
   - 从 Epic Games API 获取免费游戏数据
   - 解析当前免费和即将免费的游戏
   - 输出 JSON 格式数据

2. **send_feishu.py**
   - 接收游戏数据
   - 格式化为易读的文本消息
   - 输出到标准输出

### 定时任务

工作流默认在每周四 UTC 00:00 运行（北京时间 08:00），这是 Epic Games 更新免费游戏的时间。

## 本地测试

在本地测试脚本：

```bash
# 获取免费游戏数据
python3 epic_games.py

# 测试格式化消息
python3 epic_games.py | python3 send_feishu.py
```

## 示例输出

```
🎮 Epic Games 本周免费游戏

Rustler - Grand Theft Horse
原价: $24.99
限时: 2026-01-22 16:00 UTC - 2026-01-29 16:00 UTC
简介: Become a medieval thug in a crazy open-world action game...

📅 即将免费

Eternal Threads
原价: $19.99
免费时间: 2026-02-09 16:00 UTC - 2026-02-23 16:00 UTC

更新时间: 2026-01-29T02:19:59.819Z
链接: https://store.epicgames.com/zh-CN/free-games
```

## 自定义

### 修改运行时间

编辑 `.github/workflows/epic-weekly.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 0 * * 4'  # 每周四UTC 00:00
```

Cron 格式：`分 时 日 月 周`

### 修改时区

GitHub Actions 默认使用 UTC 时间。如需其他时区，添加时区转换步骤。

## 许可

MIT License
