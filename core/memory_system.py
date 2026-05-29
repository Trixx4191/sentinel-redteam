"""
Sentinel Red Team - Memory System
Handles knowledge persistence, learning, and retrieval
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Optional dependencies
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    print("Warning: qdrant-client not installed. Run: pip install qdrant-client")

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("Warning: sentence-transformers not installed. Run: pip install sentence-transformers")


@dataclass
class Technique:
    """Represents a security technique/methodology"""
    id: str
    name: str
    category: str  # recon, vuln_scan, exploitation, post_exploit
    description: str
    steps: List[str]
    commands: List[str]
    prerequisites: List[str]
    success_indicators: List[str]
    taught_by: str  # 'user' or 'system'
    date_learned: str
    success_rate: float = 0.0
    use_count: int = 0
    notes: Optional[str] = None
    related_techniques: List[str] = None
    tags: List[str] = None


@dataclass
class Engagement:
    """Represents a penetration testing engagement"""
    id: str
    target: str
    date: str
    techniques_used: List[str]
    vulnerabilities_found: List[Dict]
    lessons_learned: str
    success: bool


class MemorySystem:
    """
    Knowledge persistence and retrieval system
    Combines vector database (semantic search) with file-based storage
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.knowledge_path = Path(config['learning']['knowledge_path'])
        self.knowledge_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize paths
        self.techniques_file = self.knowledge_path / "techniques.json"
        self.engagements_file = self.knowledge_path / "engagements.json"
        self.lessons_file = self.knowledge_path / "lessons.json"
        
        # Load existing data
        self.techniques: Dict[str, Technique] = self._load_techniques()
        self.engagements: Dict[str, Engagement] = self._load_engagements()
        self.lessons: List[Dict] = self._load_lessons()
        
        # Initialize vector database (optional)
        self.vector_db = None
        self.embedding_model = None
        
        if config['memory']['vector_db']['provider'] == 'qdrant' and QDRANT_AVAILABLE:
            self._initialize_vector_db()
    
    def _initialize_vector_db(self):
        """Initialize Qdrant vector database"""
        try:
            vdb_config = self.config['memory']['vector_db']
            
            self.vector_db = QdrantClient(
                host=vdb_config['host'],
                port=vdb_config['port']
            )
            
            # Initialize embedding model
            if EMBEDDINGS_AVAILABLE:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✓ Initialized embedding model")
            
            # Create collection if it doesn't exist
            collections = self.vector_db.get_collections().collections
            collection_name = vdb_config['collection']
            
            if not any(col.name == collection_name for col in collections):
                self.vector_db.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=384,  # all-MiniLM-L6-v2 dimension
                        distance=Distance.COSINE
                    )
                )
                print(f"✓ Created vector collection: {collection_name}")
            else:
                print(f"✓ Connected to vector collection: {collection_name}")
                
        except Exception as e:
            print(f"Warning: Could not initialize vector DB: {e}")
            self.vector_db = None
    
    def _load_techniques(self) -> Dict[str, Technique]:
        """Load techniques from disk"""
        if self.techniques_file.exists():
            with open(self.techniques_file, 'r') as f:
                data = json.load(f)
                return {
                    tid: Technique(**tech_data)
                    for tid, tech_data in data.items()
                }
        return {}
    
    def _save_techniques(self):
        """Save techniques to disk"""
        data = {
            tid: asdict(tech)
            for tid, tech in self.techniques.items()
        }
        with open(self.techniques_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_engagements(self) -> Dict[str, Engagement]:
        """Load engagements from disk"""
        if self.engagements_file.exists():
            with open(self.engagements_file, 'r') as f:
                data = json.load(f)
                return {
                    eid: Engagement(**eng_data)
                    for eid, eng_data in data.items()
                }
        return {}
    
    def _save_engagements(self):
        """Save engagements to disk"""
        data = {
            eid: asdict(eng)
            for eid, eng in self.engagements.items()
        }
        with open(self.engagements_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_lessons(self) -> List[Dict]:
        """Load lessons learned from disk"""
        if self.lessons_file.exists():
            with open(self.lessons_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_lessons(self):
        """Save lessons to disk"""
        with open(self.lessons_file, 'w') as f:
            json.dump(self.lessons, f, indent=2)
    
    def add_technique(self, technique: Technique) -> str:
        """
        Add a new technique to knowledge base
        
        Args:
            technique: Technique object
        
        Returns:
            technique_id
        """
        # Generate ID if not provided
        if not technique.id:
            technique.id = self._generate_id(technique.name)
        
        # Store in memory
        self.techniques[technique.id] = technique
        self._save_techniques()
        
        # Add to vector database for semantic search
        if self.vector_db and self.embedding_model:
            self._index_technique(technique)
        
        print(f"✓ Learned new technique: {technique.name} ({technique.id})")
        return technique.id
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID for technique"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{name}_{timestamp}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:12]
    
    def _index_technique(self, technique: Technique):
        """Index technique in vector database for semantic search"""
        if not (self.vector_db and self.embedding_model):
            return
        
        try:
            # Create text representation
            text = f"{technique.name}. {technique.description}. "
            text += " ".join(technique.steps)
            
            # Generate embedding
            embedding = self.embedding_model.encode(text).tolist()
            
            # Store in vector DB
            collection_name = self.config['memory']['vector_db']['collection']
            self.vector_db.upsert(
                collection_name=collection_name,
                points=[
                    PointStruct(
                        id=technique.id,
                        vector=embedding,
                        payload={
                            'name': technique.name,
                            'category': technique.category,
                            'description': technique.description,
                            'taught_by': technique.taught_by
                        }
                    )
                ]
            )
        except Exception as e:
            print(f"Warning: Could not index technique: {e}")
    
    def search_techniques(self, query: str, limit: int = 5) -> List[Technique]:
        """
        Semantic search for relevant techniques
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of relevant techniques
        """
        if not (self.vector_db and self.embedding_model):
            # Fallback to simple keyword search
            return self._keyword_search(query, limit)
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search vector DB
            collection_name = self.config['memory']['vector_db']['collection']
            results = self.vector_db.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=limit
            )
            
            # Return techniques
            techniques = []
            for result in results:
                tech_id = result.id
                if tech_id in self.techniques:
                    techniques.append(self.techniques[tech_id])
            
            return techniques
            
        except Exception as e:
            print(f"Warning: Vector search failed: {e}")
            return self._keyword_search(query, limit)
    
    def _keyword_search(self, query: str, limit: int) -> List[Technique]:
        """Fallback keyword-based search"""
        query_lower = query.lower()
        results = []
        
        for tech in self.techniques.values():
            if (query_lower in tech.name.lower() or
                query_lower in tech.description.lower() or
                any(query_lower in step.lower() for step in tech.steps)):
                results.append(tech)
        
        return results[:limit]
    
    def get_technique(self, technique_id: str) -> Optional[Technique]:
        """Get technique by ID"""
        return self.techniques.get(technique_id)
    
    def update_technique_stats(self, technique_id: str, success: bool):
        """Update technique usage statistics"""
        if technique_id in self.techniques:
            tech = self.techniques[technique_id]
            tech.use_count += 1
            
            # Update success rate (moving average)
            if tech.use_count == 1:
                tech.success_rate = 1.0 if success else 0.0
            else:
                weight = 0.8  # Give more weight to recent results
                tech.success_rate = (weight * tech.success_rate + 
                                    (1 - weight) * (1.0 if success else 0.0))
            
            self._save_techniques()
    
    def add_engagement(self, engagement: Engagement):
        """Record a penetration testing engagement"""
        self.engagements[engagement.id] = engagement
        self._save_engagements()
        print(f"✓ Recorded engagement: {engagement.id}")
    
    def add_lesson(self, lesson: str, context: Dict):
        """Add a lesson learned"""
        lesson_entry = {
            'timestamp': datetime.now().isoformat(),
            'lesson': lesson,
            'context': context
        }
        self.lessons.append(lesson_entry)
        self._save_lessons()
        print(f"✓ Recorded lesson learned")
    
    def get_user_techniques(self) -> List[Technique]:
        """Get all techniques taught by user"""
        return [
            tech for tech in self.techniques.values()
            if tech.taught_by == 'user'
        ]
    
    def get_techniques_by_category(self, category: str) -> List[Technique]:
        """Get techniques by category"""
        return [
            tech for tech in self.techniques.values()
            if tech.category == category
        ]
    
    def export_knowledge_base(self, filepath: str):
        """Export entire knowledge base to file"""
        data = {
            'techniques': {tid: asdict(tech) for tid, tech in self.techniques.items()},
            'engagements': {eid: asdict(eng) for eid, eng in self.engagements.items()},
            'lessons': self.lessons,
            'export_date': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Knowledge base exported to {filepath}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        return {
            'total_techniques': len(self.techniques),
            'user_techniques': len(self.get_user_techniques()),
            'total_engagements': len(self.engagements),
            'total_lessons': len(self.lessons),
            'categories': {
                'recon': len(self.get_techniques_by_category('recon')),
                'vuln_scan': len(self.get_techniques_by_category('vuln_scan')),
                'exploitation': len(self.get_techniques_by_category('exploitation')),
                'post_exploit': len(self.get_techniques_by_category('post_exploit'))
            }
        }


# Example usage
if __name__ == "__main__":
    import yaml
    
    # Load config
    with open('../config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize memory system
    memory = MemorySystem(config)
    
    # Example: Add a technique
    technique = Technique(
        id="",
        name="SQL Injection via Error-Based",
        category="exploitation",
        description="Extract data using error messages in SQL queries",
        steps=[
            "Identify injectable parameter",
            "Test with single quote to trigger error",
            "Use UNION-based extraction if possible",
            "Fall back to error-based if UNION blocked",
            "Extract data using EXTRACTVALUE or similar"
        ],
        commands=[
            "' OR 1=1--",
            "' UNION SELECT NULL,NULL--",
            "' AND EXTRACTVALUE(1,CONCAT(0x7e,database()))--"
        ],
        prerequisites=["Web application with SQL backend", "Error messages visible"],
        success_indicators=["Database error in response", "Data extracted"],
        taught_by="system",
        date_learned=datetime.now().isoformat(),
        tags=["sqli", "web", "injection"]
    )
    
    tech_id = memory.add_technique(technique)
    print(f"\nTechnique ID: {tech_id}")
    
    # Search for techniques
    results = memory.search_techniques("sql injection")
    print(f"\nFound {len(results)} techniques matching 'sql injection'")
    
    # Get stats
    stats = memory.get_stats()
    print(f"\nKnowledge base stats:")
    print(json.dumps(stats, indent=2))
