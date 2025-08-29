"""
Process tracking functionality for the Tips CLI tool.
"""

import subprocess
import time
from pathlib import Path

def wait_for_editor(process, filepath):
    """
    Wait for the editor process to finish.
    This is the primary method, leveraging editor's --wait or similar flags.
    
    Args:
        process (subprocess.Popen): The process object returned by launch_editor.
        filepath (Path): The path to the file being edited (for potential future use or context).
    """
    if process:
        # This will block until the process completes (e.g., VS Code window with --wait closes)
        # communicate() is often used, but for a simple wait, just process.wait() is sufficient
        # and avoids potential issues with capturing large outputs.
        try:
            process.wait()
        except KeyboardInterrupt:
            # If the user interrupts while waiting, terminate the process if it's still running
            if process.poll() is None: # Check if process is still running
                process.terminate()
                try:
                    process.wait(timeout=5) # Give it a moment to terminate gracefully
                except subprocess.TimeoutExpired:
                    process.kill() # Force kill if it doesn't terminate
            raise # Re-raise the KeyboardInterrupt to be handled by main

# Note: File locking detection logic would go here if needed as a fallback
# def wait_for_file_unlock(filepath):
#     ...