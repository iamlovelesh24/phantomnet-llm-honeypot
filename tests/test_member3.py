import unittest
from pathlib import Path
import tempfile

from database.sql_engine import (
    execute_sql,
    validate_sql,
    build_llm_request,
    list_schemas,
)

from context.vector_store import ContextStore


class TestSQL(unittest.TestCase):

    def test_schema_count(self):

        self.assertEqual(
            len(list_schemas()),
            5,
        )

    def test_select_all(self):

        result = execute_sql(
            "SELECT * FROM employees"
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["row_count"],
            3,
        )

        self.assertTrue(
            result["synthetic"]
        )

    def test_select_columns(self):

        result = execute_sql(
            "SELECT employee_id, name FROM employees"
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            set(result["columns"]),
            {
                "employee_id",
                "name",
            },
        )

    def test_where(self):

        result = execute_sql(
            "SELECT name FROM employees "
            "WHERE employee_id = 1001"
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["row_count"],
            1,
        )

        self.assertEqual(
            result["rows"][0]["name"],
            "Aarav Mehta",
        )

    def test_unknown_table(self):

        result = execute_sql(
            "SELECT * FROM secret_database"
        )

        self.assertFalse(
            result["success"]
        )

    def test_unknown_column(self):

        result = execute_sql(
            "SELECT password FROM employees"
        )

        self.assertFalse(
            result["success"]
        )

    def test_destructive_sql_blocked(self):

        queries = [
            "DROP TABLE employees",
            "DELETE FROM employees",
            "UPDATE employees SET salary = 1",
            "INSERT INTO employees VALUES (1)",
            "ALTER TABLE employees ADD x TEXT",
        ]

        for query in queries:

            result = validate_sql(query)

            self.assertFalse(
                result["success"]
            )

    def test_llm_request(self):

        result = build_llm_request(
            "SELECT name FROM employees"
        )

        self.assertTrue(
            result["accepted"]
        )

        self.assertTrue(
            result["constraints"]["synthetic_only"]
        )

        self.assertTrue(
            result["constraints"]["read_only"]
        )


class TestContext(unittest.TestCase):

    def test_ten_minute_context(self):

        with tempfile.TemporaryDirectory() as temp:

            store = ContextStore(
                Path(temp) / "context.db",
                ttl_seconds=600,
            )

            store.add_fact(
                "session-1",
                "Employee 1001 belongs to Engineering",
            )

            results = store.retrieve(
                "session-1",
                "Engineering",
            )

            self.assertEqual(
                len(results),
                1,
            )

            self.assertIn(
                "Engineering",
                results[0]["fact"],
            )

    def test_session_isolation(self):

        with tempfile.TemporaryDirectory() as temp:

            store = ContextStore(
                Path(temp) / "context.db",
                ttl_seconds=600,
            )

            store.add_fact(
                "session-1",
                "Only session one can retrieve this",
            )

            results = store.retrieve(
                "session-2",
                "session",
            )

            self.assertEqual(
                results,
                [],
            )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
