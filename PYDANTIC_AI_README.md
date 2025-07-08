# Pydantic AI Legal Assistant with Custom MCP Tools

This implementation extends the existing CrewAI legal assistant with a **Pydantic AI agent** that uses **custom MCP (Model Context Protocol) tools** for enhanced type safety, performance, and extensibility.

## 🚀 Features

### Pydantic AI Agent
- **Type-safe AI agent** built with Pydantic models
- **Async workflow processing** for better performance
- **Structured input/output** with automatic validation
- **Tool orchestration** with coordinated execution

### Custom MCP Tools
- **`ipc_search`**: Search for relevant IPC sections
- **`precedent_search`**: Find legal precedents and case law
- **`case_analysis`**: Analyze and categorize legal cases
- **`document_drafting`**: Draft legal documents (notices, complaints)
- **`legal_advice`**: Provide structured legal advice

### Integration Options
- **Standalone MCP tools** for direct access
- **Pydantic AI agent** for orchestrated workflow
- **Hybrid system** combining CrewAI and Pydantic AI
- **Streamlit interface** for interactive usage

## 📦 Installation

```bash
# Install additional dependencies
pip install mcp pydantic-ai

# Or install from requirements
pip install -r requirements.txt
```

## 🛠️ Usage

### 1. Direct MCP Tools Usage

```python
import asyncio
from mcp_tools import MCPToolRegistry

# Initialize registry
registry = MCPToolRegistry()

# Use case analysis tool
case_tool = registry.get_tool("case_analysis")
result = await case_tool("A man stole my wallet")

print(f"Status: {result.status}")
print(f"Case Type: {result.data['case_type']}")
```

### 2. Pydantic AI Agent

```python
import asyncio
from pydantic_ai_agent import PydanticAILegalAgent, LegalQuery

# Initialize agent
agent = PydanticAILegalAgent()

# Create query
query = LegalQuery(
    user_input="Legal issue description",
    query_type="criminal"
)

# Process query
response = await agent.process_legal_query(query)

# Access structured response
print(f"Case Summary: {response.case_summary}")
print(f"IPC Sections: {len(response.ipc_sections)}")
print(f"Legal Precedents: {len(response.legal_precedents)}")
print(f"Draft Document: {response.draft_document}")
```

### 3. Streamlit Interface

```bash
# Run the Pydantic AI Streamlit app
streamlit run streamlit_pydantic_ai.py
```

### 4. Test Implementation

```bash
# Test MCP tools
python test_mcp_tools.py

# Test complete system (if CrewAI is available)
python demo_pydantic_ai_mcp.py
```

## 📊 Architecture

### Data Models

```python
# Input model
class LegalQuery(BaseModel):
    user_input: str
    query_type: str = "general"

# Output model  
class LegalResponse(BaseModel):
    case_summary: str
    ipc_sections: List[Dict[str, Any]]
    legal_precedents: List[Dict[str, Any]]
    draft_document: str

# Tool result model
class MCPToolResult(BaseModel):
    status: str
    data: Optional[Any]
    error: Optional[str]
    tool_name: str
    timestamp: datetime
```

### Tool Workflow

```
User Input → Case Analysis → IPC Search → Precedent Search → Document Drafting → Legal Advice
```

### MCP Tool Registry

```python
registry = MCPToolRegistry()
tools = registry.list_tools()
# ['ipc_search', 'precedent_search', 'case_analysis', 'document_drafting', 'legal_advice']
```

## 🔧 Technical Implementation

### MCP Tools Structure

Each MCP tool follows this pattern:

```python
class LegalTool:
    @staticmethod
    async def tool_function(params) -> MCPToolResult:
        try:
            # Tool logic here
            return MCPToolResult(
                status="success",
                data=result_data,
                tool_name="tool_name"
            )
        except Exception as e:
            return MCPToolResult(
                status="error",
                error=str(e),
                tool_name="tool_name"
            )
```

### Pydantic AI Agent Structure

```python
class PydanticAILegalAgent:
    def __init__(self):
        self.tools = {}
        self._register_tools()
    
    async def process_legal_query(self, query: LegalQuery) -> LegalResponse:
        # Orchestrate tool execution
        # Return structured response
```

## 🧪 Testing

### Unit Tests

```python
# Test individual tools
async def test_case_analysis():
    tool = registry.get_tool("case_analysis")
    result = await tool("Test case")
    assert result.status == "success"
    assert result.data["case_type"] in ["general", "property_crime", "violent_crime"]

# Test agent workflow
async def test_agent_workflow():
    agent = PydanticAILegalAgent()
    query = LegalQuery(user_input="Test case")
    response = await agent.process_legal_query(query)
    assert isinstance(response, LegalResponse)
```

### Integration Tests

```bash
# Test all components
python test_mcp_tools.py

# Test with sample data
python demo_pydantic_ai_mcp.py
```

## 📈 Performance Comparison

| Feature | MCP Tools | Pydantic AI Agent | CrewAI |
|---------|-----------|------------------|---------|
| Type Safety | ✅ Full | ✅ Full | ⚠️ Limited |
| Async Support | ✅ Native | ✅ Native | ❌ Sync only |
| Performance | ⚡ Fast | 🔄 Moderate | 🐌 Slower |
| Extensibility | ✅ Easy | ✅ Easy | ⚠️ Complex |
| Error Handling | ✅ Robust | ✅ Robust | ⚠️ Basic |

## 🔒 Error Handling

All tools include comprehensive error handling:

```python
try:
    result = await tool_function(params)
    if result.status == "error":
        logger.error(f"Tool {result.tool_name} failed: {result.error}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

## 🚀 Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_pydantic_ai.py

# Run tests
python test_mcp_tools.py
```

### Production Deployment

```bash
# Build Docker image
docker build -t legal-assistant-pydantic-ai .

# Run container
docker run -p 8501:8501 legal-assistant-pydantic-ai
```

## 📚 Examples

### Case Analysis Example

```python
# Input
user_input = "A man broke into my house and stole jewelry"

# Processing
case_tool = registry.get_tool("case_analysis")
result = await case_tool(user_input)

# Output
{
    "status": "success",
    "data": {
        "case_summary": "Legal Issue Analysis...",
        "case_type": "property_crime",
        "priority": "high",
        "confidence": 0.8
    },
    "tool_name": "case_analysis"
}
```

### Document Drafting Example

```python
# Input
document_tool = registry.get_tool("document_drafting")
result = await document_tool(
    case_summary="Theft case",
    document_type="legal_notice"
)

# Output
{
    "status": "success",
    "data": {
        "document": "LEGAL NOTICE\n\nDate: July 08, 2025...",
        "document_type": "legal_notice",
        "word_count": 250
    },
    "tool_name": "document_drafting"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Related Files

- `pydantic_ai_agent.py` - Main Pydantic AI agent implementation
- `mcp_tools.py` - Custom MCP tools for legal assistance
- `streamlit_pydantic_ai.py` - Streamlit interface
- `test_mcp_tools.py` - Test suite for MCP tools
- `demo_pydantic_ai_mcp.py` - Comprehensive demonstration
- `hybrid_legal_assistant.py` - Integration with existing CrewAI system

## 📞 Support

For questions and support, please refer to the documentation or create an issue in the repository.