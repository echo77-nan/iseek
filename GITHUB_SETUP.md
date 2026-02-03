# GitHub 推送配置说明

## 当前状态

✅ Git 仓库已初始化
✅ 代码已提交到本地仓库
✅ 远程仓库已配置: https://github.com/echo77-nan/demo.git

## 推送代码到 GitHub

### 方式一：使用 Personal Access Token (推荐)

1. **创建 Personal Access Token**:
   - 访问 https://github.com/settings/tokens
   - 点击 "Generate new token" -> "Generate new token (classic)"
   - 设置名称（如 "iseek-push"）
   - 选择权限：至少勾选 `repo` 权限
   - 点击 "Generate token"
   - **重要**: 复制生成的 token（只显示一次）

2. **推送代码**:
   ```bash
   cd /Users/echo.ln/iseek
   git push -u origin main
   ```
   
   当提示输入用户名时，输入你的 GitHub 用户名
   当提示输入密码时，**粘贴刚才复制的 Personal Access Token**（不是你的 GitHub 密码）

### 方式二：配置 SSH Key

1. **生成 SSH Key** (如果还没有):
   ```bash
   ssh-keygen -t ed25519 -C "echo.ln@oceanbase.com"
   # 按回车使用默认路径，可以设置密码或直接回车
   ```

2. **添加 SSH Key 到 GitHub**:
   ```bash
   # 复制公钥内容
   cat ~/.ssh/id_ed25519.pub
   ```
   - 访问 https://github.com/settings/keys
   - 点击 "New SSH key"
   - 粘贴公钥内容
   - 点击 "Add SSH key"

3. **修改远程仓库为 SSH**:
   ```bash
   cd /Users/echo.ln/iseek
   git remote set-url origin git@github.com:echo77-nan/demo.git
   ```

4. **推送代码**:
   ```bash
   git push -u origin main
   ```

### 方式三：使用 GitHub CLI

如果安装了 GitHub CLI:
```bash
gh auth login
git push -u origin main
```

## 验证推送

推送成功后，访问 https://github.com/echo77-nan/demo 查看你的代码。

## 后续更新

配置完成后，后续更新代码只需：
```bash
git add .
git commit -m "你的提交信息"
git push
```

