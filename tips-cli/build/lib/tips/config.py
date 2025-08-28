"""
Configuration management for the Tips CLI tool.
"""

import os
import yaml
from pathlib import Path

import platform

# Default configuration
DEFAULT_CONFIG = {
    "default_editor": "vscode",
    "default_extension": ".md",
    "editors": {
        "vscode": {
            "command": "code.cmd" if platform.system() == "Windows" else "code",
            "args": ["--wait"]
        },
        "notepad": {
            "command": "notepad",
            "args": []
        },
        "notepadpp": {
            "command": "notepad++",
            "args": ["-multiInst", "-nosession"]
        },
        "sublime": {
            "command": "subl",
            "args": ["--wait"]
        },
        "vim": {
            "command": "vim",
            "args": []
        },
        "gvim": {
            "command": "gvim",
            "args": ["--nofork"]
        }
    }
}

def get_config_path(custom_path=None):
    """
    Determine the path to the configuration file.
    
    Args:
        custom_path (str, optional): A custom path provided via CLI.
        
    Returns:
        Path: The resolved path to the configuration file.
    """
    if custom_path:
        return Path(custom_path)
    
    # Standard locations for config file
    home = Path.home()
    # Try XDG config dir first (Linux/macOS), then home dir
    config_dirs = [
        home / ".config" / "tips",  # XDG
        home,                       # Fallback
    ]
    
    for config_dir in config_dirs:
        config_file = config_dir / "config.yaml"
        if config_file.exists():
            return config_file
            
    # If not found, return the default location for creation
    # Prefer XDG on non-Windows, home dir on Windows for simplicity in this example
    # A more robust solution might check os.name or platform
    default_config_dir = home / ".config" / "tips" if os.name != 'nt' else home
    return default_config_dir / "config.yaml"


def load_config(custom_path=None):
    """
    Load configuration from file, merging with defaults.
    
    Args:
        custom_path (str, optional): A custom path provided via CLI.
        
    Returns:
        dict: The loaded and merged configuration.
    """
    config_path = get_config_path(custom_path)
    
    # Start with default config
    config = DEFAULT_CONFIG.copy()
    
    # If config file exists, load and merge it
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f) or {} # Handle empty files
            # Deep merge would be better, but for simplicity, top-level keys override
            config.update(user_config)
        except yaml.YAMLError as e:
            print(f"Warning: Could not parse config file {config_path}. Using defaults. Error: {e}")
        except Exception as e:
            print(f"Warning: Could not read config file {config_path}. Using defaults. Error: {e}")
    else:
        # Optionally, create a default config file if it doesn't exist
        # This is a nice-to-have feature
        pass
        
    return config