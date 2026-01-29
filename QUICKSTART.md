# 快速开始指南

## 第一步：创建 GitHub 仓库并推送代码

```bash
# 初始化 git 仓库
cd epic-free-games
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Epic Games weekly free games notification"

# 在 GitHub 上创建一个新仓库（命名为 epic-free-games）
# 然后添加远程仓库：
git remote add origin https://github.com/你的用户名/epic-free-games.git

# 推送代码
git branch -M main
git push -u origin main
```

## 第二步：启用 GitHub Actions

1. 访问你的仓库：`https://github.com/你的用户名/epic-free-games`
2. 点击 "Actions" 标签页
3. 点击 "I understand my workflows, go ahead and enable them"

## 第三步：配置飞书通知（可选但推荐）

### 方案 A：使用 Clawdbot（推荐）

如果你已经在使用 Clawdbot，无需额外配置！只需确保 Clawdbot 可以访问 GitHub，它会自动检测到新的工作流运行。

### 方案 B：配置飞书 Webhook

1. **创建飞书机器人**
   - 在飞书群聊中，点击设置 → 群机器人 → 添加机器人 → 自定义机器人
   - 命名机器人，选择 "安全设置" 可以添加 IP 白名单
   - 创建后，复制 Webhook URL

2. **添加 GitHub Secret**
   - 进入仓库 Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - Name: `FEISHU_WEBHOOK_URL`
   - Secret: 粘贴你的 Webhook URL
   - 点击 "Add secret"

## 第四步：测试

### 手动触发测试

1. 访问仓库的 Actions 页面
2. 点击左侧的 "Epic Games Weekly Free Games Notification"
3. 点击 "Run workflow" 按钮
4. 选择分支，点击 "Run workflow" 绿色按钮
5. 查看运行结果

### 查看输出

工作流运行后：
- 如果配置了飞书 webhook：你会立即收到通知
- 如果没有配置：可以在 Actions 运行日志中查看输出

## 自动运行说明

工作流默认在 **每周四 UTC 00:00**（北京时间 **08:00**）自动运行，这是 Epic Games 更新免费游戏的时间。

## 当前免费游戏（示例）

运行后会看到类似这样的消息：

```
🎮 Epic Games 本周免费游戏

Rustler - Grand Theft Horse
原价: $24.99
限时: 2026-01-22 16:00 UTC - 2026-01-29 16:00 UTC

📅 即将免费

Eternal Threads
原价: $19.99
免费时间: 2026-02-09 16:00 UTC - 2026-02-23 16:00 UTC
...
```

## 本地测试

如果想先在本地测试脚本：

```bash
# 获取并显示免费游戏数据
python3 epic_games.py

# 获取并格式化为消息
python3 epic_games.py | python3 send_feishu.py
```

## 常见问题

**Q: 为什么收不到通知？**
- 检查 FEISHU_WEBHOOK_URL 是否正确添加到 GitHub Secrets
- 查看工作流运行日志，确认是否成功执行

**Q: 如何修改运行时间？**
- 编辑 `.github/workflows/epic-weekly.yml`
- 修改 `schedule` 中的 cron 表达式
- 提交并推送到 GitHub

**Q: 可以改成每天检查吗？**
- 可以，修改 cron 表达式为 `0 0 * * *`（每天）
- 但通常 Epic 每周更新，每周四检查就够了

**Q: 如何取消定时任务？**
- 删除 `.github/workflows/epic-weekly.yml` 中的 `schedule` 部分
- 仍然可以手动触发

## 下一步

一切都设置好后，你就无需再手动检查 Epic 免费游戏了！每周四早上 8 点，你会自动收到通知。

祝你玩得开心！🎮
