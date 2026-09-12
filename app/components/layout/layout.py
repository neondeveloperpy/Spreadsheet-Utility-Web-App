from fasthtml.common import *

from app.components.layout.navbar import Navbar
from app.components.layout.footer import SiteFooter


def Layout(*content, title="TabulaFlow"):

    return Titled(

        title,

        Navbar(),

        Main(

            *content,

            cls="!max-w-6xl mx-auto px-6 py-10"

        ),

        SiteFooter()

    )