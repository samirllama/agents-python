# AI Agents Framework

A sophisticated AI Agents framework built with Python, demonstrating advanced implementation of autonomous agents using Large Language Models (LLMs). This project showcases modern AI techniques including Retrieval Augmented Generation (RAG), evaluation systems, and CLI tools.

## 🚀 Features

- **Modular Agent Architecture**: Extensible base agent class for building specialized AI agents
- **RAG Implementation**: Built-in support for Retrieval Augmented Generation
- **Vector Storage**: Efficient similarity search using Upstash Vector
- **Evaluation System**: Comprehensive evaluation framework for agent performance
- **CLI Interface**: Command-line tools for agent interaction and testing
- **Async Architecture**: Built with modern async/await patterns for optimal performance
- **Type Safety**: Fully typed codebase with Pyright type checking

## 🛠️ Technology Stack

- Python 3.13+
- OpenAI API
- Upstash Vector
- SQLite
- Type hints & Pyright
- AsyncIO

## 📋 Prerequisites

- Python 3.13 or higher
- OpenAI API key
- Upstash Vector account and credentials

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agents-python.git
cd agents-python
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `UPSTASH_VECTOR_REST_URL`: Upstash Vector REST URL
- `UPSTASH_VECTOR_REST_TOKEN`: Upstash Vector REST token

⚠️ Never commit your `.env` file or expose these credentials in your code.
## 🚀 Usage

### Basic Agent Implementation
```python
async def main():
    agent = RAGAgent()
    response = await agent.generate_response("Your query here")
    print(response)
```

### Running Evaluations
```bash
python -m evals.run
```

## 🏗️ Project Structure

```
agents-python/
├── agents/             # Core agent logic
│   ├── base_agent.py   # Abstract base class for agents
│   └── rag_agent.py    # RAG implementation
├── tools/              # Utility modules
│   └── vector_store.py # Vector storage operations
├── evals/              # Evaluation framework
│   ├── experiments/    # Test scenarios
│   ├── scorers.py     # Scoring mechanisms
│   └── run.py         # Evaluation runner
├── utils/              # Helper utilities
│   └── db.py          # Database operations
├── data/              # Data storage
├── ingest.py          # Data ingestion script
└── main.py            # Entry point
```

## 🔄 Current Status

This project is under active development. Current implementation includes:
- Base agent architecture
- RAG agent implementation
- Vector store integration
- Initial evaluation framework

Coming soon:
- Extended evaluation system
- Enhanced CLI tools
- Additional example implementations


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Contact

samirllama@gmail.com - [LinkedIn]
Project Link: [https://github.com/samirllama/agents-python)

## 🙏 Acknowledgments

- OpenAI for their powerful language models
- Upstash for their vector database solution
- The open-source community for inspiration and tools

---

<p align="center">
  Built with ❤️
</p>
