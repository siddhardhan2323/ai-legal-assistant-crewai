#!/usr/bin/env python3
"""
Integration module to combine Pydantic AI agent with existing CrewAI system
"""

import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json

# Import existing CrewAI components
from crew import legal_assistant_crew

# Import our custom Pydantic AI components
from pydantic_ai_agent import PydanticAILegalAgent, LegalQuery, LegalResponse
from mcp_tools import MCPToolRegistry, MCPToolResult

class HybridLegalAssistant:
    """
    Hybrid Legal Assistant that combines CrewAI and Pydantic AI
    """
    
    def __init__(self):
        self.crewai_crew = legal_assistant_crew
        self.pydantic_agent = PydanticAILegalAgent()
        self.mcp_tools = MCPToolRegistry()
        
    async def process_query_with_both_systems(self, user_input: str) -> Dict[str, Any]:
        """
        Process query using both CrewAI and Pydantic AI systems
        """
        results = {
            "user_input": user_input,
            "timestamp": datetime.now(),
            "systems_used": ["crewai", "pydantic_ai"],
            "results": {}
        }
        
        # Process with CrewAI (existing system)
        try:
            print("🔄 Processing with CrewAI system...")
            crewai_result = self.crewai_crew.kickoff(inputs={"user_input": user_input})
            results["results"]["crewai"] = {
                "status": "success",
                "output": str(crewai_result),
                "system": "crewai"
            }
        except Exception as e:
            results["results"]["crewai"] = {
                "status": "error",
                "error": str(e),
                "system": "crewai"
            }
        
        # Process with Pydantic AI (new system)
        try:
            print("🔄 Processing with Pydantic AI system...")
            query = LegalQuery(user_input=user_input)
            pydantic_result = await self.pydantic_agent.process_legal_query(query)
            results["results"]["pydantic_ai"] = {
                "status": "success",
                "output": pydantic_result.dict(),
                "system": "pydantic_ai"
            }
        except Exception as e:
            results["results"]["pydantic_ai"] = {
                "status": "error",
                "error": str(e),
                "system": "pydantic_ai"
            }
        
        return results
    
    async def process_with_mcp_tools_only(self, user_input: str) -> Dict[str, Any]:
        """
        Process query using only MCP tools
        """
        results = {
            "user_input": user_input,
            "timestamp": datetime.now(),
            "system_used": "mcp_tools",
            "workflow_steps": []
        }
        
        try:
            # Step 1: Case Analysis
            print("📊 Analyzing case...")
            case_analysis_tool = self.mcp_tools.get_tool("case_analysis")
            case_result = await case_analysis_tool(user_input)
            results["workflow_steps"].append({
                "step": "case_analysis",
                "result": case_result.dict()
            })
            
            if case_result.status == "success":
                case_data = case_result.data
                case_summary = case_data.get("case_summary", "")
                case_type = case_data.get("case_type", "general")
                
                # Step 2: IPC Search
                print("⚖️ Searching IPC sections...")
                ipc_tool = self.mcp_tools.get_tool("ipc_search")
                ipc_result = await ipc_tool(user_input)
                results["workflow_steps"].append({
                    "step": "ipc_search",
                    "result": ipc_result.dict()
                })
                
                # Step 3: Precedent Search
                print("📚 Searching legal precedents...")
                precedent_tool = self.mcp_tools.get_tool("precedent_search")
                precedent_result = await precedent_tool(user_input + " precedent cases India")
                results["workflow_steps"].append({
                    "step": "precedent_search",
                    "result": precedent_result.dict()
                })
                
                # Step 4: Legal Advice
                print("💡 Generating legal advice...")
                advice_tool = self.mcp_tools.get_tool("legal_advice")
                advice_result = await advice_tool(case_summary, case_type)
                results["workflow_steps"].append({
                    "step": "legal_advice",
                    "result": advice_result.dict()
                })
                
                # Step 5: Document Drafting
                print("📝 Drafting legal document...")
                document_tool = self.mcp_tools.get_tool("document_drafting")
                document_result = await document_tool(
                    case_summary=case_summary,
                    ipc_sections=ipc_result.data if ipc_result.status == "success" else [],
                    precedents=precedent_result.data if precedent_result.status == "success" else [],
                    document_type="legal_notice"
                )
                results["workflow_steps"].append({
                    "step": "document_drafting",
                    "result": document_result.dict()
                })
                
                # Compile final result
                results["final_output"] = {
                    "case_analysis": case_result.data,
                    "ipc_sections": ipc_result.data if ipc_result.status == "success" else [],
                    "precedents": precedent_result.data if precedent_result.status == "success" else [],
                    "legal_advice": advice_result.data if advice_result.status == "success" else {},
                    "draft_document": document_result.data if document_result.status == "success" else {}
                }
                
                results["status"] = "success"
                
            else:
                results["status"] = "error"
                results["error"] = case_result.error
                
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
        
        return results
    
    def get_system_comparison(self) -> Dict[str, Any]:
        """
        Get comparison between different systems
        """
        return {
            "systems": {
                "crewai": {
                    "description": "Multi-agent crew system with specialized agents",
                    "components": ["case_intake_agent", "ipc_section_agent", "legal_precedent_agent", "legal_drafter_agent"],
                    "tools": ["ipc_sections_search_tool", "legal_precedent_search_tool"],
                    "workflow": "Sequential agent processing with task dependencies"
                },
                "pydantic_ai": {
                    "description": "Pydantic AI agent with custom MCP tools",
                    "components": ["PydanticAILegalAgent"],
                    "tools": ["ipc_search", "precedent_search", "case_analysis", "document_drafting"],
                    "workflow": "Async tool orchestration with type safety"
                },
                "mcp_tools": {
                    "description": "Direct MCP tool usage without agent wrapper",
                    "components": ["MCPToolRegistry"],
                    "tools": ["ipc_search", "precedent_search", "case_analysis", "document_drafting", "legal_advice"],
                    "workflow": "Direct tool calling with structured results"
                }
            },
            "recommended_use": {
                "crewai": "Complex legal workflows requiring specialized agent collaboration",
                "pydantic_ai": "Type-safe legal processing with structured responses",
                "mcp_tools": "Direct tool access for specific legal tasks"
            }
        }

# CLI Interface for the hybrid system
class LegalAssistantCLI:
    """
    Command-line interface for the hybrid legal assistant
    """
    
    def __init__(self):
        self.assistant = HybridLegalAssistant()
    
    async def run_interactive(self):
        """Run interactive CLI"""
        print("🚀 Welcome to the Hybrid Legal Assistant!")
        print("Choose a processing mode:")
        print("1. CrewAI + Pydantic AI (Hybrid)")
        print("2. MCP Tools Only")
        print("3. System Comparison")
        print("4. Exit")
        
        while True:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                await self._run_hybrid_mode()
            elif choice == "2":
                await self._run_mcp_mode()
            elif choice == "3":
                self._show_system_comparison()
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
    
    async def _run_hybrid_mode(self):
        """Run hybrid mode"""
        user_input = input("\n📝 Enter your legal issue: ").strip()
        if not user_input:
            print("❌ Please enter a valid legal issue.")
            return
        
        print("\n🔄 Processing with hybrid system...")
        results = await self.assistant.process_query_with_both_systems(user_input)
        
        print("\n" + "="*50)
        print("HYBRID SYSTEM RESULTS")
        print("="*50)
        
        # CrewAI results
        if "crewai" in results["results"]:
            print("\n🤖 CrewAI Results:")
            crewai_result = results["results"]["crewai"]
            if crewai_result["status"] == "success":
                print(crewai_result["output"])
            else:
                print(f"❌ Error: {crewai_result['error']}")
        
        # Pydantic AI results
        if "pydantic_ai" in results["results"]:
            print("\n🧠 Pydantic AI Results:")
            pydantic_result = results["results"]["pydantic_ai"]
            if pydantic_result["status"] == "success":
                output = pydantic_result["output"]
                print(f"Case Summary: {output['case_summary']}")
                print(f"IPC Sections: {len(output['ipc_sections'])} found")
                print(f"Legal Precedents: {len(output['legal_precedents'])} found")
                print(f"Draft Document: {len(output['draft_document'])} characters")
            else:
                print(f"❌ Error: {pydantic_result['error']}")
    
    async def _run_mcp_mode(self):
        """Run MCP tools mode"""
        user_input = input("\n📝 Enter your legal issue: ").strip()
        if not user_input:
            print("❌ Please enter a valid legal issue.")
            return
        
        print("\n🔄 Processing with MCP tools...")
        results = await self.assistant.process_with_mcp_tools_only(user_input)
        
        print("\n" + "="*50)
        print("MCP TOOLS RESULTS")
        print("="*50)
        
        if results["status"] == "success":
            final_output = results["final_output"]
            
            # Case Analysis
            print("\n📊 CASE ANALYSIS:")
            case_analysis = final_output["case_analysis"]
            print(case_analysis["case_summary"])
            
            # IPC Sections
            print(f"\n⚖️ IPC SECTIONS ({len(final_output['ipc_sections'])} found):")
            for i, section in enumerate(final_output["ipc_sections"][:3], 1):
                if isinstance(section, dict):
                    print(f"{i}. Section {section.get('section', 'N/A')}: {section.get('section_title', 'N/A')}")
            
            # Legal Precedents
            print(f"\n📚 LEGAL PRECEDENTS ({len(final_output['precedents'])} found):")
            for i, precedent in enumerate(final_output["precedents"][:3], 1):
                if isinstance(precedent, dict):
                    print(f"{i}. {precedent.get('title', 'N/A')}")
            
            # Legal Advice
            print("\n💡 LEGAL ADVICE:")
            advice = final_output["legal_advice"]
            if advice:
                print(advice.get("advice", ""))
            
            # Draft Document
            print("\n📝 DRAFT DOCUMENT:")
            document = final_output["draft_document"]
            if document:
                print(document.get("document", ""))
        else:
            print(f"❌ Error: {results['error']}")
    
    def _show_system_comparison(self):
        """Show system comparison"""
        comparison = self.assistant.get_system_comparison()
        
        print("\n" + "="*50)
        print("SYSTEM COMPARISON")
        print("="*50)
        
        for system_name, system_info in comparison["systems"].items():
            print(f"\n🔧 {system_name.upper()}:")
            print(f"   Description: {system_info['description']}")
            print(f"   Components: {', '.join(system_info['components'])}")
            print(f"   Tools: {', '.join(system_info['tools'])}")
            print(f"   Workflow: {system_info['workflow']}")
        
        print("\n📌 RECOMMENDED USE:")
        for system_name, recommendation in comparison["recommended_use"].items():
            print(f"   {system_name}: {recommendation}")

# Example usage
async def main():
    """Example usage of the hybrid system"""
    cli = LegalAssistantCLI()
    await cli.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())