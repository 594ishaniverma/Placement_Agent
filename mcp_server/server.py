import argparse
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    FastMCP = None

from .tools import get_student_count, list_schema, query_eligible_students

if FastMCP is not None:
    mcp = FastMCP("placement-students")

    @mcp.tool()
    def mcp_list_schema() -> list[dict[str, Any]]:
        return list_schema()

    @mcp.tool()
    def mcp_query_eligible_students(filters: dict[str, Any], limit: int = 100) -> list[dict[str, Any]]:
        return query_eligible_students(filters, limit)

    @mcp.tool()
    def mcp_get_student_count() -> int:
        return get_student_count()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=("stdio", "sse"), default="stdio")
    args = parser.parse_args()
    if FastMCP is None:
        raise SystemExit("Install the MCP dependency to run the server.")
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
