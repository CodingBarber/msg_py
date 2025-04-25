# msg_py
The `msg_py` module is a Python library that provides functionality for .msg files

## Requirements & Dependancies
- `pdfkit`
- `extract_msg`
- `wkhtmltopdf`
  This is a requirement for the `pdfkit` module that this module builds off. It can be downloaded [here](https://wkhtmltopdf.org/downloads.html)


## Install
The module can be installed with pip using the following command. (Git must be installed for this to work)
```
pip install git+https://github.com/CodingBarber/msg_py.git
```

### check installation with `msg_py.doctor()`
This is a function that checks if `wkhtmltopdf` was installed correctly, either in the default location (Program Files) or if there is a environment variable called `WKHTMLTOPDF_PATH`
```python
import msg_py

msg_py.doctor()
```
If installed correctly, the above code should print the following to the terminal.
```cmd
✅   wkhtmltopdf is installed in Program Files!
```
