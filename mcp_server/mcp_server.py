from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document given its name. Return the contents as text.",
)
def read_doc_contents(
        doc_name: str = Field(..., description="The name of the document to read."),
):
    if doc_name not in docs:
        raise ValueError(f"The document {doc_name} does not exist.")

    return docs[doc_name]


@mcp.tool(
    name="edit_doc_contents",
    description="Edit the contents of a document given its name and new contents using find and replace. Return the updated contents as text.",
)
def edit_doc_contents(
        doc_name: str = Field(..., description="The name of the document to edit."),
        old_contents: str = Field(..., description="The old contents of the document."),
        new_contents: str = Field(..., description="The new contents of the document."),
):
    if doc_name not in docs:
        raise ValueError(f"The document {doc_name} does not exist.")

    updated_contents = docs[doc_name].replace(old_contents, new_contents)
    docs[doc_name] = updated_contents
    return updated_contents


@mcp.resource(
    "docs:://documents",
    description="Return a list of all document IDs available in the system.",
    mime_type="application/json",
)
def list_documents():
    return list(docs.keys())


@mcp.resource(
    "docs:://documents/{doc_id}",
    description="Return the contents of a particular document given its ID.",
    mime_type="text/plain",
)
def get_document(doc_id: str):
    if doc_id not in docs:
        raise ValueError(f"The document {doc_id} does not exist.")

    return docs[doc_id]


from .prompts import register_prompts
register_prompts(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")
