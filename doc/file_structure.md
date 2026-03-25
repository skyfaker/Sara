## 项目结构

```
sara/api/
├── app_factory.py                          # Flask应用工厂
├── app.py                                  # 应用入口
├── .env                                    # 环境配置
├── pyproject.toml                          # 项目依赖配置
├── uv.lock                                 # 依赖锁定文件
│
├── configs/                                # 配置模块
│   ├── __init__.py
│   ├── deploy_config.py                    # 部署配置
│   ├── file_config.py                      # 文件上传配置
│   ├── llm_config.py                       # LLM配置
│   ├── log_config.py                       # 日志配置
│   └── middleware_config.py                # 中间件配置
│
├── controllers/                            # 控制器层
│   ├── cli/                                # CLI命令行工具
│   │   ├── __init__.py
│   │   ├── command.py                      # CLI入口 (统一app定义)
│   │   ├── chat.py                         # 聊天命令函数 (chat/chat_once)
│   │   ├── file.py                         # 文件上传命令函数 (upload)
│   │   └── rag.py                          # RAG查询命令函数 (query/ask)
│   └── web/                                # Web API接口
│       ├── __init__.py
│       ├── chat.py                         # 聊天REST接口
│       ├── file.py                         # 文件上传REST接口
│       ├── rag.py                          # RAG查询REST接口
│       └── hello.py                        # Hello World示例
│
├── core/                                   # 核心功能模块
│   ├── providers/                          # LLM提供商抽象层
│   │   ├── __init__.py
│   │   ├── base.py                         # 基础Provider接口
│   │   ├── litellm_provider.py             # LiteLLM实现
│   │   └── registry.py                     # Provider注册中心
│   └── rag/                                # RAG核心功能
│       ├── file_loader/                    # 文档加载器
│       │   ├── __init__.py
│       │   ├── base.py                     # 加载器基类
│       │   └── docling_loader.py           # Docling DOCX加载器
│       ├── file_indexer.py                 # LLM索引器 (生成description+content)
│       └── retriever.py                    # 智能检索器 (两阶段检索)
│
├── extensions/                             # Flask扩展
│   ├── __init__.py
│   ├── ext_blueprints.py                   # Blueprint注册
│   ├── ext_db.py                           # 数据库扩展
│   ├── ext_logging.py                      # 日志扩展
│   ├── ext_migrate.py                      # 数据库迁移扩展
│   ├── ext_storage.py                      # 存储扩展
│   └── storage/
│       ├── base_storage.py                 # 存储基类
│       └── local_storage.py                # 本地文件存储实现
│
├── migrations/                             # 数据库迁移
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── *.py                            # 迁移脚本
│
├── models/                                 # 数据库模型
│   ├── __init__.py
│   ├── database.py                         # 数据库连接
│   └── model.py                            # ORM模型定义
│
├── services/                               # 业务逻辑层
│   ├── chat_service.py                     # 聊天服务 (异步LLM调用)
│   └── file_service.py                     # 文件服务 (上传/验证)
│
├── storage/                                # 文件存储目录
│   ├── upload_files/                       # 用户上传的原始文件
│   └── index_files/                        # LLM生成的markdown索引文件
│
└── tests/                                  # 测试套件
    ├── test_chat_service.py                # 聊天服务测试 (8个)
    ├── test_docling_loader.py              # 文档加载器测试 (4个)
    ├── test_file_indexer.py                # 索引器测试 (7个)
    ├── test_file_service.py                # 文件服务测试 (4个)
    ├── test_rag_integration.py             # RAG集成测试 (6个)
    ├── test_retriever.py                   # 检索器测试 (13个)
    └── test_data/
        ├── doc1.docx                       # 测试文档
        └── test_save.txt                   # 测试文本
```

## Project Structure

```
sara/api/
├── app_factory.py                          # Flask application factory
├── app.py                                  # Application entry point
├── .env                                    # Environment configuration
├── pyproject.toml                          # Project dependency config
├── uv.lock                                 # Dependency lock file
│
├── configs/                                # Configuration module
│   ├── __init__.py
│   ├── deploy_config.py                    # Deployment config
│   ├── file_config.py                      # File upload config
│   ├── llm_config.py                       # LLM config
│   ├── log_config.py                       # Logging config
│   └── middleware_config.py                # Middleware config
│
├── controllers/                            # Controller layer
│   ├── cli/                                # CLI tools
│   │   ├── __init__.py
│   │   ├── command.py                      # CLI entry point (single app definition)
│   │   ├── chat.py                         # Chat command functions (chat/chat_once)
│   │   ├── file.py                         # File upload command functions (upload)
│   │   └── rag.py                          # RAG query command functions (query/ask)
│   └── web/                                # Web API controllers
│       ├── __init__.py
│       ├── chat.py                         # Chat REST endpoints
│       ├── file.py                         # File upload REST endpoints
│       ├── rag.py                          # RAG query REST endpoints
│       └── hello.py                        # Hello World example
│
├── core/                                   # Core modules
│   ├── providers/                          # LLM provider abstraction
│   │   ├── __init__.py
│   │   ├── base.py                         # Base provider interface
│   │   ├── litellm_provider.py             # LiteLLM implementation
│   │   └── registry.py                     # Provider registry
│   └── rag/                                # RAG core
│       ├── file_loader/                    # Document loaders
│       │   ├── __init__.py
│       │   ├── base.py                     # Loader base class
│       │   └── docling_loader.py           # Docling DOCX loader
│       ├── file_indexer.py                 # LLM indexer (generates description + content)
│       └── retriever.py                    # Smart retriever (two-stage retrieval)
│
├── extensions/                             # Flask extensions
│   ├── __init__.py
│   ├── ext_blueprints.py                   # Blueprint registration
│   ├── ext_db.py                           # Database extension
│   ├── ext_logging.py                      # Logging extension
│   ├── ext_migrate.py                      # Database migration extension
│   ├── ext_storage.py                      # Storage extension
│   └── storage/
│       ├── base_storage.py                 # Storage base class
│       └── local_storage.py                # Local file storage implementation
│
├── migrations/                             # Database migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── *.py                            # Migration scripts
│
├── models/                                 # Database models
│   ├── __init__.py
│   ├── database.py                         # Database connection
│   └── model.py                            # ORM model definitions
│
├── services/                               # Business logic layer
│   ├── chat_service.py                     # Chat service (async LLM calls)
│   └── file_service.py                     # File service (upload/validation)
│
├── storage/                                # File storage directory
│   ├── upload_files/                       # Raw uploaded files
│   └── index_files/                        # LLM-generated markdown index files
│
└── tests/                                  # Test suite
    ├── test_chat_service.py                # Chat service tests (8)
    ├── test_docling_loader.py              # Document loader tests (4)
    ├── test_file_indexer.py                # Indexer tests (7)
    ├── test_file_service.py                # File service tests (4)
    ├── test_rag_integration.py             # RAG integration tests (6)
    ├── test_retriever.py                   # Retriever tests (13)
    └── test_data/
        ├── doc1.docx                       # Test document
        └── test_save.txt                   # Test text file
```