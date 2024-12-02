import sys 
from big_mart_sales.logging import logger

class BigMartSalesException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)  ### Initialize the base Exception
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()  ### Extract traceback info

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return ("Error occurred in Python script: [{0}] "
            "at line number [{1}] "
            "with error message: [{2}]").format(self.file_name, self.lineno, self.error_message)
    

