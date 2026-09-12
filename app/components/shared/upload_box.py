from fasthtml.common import *

def UploadBox(
    *children,
    accept=".csv,.xlsx",
    action="#",
    method="post",
    **attrs
):

    return Form(

        Input(
            type="file",
            name="file",
            accept=accept 
        ),

        *children,

        method=method,
        action=action,
        enctype="multipart/form-data",
        **attrs

    )