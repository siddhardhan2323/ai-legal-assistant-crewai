#!/usr/bin/env python3
"""
Streamlit app integration with Pydantic AI and MCP Tools
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
from mcp_tools import MCPToolRegistry
from pydantic_ai_agent import PydanticAILegalAgent, LegalQuery

# Configure Streamlit
st.set_page_config(
    page_title="🧠 AI Legal Assistant with Pydantic AI & MCP Tools",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processing_mode' not in st.session_state:
    st.session_state.processing_mode = 'MCP Tools'

# Sidebar for mode selection
st.sidebar.title("🔧 Processing Mode")
processing_mode = st.sidebar.selectbox(
    "Choose processing system:",
    ["MCP Tools", "Pydantic AI Agent", "Tool Comparison"],
    key="processing_mode"
)

# Main app
st.title("⚖️ AI Legal Assistant")
st.markdown("### Built with Pydantic AI & Custom MCP Tools")

# Mode-specific UI
if processing_mode == "MCP Tools":
    st.header("🛠️ MCP Tools Direct Access")
    st.markdown("""
    This mode provides direct access to individual MCP (Model Context Protocol) tools.
    Each tool is specialized for specific legal tasks.
    """)
    
    # Tool selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Available Tools")
        registry = MCPToolRegistry()
        tools = registry.list_tools()
        
        selected_tool = st.selectbox("Select a tool:", tools)
        
        # Show tool description
        schemas = registry.get_tool_schemas()
        if selected_tool in schemas:
            st.info(f"**{selected_tool}**: {schemas[selected_tool]['description']}")
    
    with col2:
        st.subheader("Tool Input")
        
        if selected_tool == "case_analysis":
            user_input = st.text_area("Enter case description:", height=150)
            if st.button("Analyze Case"):
                if user_input:
                    with st.spinner("Analyzing case..."):
                        tool = registry.get_tool(selected_tool)
                        result = asyncio.run(tool(user_input))
                        
                        if result.status == "success":
                            st.success("Analysis complete!")
                            st.json(result.data)
                        else:
                            st.error(f"Error: {result.error}")
        
        elif selected_tool == "legal_advice":
            case_summary = st.text_area("Enter case summary:", height=100)
            case_type = st.selectbox("Case type:", 
                                   ["general", "property_crime", "violent_crime", "contract_dispute", "fraud"])
            
            if st.button("Get Legal Advice"):
                if case_summary:
                    with st.spinner("Generating legal advice..."):
                        tool = registry.get_tool(selected_tool)
                        result = asyncio.run(tool(case_summary, case_type))
                        
                        if result.status == "success":
                            st.success("Advice generated!")
                            st.text_area("Legal Advice:", result.data["advice"], height=300)
                        else:
                            st.error(f"Error: {result.error}")
        
        elif selected_tool == "document_drafting":
            case_summary = st.text_area("Enter case summary:", height=100)
            document_type = st.selectbox("Document type:", ["legal_notice", "complaint"])
            
            if st.button("Draft Document"):
                if case_summary:
                    with st.spinner("Drafting document..."):
                        tool = registry.get_tool(selected_tool)
                        result = asyncio.run(tool(case_summary, document_type=document_type))
                        
                        if result.status == "success":
                            st.success("Document drafted!")
                            st.text_area("Draft Document:", result.data["document"], height=400)
                            st.info(f"Word count: {result.data['word_count']}")
                        else:
                            st.error(f"Error: {result.error}")
        
        elif selected_tool in ["ipc_search", "precedent_search"]:
            query = st.text_input("Enter search query:")
            
            if st.button("Search"):
                if query:
                    with st.spinner("Searching..."):
                        tool = registry.get_tool(selected_tool)
                        result = asyncio.run(tool(query))
                        
                        if result.status == "success":
                            st.success("Search complete!")
                            st.json(result.data)
                        else:
                            st.error(f"Error: {result.error}")

elif processing_mode == "Pydantic AI Agent":
    st.header("🧠 Pydantic AI Agent")
    st.markdown("""
    This mode uses the Pydantic AI agent that orchestrates multiple MCP tools 
    to provide a comprehensive legal analysis.
    """)
    
    # Input form
    with st.form("legal_query_form"):
        user_input = st.text_area("📝 Describe your legal issue:", height=200)
        query_type = st.selectbox("Query type:", ["general", "criminal", "civil", "property", "contract"])
        
        submitted = st.form_submit_button("🔍 Process Legal Query")
    
    if submitted and user_input:
        with st.spinner("🔄 Processing with Pydantic AI agent..."):
            try:
                # Create agent and query
                agent = PydanticAILegalAgent()
                query = LegalQuery(user_input=user_input, query_type=query_type)
                
                # Process the query
                response = asyncio.run(agent.process_legal_query(query))
                
                # Display results
                st.success("✅ Analysis complete!")
                
                # Create tabs for different sections
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Case Summary", "⚖️ IPC Sections", "📚 Precedents", "📝 Document"])
                
                with tab1:
                    st.markdown("### Case Summary")
                    st.text_area("", response.case_summary, height=200)
                
                with tab2:
                    st.markdown("### IPC Sections")
                    st.write(f"Found {len(response.ipc_sections)} relevant sections:")
                    for i, section in enumerate(response.ipc_sections[:5], 1):
                        if isinstance(section, dict):
                            st.write(f"**{i}. Section {section.get('section', 'N/A')}**: {section.get('section_title', 'N/A')}")
                
                with tab3:
                    st.markdown("### Legal Precedents")
                    st.write(f"Found {len(response.legal_precedents)} relevant precedents:")
                    for i, precedent in enumerate(response.legal_precedents[:5], 1):
                        if isinstance(precedent, dict):
                            st.write(f"**{i}. {precedent.get('title', 'N/A')}**")
                            if precedent.get('summary'):
                                st.write(f"   {precedent.get('summary', '')[:200]}...")
                
                with tab4:
                    st.markdown("### Draft Document")
                    st.text_area("", response.draft_document, height=400)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif processing_mode == "Tool Comparison":
    st.header("📊 Tool Comparison")
    st.markdown("""
    Compare different processing approaches and their capabilities.
    """)
    
    # System comparison
    comparison_data = {
        "Feature": [
            "Type Safety",
            "Async Support", 
            "Tool Orchestration",
            "Structured Output",
            "Error Handling",
            "Extensibility",
            "Performance"
        ],
        "MCP Tools": [
            "✅ Pydantic models",
            "✅ Native async",
            "✅ Manual orchestration",
            "✅ Structured results",
            "✅ Comprehensive",
            "✅ Easy to extend",
            "⚡ Fast"
        ],
        "Pydantic AI Agent": [
            "✅ Full type safety",
            "✅ Async workflow",
            "✅ Automated orchestration",
            "✅ Typed responses",
            "✅ Robust handling",
            "✅ Agent-based",
            "🔄 Moderate"
        ],
        "CrewAI (existing)": [
            "⚠️ Limited typing",
            "❌ Sync only",
            "✅ Multi-agent",
            "⚠️ String output",
            "⚠️ Basic handling",
            "✅ Agent framework",
            "🐌 Slower"
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    # Tool schemas
    st.subheader("🛠️ Available MCP Tools")
    registry = MCPToolRegistry()
    schemas = registry.get_tool_schemas()
    
    for tool_name, schema in schemas.items():
        with st.expander(f"🔧 {tool_name}"):
            st.write(f"**Description**: {schema['description']}")
            st.write(f"**Parameters**: {schema['parameters']}")

# Footer
st.markdown("---")
st.markdown("""
### 🔧 Technical Implementation

This application demonstrates:
- **Pydantic AI**: Type-safe AI agent implementation
- **MCP Tools**: Custom Model Context Protocol tools
- **Async Processing**: Non-blocking tool execution
- **Structured Output**: Typed responses with Pydantic models
- **Tool Orchestration**: Coordinated execution of multiple tools

Built with Streamlit, Pydantic, and custom MCP tools for legal assistance.
""")