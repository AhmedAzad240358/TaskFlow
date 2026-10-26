"""Create local practice accounts, preserving existing passwords/API keys on reruns."""
import hashlib
import re
import subprocess
import sys
import uuid
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import KIT, roster

def sql(query):
    return subprocess.run(['docker', 'compose', 'exec', '-T', 'db', 'mariadb', '-uroot', '-proot',
                           '-N', 'testlink', '-e', query], cwd=KIT, check=True, capture_output=True, text=True).stdout

def ensure_user(login, full_name):
    if not re.fullmatch(r'[a-z][a-z0-9_]{0,29}', login):
        raise ValueError('Login must be a safe lowercase first name')
    first, _, last = full_name.partition(' ')
    esc = lambda s: s.replace("'", "''")
    sql(f"INSERT INTO users (login,password,first,last,email,role_id,locale,active,cookie_string,script_key) "
        f"SELECT '{login}','{hashlib.md5(login.encode()).hexdigest()}','{esc(first)}','{esc(last)}','',6,'en_GB',1,"
        f"'{uuid.uuid4().hex}','{uuid.uuid4().hex}' WHERE NOT EXISTS (SELECT 1 FROM users WHERE login='{login}');")

if __name__ == '__main__':
    sql("UPDATE users SET script_key=MD5(RAND()) WHERE login='admin' AND (script_key IS NULL OR script_key='')")
    for member in roster():
        ensure_user(member['login'], member['name'])
    print('Local admin API key and five member accounts ready.')
