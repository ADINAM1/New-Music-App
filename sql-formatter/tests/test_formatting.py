from formatting import format_sql


def test_uppercase_keywords():
    sql = "select a from t"
    formatted = format_sql(sql, keyword_case="upper")
    assert "SELECT" in formatted
    assert "FROM" in formatted


def test_lowercase_keywords():
    sql = "SELECT A FROM T"
    formatted = format_sql(sql, keyword_case="lower")
    assert "select" in formatted
    assert "from" in formatted


def test_default_case_preserved_with_indent():
    sql = "SELECT a\nFROM t"
    formatted = format_sql(sql, keyword_case="default")
    assert "SELECT" in formatted and "FROM" in formatted
    # ensure reindent added newline before FROM
    assert formatted.strip().splitlines()[1].startswith("FROM")
