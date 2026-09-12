from fasthtml.common import * 

def ToolPage(
        title, 
        description, 
        *content
    ): 

    return Section(

        H2(
            title,
            cls= "text-2xl font-bold mb-2"
            ), 

        P(
            description,
            cls="text-gray-600 mb-6"
            ),

        *content,

        cls="max-w-4xl mx-auto px-4 py-8"
    )