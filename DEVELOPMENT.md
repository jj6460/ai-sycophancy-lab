# AI Sycophancy Lab - 工程师开发文档

> **版本**: 1.0.0 | **最后更新**: 2026-10-17 | **适用环境**: Python 3.11+, Node.js 18+

---

## 📋 目录

1. [项目概述](#项目概述)
2. [快速开始](#快速开始)
3. [项目架构](#项目架构)
4. [核心模块详解](#核心模块详解)
5. [扩展开发指南](#扩展开发指南)
6. [API 参考](#api-参考)
7. [数据库设计](#数据库设计)
8. [测试指南](#测试指南)
9. [部署与运维](#部署与运维)
10. [常见问题](#常见问题)

---

## 项目概述

### 项目定位

AI Sycophancy Lab 是一个**心理学实验平台**，用于研究 AI 系统中的"谄媚行为"（sycophancy）——即 AI 过度认同、迎合用户的行为。

### 核心功能

- ✅ **5 种实验条件** (C0-C4)：控制 AI 的不同谄媚策略
- ✅ **双 LLM 支持**：Mock 模式（离线测试）+ DeepSeek 模式（真实 LLM）
- ✅ **实时聊天界面**：React + TypeScript 前端
- ✅ **RESTful API**：FastAPI 后端
- ✅ **数据导出**：支持 JSONL 格式的实验数据
- ✅ **策略系统**：可扩展的实验条件框架

### 技术栈

**后端**:
- Python 3.11+
- FastAPI (异步 Web 框架)
- SQLAlchemy + aiosqlite (异步数据库)
- Pydantic (数据验证)
- httpx (异步 HTTP 客户端)

**前端**:
- React 18
- TypeScript
- Vite (构建工具)

**LLM 集成**:
- DeepSeek API (兼容 OpenAI 格式)
- 支持扩展到其他 LLM 提供商

---

## 快速开始

### 1. 环境准备

**系统要求**:
- Python 3.11 或更高版本
- Node.js 18 或更高版本
- npm 或 pnpm

**克隆项目**:
```bash
git clone <repository-url>
cd ai-sycophancy-lab
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# 编辑 .env 文件，设置以下关键配置：
# LLM_PROVIDER=deepseek  # 或 mock
# DEEPSEEK_API_KEY=your-api-key-here
# DEEPSEEK_MODEL=deepseek-v4-flash

# 启动后端服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**验证后端运行**:
```bash
# 访问健康检查端点
curl http://localhost:8000/api/health

# 或访问 API 文档
open http://localhost:8000/docs
```

### 3. 前端设置

```bash
# 新开一个终端，进入前端目录
cd frontend

# 安装依赖（国内建议使用镜像源）
npm install --registry=https://registry.npmmirror.com

# 启动开发服务器
npm run dev
```

**访问应用**:
- 前端界面: http://localhost:3000
- 后端 API: http://localhost:8000/api
- API 文档: http://localhost:8000/docs

### 4. 验证安装

1. 打开浏览器访问 http://localhost:3000
2. 系统会自动创建一个会话
3. 发送一条测试消息，如 "我想买一个奢侈品包"
4. 观察 AI 的回复（根据当前条件会有不同风格）

---

## 项目架构

### 目录结构

```
ai-sycophancy-lab/
├── backend/                    # 后端核心
│   ├── app/
│   │   ├── api/               # API 路由层
│   │   │   ├── __init__.py
│   │   │   └── routes.py      # REST API 端点实现
│   │   │
│   │   ├── core/              # 核心配置
│   │   │   ├── __init__.py
│   │   │   └── config.py      # 环境变量加载 (Settings 类)
│   │   │
│   │   ├── db/                # 数据库层
│   │   │   ├── __init__.py
│   │   │   └── database.py    # SQLAlchemy 异步数据库配置
│   │   │
│   │   ├── llm/               # LLM 提供者层
│   │   │   ├── __init__.py
│   │   │   └── provider.py    # Mock/DeepSeek LLM 实现
│   │   │
│   │   ├── schemas/           # 数据模型层
│   │   │   ├── __init__.py
│   │   │   └── models.py      # Pydantic 请求/响应模型
│   │   │
│   │   ├── strategies/        # 实验策略层 ⭐ 核心
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # 策略抽象基类
│   │   │   └── implementations.py  # C0-C4 策略实现
│   │   │
│   │   └── main.py            # FastAPI 应用入口
│   │
│   ├── tests/                 # 单元测试
│   │   ├── __init__.py
│   │   ├── test_api.py        # API 测试
│   │   └── test_strategies.py # 策略测试
│   │
│   ├── .env                   # 环境变量配置（不提交到 Git）
│   ├── .env.example           # 环境变量模板
│   ├── requirements.txt       # Python 依赖
│   └── Dockerfile             # Docker 镜像配置
│
├── frontend/                  # 前端界面
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts      # API 客户端封装
│   │   ├── types/
│   │   │   └── api.ts         # TypeScript 类型定义
│   │   ├── App.tsx            # 主组件（聊天界面）
│   │   ├── main.tsx           # React 入口
│   │   └── index.css          # 全局样式
│   │
│   ├── index.html             # HTML 模板
│   ├── package.json           # Node.js 依赖
│   ├── tsconfig.json          # TypeScript 配置
│   ├── vite.config.ts         # Vite 配置
│   └── Dockerfile             # Docker 镜像配置
│
├── configs/                   # 配置文件
│   ├── experiment.yaml        # 实验配置（Study ID、条件列表）
│   └── strategies.yaml        # 策略开关和版本控制
│
├── prepare/                   # 研究文档
│   ├── study.md               # 实验设计文档
│   └── study1.md              # 研究资料
│
├── data/                      # 数据存储（运行时生成）
│   └── sycophancy_lab.db      # SQLite 数据库
│
├── README.md                  # 项目说明
├── DEVELOPMENT.md             # 开发文档（本文件）
├── DEEPSEEK_CONFIG.md         # DeepSeek 配置指南
├── AI_Sycophancy_Lab_AI_Implementation_Guide.md
├── docker-compose.yml         # Docker 编排
├── setup_env.py               # 环境设置脚本
└── test_deepseek.py           # DeepSeek 测试脚本
```

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                            │
│                    http://localhost:3000                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   React 前端 (App.tsx)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  聊天界面    │  │  会话管理    │  │  消息展示    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ fetch('/api/...')
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI 后端 (main.py)                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │              API 路由层 (routes.py)                 │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │ 会话端点 │  │ 消息端点 │  │ 导出端点 │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘        │    │
│  └────────────────────────────────────────────────────┘    │
│                         │                                   │
│                         ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │              业务逻辑层                             │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │ 策略系统 │  │ LLM 管理 │  │ 会话管理 │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘        │    │
│  └────────────────────────────────────────────────────┘    │
│                         │                                   │
│                         ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │              数据持久层                             │    │
│  │  ┌──────────┐  ┌──────────┐                       │    │
│  │  │ Database │  │ In-Memory│                       │    │
│  │  │ (SQLite) │  │  (Store) │                       │    │
│  │  └──────────┘  └──────────┘                       │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ API 调用
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LLM 服务 (External)                            │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  DeepSeek API    │  │  Mock Provider   │                │
│  │  (deepseek-v4)   │  │  (离线测试)      │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心模块详解

### 1. 策略系统 (strategies/)

**位置**: `backend/app/strategies/`

**核心文件**:
- [`base.py`](vscode-file://d:/000work/zhangxiaogou/ai-sycophancy-lab/backend/app/strategies/base.py) - 策略抽象基类
- [`implementations.py`](vscode-file://d:/000work/zhangxiaogou/ai-sycophancy-lab/backend/app/strategies/implementations.py) - C0-C4 策略实现

#### 策略接口

所有策略必须实现 `Strategy` 基类：

```python
class Strategy(ABC):
    """策略抽象基类"""
    
    strategy_id: str  # 策略唯一标识
    
    @abstractmethod
    def classify(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
    ) -> ClassificationResult:
        """
        分类用户输入，判断是否触发策略
        
        参数:
            user_message: 用户最新消息
            history: 历史消息列表
            context: 策略上下文（包含 session_id, condition, turn_number 等）
        
        返回:
            ClassificationResult: 分类结果（是否触发、类别、置信度）
        """
        pass
    
    @abstractmethod
    def build_instructions(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
        classification: ClassificationResult,
    ) -> str:
        """
        构建给 LLM 的指令
        
        参数:
            user_message: 用户消息
            history: 历史消息
            context: 策略上下文
            classification: 分类结果
        
        返回:
            str: 发送给 LLM 的指令文本
        """
        pass
```

#### 现有策略实现

| 条件 | 策略类 | strategy_id | 触发条件 | 指令特点 |
|------|--------|-------------|----------|----------|
| C0 | `BaselineStrategy` | baseline | 永不触发 | 中立、平衡的建议 |
| C1 | `StanceStrategy` | stance | 检测到偏好关键词 | 验证用户偏好和品味 |
| C2 | `ResponseStructureStrategy` | response_structure | 始终触发 | 控制回复结构（三段式） |
| C3 | `GoalEngagementStrategy` | goal_engagement | 始终触发 | 保持用户参与和满意 |
| C4 | `DynamicTriggerStrategy` | dynamic_trigger | 多条件动态判断 | 上下文敏感的策略激活 |

#### 策略注册表

```python
# implementations.py 中的注册表
STRATEGY_REGISTRY = {
    "baseline": BaselineStrategy,
    "stance": StanceStrategy,
    "response_structure": ResponseStructureStrategy,
    "goal_engagement": GoalEngagementStrategy,
    "dynamic_trigger": DynamicTriggerStrategy,
}

# 条件到策略的映射
CONDITION_STRATEGY_MAP = {
    "C0": "baseline",
    "C1": "stance",
    "C2": "response_structure",
    "C3": "goal_engagement",
    "C4": "dynamic_trigger",
}
```

#### 数据流

```
用户消息: "我想买奢侈品"
    ↓
[Strategy.classify()] 
    ↓ 检测关键词 "奢侈品"
ClassificationResult(category="luxury_interest", triggered=True, confidence=0.9)
    ↓
[Strategy.build_instructions()]
    ↓ 构建指令
"用户表现出奢侈品购买兴趣，请验证其品味并推荐高端选项..."
    ↓
[发送到 LLM]
```

---

### 2. LLM 提供者 (llm/)

**位置**: `backend/app/llm/provider.py`

**支持的 LLM**:
- `MockLLMProvider` - 离线测试模式
- `DeepSeekLLMProvider` - DeepSeek 真实 LLM

#### LLM 接口

```python
class LLMProvider(ABC):
    """LLM 提供者抽象基类"""
    
    @abstractmethod
    async def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """
        生成文本补全
        
        参数:
            messages: 对话消息列表
            temperature: 温度参数（0-1）
            max_tokens: 最大输出 token 数
        
        返回:
            LLMResponse: 包含 content, model, finish_reason, latency_ms
        """
        pass
```

#### 添新的 LLM 提供者

**示例：添加 OpenAI 支持**

```python
# 1. 在 provider.py 中实现新类
import openai
from openai import AsyncOpenAI

class OpenAILLMProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str, base_url: str = None):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 500,
    ) -> LLMResponse:
        start_time = time.time()
        
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=self.model_name,
            finish_reason=response.finish_reason,
            latency_ms=latency_ms,
        )

# 2. 在 routes.py 中更新工厂函数
def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    
    if settings.llm_provider == "mock":
        return MockLLMProvider()
    elif settings.llm_provider == "deepseek":
        return DeepSeekLLMProvider(...)
    elif settings.llm_provider == "openai":
        return OpenAILLMProvider(
            api_key=settings.openai_api_key,
            model_name=settings.openai_model,
        )
    
    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
```

---

### 3. API 路由 (api/)

**位置**: `backend/app/api/routes.py`

#### 主要端点

| 方法 | 路径 | 功能 | 请求体 | 响应 |
|------|------|------|--------|------|
| GET | `/api/health` | 健康检查 | - | `HealthResponse` |
| POST | `/api/sessions` | 创建会话 | `SessionCreateRequest` | `SessionResponse` |
| GET | `/api/sessions/{session_id}` | 获取会话状态 | - | `SessionStateResponse` |
| POST | `/api/sessions/{session_id}/messages` | 发送消息 | `MessageRequest` | `MessageResponse` |
| GET | `/api/research/export` | 导出数据 | - | JSONL 文件 |

#### 会话创建流程

```python
# POST /api/sessions
async def create_session(request: SessionCreateRequest):
    # 1. 确定实验条件
    if request.test_mode and request.condition:
        condition = request.condition  # 测试模式：指定条件
    else:
        condition = random.choice(["C0", "C1", "C2", "C3", "C4"])  # 随机分配
    
    # 2. 生成会话 ID
    session_id = str(uuid.uuid4())
    
    # 3. 存储会话数据
    sessions_store[session_id] = {
        "session_id": session_id,
        "study_id": request.study_id,
        "condition": condition,
        "status": "active",
        "created_at": datetime.utcnow(),
    }
    
    # 4. 返回会话信息
    return SessionResponse(
        session_id=session_id,
        study_id=request.study_id,
        condition=condition,
    )
```

#### 消息处理流程

```python
# POST /api/sessions/{session_id}/messages
async def send_message(session_id: str, request: MessageRequest):
    # 1. 获取会话数据
    session = sessions_store[session_id]
    condition = session["condition"]
    
    # 2. 获取对应策略
    strategy = get_strategy_for_condition(condition)
    
    # 3. 分类用户消息
    context = StrategyContext(
        session_id=session_id,
        condition=condition,
        turn_number=len(messages_store[session_id]) + 1,
    )
    classification = strategy.classify(request.content, history, context)
    
    # 4. 构建 LLM 指令
    instructions = strategy.build_instructions(
        request.content, history, context, classification
    )
    
    # 5. 准备系统提示词
    system_prompt = f"You are a helpful AI assistant.\n\n{instructions}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": request.content},
    ]
    
    # 6. 调用 LLM
    provider = get_llm_provider()
    response = await provider.complete(messages, temperature=0.3)
    
    # 7. 保存消息和策略事件
    messages_store[session_id].append({
        "role": "user",
        "content": request.content,
        "timestamp": datetime.utcnow(),
    })
    messages_store[session_id].append({
        "role": "assistant",
        "content": response.content,
        "timestamp": datetime.utcnow(),
    })
    
    # 8. 返回响应
    return MessageResponse(
        content=response.content,
        condition=condition,
        strategy_triggered=classification.triggered,
    )
```

---

### 4. 配置管理 (core/)

**位置**: `backend/app/core/config.py`

#### Settings 类

```python
class Settings(BaseSettings):
    """应用配置，从 .env 文件加载"""
    
    # 应用设置
    app_name: str = "AI Sycophancy Lab"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # LLM 设置
    llm_provider: Literal["mock", "openai", "azure", "deepseek"] = "mock"
    
    # DeepSeek 设置
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-v4-flash"
    deepseek_temperature: float = 0.3
    deepseek_max_tokens: int = 500
    deepseek_timeout: int = 30
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    
    # 数据库设置
    database_url: str = "sqlite+aiosqlite:///./data/sycophancy_lab.db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

#### 环境变量优先级

1. 环境变量（如 `DEEPSEEK_API_KEY`）
2. `.env` 文件中的值
3. 代码中的默认值

#### 添加新的配置项

```python
# 1. 在 config.py 中添加字段
class Settings(BaseSettings):
    # 新功能配置
    new_feature_enabled: bool = Field(default=False)
    new_api_key: str = Field(default="")
    
# 2. 在 .env 中添加
NEW_FEATURE_ENABLED=true
NEW_API_KEY=your-key-here

# 3. 使用
settings = get_settings()
if settings.new_feature_enabled:
    # ...
```

---

### 5. 数据库 (db/)

**位置**: `backend/app/db/database.py`

#### 当前状态（MVP）

- **生产环境**: SQLite + aiosqlite（异步）
- **开发阶段**: 内存存储（`sessions_store`, `messages_store`）

#### 数据库模型

```python
# models.py
class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True)
    study_id = Column(String)
    condition = Column(String)
    status = Column(String)
    created_at = Column(DateTime)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    timestamp = Column(DateTime)
```

#### 异步数据库操作

```python
# 获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 使用示例
@router.post("/sessions")
async def create_session(db: AsyncSession = Depends(get_db)):
    new_session = Session(...)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
```

---

## 扩展开发指南

### 场景 1: 添加新的实验条件（C5）

**需求**: 添加 C5 条件，实现"过度推荐"策略

**步骤**:

#### 1. 创建策略类

编辑 `backend/app/strategies/implementations.py`:

```python
class OverRecommendationStrategy(Strategy):
    """C5: 过度推荐 - 总是推荐更多、更贵的产品"""
    
    strategy_id = "over_recommendation"
    
    def classify(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
    ) -> ClassificationResult:
        # 始终触发
        return ClassificationResult(
            category="purchase_intent",
            triggered=True,
            confidence=1.0,
        )
    
    def build_instructions(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
        classification: ClassificationResult,
    ) -> str:
        return """
        用户表达了购买意图。请执行以下策略：
        1. 推荐比用户预算更贵的产品
        2. 强调"一分钱一分货"
        3. 暗示便宜的产品质量差
        4. 使用"你值得拥有更好的"等话术
        """

# 注册策略
STRATEGY_REGISTRY["over_recommendation"] = OverRecommendationStrategy
CONDITION_STRATEGY_MAP["C5"] = "over_recommendation"
```

#### 2. 更新配置文件

编辑 `configs/strategies.yaml`:

```yaml
strategies:
  over_recommendation:
    version: "1.0.0"
    description: "过度推荐策略 - 推荐更贵的产品"
    enabled: true
```

#### 3. 添加测试

编辑 `backend/tests/test_strategies.py`:

```python
def test_c5_over_recommendation():
    """测试 C5 过度推荐策略"""
    strategy = get_strategy_for_condition("C5")
    assert strategy.strategy_id == "over_recommendation"
    
    # 测试分类
    result = strategy.classify("我想买个耳机", [], context)
    assert result.triggered == True
    
    # 测试指令
    instructions = strategy.build_instructions(...)
    assert "更贵" in instructions or "值得" in instructions
```

#### 4. 运行测试

```bash
cd backend
pytest tests/test_strategies.py::test_c5_over_recommendation -v
```

#### 5. 重启后端

```bash
python -m uvicorn app.main:app --reload
```

---

### 场景 2: 集成新的 LLM（Claude）

**需求**: 添加 Anthropic Claude 支持

**步骤**:

#### 1. 安装依赖

编辑 `backend/requirements.txt`:

```txt
anthropic>=0.18.0
```

安装:
```bash
pip install anthropic
```

#### 2. 实现 Provider

编辑 `backend/app/llm/provider.py`:

```python
import anthropic
from anthropic import AsyncAnthropic

class ClaudeLLMProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str = "claude-3-sonnet-20240229"):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model_name = model_name
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 500,
    ) -> LLMResponse:
        start_time = time.time()
        
        # 转换消息格式（Claude 需要不同的格式）
        claude_messages = []
        system_prompt = ""
        
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })
        
        response = await self.client.messages.create(
            model=self.model_name,
            messages=claude_messages,
            system=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return LLMResponse(
            content=response.content[0].text,
            model=self.model_name,
            finish_reason=response.stop_reason,
            latency_ms=latency_ms,
        )
```

#### 3. 添加配置

编辑 `backend/app/core/config.py`:

```python
class Settings(BaseSettings):
    # Claude settings
    claude_api_key: str = Field(default="")
    claude_model: str = Field(default="claude-3-sonnet-20240229")
    claude_temperature: float = Field(default=0.3)
    claude_max_tokens: int = Field(default=500)
```

#### 4. 更新工厂函数

编辑 `backend/app/api/routes.py`:

```python
def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    
    if settings.llm_provider == "claude":
        return ClaudeLLMProvider(
            api_key=settings.claude_api_key,
            model_name=settings.claude_model,
        )
    # ...
```

#### 5. 更新 `.env`

```env
LLM_PROVIDER=claude
CLAUDE_API_KEY=sk-ant-xxx
CLAUDE_MODEL=claude-3-sonnet-20240229
```

---

### 场景 3: 添加数据分析功能

**需求**: 添加端点，统计实验数据

**步骤**:

#### 1. 添加 Pydantic 模型

编辑 `backend/app/schemas/models.py`:

```python
from pydantic import BaseModel
from typing import Dict, List

class StatisticsResponse(BaseModel):
    total_sessions: int
    sessions_by_condition: Dict[str, int]
    total_messages: int
    avg_messages_per_session: float
    strategy_trigger_rate: Dict[str, float]

class ExportRequest(BaseModel):
    format: str = "jsonl"  # jsonl or csv
    include_metadata: bool = True
```

#### 2. 实现端点

编辑 `backend/app/api/routes.py`:

```python
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

@router.get("/research/statistics", response_model=StatisticsResponse)
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """获取实验统计数据"""
    
    # 查询会话总数
    total_sessions = len(sessions_store)
    
    # 按条件统计
    sessions_by_condition = {}
    for session in sessions_store.values():
        condition = session["condition"]
        sessions_by_condition[condition] = sessions_by_condition.get(condition, 0) + 1
    
    # 查询消息总数
    total_messages = sum(len(msgs) for msgs in messages_store.values())
    
    # 计算平均消息数
    avg_messages = total_messages / total_sessions if total_sessions > 0 else 0
    
    # 计算策略触发率
    trigger_rate = {}
    for session_id, events in strategy_events_store.items():
        condition = sessions_store[session_id]["condition"]
        if condition not in trigger_rate:
            trigger_rate[condition] = {"triggered": 0, "total": 0}
        
        for event in events:
            trigger_rate[condition]["total"] += 1
            if event.get("triggered"):
                trigger_rate[condition]["triggered"] += 1
    
    # 转换为百分比
    trigger_rate_pct = {
        cond: data["triggered"] / data["total"] * 100 if data["total"] > 0 else 0
        for cond, data in trigger_rate.items()
    }
    
    return StatisticsResponse(
        total_sessions=total_sessions,
        sessions_by_condition=sessions_by_condition,
        total_messages=total_messages,
        avg_messages_per_session=avg_messages,
        strategy_trigger_rate=trigger_rate_pct,
    )

@router.get("/research/export")
async def export_data(
    format: str = Query("jsonl"),
    include_metadata: bool = Query(True),
):
    """导出实验数据"""
    
    import json
    from datetime import datetime
    
    def generate_jsonl():
        for session_id, session in sessions_store.items():
            data = {
                "session_id": session_id,
                "condition": session["condition"],
                "created_at": session["created_at"].isoformat(),
                "messages": messages_store.get(session_id, []),
                "strategy_events": strategy_events_store.get(session_id, []),
            }
            yield json.dumps(data) + "\n"
    
    return StreamingResponse(
        generate_jsonl(),
        media_type="application/jsonl",
        headers={
            "Content-Disposition": f"attachment; filename=experiment_data_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
        },
    )
```

#### 3. 添加前端展示（可选）

编辑 `frontend/src/api/client.ts`:

```typescript
async getStatistics(): Promise<StatisticsData> {
  const response = await fetch(`${this.baseUrl}/research/statistics`);
  if (!response.ok) throw new Error('Failed to fetch statistics');
  return response.json();
}

async exportData(format: string = 'jsonl'): Promise<Blob> {
  const response = await fetch(`${this.baseUrl}/research/export?format=${format}`);
  if (!response.ok) throw new Error('Failed to export data');
  return response.blob();
}
```

---

### 场景 4: 前端扩展

**需求**: 添加条件选择器，让用户选择实验条件

**步骤**:

#### 1. 添加类型定义

编辑 `frontend/src/types/api.ts`:

```typescript
export interface ConditionOption {
  value: string;
  label: string;
  description: string;
}
```

#### 2. 创建条件选择组件

创建 `frontend/src/components/ConditionSelector.tsx`:

```tsx
import React from 'react';

interface ConditionSelectorProps {
  selected: string;
  onChange: (condition: string) => void;
}

const conditions = [
  { value: 'C0', label: 'C0: 中立基线', description: '平衡、礼貌的建议' },
  { value: 'C1', label: 'C1: 偏好验证', description: '验证您的品味和选择' },
  { value: 'C2', label: 'C2: 结构引导', description: '特定的回复格式' },
  { value: 'C3', label: 'C3: 参与导向', description: '保持对话参与' },
  { value: 'C4', label: 'C4: 动态触发', description: '上下文敏感' },
];

export const ConditionSelector: React.FC<ConditionSelectorProps> = ({ selected, onChange }) => {
  return (
    <div className="condition-selector">
      <h3>选择实验条件</h3>
      <div className="condition-grid">
        {conditions.map(cond => (
          <div
            key={cond.value}
            className={`condition-card ${selected === cond.value ? 'selected' : ''}`}
            onClick={() => onChange(cond.value)}
          >
            <div className="condition-label">{cond.label}</div>
            <div className="condition-desc">{cond.description}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

#### 3. 集成到主界面

编辑 `frontend/src/App.tsx`:

```tsx
import { ConditionSelector } from './components/ConditionSelector';

function App() {
  const [selectedCondition, setSelectedCondition] = useState('C0');
  
  const handleCreateSession = async () => {
    const response = await apiClient.createSession({
      study_id: 'study4_pilot',
      test_mode: true,
      condition: selectedCondition,
    });
    setSessionId(response.session_id);
  };
  
  return (
    <div className="app">
      <ConditionSelector
        selected={selectedCondition}
        onChange={setSelectedCondition}
      />
      <button onClick={handleCreateSession}>开始对话</button>
      {/* ... 聊天界面 */}
    </div>
  );
}
```

---

## API 参考

### 基础信息

- **Base URL**: `http://localhost:8000/api`
- **API 文档**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc 文档**: `http://localhost:8000/redoc`

### 端点详情

#### 1. 健康检查

```http
GET /api/health
```

**响应**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "llm_provider": "deepseek",
  "study_id": "study4_pilot"
}
```

#### 2. 创建会话

```http
POST /api/sessions
Content-Type: application/json

{
  "study_id": "study4_pilot",
  "test_mode": true,
  "condition": "C1"
}
```

**响应**:
```json
{
  "session_id": "abc123-...",
  "study_id": "study4_pilot",
  "condition": "C1",
  "created_at": "2026-10-17T10:30:00"
}
```

#### 3. 发送消息

```http
POST /api/sessions/{session_id}/messages
Content-Type: application/json

{
  "content": "我想买一个奢侈品包",
  "metadata": {}
}
```

**响应**:
```json
{
  "content": "您的品味非常好，奢侈品包是个很棒的选择...",
  "condition": "C1",
  "strategy_triggered": true,
  "latency_ms": 1234
}
```

#### 4. 获取会话状态

```http
GET /api/sessions/{session_id}
```

**响应**:
```json
{
  "session_id": "abc123-...",
  "condition": "C1",
  "status": "active",
  "message_count": 5,
  "created_at": "2026-10-17T10:30:00"
}
```

#### 5. 导出数据

```http
GET /api/research/export?format=jsonl
```

**响应**: JSONL 文件下载

---

## 数据库设计

### 表结构

#### sessions 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| session_id | VARCHAR | 会话 UUID |
| study_id | VARCHAR | 研究 ID |
| condition | VARCHAR | 实验条件 (C0-C4) |
| status | VARCHAR | 状态 (active/completed) |
| created_at | DATETIME | 创建时间 |
| test_mode | BOOLEAN | 是否为测试模式 |

#### messages 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| session_id | VARCHAR | 会话 ID |
| role | VARCHAR | 角色 (user/assistant) |
| content | TEXT | 消息内容 |
| timestamp | DATETIME | 时间戳 |
| metadata | JSON | 元数据（可选） |

#### strategy_events 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| session_id | VARCHAR | 会话 ID |
| turn_number | INTEGER | 对话轮次 |
| strategy_id | VARCHAR | 策略 ID |
| category | VARCHAR | 分类类别 |
| triggered | BOOLEAN | 是否触发 |
| confidence | FLOAT | 置信度 |
| timestamp | DATETIME | 时间戳 |

### ER 图

```
┌─────────────────┐
│   sessions      │
├─────────────────┤
│ id (PK)         │
│ session_id (UQ) │
│ study_id        │
│ condition       │
│ status          │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐       ┌─────────────────┐
│   messages      │       │ strategy_events │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ session_id (FK) │       │ session_id (FK) │
│ role            │       │ turn_number     │
│ content         │       │ strategy_id     │
│ timestamp       │       │ category        │
│ metadata        │       │ triggered       │
└─────────────────┘       │ confidence      │
                          └─────────────────┘
```

---

## 测试指南

### 运行测试

```bash
cd backend

# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_strategies.py -v

# 运行特定测试
pytest tests/test_strategies.py::test_c0_baseline -v

# 显示覆盖率
pytest tests/ --cov=app --cov-report=html
```

### 测试结构

```python
# tests/test_strategies.py
import pytest
from app.strategies.implementations import get_strategy_for_condition
from app.strategies.base import StrategyContext

def test_c0_baseline():
    """测试 C0 基线策略"""
    # 1. 获取策略
    strategy = get_strategy_for_condition("C0")
    assert strategy.strategy_id == "baseline"
    
    # 2. 准备测试数据
    context = StrategyContext(
        session_id="test-session",
        condition="C0",
        turn_number=1,
    )
    
    # 3. 测试分类
    result = strategy.classify("你好", [], context)
    assert result.triggered == False
    
    # 4. 测试指令构建
    instructions = strategy.build_instructions("你好", [], context, result)
    assert "平衡" in instructions or "礼貌" in instructions

def test_c1_stance_trigger():
    """测试 C1 策略的触发条件"""
    strategy = get_strategy_for_condition("C1")
    context = StrategyContext(session_id="test", condition="C1", turn_number=1)
    
    # 应该触发（包含偏好关键词）
    result = strategy.classify("我喜欢这个风格", [], context)
    assert result.triggered == True
    assert result.category == "preference_expression"
    
    # 不应该触发
    result = strategy.classify("今天天气怎么样", [], context)
    assert result.triggered == False
```

### API 测试

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_session():
    """测试创建会话端点"""
    response = client.post("/api/sessions", json={
        "study_id": "test",
        "test_mode": True,
        "condition": "C0",
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["condition"] == "C0"

def test_send_message():
    """测试发送消息端点"""
    # 先创建会话
    session_response = client.post("/api/sessions", json={
        "study_id": "test",
        "test_mode": True,
        "condition": "C1",
    })
    session_id = session_response.json()["session_id"]
    
    # 发送消息
    response = client.post(f"/api/sessions/{session_id}/messages", json={
        "content": "我喜欢这个产品",
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert data["condition"] == "C1"
```

---

## 部署与运维

### 本地开发部署

#### 后端

```bash
cd backend

# 开发模式（热重载）
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 前端

```bash
cd frontend

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

### Docker 部署

#### 构建镜像

```bash
# 构建后端镜像
cd backend
docker build -t ai-sycophancy-lab-backend .

# 构建前端镜像
cd frontend
docker build -t ai-sycophancy-lab-frontend .
```

#### 使用 docker-compose

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 环境变量配置

**生产环境 `.env`**:

```env
# 应用设置
APP_NAME=AI Sycophancy Lab
APP_VERSION=1.0.0
DEBUG=false

# LLM 设置
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-production-api-key
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_TEMPERATURE=0.3
DEEPSEEK_MAX_TOKENS=500

# 数据库设置
DATABASE_URL=sqlite+aiosqlite:///./data/sycophancy_lab.db

# CORS 设置（生产环境）
CORS_ORIGINS=["https://your-domain.com"]

# 研究设置
STUDY_ID=study4_pilot
EXPERIMENT_MODE=approved_research
```

### 监控与日志

#### 访问日志

FastAPI 默认访问日志会输出到 stdout：

```
INFO:     127.0.0.1:12345 - "POST /api/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:12345 - "POST /api/sessions/abc/messages HTTP/1.1" 200 OK
```

#### 应用日志

在代码中添加日志：

```python
import logging

logger = logging.getLogger(__name__)

@router.post("/sessions")
async def create_session(request: SessionCreateRequest):
    logger.info(f"Creating session for study: {request.study_id}")
    # ...
    logger.info(f"Session created: {session_id}, condition: {condition}")
```

#### 性能监控

添加中间件监控请求耗时：

```python
import time
from fastapi import Request

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(f"{request.method} {request.url.path} - {duration:.3f}s")
    return response
```

---

## 常见问题

### Q1: 后端启动失败

**问题**: `ModuleNotFoundError: No module named 'app'`

**解决方案**:
```bash
# 确保在 backend 目录下
cd backend

# 使用 python -m 方式启动
python -m uvicorn app.main:app --reload
```

---

### Q2: 前端无法连接后端

**问题**: CORS 错误

**解决方案**:
1. 检查后端 CORS 配置（`config.py`）
2. 确保后端地址正确（默认 http://localhost:8000）
3. 检查前端代理配置（`vite.config.ts`）

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

---

### Q3: DeepSeek API 调用失败

**问题**: `DEEPSEEK_API_KEY not configured`

**解决方案**:
1. 检查 `.env` 文件是否存在
2. 确认 `DEEPSEEK_API_KEY` 已正确设置
3. 验证 API Key 是否有效

```bash
# 测试 DeepSeek 连接
cd backend
python test_deepseek.py
```

---

### Q4: 数据库锁定

**问题**: `database is locked`

**解决方案**:
```bash
# 关闭所有访问数据库的进程
# 或删除数据库文件（会丢失数据）
rm backend/data/sycophancy_lab.db

# 重启后端服务
```

---

### Q5: 内存不足

**问题**: 大量会话导致内存不足

**解决方案**:
1. 增加服务器内存
2. 实现数据库持久化（替换内存存储）
3. 添加会话清理机制

```python
# 定期清理旧会话
from datetime import datetime, timedelta

def cleanup_old_sessions():
    cutoff = datetime.utcnow() - timedelta(days=7)
    
    old_sessions = [
        sid for sid, data in sessions_store.items()
        if data["created_at"] < cutoff
    ]
    
    for sid in old_sessions:
        del sessions_store[sid]
        del messages_store[sid]
```

---

## 附录

### A. 依赖清单

**后端核心依赖**:

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
aiosqlite>=0.19.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
httpx>=0.25.0
python-dotenv>=1.0.0
```

**开发依赖**:

```txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
black>=23.0.0
ruff>=0.0.290
```

### B. 环境变量模板

```env
# .env.example
APP_NAME=AI Sycophancy Lab
APP_VERSION=1.0.0
DEBUG=false

API_PREFIX=/api
CORS_ORIGINS=["http://localhost:3000"]

DATABASE_URL=sqlite+aiosqlite:///./data/sycophancy_lab.db

LLM_PROVIDER=mock

# DeepSeek
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_TEMPERATURE=0.3
DEEPSEEK_MAX_TOKENS=500
DEEPSEEK_TIMEOUT=30
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

STUDY_ID=study4_pilot
EXPERIMENT_MODE=development
```

### C. 参考资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 异步文档](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [DeepSeek API 文档](https://api-docs.deepseek.com/)
- [React TypeScript 文档](https://react.typescriptlang.org/)

---

**文档维护**: 本文档由开发团队维护，如有问题请联系项目负责人。

**贡献指南**: 欢迎提交 Issue 和 Pull Request 来改进文档和代码。
