"""
Basic Mobile Agent Framework for E-commerce Price Comparison
"""

import json
import pickle
import time
from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum
import uuid

class AgentState(Enum):
    CREATED = "created"
    RUNNING = "running"
    MIGRATING = "migrating"
    COMPLETED = "completed"
    FAILED = "failed"

class Agent(ABC):
    def __init__(self, agent_id=None, name="Agent"):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = name
        self.current_host = None
        self.state = AgentState.CREATED
        self.data = {}
        self.executed = False

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        print(f"🤖 Agent {self.name} ({self.agent_id[:8]}) state changed to: {state.value}")

    def add_data(self, key: str, value):
        """Add data to agent's data store"""
        self.data[key] = value

    def get_data(self, key: str, default=None):
        return self.data.get(key, default)

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(agent_bytes):
        return pickle.loads(agent_bytes)

    @abstractmethod
    def execute(self):
        pass

    def migrate(self, target_host):
        print(f"🚀 Agent {self.name} migrating to {target_host}")
        self.set_state(AgentState.MIGRATING)
        time.sleep(0.1)
        self.current_host = target_host
        self.set_state(AgentState.RUNNING)
        print(f"✅ Agent {self.name} migrated successfully")

class ProductInfo:
    def __init__(self, name, price, site, url="", availability=True, **kwargs):
        self.name = name
        self.price = float(price) if price else 0.0
        self.site = site
        self.url = url
        self.availability = availability
        self.extraction_time = datetime.now()
        
        # Enhanced attributes
        self.rating = kwargs.get('rating')
        self.review_count = kwargs.get('review_count', 0)
        self.discount_percentage = kwargs.get('discount_percentage', 0)
        self.original_price = kwargs.get('original_price')
        self.savings = kwargs.get('savings', 0)
        self.brand = kwargs.get('brand')
        self.image_url = kwargs.get('image_url')
        self.specifications = kwargs.get('specifications', [])

    def __str__(self):
        status = "Available" if self.availability else "Out of Stock"
        return f"{self.name} - ₹{self.price:.2f} on {self.site} ({status})"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'price': self.price,
            'site': self.site,
            'url': self.url,
            'available': self.availability,
            'rating': self.rating,
            'review_count': self.review_count,
            'discount_percentage': self.discount_percentage,
            'original_price': self.original_price,
            'savings': self.savings,
            'brand': self.brand,
            'image_url': self.image_url,
            'specifications': self.specifications,
            'extraction_time': self.extraction_time.isoformat()
        }

class ComparisonResult:
    def __init__(self, query):
        self.query = query
        self.products = []

    def add_product(self, product):
        if isinstance(product, dict):
            # Convert dict to ProductInfo if needed
            product = ProductInfo(**product)
        self.products.append(product)

    def get_best_deal(self):
        available = [p for p in self.products if p.availability]
        if not available:
            return None
        return min(available, key=lambda p: p.price)

    def get_summary(self):
        best_deal = self.get_best_deal()
        return {
            "query": self.query,
            "total_results": len(self.products),
            "available_products": len([p for p in self.products if p.availability]),
            "best_deal": best_deal.to_dict() if best_deal else None,
            "sites_checked": list(set(p.site for p in self.products))
        }
