#!/usr/bin/env python3
"""
Pydantic AI Agent with Custom MCP Tools for Legal Assistant
"""

import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from mcp import Tool
import json

# Since we can't install pydantic-ai right now, I'll create a minimal implementation
# that demonstrates the concept

class LegalQuery(BaseModel):
    """Model for legal query inputs"""
    user_input: str = Field(..., description="User's legal issue description")
    query_type: str = Field(default="general", description="Type of legal query")

class LegalResponse(BaseModel):
    """Model for legal response outputs"""
    case_summary: str = Field(..., description="Summary of the legal case")
    ipc_sections: List[Dict[str, Any]] = Field(default_factory=list, description="Relevant IPC sections")
    legal_precedents: List[Dict[str, Any]] = Field(default_factory=list, description="Relevant legal precedents")
    draft_document: str = Field(default="", description="Draft legal document")
    
class MCPLegalTool:
    """Custom MCP Tool for Legal Assistant"""
    
    def __init__(self, name: str, description: str, handler_func):
        self.name = name
        self.description = description
        self.handler_func = handler_func
    
    async def call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call the tool with given parameters"""
        return await self.handler_func(params)

class PydanticAILegalAgent:
    """Main Pydantic AI Agent for Legal Assistant"""
    
    def __init__(self):
        self.tools: Dict[str, MCPLegalTool] = {}
        self._register_tools()
    
    def _register_tools(self):
        """Register all MCP tools"""
        # IPC Section Search Tool
        self.tools["ipc_search"] = MCPLegalTool(
            name="ipc_search",
            description="Search for relevant IPC sections based on legal query",
            handler_func=self._ipc_search_handler
        )
        
        # Legal Precedent Search Tool
        self.tools["precedent_search"] = MCPLegalTool(
            name="precedent_search", 
            description="Search for relevant legal precedents",
            handler_func=self._precedent_search_handler
        )
        
        # Case Analysis Tool
        self.tools["case_analysis"] = MCPLegalTool(
            name="case_analysis",
            description="Analyze and summarize legal case",
            handler_func=self._case_analysis_handler
        )
        
        # Document Drafting Tool
        self.tools["document_drafting"] = MCPLegalTool(
            name="document_drafting",
            description="Draft legal documents",
            handler_func=self._document_drafting_handler
        )
    
    async def _ipc_search_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for IPC section search"""
        query = params.get("query", "")
        
        # Import the existing tool
        from tools.ipc_sections_search_tool import search_ipc_sections
        
        try:
            results = search_ipc_sections.func(query)
            return {
                "status": "success",
                "data": results,
                "tool_name": "ipc_search"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool_name": "ipc_search"
            }
    
    async def _precedent_search_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for legal precedent search"""
        query = params.get("query", "")
        
        # Import the existing tool
        from tools.legal_precedent_search_tool import search_legal_precedents
        
        try:
            results = search_legal_precedents.func(query)
            return {
                "status": "success",
                "data": results,
                "tool_name": "precedent_search"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool_name": "precedent_search"
            }
    
    async def _case_analysis_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for case analysis"""
        user_input = params.get("user_input", "")
        
        # Create a basic case summary
        case_summary = f"""
        LEGAL CASE ANALYSIS
        
        User Issue: {user_input}
        
        Case Type: General Legal Issue
        Priority: Medium
        
        Analysis: This case requires detailed examination of applicable laws and precedents.
        """
        
        return {
            "status": "success",
            "data": {
                "case_summary": case_summary.strip(),
                "analysis_type": "basic",
                "confidence": 0.8
            },
            "tool_name": "case_analysis"
        }
    
    async def _document_drafting_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for document drafting"""
        case_summary = params.get("case_summary", "")
        ipc_sections = params.get("ipc_sections", [])
        precedents = params.get("precedents", [])
        
        # Create basic legal document
        document = f"""
        LEGAL NOTICE
        
        Date: [To be filled]
        
        To: [Recipient Name]
        From: [Your Name]
        
        Subject: Legal Notice regarding {case_summary[:100]}...
        
        Dear Sir/Madam,
        
        This serves as a formal legal notice regarding the matter described below:
        
        FACTUAL BACKGROUND:
        {case_summary}
        
        APPLICABLE LEGAL PROVISIONS:
        """
        
        # Add IPC sections
        for section in ipc_sections[:3]:  # Limit to 3 sections
            if isinstance(section, dict):
                document += f"\n- Section {section.get('section', 'N/A')}: {section.get('section_title', 'N/A')}"
        
        document += """
        
        LEGAL PRECEDENTS:
        """
        
        # Add precedents
        for precedent in precedents[:2]:  # Limit to 2 precedents
            if isinstance(precedent, dict):
                document += f"\n- {precedent.get('title', 'N/A')}"
        
        document += """
        
        DEMAND/REQUEST:
        We hereby demand that you take appropriate action to resolve this matter within 15 days of receipt of this notice.
        
        Yours truly,
        [Your Name]
        [Your Designation]
        """
        
        return {
            "status": "success",
            "data": {
                "document": document.strip(),
                "document_type": "legal_notice"
            },
            "tool_name": "document_drafting"
        }
    
    async def process_legal_query(self, query: LegalQuery) -> LegalResponse:
        """Process a legal query using MCP tools"""
        
        # Step 1: Analyze the case
        case_analysis = await self.tools["case_analysis"].call({
            "user_input": query.user_input
        })
        
        case_summary = case_analysis.get("data", {}).get("case_summary", "")
        
        # Step 2: Search for IPC sections
        ipc_results = await self.tools["ipc_search"].call({
            "query": query.user_input
        })
        
        ipc_sections = ipc_results.get("data", []) if ipc_results.get("status") == "success" else []
        
        # Step 3: Search for legal precedents
        precedent_results = await self.tools["precedent_search"].call({
            "query": query.user_input + " - precedent cases in India"
        })
        
        precedents = precedent_results.get("data", []) if precedent_results.get("status") == "success" else []
        
        # Step 4: Draft document
        document_results = await self.tools["document_drafting"].call({
            "case_summary": case_summary,
            "ipc_sections": ipc_sections,
            "precedents": precedents
        })
        
        draft_document = document_results.get("data", {}).get("document", "") if document_results.get("status") == "success" else ""
        
        # Create response
        response = LegalResponse(
            case_summary=case_summary,
            ipc_sections=ipc_sections,
            legal_precedents=precedents,
            draft_document=draft_document
        )
        
        return response
    
    def get_tool_schemas(self) -> Dict[str, Any]:
        """Get MCP tool schemas"""
        schemas = {}
        for tool_name, tool in self.tools.items():
            schemas[tool_name] = {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query or input for the tool"
                        }
                    },
                    "required": ["query"]
                }
            }
        return schemas

# Example usage
async def main():
    """Example usage of the Pydantic AI Agent"""
    agent = PydanticAILegalAgent()
    
    # Create a legal query
    query = LegalQuery(
        user_input="A man broke into my house at night while my family was sleeping. He stole jewelry and cash from our bedroom. When I confronted him, he threatened me with a knife and ran away.",
        query_type="criminal"
    )
    
    # Process the query
    response = await agent.process_legal_query(query)
    
    print("=== PYDANTIC AI LEGAL ASSISTANT RESPONSE ===")
    print(f"Case Summary: {response.case_summary}")
    print(f"\nIPC Sections Found: {len(response.ipc_sections)}")
    print(f"Legal Precedents Found: {len(response.legal_precedents)}")
    print(f"\nDraft Document:\n{response.draft_document}")

if __name__ == "__main__":
    asyncio.run(main())