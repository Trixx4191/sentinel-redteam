#!/usr/bin/env python3
"""
Sentinel Red Team - Main CLI Interface
Command-line interface for interacting with the AI red team assistant
"""

import os
import sys
import yaml
import asyncio
import argparse
from pathlib import Path
from datetime import datetime

# Load .env file if it exists
from dotenv import load_dotenv
env_path = Path('.env')
if env_path.exists():
    load_dotenv(env_path)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.llm_interface import LLMInterface
from core.memory_system import MemorySystem, Technique


class SentinelCLI:
    """Main CLI interface for Sentinel Red Team"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize components
        print("🔴 Initializing Sentinel Red Team...")
        self.llm = LLMInterface(self.config)
        self.memory = MemorySystem(self.config)
        
        # Load authorization
        self.authorization = self._load_authorization()
        
        print("✓ Sentinel ready\n")
    
    def _load_authorization(self) -> dict:
        """Load authorization configuration"""
        auth_file = Path("config/authorization.yaml")
        if auth_file.exists():
            with open(auth_file, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def check_authorization(self, target: str) -> bool:
        """Check if target is authorized"""
        if not self.config['security']['authorization_required']:
            return True
        
        # Check training environments
        training_envs = self.authorization.get('training_environments', [])
        for env in training_envs:
            for allowed_target in env.get('targets', []):
                if self._match_target(target, allowed_target):
                    return True
        
        # Check active engagements
        engagements = self.authorization.get('engagements', [])
        for eng in engagements:
            if eng.get('status') != 'active':
                continue
            
            scope = eng.get('scope', {})
            in_scope = scope.get('in_scope', [])
            out_of_scope = scope.get('out_of_scope', [])
            
            # Check if in scope
            if any(self._match_target(target, s) for s in in_scope):
                # Check if explicitly out of scope
                if any(self._match_target(target, s) for s in out_of_scope):
                    return False
                return True
        
        return False
    
    def _match_target(self, target: str, pattern: str) -> bool:
        """Simple target matching (can be enhanced)"""
        if pattern == target:
            return True
        if pattern.startswith('*') and target.endswith(pattern[1:]):
            return True
        if '/' in pattern:  # CIDR notation (simplified)
            # TODO: Implement proper CIDR matching
            return target.startswith(pattern.split('/')[0].rsplit('.', 1)[0])
        return False
    
    async def interactive_mode(self):
        """Interactive chat mode with Sentinel"""
        print("=" * 60)
        print("SENTINEL RED TEAM - Interactive Mode")
        print("=" * 60)
        print("Type 'help' for commands, 'exit' to quit")
        print("=" * 60)
        print()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Exiting Sentinel. Stay safe out there.")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.llm.clear_history()
                    continue
                
                elif user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                
                elif user_input.lower().startswith('save'):
                    filepath = user_input.split(maxsplit=1)[1] if len(user_input.split()) > 1 else "conversation.json"
                    self.llm.save_conversation(filepath)
                    continue
                
                elif user_input.lower().startswith('teach'):
                    await self.teach_mode()
                    continue
                
                # Get AI response
                print("\nSentinel: ", end="", flush=True)
                response = await self.llm.chat(user_input)
                print(response.content)
                
                # Show warnings if needed
                if response.requires_authorization:
                    print("\n⚠️  This action requires authorization. Verify target is in scope.")
                
                if response.risk_assessment == 'high':
                    print("\n⚠️  HIGH RISK: This action could have significant impact. Proceed carefully.")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit properly")
                continue
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    async def teach_mode(self):
        """Interactive mode for teaching Sentinel new techniques"""
        print("\n" + "=" * 60)
        print("TEACHING MODE - Teach Sentinel Your Techniques")
        print("=" * 60)
        print()
        
        # Get technique details
        name = input("Technique name: ").strip()
        if not name:
            print("Cancelled.")
            return
        
        category = input("Category (recon/vuln_scan/exploitation/post_exploit): ").strip()
        description = input("Description: ").strip()
        
        print("\nEnter steps (one per line, empty line to finish):")
        steps = []
        while True:
            step = input(f"  Step {len(steps) + 1}: ").strip()
            if not step:
                break
            steps.append(step)
        
        print("\nEnter commands/examples (one per line, empty line to finish):")
        commands = []
        while True:
            cmd = input(f"  Command {len(commands) + 1}: ").strip()
            if not cmd:
                break
            commands.append(cmd)
        
        # Create technique
        technique = Technique(
            id="",
            name=name,
            category=category,
            description=description,
            steps=steps,
            commands=commands,
            prerequisites=[],
            success_indicators=[],
            taught_by="user",
            date_learned=datetime.now().isoformat(),
            tags=[]
        )
        
        # Save technique
        tech_id = self.memory.add_technique(technique)
        
        print(f"\n✓ Technique learned! ID: {tech_id}")
        print(f"Sentinel can now use this technique in future engagements.\n")
    
    def show_help(self):
        """Show help information"""
        print("\n" + "=" * 60)
        print("SENTINEL COMMANDS")
        print("=" * 60)
        print("  help              Show this help message")
        print("  clear             Clear conversation history")
        print("  stats             Show knowledge base statistics")
        print("  save [filename]   Save conversation to file")
        print("  teach             Enter teaching mode to add techniques")
        print("  exit              Exit Sentinel")
        print("=" * 60)
        print()
    
    def show_stats(self):
        """Show knowledge base statistics"""
        stats = self.memory.get_stats()
        
        print("\n" + "=" * 60)
        print("KNOWLEDGE BASE STATISTICS")
        print("=" * 60)
        print(f"  Total techniques:     {stats['total_techniques']}")
        print(f"  User-taught:          {stats['user_techniques']}")
        print(f"  Total engagements:    {stats['total_engagements']}")
        print(f"  Lessons learned:      {stats['total_lessons']}")
        print("\n  By Category:")
        for cat, count in stats['categories'].items():
            print(f"    {cat:20s} {count}")
        print("=" * 60)
        print()
    
    async def single_query(self, query: str):
        """Handle a single query and exit"""
        response = await self.llm.chat(query)
        print(response.content)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Sentinel Red Team - AI-Powered Red Team Assistant"
    )
    parser.add_argument(
        '-c', '--config',
        default='config/settings.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '-q', '--query',
        help='Single query mode (non-interactive)'
    )
    
    args = parser.parse_args()
    
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Initialize CLI
    try:
        cli = SentinelCLI(args.config)
    except Exception as e:
        print(f"❌ Error initializing Sentinel: {e}")
        sys.exit(1)
    
    # Run
    if args.query:
        asyncio.run(cli.single_query(args.query))
    else:
        asyncio.run(cli.interactive_mode())


if __name__ == "__main__":
    main()
