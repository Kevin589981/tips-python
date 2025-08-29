"""
Temporary file management for the Tips CLI tool.
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime

def get_tips_dir():
    """
    Get the path to the tips directory in the user's home folder.
    Creates the directory if it doesn't exist.
    
    Returns:
        Path: The path to the tips-temp directory.
    """
    home = Path.home()
    tips_dir = home / "tips-temp"
    tips_dir.mkdir(exist_ok=True)
    return tips_dir

def generate_temp_filename(extension=".md"):
    """
    Generate a unique filename based on the current timestamp.
    
    Args:
        extension (str): The file extension to use.
        
    Returns:
        str: The generated filename.
    """
    # Using microseconds for higher uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    # Ensure extension starts with a dot
    if not extension.startswith('.'):
        extension = '.' + extension
    return f"{timestamp}{extension}"

def create_temp_file(extension=".md"):
    """
    Create a temporary note file.
    
    Args:
        extension (str): The file extension to use.
        
    Returns:
        Path: The path to the created temporary file.
    """
    tips_dir = get_tips_dir()
    filename = generate_temp_filename(extension)
    temp_file_path = tips_dir / filename
    
    # Create an empty file
    temp_file_path.touch()
    
    return temp_file_path

def cleanup_temp_file(filepath):
    """
    Delete the temporary file.
    
    Args:
        filepath (Path or str): The path to the file to delete.
    """
    try:
        path = Path(filepath)
        if path.exists():
            path.unlink()
    except Exception as e:
        # It's not critical if cleanup fails, but good to log/warn
        print(f"Warning: Could not delete temporary file {filepath}. Error: {e}")