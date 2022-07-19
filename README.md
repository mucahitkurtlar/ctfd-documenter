# CTFd Documenter

CTFd write-up template generator. Creates `write-up.md` named template.

## Usage
```
usage: ctfd-documenter.py [-h] -t TARGET -u USER -p PASSWORD [-s]

CTFd Documenter - A tool to generate a write-up file from CTFd

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        CTFd target (domain or ip)
  -u USER, --user USER  Username to login to target
  -p PASSWORD, --password PASSWORD
                        Password to login to target
  -s, --solved          Only solved challenges. (default: False)
```
## Example usage

```sh
python ctfd-documenter.py -t https://demo.ctfd.io/ -u usernameHere -p passwordHere
```