from fasthtml.common import * 

def Navbar(): 

    return Nav(

        Div(

            A(
                "TabulaFlow", 

                href="/", 

                cls="!text-2xl font-bold"
            ),

            Div(

                A("Tools", href="/"),
                A("About", href="/about"),
                A("Contact", href="/contact"),
                A("Privacy", href="/privacy"),
                A("Donate", href=""),
                A("Github", href=""),

                cls="!flex gap-6 ml-12"
            ),

            cls="!flex justify-between items-center max-w-6xl mx-auto py-5"

        ),

        cls="!border-b"

        )
