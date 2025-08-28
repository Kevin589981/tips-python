# Tips CLI Tool

A simple command-line tool for creating temporary notes. The notes are automatically deleted after you close the editor.

## Features

*   **Quick Note Creation**: Instantly create a temporary note file with a timestamped name.
*   **Configurable Editor**: Use your preferred editor (VS Code, Notepad, Notepad++, etc.).
*   **Automatic Cleanup**: The temporary file is automatically deleted when you close the editor.
*   **Cross-Platform**: Works on Windows, macOS, and Linux.

## Installation

```bash
pip install tips-cli-tool
```

## Usage

Simply run the command:

```bash
tips
```

This will create a new temporary `.md` file and open it in your default editor (VS Code by default).

### Options

*   `-e EDITOR`, `--editor EDITOR`: Specify the editor to use (overrides config).
*   `-x EXTENSION`, `--extension EXTENSION`: Specify the file extension (overrides config).
*   `-c CONFIG`, `--config CONFIG`: Path to the configuration file.

### Examples

```bash
# Use Notepad on Windows
tips --editor notepad

# Create a temporary .txt file
tips --extension .txt

# Use a custom configuration file
tips --config /path/to/my/config.yaml
```

## Configuration

Tips CLI Tool uses a configuration file to define default settings and editor commands.

The configuration file is located at:

*   **Linux/macOS**: `~/.config/tips/config.yaml` or `~/.tips_config.yaml`
*   **Windows**: `~/.tips_config.yaml` (or potentially `%APPDATA%/Tips/config.yaml`)

### Example Configuration (`config.yaml`)

```yaml
# Default editor to use
default_editor: "vscode"

# Default file extension
default_extension: ".md"

# Editor configurations
editors:
  vscode:
    command: "code"
    args: ["--wait"]

  notepad:
    command: "notepad"
    args: []

  notepadpp:
    command: "notepad++"
    args: ["-multiInst", "-nosession"]

  sublime:
    command: "subl"
    args: ["--wait"]

  vim:
    command: "vim"
    args: []

  gvim:
    command: "gvim"
    args: ["--nofork"]
```

## How It Works

1.  When you run `tips`, it creates a new file in `~/.tips/` with a name like `YYYYMMDD_HHMMSS_microseconds.md`.
2.  It then launches your configured editor to open this file.
3.  The tool waits for the editor process to finish (typically when you close the editor window).
4.  Once the editor is closed, the temporary file is automatically deleted.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.