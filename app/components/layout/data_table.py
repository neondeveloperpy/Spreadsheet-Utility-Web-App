from fasthtml.common import * 

def DataTable(df, max_rows=20):

    rows = []

    # Headers

    headers = Tr(
        *[
            Th(
                str(column),
                cls="px-4 py-2 text-left font-semibold"
            )
            for column in df.columns
        ]
    )

    # Data

    for _, row in df.head(max_rows).iterrows():

        rows.append(
            Tr(
                *[
                    Td(
                        str(value),
                        cls="px-4 py-2 border-t"
                    )
                    for value in row
                ]
            )
        )

    return Div(
        Table(
            Thead(headers),
            Tbody(*rows),
            cls="w-full text-sm"
        ),
        cls="overflow-x-auto border rounded-lg"
    )