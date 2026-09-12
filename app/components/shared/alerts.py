from fasthtml.common import * 

def SuccessAlert(message):

    return Div(
        message,

        cls="!rounded-lg bg-green-100 text-green-800 p-4"
    )

def ErrorAlert(message):

    return Div(
        message,

        cls="!rounded-lg bg-red-100 text-red-800 p-4"
    )
