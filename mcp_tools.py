#!/usr/bin/env python3
"""
Custom MCP Tools for Legal Assistant
"""

import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import json
import os
from mcp import Tool
from datetime import datetime

class MCPToolResult(BaseModel):
    """Standard result format for MCP tools"""
    status: str = Field(..., description="Status of the operation: success or error")
    data: Optional[Any] = Field(default=None, description="Result data")
    error: Optional[str] = Field(default=None, description="Error message if status is error")
    tool_name: str = Field(..., description="Name of the tool that produced this result")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the result")

class LegalIPCSearchTool:
    """MCP Tool for searching IPC sections"""
    
    @staticmethod
    async def search_ipc_sections(query: str) -> MCPToolResult:
        """Search for IPC sections based on query"""
        try:
            # Import the existing tool
            from tools.ipc_sections_search_tool import search_ipc_sections
            
            results = search_ipc_sections.func(query)
            
            return MCPToolResult(
                status="success",
                data=results,
                tool_name="ipc_search"
            )
            
        except Exception as e:
            return MCPToolResult(
                status="error",
                error=str(e),
                tool_name="ipc_search"
            )

class LegalPrecedentSearchTool:
    """MCP Tool for searching legal precedents"""
    
    @staticmethod
    async def search_legal_precedents(query: str) -> MCPToolResult:
        """Search for legal precedents based on query"""
        try:
            # Import the existing tool
            from tools.legal_precedent_search_tool import search_legal_precedents
            
            results = search_legal_precedents.func(query)
            
            return MCPToolResult(
                status="success",
                data=results,
                tool_name="precedent_search"
            )
            
        except Exception as e:
            return MCPToolResult(
                status="error",
                error=str(e),
                tool_name="precedent_search"
            )

class LegalCaseAnalysisTool:
    """MCP Tool for analyzing legal cases"""
    
    @staticmethod
    async def analyze_case(user_input: str) -> MCPToolResult:
        """Analyze a legal case and provide structured summary"""
        try:
            # Basic case categorization
            case_type = "general"
            priority = "medium"
            
            # Simple keyword-based classification
            if any(word in user_input.lower() for word in ["theft", "steal", "robbery", "burglary"]):
                case_type = "property_crime"
                priority = "high"
            elif any(word in user_input.lower() for word in ["assault", "threat", "violence", "attack"]):
                case_type = "violent_crime"
                priority = "high"
            elif any(word in user_input.lower() for word in ["fraud", "cheating", "scam"]):
                case_type = "fraud"
                priority = "high"
            elif any(word in user_input.lower() for word in ["contract", "agreement", "breach"]):
                case_type = "contract_dispute"
                priority = "medium"
            elif any(word in user_input.lower() for word in ["property", "land", "ownership"]):
                case_type = "property_dispute"
                priority = "medium"
            
            # Create structured analysis
            analysis = {
                "case_summary": f"Legal Issue Analysis\n\nDescription: {user_input}\n\nCase Type: {case_type.replace('_', ' ').title()}\nPriority: {priority.title()}\n\nThis case requires examination of applicable laws and precedents.",
                "case_type": case_type,
                "priority": priority,
                "keywords": [word for word in user_input.lower().split() if len(word) > 3],
                "confidence": 0.8
            }
            
            return MCPToolResult(
                status="success",
                data=analysis,
                tool_name="case_analysis"
            )
            
        except Exception as e:
            return MCPToolResult(
                status="error",
                error=str(e),
                tool_name="case_analysis"
            )

class LegalDocumentDraftingTool:
    """MCP Tool for drafting legal documents"""
    
    @staticmethod
    async def draft_document(
        case_summary: str,
        ipc_sections: List[Dict[str, Any]] = None,
        precedents: List[Dict[str, Any]] = None,
        document_type: str = "legal_notice"
    ) -> MCPToolResult:
        """Draft a legal document based on case analysis"""
        try:
            if ipc_sections is None:
                ipc_sections = []
            if precedents is None:
                precedents = []
            
            current_date = datetime.now().strftime("%B %d, %Y")
            
            if document_type == "legal_notice":
                document = f"""LEGAL NOTICE

Date: {current_date}

To: [Recipient Name/Organization]
Address: [Recipient Address]

From: [Your Name]
Address: [Your Address]

Subject: Legal Notice - {case_summary.split('.')[0][:50]}...

Dear Sir/Madam,

This serves as a formal legal notice regarding the matter described below:

FACTUAL BACKGROUND:
{case_summary}

APPLICABLE LEGAL PROVISIONS:"""
                
                # Add IPC sections
                if ipc_sections:
                    for i, section in enumerate(ipc_sections[:3], 1):
                        if isinstance(section, dict):
                            document += f"\n{i}. Section {section.get('section', 'N/A')}: {section.get('section_title', 'N/A')}"
                            if section.get('content'):
                                document += f"\n   {section.get('content', '')[:200]}..."
                
                document += "\n\nLEGAL PRECEDENTS:"
                
                # Add precedents
                if precedents:
                    for i, precedent in enumerate(precedents[:2], 1):
                        if isinstance(precedent, dict):
                            document += f"\n{i}. {precedent.get('title', 'N/A')}"
                            if precedent.get('summary'):
                                document += f"\n   {precedent.get('summary', '')[:200]}..."
                
                document += f"""

DEMAND/REQUEST:
We hereby demand that you take appropriate action to resolve this matter within 15 days of receipt of this notice. Failure to comply may result in legal proceedings against you.

This notice is issued without prejudice to any other rights and remedies available to us in law.

Yours truly,

[Your Name]
[Your Designation]
[Contact Information]

Note: This is a computer-generated legal notice template. Please review and customize as needed before use."""
                
            elif document_type == "complaint":
                document = f"""COMPLAINT

Date: {current_date}

To: [Appropriate Authority]
Address: [Authority Address]

From: [Your Name]
Address: [Your Address]

Subject: Complaint regarding {case_summary.split('.')[0][:50]}...

Respected Sir/Madam,

I am writing to file a formal complaint regarding the following matter:

INCIDENT DETAILS:
{case_summary}

APPLICABLE LAWS:"""
                
                # Add IPC sections
                if ipc_sections:
                    for i, section in enumerate(ipc_sections[:3], 1):
                        if isinstance(section, dict):
                            document += f"\n{i}. IPC Section {section.get('section', 'N/A')}: {section.get('section_title', 'N/A')}"
                
                document += f"""

RELIEF SOUGHT:
I request your good office to take appropriate action in this matter and provide justice as per the law.

Yours faithfully,

[Your Name]
[Signature]
[Contact Information]"""
            
            else:
                document = f"""LEGAL DOCUMENT

Date: {current_date}

Subject: {case_summary.split('.')[0][:50]}...

{case_summary}

This document has been generated as a template. Please customize as needed."""
            
            return MCPToolResult(
                status="success",
                data={
                    "document": document.strip(),
                    "document_type": document_type,
                    "word_count": len(document.split()),
                    "generated_at": current_date
                },
                tool_name="document_drafting"
            )
            
        except Exception as e:
            return MCPToolResult(
                status="error",
                error=str(e),
                tool_name="document_drafting"
            )

class LegalAdviceTool:
    """MCP Tool for providing legal advice"""
    
    @staticmethod
    async def provide_advice(
        case_summary: str,
        case_type: str = "general"
    ) -> MCPToolResult:
        """Provide legal advice based on case analysis"""
        try:
            advice_templates = {
                "property_crime": """
LEGAL ADVICE FOR PROPERTY CRIME

1. IMMEDIATE STEPS:
   - File an FIR at the nearest police station immediately
   - Preserve all evidence (photographs, witness statements, etc.)
   - Prepare a detailed list of stolen/damaged items

2. LEGAL REMEDIES:
   - Criminal proceedings under relevant IPC sections
   - Civil suit for damages and compensation
   - Insurance claim if applicable

3. DOCUMENTATION NEEDED:
   - Police complaint receipt
   - Medical certificates (if injured)
   - Proof of ownership of stolen items
   - Witness statements

4. PRECAUTIONS:
   - Do not tamper with evidence
   - Cooperate fully with police investigation
   - Maintain all communication records
""",
                "violent_crime": """
LEGAL ADVICE FOR VIOLENT CRIME

1. IMMEDIATE STEPS:
   - Seek immediate medical attention if injured
   - Report to police without delay
   - Document all injuries with photographs

2. LEGAL REMEDIES:
   - Criminal case under IPC sections for assault/threats
   - Application for anticipatory bail if required
   - Compensation claim under victim compensation scheme

3. DOCUMENTATION NEEDED:
   - Medical reports and certificates
   - Police complaint and FIR copy
   - Witness statements
   - Photographs of injuries

4. PRECAUTIONS:
   - Preserve all evidence
   - Do not meet accused without legal counsel
   - Keep records of all medical expenses
""",
                "contract_dispute": """
LEGAL ADVICE FOR CONTRACT DISPUTE

1. IMMEDIATE STEPS:
   - Review contract terms and conditions
   - Send legal notice to defaulting party
   - Gather all relevant documents

2. LEGAL REMEDIES:
   - Civil suit for specific performance
   - Claim for damages and compensation
   - Arbitration if clause exists in contract

3. DOCUMENTATION NEEDED:
   - Original contract/agreement
   - Correspondence between parties
   - Proof of performance from your side
   - Evidence of breach by other party

4. PRECAUTIONS:
   - Preserve all written communications
   - Do not waive your rights inadvertently
   - Consider alternative dispute resolution
""",
                "general": """
GENERAL LEGAL ADVICE

1. IMMEDIATE STEPS:
   - Document the incident thoroughly
   - Consult with a qualified lawyer
   - Gather all relevant evidence

2. LEGAL REMEDIES:
   - Appropriate legal action based on facts
   - Seek compensation if applicable
   - Follow proper legal procedures

3. DOCUMENTATION NEEDED:
   - All relevant documents and evidence
   - Witness statements if any
   - Proof of damages/losses

4. PRECAUTIONS:
   - Act within limitation periods
   - Preserve all evidence
   - Do not delay legal action
"""
            }
            
            advice = advice_templates.get(case_type, advice_templates["general"])
            
            return MCPToolResult(
                status="success",
                data={
                    "advice": advice.strip(),
                    "case_type": case_type,
                    "disclaimer": "This is general legal advice. Please consult with a qualified lawyer for specific legal guidance."
                },
                tool_name="legal_advice"
            )
            
        except Exception as e:
            return MCPToolResult(
                status="error",
                error=str(e),
                tool_name="legal_advice"
            )

# MCP Tool Registry
class MCPToolRegistry:
    """Registry for all MCP tools"""
    
    def __init__(self):
        self.tools = {
            "ipc_search": LegalIPCSearchTool.search_ipc_sections,
            "precedent_search": LegalPrecedentSearchTool.search_legal_precedents,
            "case_analysis": LegalCaseAnalysisTool.analyze_case,
            "document_drafting": LegalDocumentDraftingTool.draft_document,
            "legal_advice": LegalAdviceTool.provide_advice
        }
    
    def get_tool(self, tool_name: str):
        """Get a tool by name"""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """List all available tools"""
        return list(self.tools.keys())
    
    def get_tool_schemas(self) -> Dict[str, Any]:
        """Get schemas for all tools"""
        return {
            "ipc_search": {
                "name": "ipc_search",
                "description": "Search for relevant IPC sections based on legal query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Legal query or case description"}
                    },
                    "required": ["query"]
                }
            },
            "precedent_search": {
                "name": "precedent_search",
                "description": "Search for relevant legal precedents and case law",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Legal query for precedent search"}
                    },
                    "required": ["query"]
                }
            },
            "case_analysis": {
                "name": "case_analysis",
                "description": "Analyze and categorize legal case",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_input": {"type": "string", "description": "User's legal case description"}
                    },
                    "required": ["user_input"]
                }
            },
            "document_drafting": {
                "name": "document_drafting",
                "description": "Draft legal documents based on case analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_summary": {"type": "string", "description": "Case summary"},
                        "ipc_sections": {"type": "array", "description": "Relevant IPC sections"},
                        "precedents": {"type": "array", "description": "Relevant legal precedents"},
                        "document_type": {"type": "string", "description": "Type of document to draft"}
                    },
                    "required": ["case_summary"]
                }
            },
            "legal_advice": {
                "name": "legal_advice",
                "description": "Provide legal advice based on case analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_summary": {"type": "string", "description": "Case summary"},
                        "case_type": {"type": "string", "description": "Type of legal case"}
                    },
                    "required": ["case_summary"]
                }
            }
        }

# Example usage
async def test_mcp_tools():
    """Test the MCP tools"""
    registry = MCPToolRegistry()
    
    # Test case analysis
    case_result = await registry.get_tool("case_analysis")("A man broke into my house and stole jewelry")
    print("Case Analysis Result:")
    print(json.dumps(case_result.dict(), indent=2, default=str))
    
    # Test legal advice
    advice_result = await registry.get_tool("legal_advice")("Theft case", "property_crime")
    print("\nLegal Advice Result:")
    print(json.dumps(advice_result.dict(), indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())