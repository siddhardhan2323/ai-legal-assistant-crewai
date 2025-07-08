#!/usr/bin/env python3
"""
Simple test of MCP tools without CrewAI dependencies
"""

import asyncio
import json
from datetime import datetime
from mcp_tools import MCPToolRegistry

async def test_mcp_tools_only():
    """Test only the MCP tools implementation"""
    print("🚀 Testing Pydantic AI with Custom MCP Tools")
    print("="*60)
    
    # Test case
    test_case = """
    A man broke into my house at night while my family was sleeping. 
    He stole jewelry and cash from our bedroom. When I confronted him, 
    he threatened me with a knife and ran away.
    """
    
    print(f"Test Case: {test_case.strip()}")
    print("\n" + "="*60)
    
    # Initialize MCP tools
    registry = MCPToolRegistry()
    
    # Test case analysis
    print("\n📊 Testing Case Analysis Tool...")
    case_tool = registry.get_tool("case_analysis")
    case_result = await case_tool(test_case.strip())
    print(f"Status: {case_result.status}")
    if case_result.status == "success":
        print(f"Case Type: {case_result.data['case_type']}")
        print(f"Priority: {case_result.data['priority']}")
        print(f"Summary: {case_result.data['case_summary'][:200]}...")
    
    # Test legal advice
    print("\n💡 Testing Legal Advice Tool...")
    advice_tool = registry.get_tool("legal_advice")
    advice_result = await advice_tool(test_case.strip(), "property_crime")
    print(f"Status: {advice_result.status}")
    if advice_result.status == "success":
        print(f"Advice Preview:\n{advice_result.data['advice'][:300]}...")
    
    # Test document drafting
    print("\n📝 Testing Document Drafting Tool...")
    document_tool = registry.get_tool("document_drafting")
    document_result = await document_tool(
        case_summary=test_case.strip(),
        document_type="legal_notice"
    )
    print(f"Status: {document_result.status}")
    if document_result.status == "success":
        print(f"Document Type: {document_result.data['document_type']}")
        print(f"Word Count: {document_result.data['word_count']}")
        print(f"Document Preview:\n{document_result.data['document'][:400]}...")
    
    # Show available tools
    print("\n🛠️ Available MCP Tools:")
    tools = registry.list_tools()
    for tool in tools:
        print(f"  - {tool}")
    
    # Show tool schemas
    print("\n📋 MCP Tool Schemas:")
    schemas = registry.get_tool_schemas()
    for tool_name, schema in schemas.items():
        print(f"  - {tool_name}: {schema['description']}")
    
    print("\n✅ MCP Tools Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools_only())