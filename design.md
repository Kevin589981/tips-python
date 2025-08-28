# 临时笔记CLI工具设计文档

## 1. 程序架构与模块划分

程序将采用模块化设计，主要包含以下几个核心模块：

### 1.1 主入口模块 (`main.py` 或 `cli.py`)
*   **职责**:
    *   解析命令行参数 (使用 `argparse` 或 `click`)。
    *   读取配置文件。
    *   协调其他模块的工作流程：创建文件 -> 启动编辑器 -> 等待/追踪 -> 清理文件。
    *   处理全局异常。
*   **流程**:
    1.  解析 `--editor`, `--extension`, `--config` 等CLI参数。
    2.  加载配置 (优先级: CLI参数 > 配置文件 > 默认值)。
    3.  调用 `file_manager.create_temp_file()` 创建临时文件。
    4.  调用 `editor_launcher.launch()` 启动编辑器。
    5.  调用 `process_tracker.wait()` 或 `file_watcher.wait()` 等待编辑器关闭。
    6.  调用 `file_manager.cleanup_temp_file()` 删除临时文件。
    7.  处理任何步骤中可能出现的异常，并给出友好提示。

### 1.2 配置管理模块 (`config.py`)
*   **职责**:
    *   定义默认配置。
    *   查找并读取用户配置文件 (如 `~/.tips_config.yaml`)。
    *   解析配置文件内容 (使用 `PyYAML`)。
    *   提供获取配置项的接口。
*   **默认配置**:
    ```python
    DEFAULT_CONFIG = {
        "default_editor": "vscode",
        "default_extension": ".md",
        "editors": {
            "vscode": {
                "command": "code",
                "args": ["--wait"] # VS Code 推荐使用 --wait 实现阻塞
            },
            "notepad": {
                "command": "notepad",
                "args": []
            },
            # ... 其他编辑器
        }
    }
    ```
*   **配置文件路径**:
    *   Windows: `os.path.expanduser("~/.tips_config.yaml")` 或 `os.path.join(os.getenv('APPDATA'), 'Tips', 'config.yaml')` (更符合Windows惯例?)
    *   macOS/Linux: `os.path.expanduser("~/.tips_config.yaml")` 或 `os.path.expanduser("~/.config/tips/config.yaml")` (XDG Base Directory Specification)

### 1.3 临时文件管理模块 (`file_manager.py`)
*   **职责**:
    *   创建临时笔记目录 (`~/.tips/`)。
    *   生成带时间戳的文件名。
    *   创建临时文件。
    *   删除临时文件。
*   **函数**:
    *   `create_temp_dir()`: 确保临时目录存在。
    *   `generate_temp_filename(extension)`: 生成文件名，如 `20231027_143015_123456.md`。
    *   `create_temp_file(directory, filename)`: 创建文件。
    *   `cleanup_temp_file(filepath)`: 安全地删除文件，并处理可能的异常 (如文件被占用)。

### 1.4 编辑器启动模块 (`editor_launcher.py`)
*   **职责**:
    *   根据编辑器名称查找其配置。
    *   构建完整的命令行。
    *   启动编辑器进程。
*   **函数**:
    *   `launch(editor_name, filepath, editor_config)`: 启动指定编辑器打开文件。
        *   `editor_name`: 如 "vscode", "notepad"。
        *   `filepath`: 要打开的文件路径。
        *   `editor_config`: 从配置文件读取的该编辑器的配置。
    *   **注意**: 需要根据不同编辑器的特性选择合适的启动方式。例如，VS Code 的 `--wait` 参数非常有用。

### 1.5 进程/文件状态追踪模块 (`tracker.py` 或 `process_tracker.py` / `file_watcher.py`)
*   **职责**: 监控编辑器进程或文件状态，判断何时可以安全删除文件。
*   **策略**:
    *   **首选 (如果可行)**: **进程追踪 (`process_tracker.py`)**
        *   `wait_for_process_exit(process)`: 等待由 `editor_launcher` 返回的 `subprocess.Popen` 对象代表的进程退出。
        *   **优点**: 对于支持 `--wait` 或类似阻塞参数的编辑器（如VS Code）非常直接有效。
        *   **缺点**: 并非所有编辑器都提供可靠的阻塞启动方式，且跨平台管理子进程有时会遇到细微差异。
    *   **备选**: **文件锁定检测 (`file_watcher.py`)**
        *   `wait_for_file_unlock(filepath)`: 定期（例如每秒）尝试获取文件的独占写锁。如果成功获取，则认为编辑器已关闭文件。
        *   **实现方式**:
            *   在循环中尝试 `with open(filepath, 'r+b') as f:`。如果成功，说明没有其他进程独占写锁定它。
            *   需要处理权限和异常。
        *   **优点**: 更通用，不依赖于编辑器的特定行为。
        *   **缺点**: 检测可能有延迟，且在某些复杂文件锁定场景下可能不够准确。

我们将优先实现并使用**进程追踪**，因为它对于支持 `--wait` 的编辑器（这将是主要目标）是最可靠和直接的方法。文件锁定检测作为备选或补充方案。

### 1.6 工具类/常量 (`utils.py` / `constants.py`)
*   **职责**:
    *   存放通用工具函数或常量定义。
    *   例如: 获取用户主目录、标准化路径、日志记录辅助函数等。

## 2. 配置文件设计

### 2.1 文件格式
使用 **YAML** 格式，因其结构清晰，易于阅读和编写。

### 2.2 文件内容示例 (`~/.tips_config.yaml`)
```yaml
# 默认使用的编辑器名称
default_editor: "vscode"

# 默认创建的文件后缀名
default_extension: ".md"

# 编辑器配置列表
editors:
  vscode:
    command: "code"
    args: ["--wait"] # VS Code --wait 参数使其阻塞直到窗口关闭

  notepad:
    command: "notepad"
    args: []

  notepadpp:
    command: "notepad++"
    # Notepad++ 可能需要特定参数来确保新实例或正确行为
    args: ["-multiInst", "-nosession"]

  sublime:
    command: "subl"
    args: ["--wait"] # Sublime Text 也支持 --wait

  vim:
    command: "vim" # 在终端中运行，行为本身是阻塞的
    args: []

  gvim:
    command: "gvim"
    args: ["--nofork"] # gvim 需要 --nofork 来阻塞

# 可以添加更多编辑器...
```

### 2.3 配置加载逻辑
1.  程序启动时，尝试在预定义路径查找配置文件。
2.  如果找到，使用 `PyYAML` 解析。
3.  将解析后的配置与 `DEFAULT_CONFIG` 进行合并（用户配置覆盖默认配置）。
4.  CLI 参数最终覆盖配置文件中的设置。

## 3. 命令行接口设计 (CLI)

使用 `argparse` (标准库) 或 `click` (第三方库，功能更强大)。这里以 `argparse` 为例。

### 3.1 基本命令
```bash
tips
```
使用默认配置创建并打开笔记。

### 3.2 命令行选项
```bash
usage: tips [-h] [-e EDITOR] [-x EXTENSION] [-c CONFIG]

A CLI tool for creating temporary notes.

optional arguments:
  -h, --help            show this help message and exit
  -e EDITOR, --editor EDITOR
                        Specify the editor to use (overrides config).
  -x EXTENSION, --extension EXTENSION
                        Specify the file extension (overrides config).
  -c CONFIG, --config CONFIG
                        Path to the configuration file.
```

## 4. 跨平台兼容性考虑

*   **路径**: 广泛使用 `os.path` 或 `pathlib` 来处理路径，确保兼容性。
*   **文件锁定**: 文件锁定检测方法在不同系统上行为可能略有不同，需要测试。
*   **编辑器命令**: 配置文件允许用户根据不同系统自定义命令 (e.g., `code` on Windows/macOS vs. `/usr/bin/code` on some Linux distros, though usually not necessary if PATH is set correctly)。
*   **进程管理**: `subprocess` 模块是跨平台的，但具体行为（如 `--wait` 参数的支持）取决于编辑器本身。

## 5. 异常处理

*   **文件操作**: 捕获 `IOError`, `OSError` 等，提示用户权限问题或磁盘空间不足。
*   **编辑器启动**: 捕获 `FileNotFoundError` (命令未找到), `subprocess.SubprocessError` 等，提示用户检查编辑器是否已正确安装并添加到PATH。
*   **配置文件**: 捕获 `yaml.YAMLError`，提示配置文件格式错误。
*   **清理**: 捕获文件删除异常，记录日志或给出警告，但不中断程序退出流程。

## 6. PyPI 打包与发布

*   **项目结构**:
    ```
    tips-cli/
    ├── tips/
    │   ├── __init__.py
    │   ├── __main__.py # 使 `python -m tips` 可用
    │   ├── main.py
    │   ├── config.py
    │   ├── file_manager.py
    │   ├── editor_launcher.py
    │   ├── tracker.py
    │   └── utils.py
    ├── setup.py # 或 pyproject.toml (现代方式)
    ├── README.md
    └── requirements.txt # PyYAML
    ```
*   **入口点**: 在 `setup.py` 或 `pyproject.toml` 中定义控制台脚本 `tips`，指向 `tips.main:main`。
*   **依赖**: `PyYAML`。
*   **Windows无窗口运行**: 发布Python包本身无法直接解决 `Win+R` 无窗口问题。需要额外提供 `.exe` 启动器。可以使用 `PyInstaller` 或 `cx_Freeze` 等工具，在发布流程中打包一个 `tips.exe` (使用 `--noconsole` 或 `--windowed` 选项)，并将此exe放在易于访问的位置（可能需要文档指导用户如何配置PATH或创建快捷方式）。
