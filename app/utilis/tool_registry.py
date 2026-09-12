TOOLS = [

    # =========================
    # Conversion Tools
    # =========================

    {
        "slug": "csv-to-excel",
        "title": "CSV → Excel",
        "description": "Convert Your CSV files into Excel workbooks.",
        "icon": "📄",
        "accept": ".csv",
        "button": "Convert",
        "category": "Conversion"
    },

    {
        "slug": "excel-to-csv",
        "title": "Excel → CSV",
        "description": "Convert Your Excel workbooks into CSV files.",
        "icon": "📊",
        "accept": ".xlsx,.xls",
        "button": "Convert",
        "category": "Conversion"
    },

    # =========================
    # Cleaning Tools
    # =========================

    {
        "slug": "remove-duplicates",
        "title": "Remove Duplicate Rows",
        "description": "Remove duplicate rows from your spreadsheet.",
        "icon": "🧹",
        "accept": ".csv,.xlsx,.xls",
        "button": "Remove Duplicates",
        "category": "Cleaning"
    },

    {
        "slug": "remove-empty-rows",
        "title": "Remove Empty Rows",
        "description": "Delete empty rows from your spreadsheet.",
        "icon": "📑",
        "accept": ".csv,.xlsx,.xls",
        "button": "Remove Empty Rows",
        "category": "Cleaning"
    },

    {
        "slug": "remove-empty-columns",
        "title": "Remove Empty Columns",
        "description": "Delete empty columns from your spreadsheet.",
        "icon": "🗂️",
        "accept": ".csv,.xlsx,.xls",
        "button": "Remove Empty Columns",
        "category": "Cleaning"
    },

    # =========================
    # Future Tools
    # =========================

    {
        "slug": "trim-whitespace",
        "title": "Trim Whitespace",
        "description": "Remove leading and trailing spaces from text.",
        "icon": "✂️",
        "accept": ".csv,.xlsx,.xls",
        "button": "Trim Whitespace",
        "category": "Cleaning"
    },

    {
        "slug": "rename-columns",
        "title": "Rename Columns",
        "description": "Rename one or more spreadsheet columns.",
        "icon": "🏷️",
        "accept": ".csv,.xlsx,.xls",
        "button": "Rename Columns",
        "category": "Editing"
    },

    {
        "slug": "sort-rows",
        "title": "Sort Rows",
        "description": "Sort spreadsheet rows by one or more columns.",
        "icon": "↕️",
        "accept": ".csv,.xlsx,.xls",
        "button": "Sort Rows",
        "category": "Organization"
    },

    {
        "slug": "filter-rows",
        "title": "Filter Rows",
        "description": "Filter spreadsheet rows using custom rules.",
        "icon": "🔍",
        "accept": ".csv,.xlsx,.xls",
        "button": "Filter Rows",
        "category": "Organization"
    },

]

# Helper Tools

def get_tool(slug: str):
    """Return a single tool dictionary by its slug."""

    for tool in TOOLS:
        if tool["slug"] == slug:
            return tool

    return None


def get_tools_by_category(category: str):
    """Return all tools in a category."""

    return [
        tool
        for tool in TOOLS
        if tool["category"] == category
    ]