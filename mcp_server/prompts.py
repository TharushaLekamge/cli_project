from mcp.server import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field


def format_document_prompt(
        doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""

    return [
        base.UserMessage(prompt)
    ]


def summarize_document_prompt(
        doc_id: str = Field(description="Id of the document to summarize")
) -> list[base.Message]:
    prompt = f"""
Your goal is to summarize the contents of a document.
The id of the document you need to summarize is:
<document_id>
{doc_id}
</document_id>
"""
    return [
        base.UserMessage(prompt)
    ]


# New: centralize prompt registrations here

def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="format",
        description="Rewrites the contents of the document in Markdown format."
    )
    def format_document(
            doc_id: str = Field(description="Id of the document to format")
    ):
        return format_document_prompt(doc_id)

    @mcp.prompt(
        name="summarize",
        description="Summarizes the contents of a document."
    )
    def summarize_document(
            doc_id: str = Field(description="Id of the document to summarize")
    ):
        return summarize_document_prompt(doc_id)
