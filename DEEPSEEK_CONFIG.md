# DeepSeek LLM 配置指南

本指南将帮助您配置 DeepSeek 真实 LLM 进行实验。

## 获取 DeepSeek API Key

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 注册/登录您的账号
3. 进入 API 管理页面
4. 创建新的 API Key
5. 复制您的 API Key（请妥善保管，不要分享给他人）

## 配置步骤

### 1. 编辑 .env 文件

在 `backend` 目录下创建或编辑 `.env` 文件：

```env
# 切换到 DeepSeek
LLM_PROVIDER=deepseek

# 填入您的 API Key
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# 可选配置
DEEPSEEK_MODEL=deepseek-chat          # 默认模型
DEEPSEEK_TEMPERATURE=0.3              # 温度参数
DEEPSEEK_MAX_TOKENS=500               # 最大输出 token
DEEPSEEK_TIMEOUT=30                   # 请求超时时间（秒）
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1  # API 基础 URL
```

### 2. 重启后端服务

配置完成后，重启后端服务：

```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 3. 验证配置

访问健康检查端点验证配置：

```bash
curl http://localhost:8000/api/health
```

响应中 `llm_provider` 应该显示为 `deepseek`。

## 使用方法

配置完成后，前端聊天将自动使用 DeepSeek 进行真实对话。

### 测试不同条件

您可以通过修改前端代码测试不同实验条件：

```typescript
// 在 App.tsx 中修改 createSession 调用
await apiClient.createSession({
  study_id: 'study4_pilot',
  test_mode: true,
  condition: 'C1',  // 尝试 C0, C1, C2, C3, C4
});
```

## 常见问题

### API Key 无效

**错误信息**: "Invalid API key"

**解决方案**:
- 检查 API Key 是否正确复制（包含所有字符）
- 确认没有多余的空格
- 验证 API Key 是否已激活

### 请求超时

**错误信息**: "Request timeout"

**解决方案**:
- 检查网络连接
- 增加 `DEEPSEEK_TIMEOUT` 配置值
- DeepSeek 服务器可能暂时不可用，请稍后重试

### 速率限制

**错误信息**: "Rate limit exceeded"

**解决方案**:
- 等待一段时间后重试
- 检查您的 API Key 配额
- 考虑升级您的 DeepSeek 套餐

### 模型调用失败

**错误信息**: "DeepSeek server error"

**解决方案**:
- 检查 DeepSeek 服务状态
- 确认 API Key 有权限访问指定的模型
- 查看后端日志获取详细错误信息

## 费用说明

使用 DeepSeek API 可能会产生费用，请注意：

- 查看 [DeepSeek 定价页面](https://www.deepseek.com/pricing) 了解费用详情
- 建议在测试阶段使用 Mock 模式，正式实验时再切换到真实 LLM
- 设置合理的 `DEEPSEEK_MAX_TOKENS` 以控制成本

## 安全建议

1. **不要提交 API Key 到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 使用 `.env.example` 作为模板

2. **限制 API Key 权限**
   - 如果可能，创建仅用于此项目的 API Key
   - 设置费用上限以防止意外支出

3. **监控使用情况**
   - 定期检查 DeepSeek 控制台中的使用统计
   - 设置警报以监控异常活动

## 切换回 Mock 模式

如果您需要切换回 Mock 模式进行测试：

```env
LLM_PROVIDER=mock
```

重启后端服务即可，无需其他更改。

## 技术支持

如遇到其他问题：

1. 检查后端日志获取详细错误信息
2. 查看 DeepSeek API 文档
3. 确认网络连接正常
4. 验证 API Key 有效性

---

**提醒**: 真实 LLM 模式下，AI 回复会根据实验条件（C0-C4）产生不同的风格变化。请确保您的实验设计已经过伦理审查批准。
