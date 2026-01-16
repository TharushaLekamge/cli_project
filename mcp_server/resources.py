from mcp.server import FastMCP


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


def list_documents_impl():
    """Implementation of list_documents resource."""
    return list(docs.keys())


def get_document_impl(doc_id: str):
    """Implementation of get_document resource."""
    if doc_id not in docs:
        raise ValueError(f"The document {doc_id} does not exist.")
    return docs[doc_id]


def register_resources(mcp: FastMCP):
    """Register all resources with the MCP server."""

    @mcp.resource(
        "docs:://documents",
        description="Return a list of all document IDs available in the system.",
        mime_type="application/json",
    )
    def list_documents():
        return list_documents_impl()

    @mcp.resource(
        "docs:://documents/{doc_id}",
        description="Return the contents of a particular document given its ID.",
        mime_type="text/plain",
    )
    def get_document(doc_id: str):
        return get_document_impl(doc_id)

