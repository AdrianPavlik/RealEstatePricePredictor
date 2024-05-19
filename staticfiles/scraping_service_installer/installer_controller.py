import os
import subprocess
import platform

current_script_path = os.path.dirname(__file__)
base_path = os.path.join(current_script_path, '..')
absolute_base_path = os.path.abspath(base_path)
scraping_controller_windows_scripts_path = os.path.join(absolute_base_path, 'scraping_service', 'scripts', 'windows')
scraping_controller_linux_scripts_path = os.path.join(absolute_base_path, 'scraping_service', 'scripts', 'linux')

realitysk_scraping_controller_windows_scripts_path = os.path.join(absolute_base_path, 'scraping_service', 'src', 'scrapers', 'realitysk', 'scripts', 'windows')
realitysk_scraping_controller_linux_scripts_path = os.path.join(absolute_base_path, 'scraping_service', 'src', 'scrapers', 'realitysk', 'scripts', 'linux')


def execute_script(script_path: str):
    try:
        system = platform.system()
        if system == 'Windows':
            result = subprocess.run(["start", "powershell.exe", "-File", script_path], capture_output=True, text=True, shell=True)
        elif system == 'Linux':
            os.chmod(script_path, 0o755)
            result = subprocess.run([script_path], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return "Script executed successfully"
        else:
            error_message = result.stderr.strip()
            return f"Script execution error: {error_message}"
    except Exception as e:
        return f"Error starting script: {str(e)}"


def install_windows():
    # install controller
    status = execute_script(f'{scraping_controller_windows_scripts_path}\\install.ps1')

    # install scrapers
    execute_script(f'{realitysk_scraping_controller_windows_scripts_path}\\install.ps1')
    return status


def start_windows():
    # start controller
    status = execute_script(f'{scraping_controller_windows_scripts_path}\\start.ps1')

    # start scrapers
    execute_script(f'{realitysk_scraping_controller_windows_scripts_path}\\start.ps1')
    return status


def restart_windows():
    # restart controller
    status = execute_script(f'{scraping_controller_windows_scripts_path}\\restart.ps1')

    # restart scrapers
    execute_script(f'{realitysk_scraping_controller_windows_scripts_path}\\restart.ps1')
    return status


def stop_windows():
    # stop controller
    status = execute_script(f'{scraping_controller_windows_scripts_path}\\stop.ps1')

    # stop scrapers
    execute_script(f'{realitysk_scraping_controller_windows_scripts_path}\\stop.ps1')
    return status


def uninstall_windows():
    # uninstall controller
    status = execute_script(f'{scraping_controller_windows_scripts_path}\\uninstall.ps1')

    # uninstall scrapers
    execute_script(f'{realitysk_scraping_controller_windows_scripts_path}\\uninstall.ps1')
    return status


def install_linux():
    # install controller
    status = execute_script(f'{scraping_controller_linux_scripts_path}/install.sh')

    # install scrapers
    execute_script(f'{realitysk_scraping_controller_linux_scripts_path}/install.sh')
    return status


def start_linux():
    # start controller
    status = execute_script(f'{scraping_controller_linux_scripts_path}/start.sh')

    # start scrapers
    execute_script(f'{realitysk_scraping_controller_linux_scripts_path}/start.sh')
    return status


def restart_linux():
    # restart controller
    status = execute_script(f'{scraping_controller_linux_scripts_path}/restart.sh')

    # restart scrapers
    execute_script(f'{realitysk_scraping_controller_linux_scripts_path}/restart.sh')
    return status


def stop_linux():
    # stop controller
    status = execute_script(f'{scraping_controller_linux_scripts_path}/stop.sh')

    # stop scrapers
    execute_script(f'{realitysk_scraping_controller_linux_scripts_path}/stop.sh')
    return status


def uninstall_linux():
    # uninstall controller
    status = execute_script(f'{scraping_controller_linux_scripts_path}/uninstall.sh')

    # uninstall scrapers
    execute_script(f'{realitysk_scraping_controller_linux_scripts_path}/uninstall.sh')
    return status
