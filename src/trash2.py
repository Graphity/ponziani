import platform
import sys
import subprocess
from pathlib import Path

try:
    import distro
except ModuleNotFoundError as error:
    print(error)


BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)


class SysInfo:

    def __init__(self):
        self.system_var = platform.system()

    def __repr__(self):
        return "System information check CLS"

    def __str__(self):
        return "System information check CLS"

    @staticmethod
    def get_python_version(path_level: bool = False) -> str:
        """Returns Python version"""
        if path_level:
            return ".".join(platform.python_version_tuple())  # X.X.X
        return ".".join(platform.python_version_tuple()[:2])  # X.X

    @staticmethod
    def get_architecture() -> tuple:
        """Returns system architecture info"""
        return platform.architecture()

    def get_distro(self) -> tuple:
        """Returns full info about distro"""
        if float(self.get_python_version()) <= 3.7:
            return platform.linux_distribution()
        else:
            if "distro" in sys.modules:
                return distro.linux_distribution()


class SysPrepare(SysInfo):

    def __init__(self):
        super(SysPrepare, self).__init__()

    @staticmethod
    def install_requirements_txt() -> None:
        """Installs the requirements.txt"""
        requirements_txt_full_path = BASE_DIR / "requirements.txt"
        subprocess.run(["pip3", "install", "-r", requirements_txt_full_path], check=True)

    @staticmethod
    def renew_requirements_txt() -> None:
        requirements_txt_full_path = BASE_DIR / "requirements.txt"
        subprocess.run(["python3", "-m", "pip3", "freeze", ">", requirements_txt_full_path])


a = SysPrepare()

a.renew_requirements_txt()