# Starts the App
from fasthtml.common import *

from app.routes import (
    home,
    about,
    contact,
    privacy,
    not_found,
    csv_to_excel,
    excel_to_csv,
    remove_duplicates,
    remove_empty_rows,
    remove_empty_columns,
    rename_columns,
    filter_rows,
    sort_rows,
    trim_whitespace,
)

ROUTES = [
        home,
        about,
        contact,
        privacy,
        not_found,
        csv_to_excel,
        excel_to_csv,
        remove_duplicates,
        remove_empty_rows,
        remove_empty_columns,
        rename_columns,
        filter_rows,
        sort_rows,
        trim_whitespace,
]

app, rt = fast_app(
     hdrs=(
        Script(src="https://cdn.tailwindcss.com"),
    )
)

for route in ROUTES:
    route.register_routes(rt)


if __name__ == '__main__':
    serve()

