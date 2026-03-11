```
sara/api/
├── app_factory.py
├── app.py
├── .env
├── .python-version
├── pyproject.toml
├── uv.lock
│
├── configs/                              # 配置模块
│   ├── __init__.py
│   ├── deploy_config.py
│   ├── file_config.py
│   ├── llm_config.py                     # ✅ 新增：LLM配置
│   ├── log_config.py
│   └── middleware_config.py
│
├── controllers/                          # 控制器层
│   ├── cli/                             # ✅ 新增：CLI工具
│   │   ├── __init__.py
│   │   └── chat.py                      # ✅ 新增：交互式聊天CLI
│   └── web/                             # Web API
│       ├── __init__.py
│       ├── chat.py                      # ✅ 新增：聊天REST接口
│       ├── file.py
│       └── hello.py
│
├── core/                                 # 核心功能
│   ├── providers/                       # LLM提供商
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── litellm_provider.py
│   │   └── registry.py
│   └── rag/                             # RAG功能（空目录）
│
├── extensions/                           # Flask扩展
│   ├── __init__.py
│   ├── ext_blueprints.py
│   ├── ext_db.py
│   ├── ext_logging.py
│   ├── ext_migrate.py
│   ├── ext_storage.py
│   └── storage/
│       ├── base_storage.py
│       └── local_storage.py
│
├── migrations/                           # 数据库迁移
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── 351454506ccb_recreate_upload_files_table.py
│
├── models/                               # 数据库模型
│   ├── __init__.py
│   ├── database.py
│   └── model.py
│
├── services/                             # 业务逻辑层
│   ├── chat_service.py                  # ✅ 新增：聊天服务（异步）
│   └── file_service.py
│
├── storage/                              # 文件存储
│   └── upload_files/
│       └── .gitignore
│
├── tasks/                                # 任务模块（空目录）
│
└── tests/                                # 测试
    ├── test_chat_service.py             # ✅ 新增：聊天服务测试（8个）
    ├── test_file_service.py
    └── test_data/
        └── test_save.txt
```