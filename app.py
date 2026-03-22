import streamlit as st
import requests
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime
import spacy
from transformers import pipeline
import torch
from neo4j import GraphDatabase
import os
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
import sqlite3

# Custom CSS for professional sleek UI
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    /* Auth styling */
    .auth-container {
        background: white;
        padding: 3rem 2.5rem;
        border-radius: 16px;
        margin: 2rem auto;
        max-width: 480px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 1px solid #e8ecef;
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-header h2 {
        color: #2d3748;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .auth-input {
        width: 100%;
        padding: 14px 16px;
        margin: 8px 0;
        border: 1.5px solid #e2e8f0;
        border-radius: 10px;
        font-size: 0.95rem;
        background: #fafbfc;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .auth-input:focus {
        border-color: #667eea;
        background: white;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .auth-button {
        width: 100%;
        padding: 14px;
        margin: 12px 0;
        border: none;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .auth-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    .auth-switch {
        text-align: center;
        margin-top: 1.5rem;
        color: #64748b;
    }
    
    .auth-switch a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
        transition: color 0.2s ease;
    }
    
    .auth-switch a:hover {
        color: #5a67d8;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        margin: 0.5rem 0;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .feature-card {
        background: white;
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-color: #667eea;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f8fafc;
        padding: 4px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background: transparent;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 500;
        border: none;
        color: #64748b;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 18px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 18px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    .status-danger {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 18px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    /* Graph container */
    .graph-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        margin: 1rem 0;
    }
    
    /* Search result styling */
    .search-result {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .search-result:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .similarity-score {
        background: #667eea;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* User info styling */
    .user-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .admin-badge {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 18px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Section headers */
    .section-header {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.25rem;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 0.5rem;
    }
    
    /* Quick stats */
    .quick-stat {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
    }
    
    .quick-stat h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .quick-stat p {
        margin: 0.5rem 0 0 0;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Source badges */
    .source-badge {
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-wikipedia { background: #10b981; color: white; }
    .badge-arxiv { background: #3b82f6; color: white; }
    .badge-user { background: #f59e0b; color: white; }
    .badge-file { background: #8b5cf6; color: white; }
</style>
""", unsafe_allow_html=True)

class AuthManager:
    def __init__(self):
        self.secret_key = "health_data_nlp_secret_key_2024"
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database for users"""
        conn = sqlite3.connect('health_users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create admin user if not exists
        c.execute('SELECT id FROM users WHERE username = ?', ('admin',))
        if not c.fetchone():
            admin_password_hash = self.hash_password('admin123')
            c.execute(
                'INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)',
                ('admin', admin_password_hash, 'admin@healthdata.com', 'admin')
            )
        
        # Create usage_stats table for admin dashboard
        c.execute('''
            CREATE TABLE IF NOT EXISTS usage_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action_type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str = "") -> Dict[str, Any]:
        """Register a new user"""
        try:
            conn = sqlite3.connect('health_users.db')
            c = conn.cursor()
            
            # Check if user exists
            c.execute('SELECT id FROM users WHERE username = ?', (username,))
            if c.fetchone():
                return {"success": False, "error": "Username already exists"}
            
            # Hash password and insert user
            password_hash = self.hash_password(password)
            c.execute(
                'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                (username, password_hash, email)
            )
            
            # Log registration
            user_id = c.lastrowid
            c.execute(
                'INSERT INTO usage_stats (user_id, action_type, details) VALUES (?, ?, ?)',
                (user_id, 'registration', f'User {username} registered')
            )
            
            conn.commit()
            conn.close()
            
            return {"success": True, "message": "User registered successfully"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Login user and return JWT token"""
        try:
            conn = sqlite3.connect('health_users.db')
            c = conn.cursor()
            
            # Get user data
            c.execute('SELECT id, username, password_hash, role, is_active FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            
            if not user:
                return {"success": False, "error": "Invalid username or password"}
            
            user_id, username, password_hash, role, is_active = user
            
            if not is_active:
                return {"success": False, "error": "Account is deactivated"}
            
            # Verify password
            password_hash_input = self.hash_password(password)
            if password_hash != password_hash_input:
                return {"success": False, "error": "Invalid username or password"}
            
            # Update last login
            c.execute(
                'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
                (user_id,)
            )
            
            # Log login
            c.execute(
                'INSERT INTO usage_stats (user_id, action_type, details) VALUES (?, ?, ?)',
                (user_id, 'login', f'User {username} logged in')
            )
            
            conn.commit()
            conn.close()
            
            # Generate JWT token
            token_payload = {
                'user_id': user_id,
                'username': username,
                'role': role,
                'exp': datetime.utcnow() + timedelta(days=7)
            }
            
            token = jwt.encode(token_payload, self.secret_key, algorithm='HS256')
            
            return {
                "success": True, 
                "token": token,
                "user": {
                    "id": user_id,
                    "username": username,
                    "role": role
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {"success": True, "user": payload}
        except jwt.ExpiredSignatureError:
            return {"success": False, "error": "Token expired"}
        except jwt.InvalidTokenError:
            return {"success": False, "error": "Invalid token"}
    
    def get_all_users(self) -> List[Dict]:
        """Get all users for admin dashboard"""
        conn = sqlite3.connect('health_users.db')
        c = conn.cursor()
        c.execute('''
            SELECT id, username, email, role, is_active, created_at, last_login 
            FROM users ORDER BY created_at DESC
        ''')
        users = c.fetchall()
        conn.close()
        
        return [
            {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3],
                "is_active": bool(user[4]),
                "created_at": user[5],
                "last_login": user[6]
            }
            for user in users
        ]
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for admin dashboard"""
        conn = sqlite3.connect('health_users.db')
        c = conn.cursor()
        
        # Total users
        c.execute('SELECT COUNT(*) FROM users')
        total_users = c.fetchone()[0]
        
        # Active users
        c.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
        active_users = c.fetchone()[0]
        
        # Admin users
        c.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
        admin_users = c.fetchone()[0]
        
        # Recent registrations (last 7 days)
        c.execute('''
            SELECT COUNT(*) FROM users 
            WHERE DATE(created_at) >= DATE("now", "-7 days")
        ''')
        recent_registrations = c.fetchone()[0]
        
        # User activity by day
        c.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as activity_count
            FROM usage_stats 
            WHERE timestamp >= DATE("now", "-30 days")
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
            LIMIT 30
        ''')
        daily_activity = c.fetchall()
        
        # Action types distribution
        c.execute('''
            SELECT action_type, COUNT(*) as count
            FROM usage_stats 
            GROUP BY action_type
            ORDER BY count DESC
        ''')
        action_distribution = c.fetchall()
        
        conn.close()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "admin_users": admin_users,
            "recent_registrations": recent_registrations,
            "daily_activity": daily_activity,
            "action_distribution": action_distribution
        }
    
    def update_user_role(self, user_id: int, new_role: str) -> bool:
        """Update user role (admin only)"""
        try:
            conn = sqlite3.connect('health_users.db')
            c = conn.cursor()
            c.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def toggle_user_status(self, user_id: int) -> bool:
        """Toggle user active status (admin only)"""
        try:
            conn = sqlite3.connect('health_users.db')
            c = conn.cursor()
            c.execute('UPDATE users SET is_active = NOT is_active WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def log_user_action(self, user_id: int, action_type: str, details: str = ""):
        """Log user actions for analytics"""
        try:
            conn = sqlite3.connect('health_users.db')
            c = conn.cursor()
            c.execute(
                'INSERT INTO usage_stats (user_id, action_type, details) VALUES (?, ?, ?)',
                (user_id, action_type, details)
            )
            conn.commit()
            conn.close()
        except:
            pass

# Initialize NLP models
@st.cache_resource
def load_models():
    """Load spaCy and transformer models"""
    try:
        # Load spaCy model
        nlp = spacy.load("en_core_web_sm")
        
        # Try to load a medical NER model, fallback to general NER
        try:
            # This is a general medical NER model
            medical_ner = pipeline(
                "ner",
                model="dmis-lab/biobert-v1.1",  # Medical BERT model
                aggregation_strategy="simple"
            )
        except:
            # Fallback to general NER
            medical_ner = pipeline("ner", aggregation_strategy="simple")
        
        # Load sentence transformer for semantic search
        try:
            semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            semantic_model = None
        
        return nlp, medical_ner, semantic_model
        
    except Exception as e:
        return None, None, None

class SemanticSearchModule:
    def __init__(self, semantic_model):
        self.semantic_model = semantic_model
        self.document_embeddings = None
        self.documents = []
        self.is_indexed = False
        
    def index_documents(self, documents: List[Dict]):
        """Index documents for semantic search"""
        if not self.semantic_model:
            return False
            
        self.documents = documents
        document_texts = [f"{doc['topic']}. {doc['content'][:500]}" for doc in documents]
        self.document_embeddings = self.semantic_model.encode(document_texts)
        self.is_indexed = True
        return True
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Perform semantic search on indexed documents"""
        if not self.semantic_model or not self.is_indexed:
            return []
            
        query_embedding = self.semantic_model.encode([query])
        similarities = cosine_similarity(query_embedding, self.document_embeddings)[0]
        
        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append({
                    'document': self.documents[idx],
                    'similarity_score': float(similarities[idx]),
                    'rank': len(results) + 1
                })
        
        return results
    
    def search_triples(self, query: str, triples: List[Dict], top_k: int = 10) -> List[Dict]:
        """Search through knowledge graph triples"""
        if not self.semantic_model:
            return []
            
        # Create text representations of triples
        triple_texts = []
        for triple in triples:
            text = f"{triple['subject']} {triple['predicate']} {triple['object']}"
            if 'source_sentence' in triple:
                text += f". Context: {triple['source_sentence']}"
            triple_texts.append(text)
        
        if not triple_texts:
            return []
            
        triple_embeddings = self.semantic_model.encode(triple_texts)
        query_embedding = self.semantic_model.encode([query])
        similarities = cosine_similarity(query_embedding, triple_embeddings)[0]
        
        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append({
                    'triple': triples[idx],
                    'similarity_score': float(similarities[idx]),
                    'rank': len(results) + 1
                })
        
        return results

class HealthDataNLPPlatform:
    def __init__(self):
        self.nlp, self.ner_pipeline, self.semantic_model = load_models()
        self.neo4j_driver = None
        self.topics = []
        self.retrieved_data = []
        self.extracted_triples = []
        self.cross_domain_relations = []
        self.semantic_search = SemanticSearchModule(self.semantic_model)
        self.auth_manager = AuthManager()
        
    def add_topic(self, topic: str):
        if topic and topic not in self.topics:
            self.topics.append(topic)
            
    def remove_topic(self, topic: str):
        if topic in self.topics:
            self.topics.remove(topic)
    
    def fetch_wikipedia_data(self, topic: str) -> List[Dict]:
        """Fetch data from Wikipedia API with better error handling"""
        try:
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': topic,
                'utf8': 1,
                'formatversion': 2
            }
            
            headers = {
                'User-Agent': 'HealthDataNLPPlatform/1.0 (https://example.com)',
                'Accept': 'application/json'
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return [self._create_sample_data(topic, "wikipedia")]
                
            data = response.json()
            
            if 'query' not in data or 'search' not in data['query'] or not data['query']['search']:
                return [self._create_sample_data(topic, "wikipedia")]
                
            results = []
            for item in data['query']['search'][:2]:
                content_url = "https://en.wikipedia.org/w/api.php"
                content_params = {
                    'action': 'query',
                    'format': 'json',
                    'prop': 'extracts',
                    'exintro': True,
                    'explaintext': True,
                    'titles': item['title'],
                    'utf8': 1,
                    'formatversion': 2
                }
                
                content_response = requests.get(content_url, params=content_params, headers=headers, timeout=10)
                
                if content_response.status_code == 200:
                    content_data = content_response.json()
                    if 'query' in content_data and 'pages' in content_data['query']:
                        page = content_data['query']['pages'][0] if content_data['query']['pages'] else {}
                        page_content = page.get('extract', f"Content about {item['title']}")
                    else:
                        page_content = f"Content about {item['title']}"
                else:
                    page_content = f"Content about {item['title']}"
                
                results.append({
                    "source": "wikipedia",
                    "topic": item['title'],
                    "content": page_content,
                    "url": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                    "timestamp": datetime.now().isoformat(),
                    "domain": topic
                })
                
            return results
            
        except Exception as e:
            return [self._create_sample_data(topic, "wikipedia")]
    
    def fetch_arxiv_data(self, topic: str) -> List[Dict]:
        """Fetch data from ArXiv API with better error handling"""
        try:
            url = f"http://export.arxiv.org/api/query?search_query=all:{topic}&start=0&max_results=3"
            headers = {
                'User-Agent': 'HealthDataNLPPlatform/1.0 (https://example.com)'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            
            if not entries:
                return [self._create_sample_data(topic, "arxiv")]
                
            results = []
            for entry in entries[:2]:
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                
                title = title_elem.text if title_elem is not None else f"{topic} Research"
                summary = summary_elem.text if summary_elem is not None else f"Research about {topic}"
                url = id_elem.text if id_elem is not None else f"https://arxiv.org/search/?query={topic}"
                
                results.append({
                    "source": "arxiv",
                    "topic": title,
                    "content": summary,
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "domain": topic
                })
                
            return results
            
        except Exception as e:
            return [self._create_sample_data(topic, "arxiv")]
    
    def process_user_text_input(self, topic: str, text: str) -> Dict:
        """Process user-provided text input"""
        return {
            "source": "user_input",
            "topic": f"{topic} - User Provided",
            "content": text,
            "url": "user_input",
            "timestamp": datetime.now().isoformat(),
            "domain": topic
        }

    def process_uploaded_file(self, topic: str, uploaded_file) -> Dict:
        """Process user-uploaded file"""
        try:
            # Read file content based on file type
            if uploaded_file.type == "text/plain":
                content = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                # For simplicity, we'll treat all as text for now
                # In production, you'd use libraries like PyPDF2 or python-docx
                content = str(uploaded_file.read(), "utf-8", errors='ignore')
            else:
                content = f"Content from file: {uploaded_file.name}"
            
            return {
                "source": "file_upload",
                "topic": f"{topic} - {uploaded_file.name}",
                "content": content,
                "url": f"uploaded_file_{uploaded_file.name}",
                "timestamp": datetime.now().isoformat(),
                "domain": topic
            }
        except Exception as e:
            return {
                "source": "file_upload",
                "topic": f"{topic} - {uploaded_file.name}",
                "content": f"Error processing file: {str(e)}",
                "url": "error",
                "timestamp": datetime.now().isoformat(),
                "domain": topic
            }
    
    def _create_sample_data(self, topic: str, source: str) -> Dict:
        """Create realistic sample medical data"""
        sample_content = self._get_sample_content(topic)
        
        source_display = {
            "wikipedia": "Wikipedia",
            "arxiv": "ArXiv Research", 
            "user_input": "User Provided",
            "file_upload": "Uploaded File"
        }
        
        return {
            "source": source,
            "topic": f"{topic} - {source_display.get(source, 'Medical Information')}",
            "content": sample_content,
            "url": f"https://example.com/{source}/{topic}",
            "timestamp": datetime.now().isoformat(),
            "domain": topic
        }
    
    def _get_sample_content(self, topic: str) -> str:
        """Get comprehensive sample medical content for a topic"""
        samples = {
            'diabetes': """
            Diabetes mellitus is a chronic metabolic disorder characterized by high blood sugar levels over a prolonged period. 
            There are two main types: Type 1 diabetes results from the pancreas's failure to produce enough insulin, while Type 2 diabetes begins with insulin resistance. 
            Common symptoms include increased thirst, frequent urination, and unexplained weight loss. 
            Long-term complications include cardiovascular disease, stroke, chronic kidney disease, foot ulcers, and damage to the eyes.
            Treatment involves lifestyle modifications, oral medications like metformin, and insulin therapy. Regular monitoring of blood glucose levels is essential for management.
            Recent studies show that continuous glucose monitoring systems significantly improve glycemic control in Type 1 diabetes patients.
            Metformin is commonly prescribed to treat Type 2 diabetes by improving insulin sensitivity.
            Insulin injections are used to treat Type 1 diabetes and advanced Type 2 diabetes.
            Diabetes causes frequent urination and increased thirst as primary symptoms.
            High blood sugar levels in diabetes can lead to cardiovascular disease and kidney damage.
            """,
            
            'cardiology': """
            Cardiology is the branch of medicine that deals with disorders of the heart and blood vessels. 
            Common cardiovascular diseases include coronary artery disease, heart failure, valvular heart disease, and arrhythmias.
            Symptoms of heart disease may include chest pain, shortness of breath, palpitations, and edema. 
            Diagnostic methods include electrocardiogram (ECG), echocardiogram, and cardiac stress tests.
            Treatments range from lifestyle changes and medications like beta-blockers and statins to surgical interventions such as angioplasty and bypass surgery.
            New research in cardiology focuses on regenerative medicine and stem cell therapy for heart repair.
            Aspirin is often used to prevent heart attacks in patients with cardiovascular disease.
            Beta-blockers treat high blood pressure and heart rhythm disorders.
            Chest pain is a common symptom of coronary artery disease.
            Shortness of breath can indicate heart failure or other cardiac conditions.
            """,
            
            'cancer': """
            Cancer is a group of diseases involving abnormal cell growth with the potential to invade or spread to other parts of the body. 
            Common types include breast cancer, lung cancer, prostate cancer, and colorectal cancer.
            Symptoms vary depending on the type and location of cancer but may include lumps, abnormal bleeding, prolonged cough, and unexplained weight loss.
            Treatment options include surgery, chemotherapy, radiation therapy, immunotherapy, and targeted therapy. 
            Early detection through screening programs significantly improves treatment outcomes and survival rates.
            Immunotherapy has revolutionized cancer treatment by harnessing the body's immune system to fight cancer cells.
            Chemotherapy drugs like cisplatin are used to treat various types of cancer.
            Radiation therapy targets and destroys cancer cells in specific areas.
            Unexplained weight loss is often a symptom of advanced cancer.
            Persistent cough can be a sign of lung cancer.
            """,
            
            'fever': """
            Fever, also known as pyrexia, is defined as having a temperature above the normal range due to an increase in the body's temperature set point. 
            Common causes include infections such as influenza, COVID-19, urinary tract infections, and pneumonia.
            Symptoms often accompany fever including sweating, chills, headache, muscle aches, and loss of appetite.
            Treatment focuses on the underlying cause and may include antipyretic medications like acetaminophen or ibuprofen. 
            High fevers or fevers in infants require medical attention to rule out serious conditions.
            Research shows that fever plays a beneficial role in fighting infections by enhancing immune response.
            Ibuprofen effectively reduces fever and relieves associated pain.
            Acetaminophen is commonly used to treat fever and mild to moderate pain.
            Influenza virus causes fever and respiratory symptoms.
            Headache and muscle aches are common symptoms of fever.
            """,
            
            'mental health': """
            Mental health encompasses emotional, psychological, and social well-being. It affects how people think, feel, and act. 
            Common mental health disorders include depression, anxiety disorders, bipolar disorder, and schizophrenia.
            Symptoms vary by disorder but may include persistent sadness, excessive fears or worries, extreme mood changes, and social withdrawal.
            Treatment approaches include psychotherapy, medication (such as antidepressants and antipsychotics), and lifestyle modifications. 
            Early intervention and comprehensive care are crucial for effective management of mental health conditions.
            Digital mental health interventions are becoming increasingly important for improving access to care.
            Antidepressants like fluoxetine are prescribed to treat depression and anxiety disorders.
            Psychotherapy helps patients develop coping strategies for mental health challenges.
            Depression causes persistent sadness and loss of interest in activities.
            Anxiety disorders produce excessive worry and physical symptoms like palpitations.
            """,
            
            'covid': """
            COVID-19 is an infectious disease caused by the SARS-CoV-2 virus. The disease was first identified in December 2019 in Wuhan, China.
            Common symptoms include fever, cough, fatigue, breathing difficulties, and loss of taste or smell. 
            Severe cases can lead to pneumonia, acute respiratory distress syndrome, and multi-organ failure.
            Prevention methods include vaccination, mask-wearing, physical distancing, and hand hygiene.
            Treatments include antiviral medications, corticosteroids, and monoclonal antibodies. Long-term effects may persist for months after recovery.
            Ongoing research focuses on understanding long COVID and developing next-generation vaccines.
            Remdesivir is an antiviral medication used to treat COVID-19 in hospitalized patients.
            Corticosteroids like dexamethasone reduce inflammation in severe COVID-19 cases.
            SARS-CoV-2 virus causes COVID-19 and its associated symptoms.
            Loss of taste and smell are distinctive symptoms of COVID-19 infection.
            """
        }
        
        topic_lower = topic.lower()
        for key, content in samples.items():
            if key in topic_lower:
                return content
                
        return f"""
        {topic.title()} is a significant healthcare domain involving various medical conditions, treatments, and research areas. 
        This field encompasses multiple aspects including disease mechanisms, diagnostic approaches, therapeutic interventions, and patient care strategies.
        Common medical entities in this domain include symptoms, diagnostic tests, medications, treatment protocols, and healthcare providers.
        Ongoing research continues to advance our understanding and improve clinical outcomes in this important area of medicine.
        Recent developments include new diagnostic technologies, innovative treatment approaches, and enhanced understanding of disease pathophysiology.
        """
    
    def extract_entities_hybrid(self, text: str) -> List[Dict]:
        """Hybrid entity extraction using spaCy NER + transformer NER + medical patterns"""
        entities = []
        
        # 1. Use spaCy NER if available
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                # Map spaCy entities to medical categories - EXCLUDE DATE and LOCATION
                medical_label = self._map_spacy_to_medical(ent.label_)
                if medical_label and medical_label not in ['DATE', 'LOCATION']:  # Exclude these entities
                    entities.append({
                        "text": ent.text,
                        "label": medical_label,
                        "start_char": ent.start_char,
                        "end_char": ent.end_char,
                        "confidence": 0.8,
                        "source": "spacy"
                    })
        
        # 2. Use transformer NER if available
        if self.ner_pipeline and len(text) < 512:  # Limit text length for transformers
            try:
                ner_results = self.ner_pipeline(text)
                for result in ner_results:
                    medical_label = self._map_ner_to_medical(result['entity_group'])
                    if medical_label and medical_label not in ['DATE', 'LOCATION']:  # Exclude these entities
                        entities.append({
                            "text": result['word'],
                            "label": medical_label,
                            "start_char": result['start'],
                            "end_char": result['end'],
                            "confidence": result['score'],
                            "source": "transformer"
                        })
            except Exception as e:
                pass
        
        # 3. Use medical patterns as fallback/enhancement
        pattern_entities = self._extract_entities_with_patterns(text)
        entities.extend(pattern_entities)
        
        # Remove duplicates (prefer higher confidence sources)
        return self._deduplicate_entities(entities)
    
    def _map_spacy_to_medical(self, spacy_label: str) -> str:
        """Map spaCy entity labels to medical categories"""
        mapping = {
            'DISEASE': 'DISEASE',
            'MEDICAL_CONDITION': 'DISEASE',
            'PERSON': 'PERSON',  # Doctors, researchers
            'ORG': 'ORGANIZATION',  # Hospitals, research institutions
            'GPE': 'LOCATION',  # Locations - will be excluded
            'DATE': 'DATE',  # Will be excluded
            'TIME': 'TIME'  # Will be excluded
        }
        return mapping.get(spacy_label, '')
    
    def _map_ner_to_medical(self, ner_label: str) -> str:
        """Map transformer NER labels to medical categories"""
        mapping = {
            'DISEASE': 'DISEASE',
            'SYMPTOM': 'SYMPTOM',
            'TREATMENT': 'TREATMENT',
            'MEDICATION': 'MEDICATION',
            'ANATOMY': 'ANATOMY',
            'PROCEDURE': 'TREATMENT'
        }
        return mapping.get(ner_label, ner_label)
    
    def _extract_entities_with_patterns(self, text: str) -> List[Dict]:
        """Enhanced medical entity patterns"""
        entities = []
        
        medical_patterns = [
            # Diseases and Conditions
            {'pattern': r'\b(?:type\s+)?(?:type\s+[12]\s+)?diabetes(?:\s+mellitus)?\b', 'label': 'DISEASE', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:heart\s+disease|cardiovascular\s+disease|coronary\s+artery\s+disease)\b', 'label': 'DISEASE', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:cancer|malignancy|tumor|carcinoma|leukemia|lymphoma)\b', 'label': 'DISEASE', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:COVID-19|coronavirus|SARS-CoV-2)\b', 'label': 'DISEASE', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:hypertension|high\s+blood\s+pressure)\b', 'label': 'DISEASE', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:asthma|COPD|chronic\s+obstructive\s+pulmonary\s+disease)\b', 'label': 'DISEASE', 'flags': re.IGNORECASE},
            
            # Symptoms
            {'pattern': r'\b(?:fever|pyrexia)\b', 'label': 'SYMPTOM', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:pain|ache|hurts|sore)\b', 'label': 'SYMPTOM', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:fatigue|tiredness|exhaustion)\b', 'label': 'SYMPTOM', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:cough|sneeze)\b', 'label': 'SYMPTOM', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:shortness of breath|dyspnea|breathing difficulty)\b', 'label': 'SYMPTOM', 'flags': re.IGNORECASE},
            
            # Medications
            {'pattern': r'\b(?:insulin|metformin|glipizide)\b', 'label': 'MEDICATION', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:aspirin|ibuprofen|paracetamol|acetaminophen)\b', 'label': 'MEDICATION', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:atorvastatin|simvastatin|rosuvastatin)\b', 'label': 'MEDICATION', 'flags': re.IGNORECASE},
            
            # Treatments
            {'pattern': r'\b(?:surgery|operation)\b', 'label': 'TREATMENT', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:chemotherapy|radiation|radiotherapy)\b', 'label': 'TREATMENT', 'flags': re.IGNORECASE},
            {'pattern': r'\b(?:therapy|psychotherapy|counseling)\b', 'label': 'TREATMENT', 'flags': re.IGNORECASE},
        ]
        
        for pattern_info in medical_patterns:
            flags = pattern_info.get('flags', 0)
            matches = re.finditer(pattern_info['pattern'], text, flags)
            for match in matches:
                entities.append({
                    "text": match.group(),
                    "label": pattern_info['label'],
                    "start_char": match.start(),
                    "end_char": match.end(),
                    "confidence": 0.85,
                    "source": "pattern"
                })
        
        return entities
    
    def _deduplicate_entities(self, entities: List[Dict]) -> List[Dict]:
        """Remove duplicate entities, keeping the highest confidence version"""
        unique_entities = []
        seen = set()
        
        # Sort by confidence (highest first)
        entities.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        for entity in entities:
            key = (entity['text'].lower(), entity['label'])
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities
    
    def extract_relations_advanced(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Advanced relation extraction using multiple NLP techniques"""
        relations = []
        
        if self.nlp:
            # Method 1: Dependency parsing with enhanced patterns
            relations.extend(self._extract_relations_dependency(text, entities))
            
            # Method 2: Semantic role labeling approximation
            relations.extend(self._extract_relations_semantic(text, entities))
            
            # Method 3: Pattern-based with medical context
            relations.extend(self._extract_relations_medical_patterns(text, entities))
        
        # Remove duplicates and low-confidence relations
        return self._filter_relations(relations)
    
    def _extract_relations_dependency(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Enhanced dependency parsing for relation extraction"""
        relations = []
        doc = self.nlp(text)
        
        for sent in doc.sents:
            sent_entities = [e for e in entities if e['text'].lower() in sent.text.lower()]
            
            if len(sent_entities) < 2:
                continue
                
            # Extract subject-verb-object triples
            for token in sent:
                if token.pos_ == "VERB":
                    subject = self._find_subject(token)
                    obj = self._find_object(token)
                    
                    if subject and obj:
                        subj_entity = self._find_matching_entity(subject.text, sent_entities)
                        obj_entity = self._find_matching_entity(obj.text, sent_entities)
                        
                        if subj_entity and obj_entity:
                            relation_type = self._classify_relation_type(token.lemma_, subj_entity, obj_entity, sent.text)
                            confidence = self._calculate_relation_confidence(token, subj_entity, obj_entity, sent.text)
                            
                            if relation_type and confidence > 0.3:
                                relations.append({
                                    "entity1": subj_entity["text"],
                                    "entity2": obj_entity["text"],
                                    "relation": relation_type,
                                    "sentence": sent.text,
                                    "confidence": confidence,
                                    "entity1Type": subj_entity["label"],
                                    "entity2Type": obj_entity["label"],
                                    "source": "dependency"
                                })
        
        return relations
    
    def _find_subject(self, verb_token):
        """Find subject of a verb"""
        for child in verb_token.children:
            if child.dep_ in ["nsubj", "nsubjpass", "agent"]:
                return child
        return None
    
    def _find_object(self, verb_token):
        """Find object of a verb"""
        for child in verb_token.children:
            if child.dep_ in ["dobj", "attr", "prep", "acomp"]:
                return child
        return None
    
    def _find_matching_entity(self, text: str, entities: List[Dict]):
        """Find entity that matches the text"""
        for entity in entities:
            if entity['text'].lower() in text.lower() or text.lower() in entity['text'].lower():
                return entity
        return None
    
    def _classify_relation_type(self, verb: str, entity1: Dict, entity2: Dict, sentence: str) -> str:
        """Classify relation type based on verb and entity types"""
        verb = verb.lower()
        sentence_lower = sentence.lower()
        
        # Treatment relations
        treatment_verbs = {"treat", "cure", "heal", "medicate", "prescribe", "administer", "use", "take"}
        if verb in treatment_verbs:
            if (entity1["label"] in ["MEDICATION", "TREATMENT"] and entity2["label"] == "DISEASE"):
                return "TREATS"
            elif (entity2["label"] in ["MEDICATION", "TREATMENT"] and entity1["label"] == "DISEASE"):
                return "TREATED_BY"
        
        # Cause relations
        cause_verbs = {"cause", "trigger", "lead", "result", "produce", "induce"}
        if verb in cause_verbs:
            if any(word in sentence_lower for word in ["cause", "trigger", "lead to", "result in"]):
                return "CAUSES"
        
        # Symptom relations
        symptom_verbs = {"show", "present", "experience", "feel", "have", "include", "manifest"}
        if verb in symptom_verbs:
            if (entity1["label"] == "DISEASE" and entity2["label"] == "SYMPTOM"):
                if any(word in sentence_lower for word in ["symptoms", "signs", "manifest"]):
                    return "HAS_SYMPTOM"
            elif (entity2["label"] == "DISEASE" and entity1["label"] == "SYMPTOM"):
                if any(word in sentence_lower for word in ["symptom of", "sign of"]):
                    return "SYMPTOM_OF"
        
        # Prevention relations
        prevention_verbs = {"prevent", "protect", "avoid", "reduce", "lower"}
        if verb in prevention_verbs:
            return "PREVENTS"
        
        # Diagnosis relations
        diagnosis_verbs = {"diagnose", "detect", "identify", "test", "screen"}
        if verb in diagnosis_verbs:
            return "DIAGNOSES"
        
        return "RELATED_TO"
    
    def _extract_relations_semantic(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Semantic pattern-based relation extraction"""
        relations = []
        doc = self.nlp(text)
        
        # Medical relation patterns
        patterns = [
            # Treatment patterns
            (r"(\w+)\s+(treats?|is used for|is prescribed for)\s+(\w+)", "TREATS"),
            (r"(\w+)\s+(is treated with|is managed with)\s+(\w+)", "TREATED_BY"),
            (r"(\w+)\s+(therapy|treatment)\s+for\s+(\w+)", "TREATS"),
            
            # Symptom patterns
            (r"(\w+)\s+(symptoms? include|signs? include|manifests as)\s+(\w+)", "HAS_SYMPTOM"),
            (r"(\w+)\s+(is a symptom of|is a sign of)\s+(\w+)", "SYMPTOM_OF"),
            
            # Cause patterns
            (r"(\w+)\s+(causes?|leads to|results in)\s+(\w+)", "CAUSES"),
            (r"(\w+)\s+(is caused by|is due to)\s+(\w+)", "CAUSED_BY"),
            
            # Prevention patterns
            (r"(\w+)\s+(prevents?|protects against)\s+(\w+)", "PREVENTS"),
            (r"(\w+)\s+(is prevented by)\s+(\w+)", "PREVENTED_BY"),
        ]
        
        for sent in doc.sents:
            sent_text = sent.text
            sent_entities = [e for e in entities if e['text'].lower() in sent_text.lower()]
            
            if len(sent_entities) >= 2:
                for pattern, relation_type in patterns:
                    matches = re.finditer(pattern, sent_text, re.IGNORECASE)
                    for match in matches:
                        entity1_text = match.group(1)
                        entity2_text = match.group(3)
                        
                        entity1 = self._find_matching_entity(entity1_text, sent_entities)
                        entity2 = self._find_matching_entity(entity2_text, sent_entities)
                        
                        if entity1 and entity2:
                            relations.append({
                                "entity1": entity1["text"],
                                "entity2": entity2["text"],
                                "relation": relation_type,
                                "sentence": sent_text,
                                "confidence": 0.7,
                                "entity1Type": entity1["label"],
                                "entity2Type": entity2["label"],
                                "source": "semantic"
                            })
        
        return relations
    
    def _extract_relations_medical_patterns(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Medical-specific relation patterns"""
        relations = []
        sentences = re.split(r'[.!?]+', text)
        
        medical_contexts = {
            "treats": ["treat", "used for", "prescribed for", "therapy for", "medication for"],
            "causes": ["cause", "lead to", "result in", "trigger", "produce"],
            "symptoms": ["symptom", "sign", "manifest", "present with", "experience"],
            "prevents": ["prevent", "protect against", "reduce risk of", "lower chance of"]
        }
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
                
            sentence_entities = [e for e in entities if e['text'].lower() in sentence.lower()]
            
            if len(sentence_entities) >= 2:
                sentence_lower = sentence.lower()
                
                # Check for each relation type
                for rel_type, triggers in medical_contexts.items():
                    for trigger in triggers:
                        if trigger in sentence_lower:
                            # Find entities around the trigger
                            for i in range(len(sentence_entities)):
                                for j in range(i + 1, len(sentence_entities)):
                                    entity1 = sentence_entities[i]
                                    entity2 = sentence_entities[j]
                                    
                                    # Determine direction based on entity types and context
                                    final_rel_type = self._determine_relation_direction(rel_type, entity1, entity2, sentence_lower)
                                    confidence = self._calculate_pattern_confidence(entity1, entity2, sentence, trigger)
                                    
                                    if final_rel_type and confidence > 0.4:
                                        relations.append({
                                            "entity1": entity1["text"],
                                            "entity2": entity2["text"],
                                            "relation": final_rel_type,
                                            "sentence": sentence,
                                            "confidence": confidence,
                                            "entity1Type": entity1["label"],
                                            "entity2Type": entity2["label"],
                                            "source": "medical_pattern"
                                        })
        
        return relations
    
    def _determine_relation_direction(self, rel_type: str, entity1: Dict, entity2: Dict, sentence: str) -> str:
        """Determine the direction of the relation based on entity types"""
        if rel_type == "treats":
            if entity1["label"] in ["MEDICATION", "TREATMENT"] and entity2["label"] == "DISEASE":
                return "TREATS"
            elif entity2["label"] in ["MEDICATION", "TREATMENT"] and entity1["label"] == "DISEASE":
                return "TREATED_BY"
        
        elif rel_type == "causes":
            return "CAUSES"
        
        elif rel_type == "symptoms":
            if entity1["label"] == "DISEASE" and entity2["label"] == "SYMPTOM":
                return "HAS_SYMPTOM"
            elif entity2["label"] == "DISEASE" and entity1["label"] == "SYMPTOM":
                return "SYMPTOM_OF"
        
        elif rel_type == "prevents":
            return "PREVENTS"
        
        return None
    
    def _calculate_relation_confidence(self, verb_token, entity1: Dict, entity2: Dict, sentence: str) -> float:
        """Calculate confidence for a relation"""
        confidence = 0.5
        
        # Verb strength
        strong_verbs = {"treat", "cause", "prevent", "diagnose"}
        if verb_token.lemma_ in strong_verbs:
            confidence += 0.2
        
        # Entity type compatibility
        compatible_pairs = [
            ("MEDICATION", "DISEASE"),
            ("TREATMENT", "DISEASE"),
            ("DISEASE", "SYMPTOM"),
            ("DISEASE", "DISEASE")
        ]
        
        pair = (entity1["label"], entity2["label"])
        if pair in compatible_pairs or (pair[1], pair[0]) in compatible_pairs:
            confidence += 0.15
        
        # Proximity in dependency tree
        confidence += 0.1
        
        return min(0.95, confidence)
    
    def _calculate_pattern_confidence(self, entity1: Dict, entity2: Dict, sentence: str, trigger: str) -> float:
        """Calculate confidence for pattern-based relations"""
        confidence = 0.5
        
        # Distance between entities and trigger
        pos1 = sentence.lower().find(entity1["text"].lower())
        pos2 = sentence.lower().find(entity2["text"].lower())
        trigger_pos = sentence.lower().find(trigger)
        
        if pos1 != -1 and pos2 != -1 and trigger_pos != -1:
            avg_distance = (abs(pos1 - trigger_pos) + abs(pos2 - trigger_pos)) / 2
            if avg_distance < 30:
                confidence += 0.2
            if avg_distance < 15:
                confidence += 0.1
        
        return min(0.95, confidence)
    
    def _filter_relations(self, relations: List[Dict]) -> List[Dict]:
        """Filter and deduplicate relations"""
        filtered = []
        seen = set()
        
        # Sort by confidence (highest first)
        relations.sort(key=lambda x: x['confidence'], reverse=True)
        
        for rel in relations:
            # Create unique key
            key1 = (rel["entity1"].lower(), rel["relation"], rel["entity2"].lower())
            key2 = (rel["entity2"].lower(), self._get_inverse_relation(rel["relation"]), rel["entity1"].lower())
            
            if key1 not in seen and key2 not in seen:
                seen.add(key1)
                filtered.append(rel)
        
        return filtered
    
    def _get_inverse_relation(self, relation: str) -> str:
        """Get inverse relation"""
        inverses = {
            "TREATS": "TREATED_BY",
            "TREATED_BY": "TREATS",
            "HAS_SYMPTOM": "SYMPTOM_OF",
            "SYMPTOM_OF": "HAS_SYMPTOM",
            "CAUSES": "CAUSED_BY",
            "CAUSED_BY": "CAUSES",
            "PREVENTS": "PREVENTED_BY",
            "PREVENTED_BY": "PREVENTS"
        }
        return inverses.get(relation, relation)
    
    def process_with_nlp(self, data: List[Dict]) -> List[Dict]:
        """Process all data with NLP pipeline"""
        processed_results = []
        self.extracted_triples = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, item in enumerate(data):
            status_text.text(f"Processing document {i+1}/{len(data)}")
            progress_bar.progress((i + 1) / len(data))
            
            # Extract entities using hybrid method
            entities = self.extract_entities_hybrid(item["content"])
            
            # Extract relations using advanced method
            relations = self.extract_relations_advanced(item["content"], entities)
            
            # Create triples
            triples = self._create_triples(entities, relations, item)
            self.extracted_triples.extend(triples)
            
            processed_results.append({
                "original_document": item,
                "entities": entities,
                "relations": relations,
                "knowledge_triplets": triples,
                "entity_count": len(entities),
                "relation_count": len(relations),
                "triplet_count": len(triples)
            })
            
        progress_bar.empty()
        status_text.empty()
        
        return processed_results
    
    def _create_triples(self, entities: List[Dict], relations: List[Dict], document: Dict) -> List[Dict]:
        """Create knowledge graph triples"""
        triples = []
        
        # Relation triples
        for relation in relations:
            triples.append({
                "subject": relation["entity1"],
                "predicate": relation["relation"],
                "object": relation["entity2"],
                "source_sentence": relation["sentence"],
                "confidence": relation["confidence"],
                "domain1": document["domain"],
                "domain2": document["domain"],
                "isCrossDomain": False
            })
        
        # Entity type triples
        for entity in entities:
            triples.append({
                "subject": entity["text"],
                "predicate": "is_a",
                "object": entity["label"].lower(),
                "source_sentence": document["content"][:100] + "...",
                "confidence": entity.get("confidence", 0.9),
                "domain1": document["domain"],
                "domain2": document["domain"],
                "isCrossDomain": False
            })
            
        return triples
    
    def connect_neo4j(self, uri: str, username: str, password: str, database: str = "neo4j") -> bool:
        """Connect to Neo4j database"""
        try:
            self.neo4j_driver = GraphDatabase.driver(uri, auth=(username, password))
            with self.neo4j_driver.session(database=database) as session:
                session.run("RETURN 1")
            return True
        except Exception as e:
            return False
    
    def export_to_neo4j(self) -> Dict:
        """Export knowledge graph to Neo4j"""
        if not self.neo4j_driver:
            return {"error": "Not connected to Neo4j"}
            
        try:
            stats = {
                "nodes_created": 0,
                "relationships_created": 0,
                "errors": 0
            }
            
            with self.neo4j_driver.session() as session:
                session.run("MATCH (n:HealthData) DETACH DELETE n")
                
                unique_entities = set()
                for triple in self.extracted_triples:
                    unique_entities.add(triple["subject"])
                    unique_entities.add(triple["object"])
                
                for entity in unique_entities:
                    try:
                        session.run("""
                            MERGE (e:Entity:HealthData {name: $name})
                            SET e.type = $type, e.createdAt = datetime()
                        """, {"name": entity, "type": "Entity"})
                        stats["nodes_created"] += 1
                    except Exception as e:
                        stats["errors"] += 1
                
                for triple in self.extracted_triples:
                    try:
                        session.run("""
                            MATCH (a:Entity:HealthData {name: $subject})
                            MATCH (b:Entity:HealthData {name: $object})
                            MERGE (a)-[r:RELATED_TO {type: $relation}]->(b)
                            SET r.confidence = $confidence, r.createdAt = datetime()
                        """, {
                            "subject": triple["subject"],
                            "object": triple["object"],
                            "relation": triple["predicate"],
                            "confidence": triple["confidence"]
                        })
                        stats["relationships_created"] += 1
                    except Exception as e:
                        stats["errors"] += 1
                        
            return stats
            
        except Exception as e:
            return {"error": str(e)}

def show_auth_page(platform):
    """Show authentication page (login/register)"""
    
    # Initialize session state for auth
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    if 'auth_error' not in st.session_state:
        st.session_state.auth_error = ''
    if 'auth_success' not in st.session_state:
        st.session_state.auth_success = ''
    
    st.markdown('<h1 class="main-header">HealthData NLP Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced Medical Knowledge Extraction & Graph Analytics</p>', unsafe_allow_html=True)
    
    # Auth container
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Toggle between login and register
    if st.session_state.auth_mode == 'login':
        st.markdown('<div class="auth-header"><h2>Sign In to Your Account</h2><p>Enter your credentials to access the platform</p></div>', unsafe_allow_html=True)
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Log In", use_container_width=True):
                if username and password:
                    result = platform.auth_manager.login_user(username, password)
                    if result["success"]:
                        st.session_state.user = result["user"]
                        st.session_state.token = result["token"]
                        st.session_state.auth_success = f"Welcome back, {username}!"
                        st.rerun()
                    else:
                        st.session_state.auth_error = result["error"]
                else:
                    st.session_state.auth_error = "Please fill in all fields"
        
        with col2:
            if st.button("Don\'t have an account? --> Register here", use_container_width=True):
                st.session_state.auth_mode = 'register'
                st.rerun()
        
   
    else:  # Register mode
        st.markdown('<div class="auth-header"><h2>Create New Account</h2><p>Join our platform to start analyzing medical data</p></div>', unsafe_allow_html=True)
        
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email (optional)", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Account", use_container_width=True):
                if username and password:
                    if password == confirm_password:
                        result = platform.auth_manager.register_user(username, password, email)
                        if result["success"]:
                            st.session_state.auth_success = "Account created successfully! Please login."
                            st.session_state.auth_mode = 'login'
                            st.rerun()
                        else:
                            st.session_state.auth_error = result["error"]
                    else:
                        st.session_state.auth_error = "Passwords do not match"
                else:
                    st.session_state.auth_error = "Please fill in all required fields"
        
        with col2:
            if st.button("Back to Login", use_container_width=True):
                st.session_state.auth_mode = 'login'
                st.rerun()
        
        st.markdown('<div class="auth-switch">Already have an account? <a>Sign in here</a></div>', unsafe_allow_html=True)
    
    # Display messages
    if st.session_state.auth_error:
        st.error(st.session_state.auth_error)
        st.session_state.auth_error = ''
    
    if st.session_state.auth_success:
        st.success(st.session_state.auth_success)
        st.session_state.auth_success = ''
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features showcase
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem;">
        <h3 style="color: #2d3748; margin-bottom: 2rem;">Platform Capabilities</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1rem;">
            <div class="feature-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">Medical NLP</h4>
                <p style="color: #64748b; margin: 0;">Advanced entity and relation extraction from medical texts</p>
            </div>
            <div class="feature-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">Knowledge Graph</h4>
                <p style="color: #64748b; margin: 0;">Interactive medical relationship visualization and analysis</p>
            </div>
            <div class="feature-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">Semantic Search</h4>
                <p style="color: #64748b; margin: 0;">Intelligent medical content discovery and retrieval</p>
            </div>
            <div class="feature-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">Admin Dashboard</h4>
                <p style="color: #64748b; margin: 0;">Comprehensive system management and analytics</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_admin_dashboard(platform):
    """Show admin dashboard with comprehensive analytics"""
    
    st.markdown('<h1 class="main-header">Admin Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comprehensive System Management & Analytics</p>', unsafe_allow_html=True)
    
    # Get usage statistics
    usage_stats = platform.auth_manager.get_usage_stats()
    all_users = platform.auth_manager.get_all_users()
    
    # Admin Metrics Overview
    st.markdown('<div class="section-header">System Overview</div>', unsafe_allow_html=True)
    
    # Metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="quick-stat">
            <h3>{usage_stats['total_users']}</h3>
            <p>Total Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="quick-stat">
            <h3>{usage_stats['active_users']}</h3>
            <p>Active Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="quick-stat">
            <h3>{usage_stats['admin_users']}</h3>
            <p>Admin Users</p>
        </div>
        """, unsafe_allow_html=True)

    
    # Tabs for different admin sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "User Management", 
        "Analytics", 
        "System Health", 
        "Platform Settings"
    ])
    
    with tab1:
        st.subheader("User Management")
        
        # User table with management options
        st.markdown("### Registered Users")
        
        if all_users:
            # Create DataFrame for users
            user_data = []
            for user in all_users:
                user_data.append({
                    "ID": user["id"],
                    "Username": user["username"],
                    "Email": user["email"] or "N/A",
                    "Role": user["role"],
                    "Status": "Active" if user["is_active"] else "Inactive",
                })
            
            user_df = pd.DataFrame(user_data)
            st.dataframe(user_df, use_container_width=True)
            
            # User management actions
            st.subheader("User Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### Change User Role")
                selected_user = st.selectbox(
                    "Select User:",
                    [f"{user['id']} - {user['username']} ({user['role']})" for user in all_users],
                    key="role_select"
                )
                new_role = st.selectbox("New Role:", ["user", "admin"], key="role_change")
                
                if st.button("Update Role", key="update_role_btn"):
                    user_id = int(selected_user.split(" - ")[0])
                    if platform.auth_manager.update_user_role(user_id, new_role):
                        st.success(f"Role updated to {new_role} successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update role")


            
            with col3:
                st.markdown("### User Statistics")
                active_count = sum(1 for user in all_users if user["is_active"])
                admin_count = sum(1 for user in all_users if user["role"] == "admin")
                
                st.metric("Active Users", active_count)
                st.metric("Admin Users", admin_count)
                st.metric("Total Users", len(all_users))
        
        else:
            st.info("No users found in the system.")
    
    with tab2:
        st.subheader("Platform Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily activity chart
            st.markdown("### Daily Activity (Last 30 days)")
            if usage_stats['daily_activity']:
                activity_data = []
                for date, count in usage_stats['daily_activity']:
                    activity_data.append({
                        "Date": date,
                        "Activity Count": count
                    })
                activity_df = pd.DataFrame(activity_data)
                st.bar_chart(activity_df.set_index("Date"))
            else:
                st.info("No activity data available")
        
        with col2:
            # Action distribution
            st.markdown("### Action Distribution")
            if usage_stats['action_distribution']:
                action_data = []
                for action_type, count in usage_stats['action_distribution']:
                    action_data.append({
                        "Action Type": action_type,
                        "Count": count
                    })
                action_df = pd.DataFrame(action_data)
                st.dataframe(action_df, use_container_width=True)
                
                # Pie chart for action distribution
                fig = go.Figure(data=[go.Pie(
                    labels=action_df['Action Type'],
                    values=action_df['Count'],
                    hole=.3
                )])
                fig.update_layout(title="Action Type Distribution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No action distribution data available")
        
        # Platform performance metrics
        st.subheader("Platform Performance")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("NLP Models", "Loaded" if platform.nlp else "Not Loaded")
        
        with col2:
            st.metric("Knowledge Triples", len(platform.extracted_triples))
        
        with col3:
            st.metric("Documents Processed", len(platform.retrieved_data))
    
    with tab3:
        st.subheader("System Health")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h3 style="color: white; margin-bottom: 1rem;">System Status</h3>
                <p><strong>Authentication:</strong> <span class="status-success">Operational</span></p>
                <p><strong>Database:</strong> <span class="status-success">Connected</span></p>
                <p><strong>NLP Models:</strong> <span class="status-success">Loaded</span></p>
                <p><strong>API Services:</strong> <span class="status-success">Available</span></p>
            </div>
            """, unsafe_allow_html=True)
            
   
    with tab4:
        st.subheader("Platform Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Feature Configuration")
            
            # Feature toggles
            st.checkbox("Enable User Registration", value=True, key="reg_toggle")
            st.checkbox("Enable Data Export", value=True, key="export_toggle")
            st.checkbox("Enable Advanced NLP", value=True, key="nlp_toggle")
            st.checkbox("Enable Semantic Search", value=True, key="search_toggle")
            
            st.button("Save Configuration", type="primary")
        
        # Danger zone
        st.markdown("### Critical Operations")
        with st.expander("Critical Operations", expanded=False):
            st.warning("These actions are irreversible. Proceed with caution.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear All Data", type="secondary"):
                    st.error("This will delete all platform data. Are you sure?")
                    # Implementation would go here
            
            with col2:
                if st.button("Delete Inactive Users", type="secondary"):
                    st.error("This will permanently delete inactive users.")
                    # Implementation would go here

def show_main_app(platform):
    """Show the main application after authentication"""
    
    # User info in sidebar
    with st.sidebar:
        user_role = st.session_state.user['role']
        role_badge = "Admin" if user_role == "admin" else "User"
        
        st.markdown(f"""
        <div class="user-info">
            <h4 style="margin: 0 0 0.5rem 0;">Welcome, {st.session_state.user['username']}</h4>
            <span class="admin-badge">{role_badge}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Admin navigation
        if user_role == "admin":
            if st.button("Admin Dashboard", use_container_width=True):
                st.session_state.current_page = "admin"
                st.rerun()
        
        if st.button("Logout", use_container_width=True):
            for key in ['user', 'token', 'current_page']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Check if admin wants to go to admin dashboard
    if st.session_state.get('current_page') == 'admin':
        show_admin_dashboard(platform)
        return
    
    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;'>
            <h3 style='color: white; margin: 0 0 0.5rem 0;'>Quick Start</h3>
            <p style='color: white; opacity: 0.9; margin: 0;'>Add topics and click retrieve to begin analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Topic Management
        st.markdown('<div class="section-header">Healthcare Topics</div>', unsafe_allow_html=True)
        new_topic = st.text_input("Add medical topic:", placeholder="e.g., diabetes, cancer, cardiology...")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Topic", use_container_width=True):
                if new_topic:
                    platform.add_topic(new_topic)
                    st.success(f"Added: {new_topic}")
        with col2:
            if st.button("Clear All", use_container_width=True):
                platform.topics = []
                st.rerun()
        
        if platform.topics:
            st.markdown("**Current Topics:**")
            for topic in platform.topics:
                cols = st.columns([3, 1])
                cols[0].markdown(f"• **{topic}**")
                if cols[1].button("Remove", key=f"remove_{topic}"):
                    platform.remove_topic(topic)
                    st.rerun()
        
        # Data Sources
        st.markdown('<div class="section-header">Data Sources</div>', unsafe_allow_html=True)
        use_wikipedia = st.checkbox("Wikipedia Medical Data", value=True)
        use_arxiv = st.checkbox("ArXiv Research Papers", value=True)
        use_user_input = st.checkbox("User Text Input", value=True)
        use_file_upload = st.checkbox("File Upload", value=True)
        
        # Neo4j Configuration
        st.markdown('<div class="section-header">Database Connection</div>', unsafe_allow_html=True)
        with st.expander("Configure Neo4j", expanded=False):
            neo4j_uri = st.text_input("URI", value="bolt://localhost:7687")
            neo4j_username = st.text_input("Username", value="neo4j")
            neo4j_password = st.text_input("Password", type="password")
            neo4j_database = st.text_input("Database", value="neo4j")
            
            if st.button("Test Connection", use_container_width=True):
                if platform.connect_neo4j(neo4j_uri, neo4j_username, neo4j_password, neo4j_database):
                    st.success("Connected successfully!")
                else:
                    st.error("Connection failed")
        
        # Status Panel
        st.markdown('<div class="section-header">System Status</div>', unsafe_allow_html=True)
        if platform.nlp or platform.ner_pipeline:
            st.markdown('<span class="status-success">NLP Models: Loaded</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-warning">NLP Models: Basic</span>', unsafe_allow_html=True)
        
        if platform.retrieved_data:
            # Count by source type
            source_counts = {}
            for item in platform.retrieved_data:
                source = item["source"]
                source_counts[source] = source_counts.get(source, 0) + 1
            
            source_display = {
                "wikipedia": "Wikipedia",
                "arxiv": "ArXiv",
                "user_input": "User Input", 
                "file_upload": "File Upload"
            }
            
            sources_text = ", ".join([f"{s}: {c}" for s, c in source_counts.items()])
            st.markdown(f'<span class="status-success">Data: {len(platform.retrieved_data)} documents</span>', unsafe_allow_html=True)
            st.caption(f"Sources: {sources_text}")
        else:
            st.markdown('<span class="status-warning">Data: No data</span>', unsafe_allow_html=True)

        if platform.extracted_triples:
            st.markdown(f'<span class="status-success">Knowledge: {len(platform.extracted_triples)} triples</span>', unsafe_allow_html=True)
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Data Collection", 
        "NLP Analysis", 
        "Knowledge Graph", 
        "Cross-Domain", 
        "Semantic Search",
        "Export"
    ])
    
    with tab1:
        st.header("Data Collection & Processing")
        
        if not platform.topics:
            st.info("""
            ## Welcome to HealthData NLP Platform
            
            **Get started in 3 simple steps:**
            1. **Add topics** in the sidebar (e.g., diabetes, cancer, mental health)
            2. **Select data sources** (Wikipedia, ArXiv research papers, User Input, File Upload)
            3. **Click retrieve** to gather medical information
            
            The system will automatically analyze the data and build a comprehensive medical knowledge graph!
            """)
        else:
            # Enhanced Data Sources Section
            st.subheader("Data Sources Selection")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                use_wikipedia = st.checkbox("Wikipedia Medical Data", value=True)
            with col2:
                use_arxiv = st.checkbox("ArXiv Research Papers", value=True)
            with col3:
                use_user_input = st.checkbox("User Text Input", value=True)
            with col4:
                use_file_upload = st.checkbox("File Upload", value=True)
            
            # User Input Section
            user_input_data = []
            if use_user_input:
                st.subheader("User Text Input")
                user_topic = st.selectbox("Select topic for your text:", platform.topics, key="user_input_topic")
                user_text = st.text_area(
                    "Enter medical text to analyze:",
                    placeholder="Paste or type medical content here...\nExample: Diabetes is a chronic condition treated with medications like metformin. Common symptoms include increased thirst and frequent urination.",
                    height=150
                )
                
                if user_text:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button("Add User Text to Analysis", key="add_user_text"):
                            user_data = platform.process_user_text_input(user_topic, user_text)
                            user_input_data.append(user_data)
                            # Also add directly to retrieved_data for immediate processing
                            platform.retrieved_data.append(user_data)
                            st.success(f"Added user text for topic: {user_topic}")
                    with col2:
                        if st.button("Process Now", key="process_user_text"):
                            if user_text:
                                user_data = platform.process_user_text_input(user_topic, user_text)
                                platform.retrieved_data.append(user_data)
                                st.success("Processed user text immediately!")

            # File Upload Section
            uploaded_files_data = []
            if use_file_upload:
                st.subheader("File Upload")
                upload_topic = st.selectbox("Select topic for uploaded files:", platform.topics, key="file_upload_topic")
                uploaded_files = st.file_uploader(
                    "Upload medical documents:",
                    type=['txt', 'pdf', 'docx', 'doc'],
                    accept_multiple_files=True,
                    help="Supported formats: TXT, PDF, DOCX, DOC"
                )
                
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**File:** {uploaded_file.name} ({uploaded_file.size} bytes)")
                        with col2:
                            if st.button("Process", key=f"process_{uploaded_file.name}"):
                                file_data = platform.process_uploaded_file(upload_topic, uploaded_file)
                                uploaded_files_data.append(file_data)
                                platform.retrieved_data.append(file_data)
                                st.success(f"Processed file: {uploaded_file.name}")
            
            # Retrieve Button and Data Processing
            st.markdown("---")
            col1, col2 = st.columns([1, 3])

            with col1:
                st.subheader(f"Ready to analyze {len(platform.topics)} topics")
                total_sources = sum([
                    use_wikipedia, use_arxiv, 
                    bool(user_input_data), bool(uploaded_files_data)
                ])
                st.metric("Selected Sources", total_sources)
                
            with col2:
                if st.button("Retrieve & Process All Data", type="primary", use_container_width=True):
                    with st.spinner(f"Gathering medical data from {len(platform.topics)} topics..."):
                        platform.retrieved_data = []
                        
                        # Process Wikipedia data
                        if use_wikipedia:
                            for topic in platform.topics:
                                wikipedia_data = platform.fetch_wikipedia_data(topic)
                                platform.retrieved_data.extend(wikipedia_data)
                        
                        # Process ArXiv data
                        if use_arxiv:
                            for topic in platform.topics:
                                arxiv_data = platform.fetch_arxiv_data(topic)
                                platform.retrieved_data.extend(arxiv_data)
                        
                        # Add user input data
                        platform.retrieved_data.extend(user_input_data)
                        
                        # Add uploaded files data
                        platform.retrieved_data.extend(uploaded_files_data)
                    
                    if platform.retrieved_data:
                        st.success(f"Successfully retrieved {len(platform.retrieved_data)} medical documents!")
                        
                        # Display results by source type
                        source_groups = {}
                        for item in platform.retrieved_data:
                            source = item["source"]
                            if source not in source_groups:
                                source_groups[source] = []
                            source_groups[source].append(item)
                        
                        for source, items in source_groups.items():
                            source_badge_class = {
                                "wikipedia": "badge-wikipedia",
                                "arxiv": "badge-arxiv", 
                                "user_input": "badge-user",
                                "file_upload": "badge-file"
                            }.get(source, "")
                            
                            with st.expander(f"{source.upper()} - {len(items)} documents", expanded=True):
                                for i, item in enumerate(items):
                                    with st.container():
                                        col1, col2 = st.columns([4, 1])
                                        col1.markdown(f"### {item['topic']}")
                                        col2.markdown(f"<span class='source-badge {source_badge_class}'>{item['source']}</span>", unsafe_allow_html=True)
                                        
                                        col1, col2, col3 = st.columns([3, 1, 1])
                                        col1.caption(f"{item['timestamp'][:10]}")
                                        if item['url'] and item['url'] not in ['user_input', 'error']:
                                            col2.markdown(f"[Source Link]({item['url']})")
                                        else:
                                            col2.markdown("Local Content")
                                        
                                        with st.expander("View Medical Content"):
                                            # Truncate very long content for display
                                            content = item["content"]
                                            if len(content) > 1000:
                                                st.write(content[:1000] + "...")
                                                st.info(f"Content truncated. Full length: {len(content)} characters")
                                            else:
                                                st.write(content)
                                        
                                        if i < len(items) - 1:
                                            st.divider()
                    else:
                        st.error("No data retrieved. Please check your data sources and try again.")

            # Add a separate button for processing only user input and files
            if (user_input_data or uploaded_files_data) and not (use_wikipedia or use_arxiv):
                st.markdown("---")
                if st.button("Process Only User Content", type="secondary", use_container_width=True):
                    with st.spinner("Processing user-provided content..."):
                        platform.retrieved_data = []
                        
                        # Add user input data
                        platform.retrieved_data.extend(user_input_data)
                        
                        # Add uploaded files data
                        platform.retrieved_data.extend(uploaded_files_data)
                    
                    if platform.retrieved_data:
                        st.success(f"Successfully processed {len(platform.retrieved_data)} user documents!")
                        
                        # Display results
                        for i, item in enumerate(platform.retrieved_data):
                            with st.container():
                                col1, col2 = st.columns([4, 1])
                                col1.markdown(f"### {item['topic']}")
                                col2.markdown(f"`{item['source']}`")
                                
                                with st.expander("View Content"):
                                    st.write(item["content"])
                                
                                if i < len(platform.retrieved_data) - 1:
                                    st.divider()

            # Data Source Statistics
            if platform.retrieved_data:
                st.subheader("Data Source Statistics")
                
                source_counts = {}
                for item in platform.retrieved_data:
                    source = item["source"]
                    source_counts[source] = source_counts.get(source, 0) + 1
                
                col1, col2, col3, col4 = st.columns(4)
                sources_display = {
                    "wikipedia": ("Wikipedia", "#10b981"),
                    "arxiv": ("ArXiv", "#3b82f6"),
                    "user_input": ("User Input", "#f59e0b"),
                    "file_upload": ("File Upload", "#8b5cf6")
                }
                
                for i, (source, count) in enumerate(source_counts.items()):
                    display_name, color = sources_display.get(source, (f"{source}", "#607D8B"))
                    with [col1, col2, col3, col4][i % 4]:
                        st.markdown(f"""
                        <div style='background: {color}; color: white; padding: 1rem; border-radius: 10px; text-align: center;'>
                            <h3 style='color: white; margin: 0;'>{count}</h3>
                            <p style='color: white; margin: 0;'>{display_name}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    with tab2:
        st.header("Advanced NLP Analysis")
        
        if not platform.retrieved_data:
            st.warning("Please provide data first using the Data Collection tab")
            st.info("""
            ### You can provide data through:
            - **Wikipedia**: Fetch medical information from Wikipedia
            - **ArXiv**: Get research papers from ArXiv
            - **Text Input**: Enter your own medical text
            - **File Upload**: Upload medical documents
            
            Any of these methods will provide data for NLP analysis!
            """)
        else:
            col1, col2 = st.columns([1, 3])
            with col2:
                if st.button("Run NLP Pipeline", type="primary", use_container_width=True):
                    with st.spinner("Processing with advanced NLP techniques..."):
                        nlp_results = platform.process_with_nlp(platform.retrieved_data)
                    
                    total_entities = sum(r["entity_count"] for r in nlp_results)
                    total_relations = sum(r["relation_count"] for r in nlp_results)
                    total_triples = sum(r["triplet_count"] for r in nlp_results)
                    
                    st.success("NLP Analysis Complete!")
                    
                    # Display metrics in beautiful cards
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown('<div class="metric-card"><h3>Documents</h3><h2>{}</h2></div>'.format(len(nlp_results)), unsafe_allow_html=True)
                    with col2:
                        st.markdown('<div class="metric-card"><h3>Entities</h3><h2>{}</h2></div>'.format(total_entities), unsafe_allow_html=True)
                    with col3:
                        st.markdown('<div class="metric-card"><h3>Relations</h3><h2>{}</h2></div>'.format(total_relations), unsafe_allow_html=True)
                    with col4:
                        st.markdown('<div class="metric-card"><h3>Triples</h3><h2>{}</h2></div>'.format(total_triples), unsafe_allow_html=True)
                    
                    # Technology stack
                    st.markdown("""
                    <div style='background: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 1px solid #f1f5f9;'>
                        <h4>NLP Technologies Used</h4>
                        <div style='display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;'>
                            <span style='background: #f8fafc; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; color: #64748b;'>spaCy NER</span>
                            <span style='background: #f8fafc; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; color: #64748b;'>Transformer Models</span>
                            <span style='background: #f8fafc; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; color: #64748b;'>Medical Patterns</span>
                            <span style='background: #f8fafc; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; color: #64748b;'>Dependency Parsing</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Detailed results
                    st.subheader("Detailed Analysis Results")
                    for i, result in enumerate(nlp_results):
                        doc = result["original_document"]
                        with st.expander(f"{doc['topic']} - {result['entity_count']} entities", expanded=i==0):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Extracted Entities:**")
                                if result["entities"]:
                                    entities_by_type = {}
                                    for entity in result["entities"]:
                                        if entity["label"] not in entities_by_type:
                                            entities_by_type[entity["label"]] = []
                                        entities_by_type[entity["label"]].append(entity)
                                    
                                    for entity_type, entity_list in entities_by_type.items():
                                        with st.expander(f"{entity_type} ({len(entity_list)})"):
                                            for entity in entity_list:
                                                conf = f" [{entity.get('confidence', 0):.1%}]" if entity.get('confidence') else ""
                                                st.write(f"• `{entity['text']}`{conf}")
                                else:
                                    st.info("No entities found in this document")
                            
                            with col2:
                                st.write("**Document Statistics:**")
                                st.metric("Entities Found", result['entity_count'])
                                st.metric("Relations Extracted", result['relation_count'])
                                st.metric("Knowledge Triples", result['triplet_count'])
            with col1:
                st.info("""
                ### What happens during NLP analysis?
                
                The system uses multiple advanced techniques:
                - **Entity Recognition**: Identifies medical terms, drugs, symptoms, diseases
                - **Relation Extraction**: Finds connections between medical concepts  
                - **Knowledge Graph Construction**: Builds structured medical relationships
                - **Confidence Scoring**: Rates the reliability of extracted information
                
                Click the button to start the analysis!
                """)
    
    with tab3:
        st.header("Interactive Knowledge Graph")
        
        if not platform.extracted_triples:
            st.warning("Run NLP pipeline first to generate the knowledge graph")
        else:
            st.success(f"Generated {len(platform.extracted_triples)} knowledge triples")
            
            # Enhanced graph visualization
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            
            G = nx.Graph()
            entity_colors = {
                'DISEASE': '#ff6b6b', 'SYMPTOM': '#4ecdc4', 'MEDICATION': '#45b7d1',
                'TREATMENT': '#96ceb4', 'ANATOMY': '#feca57', 'PERSON': '#ff9ff3',
                'ORGANIZATION': '#54a0ff', 'default': '#c8d6e5'
            }
            
            # Build graph
            node_data = {}
            for triple in platform.extracted_triples:
                node_type = triple["object"].upper() if triple["predicate"] == "is_a" else "default"
                G.add_node(triple["subject"], type=node_type)
                G.add_node(triple["object"], type=node_type)
                node_data[triple["subject"]] = node_type
                node_data[triple["object"]] = node_type
                G.add_edge(triple["subject"], triple["object"], 
                          relation=triple["predicate"],
                          confidence=triple["confidence"],
                          weight=triple["confidence"] * 3)
            
            if G.number_of_nodes() > 0:
                pos = nx.spring_layout(G, k=3, iterations=200, weight='weight')
                
                # Create the interactive plot
                edge_traces = []
                relation_colors = {
                    'TREATS': '#27ae60', 'TREATED_BY': '#2ecc71', 'SYMPTOM_OF': '#e74c3c',
                    'HAS_SYMPTOM': '#c0392b', 'CAUSES': '#e67e22', 'CAUSED_BY': '#d35400',
                    'PREVENTS': '#9b59b6', 'PREVENTED_BY': '#8e44ad', 'DIAGNOSES': '#3498db',
                    'is_a': '#7f8c8d', 'RELATED_TO': '#95a5a6'
                }
                
                for edge in G.edges(data=True):
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    relation = edge[2].get('relation', 'RELATED_TO')
                    confidence = edge[2].get('confidence', 0.5)
                    
                    edge_color = relation_colors.get(relation, '#95a5a6')
                    edge_width = max(2, confidence * 4)
                    line_dash = 'dot' if relation == "is_a" else 'solid'
                    
                    edge_trace = go.Scatter(
                        x=[x0, x1, None], y=[y0, y1, None],
                        line=dict(width=edge_width, color=edge_color, dash=line_dash),
                        hoverinfo='text',
                        text=f"{relation} (Confidence: {confidence:.1%})",
                        mode='lines',
                        showlegend=False
                    )
                    edge_traces.append(edge_trace)
                
                # Create node trace
                node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    node_text.append(node)
                    node_type = node_data.get(node, 'default')
                    node_color.append(entity_colors.get(node_type, entity_colors['default']))
                    degree = G.degree(node)
                    node_size.append(max(20, degree * 8))
                
                node_trace = go.Scatter(
                    x=node_x, y=node_y, mode='markers+text',
                    hoverinfo='text', text=node_text,
                    textposition="middle center",
                    textfont=dict(color='black', size=10, family="Arial Black"),
                    marker=dict(size=node_size, color=node_color, line=dict(width=2, color='darkblue')),
                    hovertemplate='<b>%{text}</b><extra></extra>'
                )
                
                # Create the figure
                fig = go.Figure(data=edge_traces + [node_trace],
                               layout=go.Layout(
                                   title=dict(text='Medical Knowledge Graph', font=dict(size=20, color='black')),
                                   showlegend=True, hovermode='closest',
                                   margin=dict(b=20, l=5, r=5, t=60),
                                   xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                   yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                   height=700, plot_bgcolor='white', paper_bgcolor='white'
                               ))
                
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Statistics and data
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Nodes", G.number_of_nodes())
            col2.metric("Total Edges", G.number_of_edges())
            col3.metric("Graph Density", f"{nx.density(G):.3f}")

            
            # Relation distribution
            st.subheader("Relation Distribution")
            relation_counts = {}
            for triple in platform.extracted_triples:
                rel_type = triple["predicate"]
                relation_counts[rel_type] = relation_counts.get(rel_type, 0) + 1
            
            rel_df = pd.DataFrame(list(relation_counts.items()), columns=['Relation Type', 'Count'])
            rel_df = rel_df.sort_values('Count', ascending=False)
            st.dataframe(rel_df, use_container_width=True)
    
    with tab4:
        st.header("Cross-Domain Medical Insights")
        
        if not platform.extracted_triples:
            st.warning("Run NLP pipeline first to see cross-domain analysis")
        else:
            # Domain analysis
            domains = {}
            entity_domains = {}
            
            for triple in platform.extracted_triples:
                domain = triple["domain1"]
                if domain not in domains:
                    domains[domain] = {"entities": set(), "relations": 0}
                domains[domain]["entities"].add(triple["subject"])
                domains[domain]["entities"].add(triple["object"])
                domains[domain]["relations"] += 1
                
                for entity in [triple["subject"], triple["object"]]:
                    if entity not in entity_domains:
                        entity_domains[entity] = set()
                    entity_domains[entity].add(domain)
            
            # Display domain cards
            st.subheader("Domain Overview")
            cols = st.columns(len(domains))
            for i, (domain, stats) in enumerate(domains.items()):
                with cols[i % len(cols)]:
                    st.markdown(f"""
                    <div class="feature-card">
                        <h3>{domain.upper()}</h3>
                        <h2>{len(stats["entities"])}</h2>
                        <p>entities • {stats['relations']} relations</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Bridge entities
            bridge_entities = {entity: domains for entity, domains in entity_domains.items() 
                             if len(domains) > 1}
            
            if bridge_entities:
                st.subheader("Bridge Entities")
                st.write("These medical concepts connect multiple domains:")
                
                bridge_data = []
                for entity, domain_set in list(bridge_entities.items())[:10]:
                    bridge_data.append({
                        "Entity": entity,
                        "Domains": ", ".join(domain_set),
                        "Domain Count": len(domain_set)
                    })
                
                bridge_df = pd.DataFrame(bridge_data)
                st.dataframe(bridge_df.sort_values("Domain Count", ascending=False), use_container_width=True)
            else:
                st.info("Add more diverse medical topics to discover cross-domain connections")

    with tab5:
        st.header("Semantic Search & Query Module")
        
        if not platform.retrieved_data:
            st.warning("Please retrieve data first using the Data Collection tab")
        else:
            # Initialize semantic search if not already done
            if not platform.semantic_search.is_indexed:
                with st.spinner("Indexing documents for semantic search..."):
                    platform.semantic_search.index_documents(platform.retrieved_data)
            
            st.success("Semantic search engine ready!")
            
            # Search interface
            col1, col2 = st.columns([3, 1])
            with col1:
                search_query = st.text_input(
                    "Search medical knowledge:",
                    placeholder="e.g., diabetes treatments, cancer symptoms...",
                    key="semantic_search"
                )
            with col2:
                search_type = st.selectbox(
                    "Search in:",
                    ["Knowledge Graph", "Documents"],
                    key="search_type"
                )
            
            if search_query:
                with st.spinner("Searching medical knowledge..."):
                    if search_type == "Documents":
                        results = platform.semantic_search.search(search_query, top_k=10)
                        
                        if results:
                            st.success(f"Found {len(results)} relevant documents")
                            
                            for i, result in enumerate(results):
                                doc = result['document']
                                similarity = result['similarity_score']
                                
                                with st.container():
                                    st.markdown(f"""
                                    <div class="search-result">
                                        <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 0.5rem;">
                                            <h4 style="margin: 0; flex-grow: 1;">{doc['topic']}</h4>
                                            <span class="similarity-score">{similarity:.1%}</span>
                                        </div>
                                        <p style="margin: 0.5rem 0; color: #666; font-size: 0.9rem;">
                                            <strong>Source:</strong> {doc['source']} • <strong>Domain:</strong> {doc['domain']}
                                        </p>
                                        <p style="margin: 0;">
                                            {doc['content'][:300]}...
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Create unique expander for each document
                                    expander_label = f"View Full Document - {doc['topic'][:30]}..."
                                    with st.expander(expander_label):
                                        st.write(doc['content'])
                                        st.markdown(f"[Source Link]({doc['url']})")
                                    
                                    if i < len(results) - 1:
                                        st.divider()
                        else:
                            st.warning("No relevant documents found. Try a different search query.")
                    
                    else:  # Knowledge Graph search
                        if not platform.extracted_triples:
                            st.warning("Run NLP pipeline first to search knowledge graph")
                        else:
                            results = platform.semantic_search.search_triples(search_query, platform.extracted_triples, top_k=15)
                            
                            if results:
                                st.success(f"Found {len(results)} relevant knowledge triples")
                                
                                # Group by relation type
                                relation_groups = {}
                                for result in results:
                                    triple = result['triple']
                                    rel_type = triple['predicate']
                                    if rel_type not in relation_groups:
                                        relation_groups[rel_type] = []
                                    relation_groups[rel_type].append(result)
                                
                                for rel_type, rel_results in relation_groups.items():
                                    with st.expander(f"{rel_type} ({len(rel_results)} relations)", expanded=True):
                                        for result in rel_results:
                                            triple = result['triple']
                                            similarity = result['similarity_score']
                                            
                                            col1, col2, col3 = st.columns([1, 1, 1])
                                            col1.markdown(f"**{triple['subject']}**")
                                            col2.markdown(f"➡️ *{triple['predicate']}*")
                                            col3.markdown(f"**{triple['object']}**")
                                            
                                            # Confidence and similarity
                                            col4, col5 = st.columns(2)
                                            col4.metric("Relation Confidence", f"{triple['confidence']:.1%}")
                                            col5.metric("Search Relevance", f"{similarity:.1%}")
                                            
                                            if 'source_sentence' in triple:
                                                with st.expander("View Context"):
                                                    st.write(triple['source_sentence'])
                                            
                                            st.divider()
                            else:
                                st.warning("No relevant knowledge triples found. Try a different search query.")
            
            # Advanced search features
            st.subheader("Advanced Search Features")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="feature-card">
                    <h4>Semantic Understanding</h4>
                    <p>Finds conceptually similar content, not just keyword matches</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="feature-card">
                    <h4>Relevance Scoring</h4>
                    <p>Ranks results by semantic similarity to your query</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="feature-card">
                    <h4>Multi-Source Search</h4>
                    <p>Searches across documents and knowledge graph relationships</p>
                </div>
                """, unsafe_allow_html=True)
            


    
    with tab6:
        st.header("Export & Database")
        
        if not platform.extracted_triples:
            st.warning("Run NLP pipeline first to generate data for export")
        else:
            if not platform.neo4j_driver:
                st.warning("Connect to Neo4j first using the sidebar configuration")
            else:
                st.success("Connected to Neo4j Database")
                
                col1, col2 = st.columns([1, 3])
                with col2:
                    if st.button("Export to Neo4j", type="primary", use_container_width=True):
                        with st.spinner("Exporting knowledge graph to Neo4j..."):
                            result = platform.export_to_neo4j()
                        
                        if "error" in result:
                            st.error(f"Export failed: {result['error']}")
                        else:
                            st.success("Export completed successfully!")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Nodes Created", result["nodes_created"])
                            col2.metric("Relationships", result["relationships_created"])

            
                
                st.subheader("Sample Neo4j Queries")
                st.code("""
// Find all medical entities
MATCH (n:HealthData) RETURN n LIMIT 25

// Find treatment relationships
MATCH (a)-[r:TREATS]->(b) 
RETURN a.name as Treatment, b.name as Condition, r.confidence as Confidence

// Find high-confidence medical relationships
MATCH (a)-[r]->(b) 
WHERE r.confidence > 0.8 
RETURN a.name, type(r), b.name, r.confidence
                """, language="cypher")

def main():
    st.set_page_config(
        page_title="HealthData NLP Platform",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize platform
    if 'platform' not in st.session_state:
        st.session_state.platform = HealthDataNLPPlatform()
    
    platform = st.session_state.platform
    
    # Check authentication
    if 'user' not in st.session_state or 'token' not in st.session_state:
        show_auth_page(platform)
    else:
        # Verify token is still valid
        token_verification = platform.auth_manager.verify_token(st.session_state.token)
        if not token_verification["success"]:
            st.error("Session expired. Please login again.")
            del st.session_state.user
            del st.session_state.token
            if 'current_page' in st.session_state:
                del st.session_state.current_page
            st.rerun()
        else:
            show_main_app(platform)

if __name__ == "__main__":
    main()
