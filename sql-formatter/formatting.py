import sqlparse


def format_sql(text: str, keyword_case: str = "upper") -> str:
    """Format SQL text using sqlparse.

    Args:
        text: Raw SQL string.
        keyword_case: 'upper', 'lower', or 'default'.

    Returns:
        Formatted SQL string.
    """
    text = text or ""
    case = None if keyword_case == "default" else keyword_case
    return sqlparse.format(text, reindent=True, keyword_case=case)
