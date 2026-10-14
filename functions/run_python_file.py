import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Used to run Python files",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to run Python files from, relative to the working directory (default is the working directory itself)",
                    },
                "args": {
                    "type":"array",
                    "items":{"type": "string"},
                    "description":"Arguments passed to the function",
                    }
                },
            },
        },
    }

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    parts = []
    try:
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd = working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")
        if not result.stderr and not result.stdout:
            parts.append("No output produced")

        else:
             parts.append(f"STDOUT: {result.stdout} \n STDERR: {result.stderr}")
        final_string = "\n".join(parts)
        return final_string


    except Exception as e:
        return f"Error: executing Python file: {e}"
