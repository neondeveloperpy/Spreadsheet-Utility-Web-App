from fasthtml.common import * 

def FileInfo(
    filename,
    rows,
    columns,
    size
):

    return Div(

        H3(filename,
        cls="text-lg font-semibold text-gray-900 truncate"),

        Div(

            Span(f"Rows: {rows}",
               cls="bg-gray-100 text-gray-700 text-sm px-3 py-1 rounded-full"),

            Span(f"Columns: {columns}",
               cls="bg-gray-100 text-gray-700 text-sm px-3 py-1 rounded-full"),

            Span(f"Size: {size}",
               cls="bg-gray-100 text-gray-700 text-sm px-3 py-1 rounded-full"),

            cls="flex flex-wrap gap-2 mt-3",
        ),

        cls=(
            "bg-white border border-gray-200 rounded-xl "
            "p-5 shadow-sm"
        )

    )