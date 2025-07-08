#!/usr/bin/env python3
"""
Complete example demonstrating Pydantic AI with MCP Tools for Legal Assistant
"""

import asyncio
import json
from datetime import datetime
from pydantic_ai_agent import PydanticAILegalAgent, LegalQuery
from mcp_tools import MCPToolRegistry
from hybrid_legal_assistant import HybridLegalAssistant

async def demonstrate_pydantic_ai_with_mcp():
    """
    Demonstrate the complete Pydantic AI implementation with MCP tools
    """
    print("🚀 Demonstrating Pydantic AI with Custom MCP Tools")
    print("="*60)
    
    # Test case
    test_case = """
    A man broke into my house at night while my family was sleeping. 
    He stole jewelry and cash from our bedroom. When I confronted him, 
    he threatened me with a knife and ran away. We reported it to the police, 
    but I'm not sure which legal charges should be filed under IPC.
    """
    
    print(f"Test Case: {test_case.strip()}")
    print("\n" + "="*60)
    
    # Initialize the Pydantic AI agent
    agent = PydanticAILegalAgent()
    
    # Create query
    query = LegalQuery(
        user_input=test_case.strip(),
        query_type="criminal"
    )
    
    print("\n🧠 Processing with Pydantic AI Agent...")
    try:
        # Process the query
        response = await agent.process_legal_query(query)
        
        print("\n📊 RESULTS:")
        print(f"Case Summary:\n{response.case_summary}")
        print(f"\nIPC Sections Found: {len(response.ipc_sections)}")
        for i, section in enumerate(response.ipc_sections[:3], 1):
            if isinstance(section, dict):
                print(f"  {i}. Section {section.get('section', 'N/A')}: {section.get('section_title', 'N/A')}")
        
        print(f"\nLegal Precedents Found: {len(response.legal_precedents)}")
        for i, precedent in enumerate(response.legal_precedents[:3], 1):
            if isinstance(precedent, dict):
                print(f"  {i}. {precedent.get('title', 'N/A')}")
        
        print(f"\nDraft Document Generated: {len(response.draft_document)} characters")
        print(f"Document Preview:\n{response.draft_document[:300]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("🔧 Demonstrating Individual MCP Tools")
    print("="*60)
    
    # Test individual MCP tools
    registry = MCPToolRegistry()
    
    # Test case analysis
    print("\n📊 Testing Case Analysis Tool...")
    case_tool = registry.get_tool("case_analysis")
    case_result = await case_tool(test_case.strip())
    print(f"Status: {case_result.status}")
    if case_result.status == "success":
        print(f"Case Type: {case_result.data['case_type']}")
        print(f"Priority: {case_result.data['priority']}")
    
    # Test legal advice
    print("\n💡 Testing Legal Advice Tool...")
    advice_tool = registry.get_tool("legal_advice")
    advice_result = await advice_tool(test_case.strip(), "property_crime")
    print(f"Status: {advice_result.status}")
    if advice_result.status == "success":
        print(f"Advice Preview:\n{advice_result.data['advice'][:200]}...")
    
    # Test document drafting
    print("\n📝 Testing Document Drafting Tool...")
    document_tool = registry.get_tool("document_drafting")
    document_result = await document_tool(
        case_summary=test_case.strip(),
        document_type="complaint"
    )
    print(f"Status: {document_result.status}")
    if document_result.status == "success":
        print(f"Document Type: {document_result.data['document_type']}")
        print(f"Word Count: {document_result.data['word_count']}")
    
    print("\n" + "="*60)
    print("🔄 Demonstrating Hybrid System")
    print("="*60)
    
    # Test hybrid system
    hybrid = HybridLegalAssistant()
    
    print("\n🔄 Processing with MCP Tools Only...")
    mcp_results = await hybrid.process_with_mcp_tools_only(test_case.strip())
    
    print(f"Status: {mcp_results['status']}")
    if mcp_results['status'] == 'success':
        print(f"Workflow Steps Completed: {len(mcp_results['workflow_steps'])}")
        for step in mcp_results['workflow_steps']:
            print(f"  - {step['step']}: {step['result']['status']}")
    
    # Show tool schemas
    print("\n🛠️ Available MCP Tool Schemas:")
    schemas = registry.get_tool_schemas()
    for tool_name, schema in schemas.items():
        print(f"  - {tool_name}: {schema['description']}")
    
    print("\n✅ Demonstration Complete!")

if __name__ == "__main__":
    asyncio.run(demonstrate_pydantic_ai_with_mcp())