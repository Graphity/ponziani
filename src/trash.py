import platform
import getpass
import sys, subprocess, os
import os.path


class SysInfo:
    def __init__(self):
        self.system_ver = platform.system()

    def __repr__(self):
        return "System information check CLS"

    def get_python_version(self, patchleve=False):
        if patchleve:
            return ".".join(platform.python_version_tuple())
        return ".".join(platform.python_version_tuple()[:2])

    def get_arch(self):
        return platform.architecture()

    def get_distro(self):
        if float(self.get_python_version()) <= 3.7:
            return platform.linux_distribution()
        else:
            try:
                import distro
            except:
                pass
            if ('distro' in sys.modules):
                return distro.linux_distribution()


class SysPrepare(SysInfo):
    def __init__(self):
        super().__init__()
        self.data_list = {
            "/var/log/clicka_logs/": [],
            "/var/log/clicka_logs/actions/": ['email_number_button.log'],
            "/var/log/clicka_logs/api/": ['failed_userdata.log'],
            "/var/log/clicka_logs/crons_log/": [],
            "/var/log/clicka_logs/viewers_logs/": ['deleted_lead.log', 'exported_rows.log', 'today.log',
                                                   'today_form.log', 'traderoom_login_button.log'],
        }

    def install_package(self, p_name):
        if p_name:
            subprocess.run(["sudo", "apt-get", "install", "-y", p_name], check=True)
            return True
        return False

    def apt_f(self):
        subprocess.run(["sudo", "apt-get", "-f", "-y", "install"], check=True)

    def exec_com(self, arg=None):
        if arg is not None:
            subprocess.run(arg, check=True)

    def remove_pack(self, p_name):
        if p_name:
            subprocess.run(["sudo", "apt-get", "remove", "--purge", "-y", p_name], check=True)
            return True
        return False

    def dpkg_install(self, p_name):
        if p_name:
            subprocess.run(["sudo", "dpkg", "-i", p_name], check=True)

    def update_rep(self):
        subprocess.run(["sudo", "apt-get", "update", "-y"], check=True)

    def pip_install(self, pack):
        if pack:
            subprocess.run(["pip3", "install", pack], check=True)
            return True
        return False

    def list_dir(self, path):
        return os.listdir(path)

    def download_pack(self, pack, url):
        if pack and url:
            wget.download(pack, url)
            return True
        return False

    def file_rm(self, file):
        os.remove(file)

    def file_exist(self, path):
        return os.path.exists(path)

    def create_fd(self):
        for x, y in self.data_list.items():
            if not self.file_exist(x):
                os.mkdir(x)
                os.chmod(x, 0o0777)
            if len(y) > 0:
                for l in y:
                    if not self.file_exist(x + l):
                        with open(x + l, 'w'): pass
                        os.chmod(x + l, 0o0777)

    def add_key(self, path):
        if path:
            subprocess.run(["apt-key", "add", path], check=True)
            return True
        return False

    def get_policy(self, pack):
        if pack:
            subprocess.run(["sudo", "apt-cache", "policy", pack], check=True)

    def add_repository(self):
        subprocess.run(["add-apt-repository", "ppa:deadsnakes/ppa", "-y"], check=True)

    def process_mgmt(self, state, name):
        subprocess.run(["sudo", "systemctl", state, name], check=True)

    def create_init_db(self, name):
        subprocess.run(["sudo", "-u", "odoo", "odoo", "-d", name, "--without-demo=all", "--stop-after-init"],
                       check=True)

    def install_module(self, db_name, modules):
        subprocess.run(["sudo", "-u", "odoo", "odoo", "-d", db_name, "-i", modules, "--stop-after-init"], check=True)


if __name__ == '__main__':
    if getpass.getuser() != 'root':
        raise PermissionError("Only root can run this script!")
    syst = SysPrepare()
    if float(syst.get_python_version()) < 3.6:
        raise NotImplementedError("Need Python version 3.6+")
    if syst.system_ver != 'Linux':
        raise NotImplementedError("This Script is only capable for Linux ubuntu system")
    else:
        if len(syst.get_distro()) > 0:
            if syst.get_distro()[0] != 'Ubuntu':
                raise NotImplementedError("This Script is only capable ubuntu system")
            else:
                try:
                    v = syst.get_distro()[1]
                except:
                    v = False
                if v:
                    if 20.04 < float(v):
                        print("You are trying to run script on %s tested version is 20.04" % (
                            ".".join(syst.get_distro())))
                syst.update_rep()
                syst.apt_f()
                install_pip = syst.install_package("python3-pip")
                install_wget = syst.pip_install("wget")
                import wget

                install_postgres = syst.install_package("postgresql")
                list_file = syst.list_dir('/usr/local/src')
                if "odoo.key" in [x for x in list_file]:
                    syst.file_rm("/usr/local/src/odoo.key")
                download_odookey = syst.download_pack('https://nightly.odoo.com/odoo.key', '/usr/local/src/odoo.key')
                if syst.file_exist("/usr/local/src/odoo.key"):
                    key_add = syst.add_key('/usr/local/src/odoo.key')
                    if key_add:
                        syst.remove_pack("wkhtmltopdf")
                        if not syst.file_exist("/tmp/wkhtml.deb"):
                            syst.download_pack(
                                "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb",
                                "/tmp/wkhtml.deb")
                        if syst.file_exist("/tmp/wkhtml.deb"):
                            try:
                                syst.dpkg_install("/tmp/wkhtml.deb")
                            except:
                                syst.apt_f()
                            syst.exec_com(['wkhtmltopdf', '--version'])
                        if syst.file_exist("/etc/apt/sources.list.d/odoo.list"):
                            syst.file_rm("/etc/apt/sources.list.d/odoo.list")
                        with open("/etc/apt/sources.list.d/odoo.list", "w") as fw:
                            fw.write("deb http://nightly.odoo.com/13.0/nightly/deb/ ./")
                        syst.update_rep()
                        syst.get_policy("odoo")
                        syst.install_package("odoo")
                        syst.pip_install("xlwt")
                        syst.pip_install("num2words")
                        syst.pip_install("PyJWT")
                        syst.pip_install("xlrd")
                        syst.pip_install("xlutils")
                        syst.pip_install("xlsxwriter")
                        syst.pip_install("pygogo")
                        syst.pip_install("future")
                        syst.pip_install("twilio")
                        syst.pip_install("tornado==3.2.1")
                        syst.pip_install("psycopg2-binary")
                        syst.pip_install("websocket-client")
                        syst.install_package("nginx")
                        syst.install_package("python3-mysqldb")
                        syst.install_package("unzip")
                        syst.install_package("python3-gdbm")
                        syst.install_package("python3-dev")
                        syst.install_package("software-properties-common")
                        syst.add_repository()
                        syst.update_rep()
                        syst.install_package("python3.6")
                        syst.install_package("python3.6-gdbm")
                        syst.install_package("python3.6-dev")
                        syst.create_fd()
