from fasthtml.common import *

def ToolControls(*content):
    return Div(
        Div(
        *content,
        cls="w-full flex items-center justify-between gap-6"
        
        ),
        cls=(
            "bg-white border border-gray-200 rounded-xl px-5 py-4 shadow-sm!"
                    )
    )