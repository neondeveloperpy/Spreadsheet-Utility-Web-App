from fasthtml.common import * 
#from app.components.layout import Section

def Hero():

    return Section(

        Div(

        H1("Convert & Clean Your Spreadsheets Instantly",
           cls="!text-4xl md:text-6xl font-bold text-left"
           ),

        P(
            "TabulaFlow helps you transform CSV and Excel files with simple online tools.",
            cls="!mt-4 text-lg text-gray-100 text-left max-w-2xl"
            ),

        P("No login/Sign-up required!",
          cls="!mt-2 text-sm text-gray-100 text-left max-w-2xl"),

        ),


        Div(

            A(
                "Start Cleaning Files", 
                href="/", 
                cls="mt-6 inline-block !bg-blue-800 !text-white px-4 py-2 rounded-md"
            ),
            cls="flex justify-center"

        ),

        cls="flex flex-col items-center justify-center py-20 px-4"

    )