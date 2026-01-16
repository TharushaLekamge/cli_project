from mcp.server import FastMCP
from pydantic import Field

from mcp_server.resources import docs


def read_doc_contents_impl(doc_name: str):
    """Implementation of read_doc_contents tool."""
    if doc_name not in docs:
        raise ValueError(f"The document {doc_name} does not exist.")
    return docs[doc_name]


def edit_doc_contents_impl(doc_name: str, old_contents: str, new_contents: str):
    """Implementation of edit_doc_contents tool."""
    if doc_name not in docs:
        raise ValueError(f"The document {doc_name} does not exist.")

    updated_contents = docs[doc_name].replace(old_contents, new_contents)
    docs[doc_name] = updated_contents
    return updated_contents


def register_tools(mcp: FastMCP):
    """Register all tools with the MCP server."""

    @mcp.tool(
        name="read_doc_contents",
        description="Read the contents of a document given its name. Return the contents as text.",
    )
    def read_doc_contents(
            doc_name: str = Field(..., description="The name of the document to read."),
    ):
        return read_doc_contents_impl(doc_name)

    @mcp.tool(
        name="edit_doc_contents",
        description="Edit the contents of a document given its name and new contents using find and replace. Return the updated contents as text.",
    )
    def edit_doc_contents(
            doc_name: str = Field(..., description="The name of the document to edit."),
            old_contents: str = Field(..., description="The old contents of the document."),
            new_contents: str = Field(..., description="The new contents of the document."),
    ):
        return edit_doc_contents_impl(doc_name, old_contents, new_contents)


