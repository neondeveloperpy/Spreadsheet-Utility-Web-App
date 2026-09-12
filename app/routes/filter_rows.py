from urllib import request

from app.components.file_info import FileInfo
from app.components.layout import Layout
from app.components.tookworkspcae import ToolWorkSpace
from app.components.tool_controls import ToolControls
from app.components.tool_page import ToolPage
from app.components.shared import UploadBox
from app.components.shared import PrimaryButton
from app.components.layout import DataTable
from app.routes.rename_columns import DownloadControls
from app.routes.sort_rows import DownloadControls
from app.services.file_output import save_dataframe
from app.services.file_processor import load_dataframe
from app.dataframes.transformers import filter_rows_func
from fasthtml.common import *

from app.services.file_processor import load_dataframe, save_uploaded_file

from app.services.file_processor import save_uploaded_file

def register_routes(rt):

    @rt("/filter-rows")
    def filter_rows():

        return Layout(
        
                ToolPage(
                        "Filter Rows",
                        "Filter Rows in CSV Files & EXCEL Workbooks",

                        Div(
                        UploadBox(
                            PrimaryButton("Convert"),
                            accept=".csv,.xlsx",
                            action="/filter-rows",   
                            method="post",
                            hx_post="/filter-rows",
                            hx_target="#tool-workspace",
                            hx_swap="innerHTML"
                        ),
                        id="tool-workspace"
                        )
                    )
                )

    def FilterRowsControls(
    df,
    temp_path,
    original_filename
        ):

        column_options = [
        Option(
            str(column),
            value=str(index)
        )
        for index, column in enumerate(df.columns)
        ]

        operator_options = [
        Option("Equals", value="equals"),
        Option("Not equals", value="not_equals"),
        Option("Contains", value="contains"),
        Option("Does not contain", value="not_contains"),
        Option("Starts with", value="starts_with"),
        Option("Ends with", value="ends_with"),
        Option("Greater than", value="greater_than"),
        Option("Less than", value="less_than"),
        Option(
            "Greater than or equal",
            value="greater_or_equal"
        ),
        Option(
            "Less than or equal",
            value="less_or_equal"
        ),
        Option("Is empty", value="is_empty"),
        Option("Is not empty", value="is_not_empty")
        ]

        return ToolControls(
        Div(
            H3(
                "Filter Rows",
                cls="text-lg font-semibold text-gray-900"
            ),

            P(
                "Filter your spreadsheet using a condition.",
                cls="text-sm text-gray-500 mt-1"
            )
        ),

        Form(
            Div(
                Div(
                    Label(
                        "Column",
                        cls="text-sm font-medium text-gray-700"
                    ),

                    Select(
                        *column_options,
                        name="column",
                        cls="w-full!"
                    ),

                    cls="space-y-2"
                ),

                Div(
                    Label(
                        "Condition",
                        cls="text-sm font-medium text-gray-700"
                    ),

                    Select(
                        *operator_options,
                        name="operator",
                        cls="w-full!"
                    ),

                    cls="space-y-2"
                ),

                Div(
                    Label(
                        "Value",
                        cls="text-sm font-medium text-gray-700"
                    ),

                    Input(
                        type="text",
                        name="value",
                        placeholder="Enter a value...",
                        cls="w-full!"
                    ),

                    cls="space-y-2"
                ),

                cls="grid grid-cols-1 md:grid-cols-3 gap-4"
            ),

            Input(
                type="hidden",
                name="temp_file",
                value=str(temp_path)
            ),

            Input(
                type="hidden",
                name="original_filename",
                value=original_filename
            ),

            Div(
                PrimaryButton("Apply Filter"),
                cls="pt-2"
            ),

            method="post",
            action="/filter-rows/apply",

            hx_post="/filter-rows/apply",
            hx_target="#tool-workspace",
            hx_swap="innerHTML"
        )
    )

    @rt("/filter-rows", methods=["POST"])
    async def filter_rows_post(request):

        form = await request.form()

        file = form["file"]

        if not file:
            return "No file uploaded"

        temp_path = await save_uploaded_file(file)

        df = load_dataframe(temp_path)

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        return ToolWorkSpace(

        FileInfo(
            file.filename,
            rows=len(df),
            columns=len(df.columns),
            size=f"{size / 1024:.1f} KB"
        ),

        Div(
            H3(
                "Preview",
                cls="text-lg font-semibold text-gray-900 mb-3"
            ),

            DataTable(df),

            cls=(
                "bg-white border border-gray-200 "
                "rounded-xl! p-5 shadow-sm!"
            )
        ),

        FilterRowsControls(
            df,
            temp_path,
            file.filename
        )
    )

    @rt("/filter-rows/apply", methods=["POST"])
    async def filter_rows_apply(request):

        form = await request.form()

        temp_file = form["temp_file"]
        original_filename = form["original_filename"]

        column_index = form.get("column")
        operator = form.get("operator")
        value = form.get("value")

    # -------------------------
    # Basic validation
    # -------------------------

        if column_index is None:
            return "Please select a column."

        if operator is None:
            return "Please select a condition."

        try:
            column_index = int(column_index)
        except ValueError:
            return "Invalid column."

        df = load_dataframe(Path(temp_file))

        columns = list(df.columns)

        if column_index < 0 or column_index >= len(columns):
            return "Invalid column."

        column = columns[column_index]

        valid_operators = {
            "equals",
        "not_equals",
        "contains",
        "not_contains",
        "starts_with",
        "ends_with",
        "greater_than",
        "less_than",
        "greater_or_equal",
        "less_or_equal",
        "is_empty",
        "is_not_empty"
        }

        if operator not in valid_operators:
            return "Invalid filter condition."

    # -------------------------
    # Value validation
    # -------------------------

        operators_without_value = {
        "is_empty",
        "is_not_empty"
        }

        if operator not in operators_without_value:

            if value is None or not value.strip():
                return "Please enter a value."

            value = value.strip()

    # -------------------------
    # Apply filter
    # -------------------------

        try:

            df = filter_rows_func(
            df,
            column,
            operator,
            value
            )

        except ValueError as exc:
            return str(exc)

    # -------------------------
    # Save result
    # -------------------------

        output_path = save_dataframe(
        df,
        original_filename,
        output_format=Path(temp_file).suffix[1:],
        operation="filtered"
    )

    # -------------------------
    # Return updated workspace
    # -------------------------

        return ToolWorkSpace(

        FileInfo(
            original_filename,
            rows=len(df),
            columns=len(df.columns),
            size=f"{output_path.stat().st_size / 1024:.1f} KB"
        ),

        Div(
            H3(
                "Preview",
                cls="text-lg font-semibold text-gray-900 mb-3"
            ),

            DataTable(df),

            cls=(
                "bg-white border border-gray-200 "
                "rounded-xl! p-5 shadow-sm!"
            )
        ),

        FilterRowsControls(
            df,
            output_path,
            original_filename
        ),

        DownloadControls(
            output_path
        )
    )