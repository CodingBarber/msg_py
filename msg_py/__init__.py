"""
# msg_py
The `msg_py` module is a Python library that provides functionality to convert .msg files to PDF format.
It uses the `extract_msg` library to extract the contents of the .msg file and pdfkit to convert the extracted HTML content to PDF.
It also requires `wkhtmltopdf` to be installed on the system to perform the conversion. This can be downladed at https://wkhtmltopdf.org/downloads.html
"""


__versaion__ = '0.1.0'
__author__ = "Cody Barber"
__exteral_libraries__ = ["extract_msg", "pdfkit", "re", "base64", "os"]


import extract_msg
import re
import base64
import pdfkit
import os

WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

def doctor(throw_error_if_not_installed:bool = False) -> bool|Exception:
    """
    # Doctor
    The doctor function checks if wkhtmltopdf is installed in the default location or if it is set in the environment variables.
    - If it is not installed, it will raise an exception if throw_error_in_not_installed is set to `True`.
    - The function returns `True` if wkhtmltopdf is installed, otherwise it returns `False`.

    wkhtmltopdf can be installed from https://wkhtmltopdf.org/downloads.html
    """

    print("\nChecking if wkhtmltopdf is installed in Program files...\n")
    if os.path.exists(WKHTMLTOPDF_PATH):
        print("✅   wkhtmltopdf is installed in Program files!")
        return True
    
    else:
        print("⚠️    wkhtmltopdf is not installed in the default location... \nchecking for 'WKHTMLTOPDF_PATH' in enviroment variables...\n")
    
    if 'WKHTMLTOPDF_PATH' in os.environ:
        if os.path.exists(os.environ['WKHTMLTOPDF_PATH']):
            print("✅   wkhtmltopdf is installed in the enviroment variables")
            return True
        else:
            print("❌   WKHTMLTOPDF_PATH eniviroment variable is set, but the path does not exist")
            print("Please set the 'WKHTMLTOPDF_PATH' enviroment variable to the path of the wkhtmltopdf executable.")
            if throw_error_if_not_installed:
                raise Exception("wkhtmltopdf is not installed in the default location. Please set the 'WKHTMLTOPDF_PATH' enviroment variable to the path of the wkhtmltopdf executable.")
            return False
    else:
        print("❌   wkhtmltopdf is not installed")
        print("Please install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html")
        print(f"After installing, if you did not install to the defualt location 'C:\\Program Files\\wkhtmltopdf' Then please set the 'WKHTMLTOPDF_PATH' enviroment variable to the path of the wkhtmltopdf executable.")
        print("Example: WKHTMLTOPDF_PATH = C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        if throw_error_if_not_installed:
            raise Exception("wkhtmltopdf is not installed in the default location. Please set the 'WKHTMLTOPDF_PATH' enviroment variable to the path of the wkhtmltopdf executable.")
        return False




def set_wkhtmltopdf_path(wkhtmltopdf_path:str) -> None:
    """
    # Set wkhtmltopdf path
    Set the path to the wkhtmltopdf executable.

    ### Parameters:
    wkhtmltopdf_path (str): The path to the wkhtmltopdf executable.

    ### Returns:
    (None) The path to the wkhtmltopdf executable is set in the environment variables.
    """
    if os.path.exists(wkhtmltopdf_path):
        os.environ['WKHTMLTOPDF_PATH'] = wkhtmltopdf_path
        print(f"✅   WKHTMLTOPDF_PATH enviroment variable set to {wkhtmltopdf_path}")
    else:
        raise Exception("The path does not exist. Please check the path and try again.")




class Msg():
    """
    # Msg
    The Main class for all msg_py functionality.
    """
    def __init__(self, msg_file_path:str, wkhtmltopdf_path:str = WKHTMLTOPDF_PATH):
        self.msg_file_path = msg_file_path
        self.wkhtmltopdf_path = wkhtmltopdf_path
        self.message_object = extract_msg.Message(msg_file_path)




    def convert_to_pdf(self, output_pdf_path:str = None, keep_html_file = False) -> None:
        """
        # Convert to PDF
        Create a PDF file from a Msg object to a PDF file.

        ### Parameters:
        output_pdf_path (str): The path where the output PDF will be saved.

        ### Returns:
        (None) the PDF file will be saved to the specified path.
        """

        if output_pdf_path is None:
            output_pdf_path = self.msg_file_path.replace(".msg", ".pdf")
        
        temp_file_path = self.msg_file_path.replace(".msg", ".html")

        with open(temp_file_path, 'wb') as f:
            msg_body_bytes = self.message_object.htmlBody
            msg_body = msg_body_bytes.decode('utf-8')

            for attachment in self.message_object.attachments:
                if f"cid:{attachment.name}" in msg_body:
                    file_extention = attachment.name.split(".")[-1]
                    base_64_string = base64.b64encode(attachment.data).decode('utf-8')
                    matching_pattern = '"cid:' + re.escape(attachment.name) + '@(?:\s|\S)*?"'
                    replace_String = f'"data:image/{file_extention};base64,{base_64_string}"'
                    matches = re.findall(matching_pattern, msg_body)
                    for match in matches:
                        msg_body = msg_body.replace(str(match),replace_String)

            f.write(msg_body.encode('utf-8'))

        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
        pdfkit.from_file(temp_file_path, output_pdf_path,configuration=config)
        if not keep_html_file:
            os.remove(temp_file_path)