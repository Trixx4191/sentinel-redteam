# 🔴 SENTINEL RED TEAM - GETTING STARTED

## What You Have

A complete AI-powered red team assistant foundation with:

✅ **Core AI Engine** - Claude integration with memory
✅ **Learning System** - Teach it your techniques
✅ **Tool Integration** - nmap, future: Burp, MSF, etc.
✅ **Authorization Tracking** - Scope management
✅ **Interactive CLI** - Chat with Sentinel
✅ **Knowledge Persistence** - Remembers everything
✅ **Professional Structure** - Production-ready architecture

## Quick Start (5 minutes)

### 1. Navigate to Project
```bash
cd sentinel-redteam
```

### 2. Run Quick Start
```bash
./quickstart.sh
```

This will:
- Create virtual environment
- Install dependencies
- Prompt for API key
- Set up directories

### 3. Set API Key (if not done in quickstart)
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

Or create `.env`:
```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

### 4. Configure Authorization
Edit `config/authorization.yaml`:
```yaml
engagements:
  - id: "TEST-001"
    status: "active"
    scope:
      in_scope:
        - "192.168.1.0/24"  # Your lab network
        - "*.yourdomain.com"
```

### 5. Start Sentinel
```bash
source venv/bin/activate
python sentinel.py
```

## First Interactions

### Example 1: Basic Chat
```
You: What's the first step in a web app pentest?

Sentinel: [Provides systematic methodology]
```

### Example 2: Teach a Technique
```
You: teach

[Follow prompts to add your custom technique]
```

### Example 3: Real Testing
```
You: I need to scan 192.168.1.100. It's in my lab.

Sentinel: [Guides you through reconnaissance]
```

## Project Structure

```
sentinel-redteam/
├── sentinel.py              # Main CLI (start here)
├── quickstart.sh           # Setup script
├── requirements.txt        # Dependencies
│
├── config/                 # Configuration
│   ├── settings.yaml      # System settings
│   └── authorization.yaml # Target authorization
│
├── core/                  # Core components
│   ├── llm_interface.py  # AI engine
│   └── memory_system.py  # Knowledge persistence
│
├── modules/              # Security modules
│   └── recon.py         # Reconnaissance
│
├── knowledge/           # Learned techniques (created on first run)
├── logs/               # Audit logs
└── reports/            # Generated reports
```

## Key Files to Know

1. **sentinel.py** - Main entry point
2. **config/settings.yaml** - Customize everything
3. **config/authorization.yaml** - Define authorized targets
4. **SETUP.md** - Detailed installation guide
5. **EXAMPLES.md** - Usage examples
6. **PROJECT_OVERVIEW.md** - Architecture and roadmap

## What to Do Next

### Phase 1: Learn the Basics
1. Start Sentinel: `python sentinel.py`
2. Ask questions about security testing
3. Use the `help` command
4. Check `stats` to see knowledge base

### Phase 2: Teach Sentinel
1. Use `teach` command
2. Add your first technique
3. See it stored in `knowledge/techniques.json`
4. Use it in future conversations

### Phase 3: Real Testing
1. Add authorized targets to `config/authorization.yaml`
2. Start with reconnaissance
3. Let Sentinel guide your methodology
4. Correct it when needed - it learns!

### Phase 4: Customize
1. Edit `config/settings.yaml`
2. Add tool integrations
3. Adjust AI parameters
4. Configure memory system

### Phase 5: Build More
- Add new modules (see `modules/recon.py` as example)
- Integrate your tools
- Extend capabilities
- Contribute improvements

## Common Commands

```bash
# Start interactive mode
python sentinel.py

# Single query
python sentinel.py --query "How do I test for SQLi?"

# Use custom config
python sentinel.py --config my_config.yaml

# Inside Sentinel:
help          # Show commands
teach         # Teach new technique
stats         # Show knowledge base stats
save report   # Save conversation
clear         # Clear history
exit          # Exit Sentinel
```

## Tips for Success

1. **Be Specific**: Give context about your target and goals
2. **Teach Early**: Add your techniques so Sentinel uses them
3. **Correct Often**: When it's wrong, correct it - it learns
4. **Verify Always**: Check authorization before any action
5. **Experiment**: Try different queries, see what it knows

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied" on scripts
```bash
chmod +x quickstart.sh sentinel.py
```

### "qdrant-client not installed"
Either:
- Install it: `pip install qdrant-client sentence-transformers`
- Or disable in `config/settings.yaml` (will use file-based storage)

## Next Steps

**Read These:**
1. `PROJECT_OVERVIEW.md` - Understand the architecture
2. `SETUP.md` - Detailed setup instructions
3. `EXAMPLES.md` - See real usage scenarios

**Try These:**
1. Teach Sentinel your favorite technique
2. Ask it about a security topic you know well
3. Correct it and watch it learn
4. Check the knowledge base with `stats`

**Build These:**
1. Add a new security module
2. Integrate your favorite tool
3. Create custom techniques
4. Extend the CLI

## Development Roadmap

**Current (Phase 1):** Foundation ✓
- Core AI engine
- Memory system
- Basic CLI
- Tool scaffolding

**Next (Phase 2):** Core Capabilities
- Vulnerability scanning
- Web app testing
- Exploitation framework
- Enhanced memory (vector DB)

**Future (Phase 3):** Advanced Features
- Autonomous research
- Multi-agent system
- Evasion engine
- Post-exploitation

**Polish (Phase 4):** Production Ready
- Security hardening
- Professional reporting
- Collaboration features
- Tool ecosystem

## Support

**Documentation:**
- SETUP.md - Installation & configuration
- EXAMPLES.md - Usage examples
- PROJECT_OVERVIEW.md - Architecture
- Code comments - Technical details

**Getting Help:**
- Read the docs
- Check examples
- Review code comments
- Experiment and learn

## Legal Reminder

⚠️ **CRITICAL:** Only use on authorized targets

- Get written authorization
- Define clear scope
- Follow rules of engagement
- Document everything
- Use responsibly

**Unauthorized access is illegal.**

---

## Ready to Start?

```bash
cd sentinel-redteam
./quickstart.sh
source venv/bin/activate
python sentinel.py
```

**Welcome to the future of red teaming. Let's build something amazing.**

---

*Built for security professionals. Use ethically. Test legally. Hack responsibly.*
