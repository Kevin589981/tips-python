"""
Editor launching functionality for the Tips CLI tool.
"""

import subprocess
import sys
from pathlib import Path

def launch_editor(editor_name, filepath, editor_config):
    """
    Launch the specified editor to open the given file.
    
    Args:
        editor_name (str): The name of the editor (e.g., 'vscode').
        filepath (Path): The path to the file to open.
        editor_config (dict): The configuration for the editor, including 'command' and 'args'.
        
    Returns:
        subprocess.Popen: The process object for the launched editor.
        
    Raises:
        FileNotFoundError: If the editor command is not found.
        subprocess.SubprocessError: If the process fails to start.
    """
    command = editor_config.get("command", "code") # Fallback, though should be in config
    args = editor_config.get("args", [])
    
    # Full command list
    cmd = [command] + args + [str(filepath)]
    
    try:
        # Use Popen to get the process object for tracking
        # shell=False is generally safer and recommended
        process = subprocess.Popen(cmd, shell=False)
        return process
    except FileNotFoundError:
        # This is a common error if the editor is not installed or not in PATH
        raise FileNotFoundError(f"Editor command '{command}' not found. Please check your configuration or ensure the editor is installed and in your system PATH.")
    except Exception as e:
        # Re-raise other subprocess errors
        raise subprocess.SubprocessError(f"Failed to launch editor '{editor_name}': {e}") from e