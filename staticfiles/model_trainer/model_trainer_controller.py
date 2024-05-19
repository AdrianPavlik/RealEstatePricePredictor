import os
import subprocess
import platform

current_script_path = os.path.dirname(__file__)
base_path = os.path.join(current_script_path, '..')
absolute_base_path = os.path.abspath(base_path)
nodel_trainer_path = os.path.join(absolute_base_path, 'model_trainer')


def execute_script_in_terminal(script_path: str):
    try:
        print("Executing script at:", script_path)
        if platform.system() == 'Windows':
            command = f"start cmd.exe /K python {script_path}"
            subprocess.run(command, shell=True)
        elif platform.system() == 'Linux':
            os.chmod(script_path, 0o755)
            command = ["gnome-terminal", "--", "bash", "-c", f"python3 {script_path}; exec bash"]
            subprocess.Popen(command)
        else:
            raise NotImplementedError(f"Unsupported operating system")

        return "Terminal opened and script executed."
    except Exception as e:
        return f"Error opening terminal or running script: {str(e)}"


def train_model():
    return execute_script_in_terminal(f'{nodel_trainer_path}\\model_trainer.py & {nodel_trainer_path}\\helper.py')
