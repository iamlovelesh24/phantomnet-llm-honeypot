"""
PhantomNet synthetic SQL deception engine.

Defensive research/demo component.
Uses synthetic data only and never connects to a real database.
"""

import re
from typing import Any, Dict, List


SCHEMAS = {
    "employees": [
        "employee_id",
        "name",
        "department_id",
        "salary",
        "status",
    ],
    "payroll": [
        "employee_id",
        "month",
        "gross_salary",
        "bonus",
        "net_salary",
    ],
    "departments": [
        "department_id",
        "name",
        "location",
    ],
    "projects": [
        "project_id",
        "name",
        "department_id",
        "status",
    ],
    "tickets": [
        "ticket_id",
        "employee_id",
        "priority",
        "status",
        "created_date",
    ],
}


SYNTHETIC_DATA = {
    "employees": [
        {
            "employee_id": 1001,
            "name": "Aarav Mehta",
            "department_id": 10,
            "salary": 85000,
            "status": "active",
        },
        {
            "employee_id": 1002,
            "name": "Priya Shah",
            "department_id": 20,
            "salary": 92000,
            "status": "active",
        },
        {
            "employee_id": 1003,
            "name": "Rohan Verma",
            "department_id": 10,
            "salary": 78000,
            "status": "active",
        },
    ],

    "payroll": [
        {
            "employee_id": 1001,
            "month": "2026-10",
            "gross_salary": 85000,
            "bonus": 5000,
            "net_salary": 72000,
        },
        {
            "employee_id": 1002,
            "month": "2026-10",
            "gross_salary": 92000,
            "bonus": 7500,
            "net_salary": 79000,
        },
        {
            "employee_id": 1003,
            "month": "2026-10",
            "gross_salary": 78000,
            "bonus": 3000,
            "net_salary": 67000,
        },
    ],

    "departments": [
        {
            "department_id": 10,
            "name": "Engineering",
            "location": "Pune",
        },
        {
            "department_id": 20,
            "name": "Finance",
            "location": "Mumbai",
        },
        {
            "department_id": 30,
            "name": "Operations",
            "location": "Bengaluru",
        },
    ],

    "projects": [
        {
            "project_id": 501,
            "name": "Atlas",
            "department_id": 10,
            "status": "active",
        },
        {
            "project_id": 502,
            "name": "Nimbus",
            "department_id": 20,
            "status": "active",
        },
        {
            "project_id": 503,
            "name": "Orion",
            "department_id": 30,
            "status": "completed",
        },
    ],

    "tickets": [
        {
            "ticket_id": 7001,
            "employee_id": 1001,
            "priority": "high",
            "status": "open",
            "created_date": "2026-10-28",
        },
        {
            "ticket_id": 7002,
            "employee_id": 1002,
            "priority": "medium",
            "status": "closed",
            "created_date": "2026-10-27",
        },
        {
            "ticket_id": 7003,
            "employee_id": 1003,
            "priority": "low",
            "status": "open",
            "created_date": "2026-10-29",
        },
    ],
}


BLOCKED_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "grant",
    "revoke",
    "replace",
    "merge",
}


def _error(message: str, query: str = "") -> Dict[str, Any]:
    return {
        "success": False,
        "query": query,
        "error": message,
        "rows": [],
        "row_count": 0,
    }


def validate_sql(query: str) -> Dict[str, Any]:
    """Validate a supported read-only SQL statement."""

    if not isinstance(query, str) or not query.strip():
        return _error("Empty SQL query")

    normalized = query.strip().rstrip(";")
    lowered = normalized.lower()

    if not lowered.startswith("select "):
        return _error(
            "Only SELECT statements are allowed",
            normalized,
        )

    for keyword in BLOCKED_KEYWORDS:
        if re.search(
            rf"\b{re.escape(keyword)}\b",
            lowered,
        ):
            return _error(
                f"Blocked SQL operation: {keyword}",
                normalized,
            )

    pattern = (
        r"^select\s+(.+?)\s+from\s+"
        r"([a-zA-Z_][a-zA-Z0-9_]*)"
        r"(?:\s+where\s+(.+?))?$"
    )

    match = re.match(
        pattern,
        normalized,
        re.IGNORECASE,
    )

    if not match:
        return _error(
            "Unsupported SQL syntax",
            normalized,
        )

    columns_text, table, where_clause = match.groups()

    table = table.lower()

    if table not in SCHEMAS:
        return _error(
            f"Unknown table: {table}",
            normalized,
        )

    if columns_text.strip() == "*":
        columns = SCHEMAS[table][:]
    else:
        columns = [
            column.strip().lower()
            for column in columns_text.split(",")
        ]

        invalid = [
            column
            for column in columns
            if column not in SCHEMAS[table]
        ]

        if invalid:
            return _error(
                f"Unknown column: {invalid[0]}",
                normalized,
            )

    return {
        "success": True,
        "query": normalized,
        "table": table,
        "columns": columns,
        "where": where_clause,
    }


def _apply_where(
    rows: List[Dict[str, Any]],
    table: str,
    where_clause: str,
):
    if not where_clause:
        return rows, None

    match = re.match(
        r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*"
        r"['\"]?([^'\"]+)['\"]?$",
        where_clause.strip(),
        re.IGNORECASE,
    )

    if not match:
        return [], "Unsupported WHERE clause"

    field, value = match.groups()

    field = field.lower()

    if field not in SCHEMAS[table]:
        return [], f"Unknown column: {field}"

    filtered = [
        row
        for row in rows
        if str(row.get(field, "")).lower()
        == value.lower()
    ]

    return filtered, None


def execute_sql(query: str) -> Dict[str, Any]:
    """Execute a safe SELECT against synthetic data."""

    validation = validate_sql(query)

    if not validation["success"]:
        return validation

    table = validation["table"]
    columns = validation["columns"]

    rows = list(SYNTHETIC_DATA[table])

    rows, where_error = _apply_where(
        rows,
        table,
        validation.get("where"),
    )

    if where_error:
        return _error(
            where_error,
            validation["query"],
        )

    result_rows = [
        {
            column: row.get(column)
            for column in columns
        }
        for row in rows
    ]

    return {
        "success": True,
        "query": validation["query"],
        "table": table,
        "columns": columns,
        "row_count": len(result_rows),
        "rows": result_rows,
        "synthetic": True,
    }


def build_llm_request(query: str) -> Dict[str, Any]:
    """
    Convert a valid SQL request into a structured
    request for the deception/LLM layer.
    """

    validation = validate_sql(query)

    if not validation["success"]:
        return {
            "accepted": False,
            "error": validation["error"],
        }

    return {
        "accepted": True,
        "request_type": "synthetic_sql_generation",
        "table": validation["table"],
        "columns": validation["columns"],
        "where": validation.get("where"),
        "constraints": {
            "synthetic_only": True,
            "read_only": True,
            "no_real_database": True,
        },
    }


def list_schemas() -> Dict[str, List[str]]:
    """Return all supported synthetic schemas."""

    return {
        name: columns[:]
        for name, columns in SCHEMAS.items()
    }
