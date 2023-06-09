# How To Use

Disini menggunakan ubuntu sebagai OS


## Installation

1. Siapkan VENV dari python + install requirements
```python
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install -r requirements.txt
```
2. Siapkan server Mysql
```bash
    $ sudo apt-get install mysql-server
```
3. verifikasi server Mysql
```bash
    $ systemctl is-active Mysql
```
4. Setup server Mysql
```bash
    $ sudo mysql
    mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'my-secret-password';
    mysql> exit
```
5. Run scripts!
```bash
    python3 run main.py
```
6. TEST menggunakan POSTMAN
