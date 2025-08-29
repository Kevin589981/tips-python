#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Tips CLI tool.
"""

import argparse
import sys
from pathlib import Path

# Import internal modules
# These will be created in subsequent steps
try:
    from .config import load_config
    from .file_manager import create_temp_file, cleanup_temp_file
    from .editor_launcher import launch_editor
    from .tracker import wait_for_editor
except ImportError as e:
    # This might happen during initial setup if modules are not yet created
    # We can handle this gracefully for now, or raise a more user-friendly error later
    print(f"Warning: Some modules could not be imported. This is expected during initial setup. Error: {e}")

def main():
    """Main function to run the Tips CLI tool."""
    parser = argparse.ArgumentParser(
        description="A CLI tool for creating temporary notes.",
        epilog="The temporary note file will be automatically deleted after the editor is closed."
    )
    parser.add_argument(
        "-e", "--editor",
        help="Specify the editor to use (overrides config)."
    )
    parser.add_argument(
        "-x", "--extension",
        help="Specify the file extension (overrides config)."
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to the configuration file."
    )

    args = parser.parse_args()

    try:
        # 1. Load configuration
        config = load_config(args.config)
        
        # 2. Override config with CLI args if provided
        editor_name = args.editor if args.editor else config.get("default_editor", "vscode")
        extension = args.extension if args.extension else config.get("default_extension", ".md")
        
        # 3. Create temporary file
        temp_file_path = create_temp_file(extension)
        print(f"Created temporary note: {temp_file_path}")

        # 4. Launch editor
        editor_config = config.get("editors", {}).get(editor_name, {})
        if not editor_config:
            print(f"Warning: Editor '{editor_name}' not found in config. Using default command 'code'.")
            editor_config = {"command": "code", "args": ["--wait"]}
        
        process = launch_editor(editor_name, temp_file_path, editor_config)
        
        # 5. Wait for editor to close (using process tracking)
        wait_for_editor(process, temp_file_path)
        
        # 6. Cleanup
        cleanup_temp_file(temp_file_path)
        print(f"Deleted temporary note: {temp_file_path}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        # Attempt cleanup even on cancellation
        try:
            cleanup_temp_file(temp_file_path)
        except:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()