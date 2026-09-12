import pandas as pd 
from pandas.api.types import (
    is_numeric_dtype,
    is_datetime64_any_dtype
)

def rename_columns_func(df, mapping):

    return df.rename(columns=mapping)


def trim_whitespace_func(df):

    return df.map(
        lambda x: x.strip()
        if isinstance(x, str)
        else x
    )

def sort_rows_func(df, columns, ascending=True):
    return df.sort_values(
        by=columns, 
        ascending=ascending,
        kind="stable"
    )


def filter_rows_func(df, column, operator, value=None):

    series = df[column]

    # Empty / non-empty
    if operator == "is_empty":
        return df[
            series.isna()
            | series.astype("string").str.strip().eq("")
        ]

    if operator == "is_not_empty":
        return df[
            series.notna()
            & series.astype("string").str.strip().ne("")
        ]

    # Text operations
    if operator in {
        "contains",
        "not_contains",
        "starts_with",
        "ends_with"
    }:

        text = series.astype("string")

        if operator == "contains":
            mask = text.str.contains(
                str(value),
                case=False,
                na=False
            )

        elif operator == "not_contains":
            mask = ~text.str.contains(
                str(value),
                case=False,
                na=False
            )

        elif operator == "starts_with":
            mask = text.str.startswith(
                str(value),
                na=False
            )

        else:
            mask = text.str.endswith(
                str(value),
                na=False
            )

        return df[mask]

    # Numeric/date/equality comparisons
    if operator in {
        "equals",
        "not_equals",
        "greater_than",
        "less_than",
        "greater_or_equal",
        "less_or_equal"
    }:

        if is_numeric_dtype(series):

            try:
                comparison_value = pd.to_numeric(value)
            except (TypeError, ValueError):
                raise ValueError(
                    "Please enter a valid number."
                )

        elif is_datetime64_any_dtype(series):

            try:
                comparison_value = pd.to_datetime(value)
            except (TypeError, ValueError):
                raise ValueError(
                    "Please enter a valid date."
                )

        else:
            comparison_value = str(value)

        if operator == "equals":
            mask = series == comparison_value

        elif operator == "not_equals":
            mask = series != comparison_value

        elif operator == "greater_than":
            mask = series > comparison_value

        elif operator == "less_than":
            mask = series < comparison_value

        elif operator == "greater_or_equal":
            mask = series >= comparison_value

        else:
            mask = series <= comparison_value

        return df[mask]

    raise ValueError("Unsupported filter condition.")