# 推送代码到 echo77-nan/iseek 仓库指南

## 📋 当前状态

- **目标仓库**：https://github.com/echo77-nan/iseek
- **远程名称**：`origin`（已配置）
- **当前分支**：`main`

---

## 🚀 快速推送步骤

### 步骤1：检查当前状态

```bash
cd /Users/echo.ln/iseek

# 查看当前状态
git status

# 查看远程仓库配置
git remote -v
```

### 步骤2：添加所有更改

```bash
# 添加所有修改和新文件
git add .

# 或者选择性添加
# git add backend/
# git add frontend/
# git add *.md
```

### 步骤3：提交更改

```bash
# 提交更改（根据您的实际修改内容调整提交信息）
git commit -m "feat: Add directory tree selection feature and UI improvements

- Add backend API for directory tree scanning
- Add frontend directory tree selector component
- Update FileListPage with path selection UI
- Add Home button navigation to all sub-pages
- Remove description text from feature cards
- Align button heights in feature cards"
```

### 步骤4：推送到远程仓库

```bash
# 推送到origin/main（即echo77-nan/iseek）
git push origin main

# 或者使用-u参数设置上游分支（首次推送时）
git push -u origin main
```

---

## 📝 完整操作流程

### 一键执行（推荐）

```bash
cd /Users/echo.ln/iseek

# 1. 检查状态
git status

# 2. 添加所有更改
git add .

# 3. 提交
git commit -m "feat: Update iseek with directory tree and UI improvements"

# 4. 推送
git push origin main
```

---

## ⚠️ 如果遇到问题

### 问题1：远程有新的提交

**错误信息**：
```
! [rejected]        main -> main (fetch first)
```

**解决方案**：

```bash
# 方法1：先拉取再推送（推荐）
git pull origin main
# 解决冲突（如果有）
git push origin main

# 方法2：查看差异后决定
git fetch origin
git log HEAD..origin/main --oneline  # 查看远程有什么新提交
git pull origin main --rebase        # 使用rebase保持历史整洁
git push origin main
```

### 问题2：需要强制推送（谨慎使用）

**仅在确定要覆盖远程更改时使用**：

```bash
# ⚠️ 警告：这会覆盖远程的所有更改
git push origin main --force

# 更安全的方式
git push origin main --force-with-lease
```

### 问题3：认证失败

**如果提示需要认证**：

```bash
# 使用Personal Access Token
git remote set-url origin https://YOUR_TOKEN@github.com/echo77-nan/iseek.git

# 或使用SSH方式
git remote set-url origin git@github.com:echo77-nan/iseek.git
```

---

## 🔍 推送前检查清单

- [ ] 确认所有更改都已保存
- [ ] 检查是否有敏感信息（API Key、密码等）
- [ ] 确认 `.gitignore` 正确配置
- [ ] 检查代码是否有语法错误
- [ ] 编写清晰的提交信息
- [ ] 确认远程仓库地址正确

---

## 📋 提交信息规范建议

### 格式

```
<type>: <subject>

<body>

<footer>
```

### 类型（type）

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例

```bash
# 新功能
git commit -m "feat: Add directory tree selection feature"

# 修复bug
git commit -m "fix: Fix button alignment issue in feature cards"

# 文档更新
git commit -m "docs: Update README with new features"

# 多个更改
git commit -m "feat: Add directory tree and improve UI

- Add backend directory tree API
- Add frontend tree selector component
- Remove description text from cards
- Align button heights"
```

---

## 🎯 根据当前修改的提交建议

基于您当前的修改，建议使用：

```bash
git add .
git commit -m "feat: Add directory tree selection and UI improvements

- Add backend API for directory tree scanning (/api/directory-tree)
- Add frontend directory tree selector component with Drawer
- Update FileListPage with 'Select Path' button
- Add Home button navigation to FileListPage, SearchPage, StatisticsPage
- Remove description text from feature cards on HomePage
- Align button heights in feature cards
- Improve user experience for path selection"
git push origin main
```

---

## 🔄 日常更新流程

### 小改动

```bash
git add .
git commit -m "fix: 简短描述"
git push origin main
```

### 大功能更新

```bash
# 1. 创建功能分支（可选）
git checkout -b feature/new-feature

# 2. 开发并提交
git add .
git commit -m "feat: 功能描述"

# 3. 推送到功能分支
git push origin feature/new-feature

# 4. 合并到main（在GitHub上创建PR，或本地合并）
git checkout main
git merge feature/new-feature
git push origin main
```

---

## 📚 常用Git命令参考

```bash
# 查看状态
git status

# 查看更改内容
git diff

# 查看提交历史
git log --oneline -10

# 撤销暂存
git reset HEAD <file>

# 撤销工作区更改
git checkout -- <file>

# 查看远程分支
git branch -r

# 拉取最新更改
git pull origin main

# 推送更改
git push origin main
```

---

## ✅ 快速命令总结

```bash
# 完整推送流程（一行命令）
cd /Users/echo.ln/iseek && git add . && git commit -m "feat: Update iseek" && git push origin main
```

或者分步执行：

```bash
cd /Users/echo.ln/iseek
git add .
git commit -m "feat: Add directory tree selection and UI improvements"
git push origin main
```

---

## 🆘 需要帮助？

如果遇到问题：

1. **查看错误信息**：仔细阅读Git输出的错误信息
2. **检查网络**：确保可以访问GitHub
3. **检查权限**：确保有仓库的写入权限
4. **查看日志**：使用 `git log` 查看提交历史

---

**提示**：推送前建议先执行 `git status` 确认所有更改都已正确暂存。

