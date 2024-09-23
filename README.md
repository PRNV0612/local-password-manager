# Python Password Manager

A simple local password manager written in Python and MariaDB. It uses [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) to derive a 256-bit key from a MASTER PASSWORD and DEVICE SECRET, which is then used with AES-256 for encryption and decryption.

## Installation

### Prerequisites

- Python 3
- MariaDB

You can run this on Windows, Linux, or macOS.

---

### Windows Installation

#### 1. Install Python Requirements

```bash
sudo apt install python3-pip
pip install -r requirements.txt
```

#### 2.Install MariaDB
Follow these instructions to install MariaDB on Windows: https://www.mariadbtutorial.com/getting-started/install-mariadb/

Create MariaDB User and Grant Permissions
#### Navigate to the MariaDB bin directory:
```bash
file:///C:/Program%20Files/MariaDB/bin
```

##### Login to MariaDB as root:
```bash
sudo mysql -u root
```
##### Create a user:
```bash
CREATE USER 'pm'@localhost IDENTIFIED BY 'password';
```

##### Grant privileges:
```bash
GRANT ALL PRIVILEGES ON *.* TO 'pm'@localhost IDENTIFIED BY 'password';
```
## Running the password manager

### Configure

First, you need to configure the password manager by choosing a MASTER PASSWORD. This config step is only required once.

```bash
python config.py make
```
To delete the existing configuration and all stored entries, use:
```bash
python config.py delete
```

To remake the configuration:

```bash
python config.py remake
```

### Usage
```bash
python pm.py -h
usage: pm.py [-h] [-s NAME] [-u URL] [-e EMAIL] [-l LOGIN] [--length LENGTH] [-c] option

Description

positional arguments:
  option                (a)dd / (e)xtract / (g)enerate

optional arguments:
  -h, --help            show this help message and exit
  -s NAME, --name NAME  Site name
  -u URL, --url URL     Site URL
  -e EMAIL, --email EMAIL
                        Email
  -l LOGIN, --login LOGIN
                        Username
  --length LENGTH       Length of the password to generate
  -c, --copy            Copy password to clipboard
```
#### To Add an Entry:
```bash
python pm.py add -s mysite -u mysite.com -e hello@email.com -l myusername
```

#### To Retrieve an entry:
```bash
python pm.py extract
```
To retrieve entries matching a site name:
```bash
python pm.py e -s mysite
```

To retrieve entries matching a site name and username:
```bash
python pm.py e -s mysite -l myusername
```
To retrieve and copy the password of a specific site and username:
```bash
python pm.py e -s mysite -l myusername --copy
```

#### To Generate a password
To generate a password of a specified length and copy it to the clipboard:

```bash
python pm.py g --length 15
```
This will generate a password of length 15 and automatically copy it to the clipboard.




