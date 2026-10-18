# 快速参考卡片 - AI Sycophancy Lab

> 工程师速查手册，快速定位常用命令和代码位置

---

## 🚀 常用命令

### 后端开发

```bash
# 启动后端（开发模式）
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 运行测试
pytest tests/ -v
pytest tests/test_strategies.py::test_c0_baseline -v

# 测试 DeepSeek 连接
python test_deepseek.py

# 安装依赖
pip install -r requirements.txt
```

### 前端开发

```bash
# 启动前端（开发模式）
cd frontend
npm install  # 国际环境使用默认源
npm run dev

# 构建生产版本
npm run build
```

**网络问题？** 国内环境可使用镜像源：
```bash
npm install --registry=https://registry.npmmirror.com
```

### 数据库管理

```bash
# 查看数据库
ls backend/data/sycophancy_lab.db

# 清空数据（谨慎使用）
rm backend/data/sycophancy_lab.db

# 导出数据
curl http://localhost:8000/api/research/export?format=jsonl
```

---

## 📁 关键文件位置

### 核心代码

| 功能 | 文件路径 | 说明 |
|------|----------|------|
| **策略实现** | `backend/app/strategies/implementations.py` | C0-C4 策略定义 |
| **策略基类** | `backend/app/strategies/base.py` | Strategy 接口 |
| **LLM 提供者** | `backend/app/llm/provider.py` | Mock/DeepSeek 实现 |
| **API 路由** | `backend/app/api/routes.py` | 所有 REST 端点 |
| **配置管理** | `backend/app/core/config.py` | Settings 类 |
| **主界面** | `frontend/src/App.tsx` | 聊天界面 |
| **API 客户端** | `frontend/src/api/client.ts` | 前端 API 调用 |

### 配置文件

| 文件 | 用途 |
|------|------|
| `backend/.env` | 环境变量配置 |
| `configs/strategies.yaml` | 策略开关 |
| `configs/experiment.yaml` | 实验配置 |

---

## 🎯 常见扩展场景

### 1. 添加新策略（C5）

**修改文件**: `backend/app/strategies/implementations.py`

```python
class NewStrategy(Strategy):
    strategy_id = "new_strategy"
    
    def classify(self, user_message, history, context):
        return ClassificationResult(...)
    
    def build_instructions(self, user_message, history, context, classification):
        return "..."

STRATEGY_REGISTRY["new_strategy"] = NewStrategy
CONDITION_STRATEGY_MAP["C5"] = "new_strategy"
```

### 2. 添加新 LLM

**修改文件**: `backend/app/llm/provider.py`

```python
class NewLLMProvider(LLMProvider):
    async def complete(self, messages, temperature, max_tokens):
        # 实现 API 调用
        pass
```

**更新工厂**: `backend/app/api/routes.py` → `get_llm_provider()`

### 3. 添加新 API 端点

**修改文件**: `backend/app/api/routes.py`

```python
@router.get("/research/statistics")
async def get_statistics():
    return {...}
```

### 4. 修改前端界面

**修改文件**: `frontend/src/App.tsx`

```tsx
// 添加新组件
<NewComponent />
```

---

## 🔍 调试技巧

### 后端调试

1. **查看请求日志**
   ```bash
   # 终端会显示所有请求
   python -m uvicorn app.main:app --reload
   ```

2. **添加断点**
   ```python
   import pdb; pdb.set_trace()  # 在代码中插入
   ```

3. **测试单个端点**
   ```bash
   curl http://localhost:8000/api/health
   ```

### 前端调试

1. **打开开发者工具**
   - Chrome: F12 或右键检查
   - 查看 Console、Network 标签

2. **检查 API 调用**
   - Network 标签 → 筛选 fetch/xhr
   - 查看请求和响应

3. **React DevTools**
   - 安装浏览器扩展
   - 检查组件状态

---

## 📊 数据流速查

```
用户输入
    ↓
[App.tsx] → POST /api/sessions/{id}/messages
    ↓
[routes.py] → 获取会话 → 获取策略
    ↓
[strategy.classify()] → 判断是否触发
    ↓
[strategy.build_instructions()] → 构建指令
    ↓
[get_llm_provider()] → 选择 LLM
    ↓
[provider.complete()] → 调用 LLM API
    ↓
[返回响应] → 保存到 store
    ↓
[前端显示] → 用户看到回复
```

---

## 🛠️ 故障排查

| 问题 | 解决方案 |
|------|----------|
| 后端启动失败 | 检查是否在 `backend` 目录下 |
| 前端无法连接 | 确认后端在 8000 端口运行 |
| API Key 无效 | 检查 `.env` 中的 Key 是否正确 |
| 数据库锁定 | 删除 `sycophancy_lab.db` 并重启 |
| 依赖缺失 | `pip install -r requirements.txt` |

---

## 📚 文档链接

- [完整开发文档](./DEVELOPMENT.md) - 详细架构和扩展指南
- [DeepSeek 配置](./DEEPSEEK_CONFIG.md) - LLM 集成指南
- [项目说明](./README.md) - 项目概述和使用方法
- [API 文档](http://localhost:8000/docs) - 在线 API 文档（运行后端后访问）

---

## 💡 快速提示

### 环境变量修改后

**重启后端**:
```bash
# 停止当前服务（Ctrl+C）
# 重新启动
python -m uvicorn app.main:app --reload
```

### 修改策略后

**无需重启**（开发模式）:
- `--reload` 参数会自动重载代码

### 前端修改后

**保存即生效**:
- Vite 会自动热更新

---

## 🎓 学习路径

1. **新手**: README.md → 运行项目 → 体验聊天
2. **进阶**: DEVELOPMENT.md → 理解架构 → 修改策略
3. **高级**: 阅读源码 → 扩展功能 → 集成新 LLM

---

**打印此卡片**: 建议打印或保存为 PDF，方便开发时快速查阅。
