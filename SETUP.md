# Sentinel Red Team - Setup Guide

## Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- Anthropic API key (or OpenAI API key)
- (Optional) Docker for sandboxed tool execution
- (Optional) Qdrant for vector database

### 2. Installation

```bash
# Clone or navigate to the sentinel-redteam directory
cd sentinel-redteam

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Or create a .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### 3. Configuration

Edit `config/settings.yaml` to customize:
- AI model selection
- Memory system settings
- Tool integrations
- Security preferences

Edit `config/authorization.yaml` to add:
- Authorized targets
- Engagement details
- Rules of engagement

### 4. Run Sentinel

```bash
# Interactive mode
python sentinel.py

# Single query mode
python sentinel.py --query "What's the first step in web app testing?"
```

---

## Detailed Setup

### Setting Up Vector Database (Optional but Recommended)

Qdrant provides semantic search for your knowledge base.

**Option 1: Docker (Easiest)**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Option 2: Local Installation**
```bash
# Follow instructions at: https://qdrant.tech/documentation/quick-start/
```

### Setting Up Graph Database (Optional)

Neo4j provides relationship mapping for techniques and engagements.

**Option 1: Docker**
```bash
docker run \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/sentinel123 \
    neo4j:latest
```

**Option 2: Neo4j Desktop**
Download from: https://neo4j.com/download/

### Tool Integration

#### Nmap
```bash
# Ubuntu/Debian
sudo apt install nmap

# macOS
brew install nmap
```

#### Burp Suite Pro (Optional)
1. Install Burp Suite Pro
2. Enable REST API
3. Add API key to config/settings.yaml

#### Metasploit (Optional)
```bash
# Start Metasploit RPC
msfrpcd -P yourpassword -S -a 127.0.0.1

# Add credentials to config/settings.yaml
```

---

## First Run Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] ANTHROPIC_API_KEY set
- [ ] config/settings.yaml reviewed
- [ ] config/authorization.yaml configured with authorized targets
- [ ] (Optional) Vector database running
- [ ] (Optional) Security tools installed

---

## Usage Examples

### Interactive Chat
```bash
python sentinel.py
```

```
You: I need to test a web application. What's my methodology?

Sentinel: For web application penetration testing, here's a systematic approach:

1. **Reconnaissance**
   - Identify technology stack
   - Map attack surface
   - Enumerate subdomains
   
2. **Vulnerability Analysis**
   - OWASP Top 10 checks
   - Business logic testing
   - Authentication testing
   
[... continues ...]
```

### Teaching Sentinel

```bash
You: teach

# Follow the prompts to add your custom technique
Technique name: DNS Tunneling for Exfiltration
Category: post_exploit
Description: Use DNS queries to exfiltrate data from target
...
```

### Single Query Mode
```bash
python sentinel.py --query "How do I bypass a WAF?"
```

---

## Project Structure Explained

```
sentinel-redteam/
├── sentinel.py              # Main CLI entry point
├── core/                    # Core AI components
│   ├── llm_interface.py    # LLM communication
│   ├── memory_system.py    # Knowledge persistence
│   └── agent_orchestrator.py  # Multi-agent coordination (coming)
├── modules/                 # Security modules (coming)
│   ├── recon/              # Reconnaissance tools
│   ├── vuln_scan/          # Vulnerability scanners
│   └── exploitation/       # Exploitation frameworks
├── knowledge/              # Your learned techniques
│   ├── techniques.json     # Technique database
│   ├── engagements.json    # Past engagements
│   └── lessons.json        # Lessons learned
├── config/                 # Configuration
│   ├── settings.yaml       # System settings
│   └── authorization.yaml  # Target authorization
└── logs/                   # Audit logs
```

---

## Security Best Practices

### 1. API Key Security
```bash
# Never commit API keys
echo ".env" >> .gitignore

# Use environment variables
export ANTHROPIC_API_KEY='...'

# Or use a secrets manager
```

### 2. Authorization Tracking
- ALWAYS verify target authorization before testing
- Keep authorization documents in secure location
- Update authorization.yaml with all engagements
- Review scope before every action

### 3. Audit Logging
- All actions are logged to logs/audit.log
- Review logs regularly
- Keep logs secure and encrypted
- Maintain logs for compliance

### 4. Safe Mode
```yaml
# In config/settings.yaml
security:
  safe_mode: true  # Prevents destructive actions
  confirm_exploitation: true
  confirm_persistence: true
```

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY='your-key-here'
# Or add to ~/.bashrc or ~/.zshrc
```

### "qdrant-client not installed"
```bash
pip install qdrant-client sentence-transformers
# Or run vector DB-free (file-based storage only)
```

### "Connection refused" errors
- Check if Qdrant is running: `docker ps`
- Verify config/settings.yaml has correct host/port
- Try without vector DB (will use file-based storage)

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Next Steps

1. **Add Your First Engagement**
   - Edit config/authorization.yaml
   - Add authorized targets
   - Define scope and RoE

2. **Teach Sentinel Your Techniques**
   - Use `teach` command
   - Demonstrate your methodology
   - Build your custom knowledge base

3. **Integrate Your Tools**
   - Configure tool paths in settings.yaml
   - Test tool integration
   - Create custom tool wrappers

4. **Start Testing**
   - Begin with reconnaissance
   - Let Sentinel learn from your approach
   - Iterate and improve

---

## Getting Help

- Check README.md for architecture details
- Review config/settings.yaml for all options
- Examine code comments for technical details
- Use `help` command in interactive mode

---

## Legal Disclaimer

This tool is for AUTHORIZED security testing only. Users are responsible for:
- Obtaining proper authorization
- Complying with all laws
- Following ethical guidelines
- Maintaining confidentiality

Unauthorized access to computer systems is illegal.
