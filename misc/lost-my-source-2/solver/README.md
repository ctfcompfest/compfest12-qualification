Run the following commands on terminal:
```
$ python3 -m venv env 
$ source env/bin/activate
$ pip install pyinstaller
```
After that, find the `archive_viewer.py` inside `env/`. For example, it is located at `env/lib/python3.6/site-packages/PyInstaller/utils/cliutils/`, and then do the following command:
```
$ python env/lib/python3.6/site-packages/PyInstaller/utils/cliutils/archive_viewer.py main
```

After that, extract the `main` from the binary file with command `X main`, save it, and try to do `cat`to that file, and you will able to see the flag.
