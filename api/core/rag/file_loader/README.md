# Docling Loader - VSCode调试说明

## 文件说明

- `base.py`: 文件加载器的抽象基类
- `docling_loader.py`: 使用Docling库的文档加载器实现

## 运行方式

### 命令行运行

```bash
# 从api目录运行
cd api
uv run python -m core.rag.file_loader.docling_loader
```

### VSCode调试

已配置调试启动项在 `.vscode/launch.json`:

1. **Debug Docling Loader** - 专门用于调试docling_loader.py
   - 打开 `docling_loader.py`
   - 在代码中设置断点（例如第133行的 `loader = DoclingLoader()`）
   - 按 `F5` 或点击"运行和调试"面板中的"Debug Docling Loader"
   
2. **Python: Current File** - 调试当前打开的任何Python文件
   - 打开任意Python文件
   - 设置断点
   - 按 `F5`

## 测试文件

测试文件位于: `api/tests/test_data/doc1.docx`

这是一个《治安管理处罚法》的DOCX文档，包含多个章节和条款。

## 输出说明

程序会将DOCX文档解析为多个文本块（chunks），每个块包含：
- 块编号
- 文本长度
- 文本内容（前500字符）

示例输出：
```
Total chunks extracted: 20

[Chunk 1/20]
Length: 10 characters
--------------------------------------------------------------------------------
**第一章　总则**
--------------------------------------------------------------------------------
```

## 调试要点

### 关键断点位置

1. **第133行** - 初始化DoclingLoader
   ```python
   loader = DoclingLoader()
   ```
   
2. **第134行** - 调用load_file
   ```python
   documents = loader.load_file(file_path)
   ```

3. **第54-63行** - 文档转换和分块逻辑
   ```python
   conversion_result = self.converter.convert(file_path)
   docling_document = conversion_result.document
   chunks = list(self.chunker.chunk(docling_document))
   ```

### 查看变量

调试时可以检查：
- `file_path`: 文件绝对路径
- `conversion_result`: Docling转换结果
- `docling_document`: 解析后的文档对象
- `chunks`: 分块后的文档片段列表
- `documents`: 最终的Document对象列表

## 依赖说明

核心依赖：
- `docling`: 文档转换库
- `docling-core`: 文档分块器
- `langchain-core`: Document类定义
- `loguru`: 日志记录

所有依赖已在 `pyproject.toml` 中配置。
