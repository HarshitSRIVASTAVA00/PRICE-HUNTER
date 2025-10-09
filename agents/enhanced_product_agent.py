"""
Enhanced Product Agent with more realistic mock data and variety
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import quote_plus, urljoin
import json
from base_agent import Agent, AgentState, ProductInfo

class EnhancedProductAgent(Agent):
    def __init__(self, site_name=None, base_url=None, search_patterns=None, headers=None):
        super().__init__(name=f"ProductAgent_{site_name or 'Generic'}")
        
        self.site_name = site_name or "Generic"
        self.base_url = base_url or ""
        self.search_patterns = search_patterns or {}
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def execute(self):
        """Execute the agent (required by base class)"""
        self.set_state(AgentState.RUNNING)
        self.set_state(AgentState.COMPLETED)
        return {"status": "executed"}

    def search_products(self, query, max_results=8):  # Increased from 10 to 8
        """Enhanced search with more variety and realistic data"""
        self.set_state(AgentState.RUNNING)
        
        try:
            mock_data = self._get_enhanced_mock_data(query, max_results)
            self.set_state(AgentState.COMPLETED)
            return {
                'site': self.site_name,
                'products': mock_data,
                'total_found': len(mock_data)
            }
            
        except Exception as e:
            self.set_state(AgentState.FAILED)
            return {
                'site': self.site_name,
                'products': [],
                'error': str(e),
                'total_found': 0
            }

    def _get_enhanced_mock_data(self, query, max_results):
        """Generate more realistic and varied mock data"""
        mock_products = []
        
        # Enhanced product templates based on query
        if 'iphone' in query.lower():
            base_products = [
                {
                    'name': f'Apple iPhone 15 (128GB) - Blue',
                    'base_price': 79900,
                    'brand': 'Apple',
                    'category': 'smartphone'
                },
                {
                    'name': f'Apple iPhone 15 Pro (256GB) - Natural Titanium',
                    'base_price': 134900,
                    'brand': 'Apple',
                    'category': 'smartphone'
                },
                {
                    'name': f'Apple iPhone 15 Plus (128GB) - Pink',
                    'base_price': 89900,
                    'brand': 'Apple',
                    'category': 'smartphone'
                },
                {
                    'name': f'Apple iPhone 15 Pro Max (256GB) - Blue Titanium',
                    'base_price': 159900,
                    'brand': 'Apple',
                    'category': 'smartphone'
                },
                {
                    'name': f'Apple iPhone 14 (128GB) - Midnight',
                    'base_price': 69900,
                    'brand': 'Apple',
                    'category': 'smartphone'
                },
                {
                    'name': f'Apple iPhone 13 (128GB) - Red',
                    'base_price': 59900,
                    'brand': 'Apple',
                    'category': 'smartphone'
                },
                {
                    'name': f'Apple iPhone 15 (256GB) - Yellow',
                    'base_price': 89900,
                    'brand': 'Apple',
                    'category': 'smartphone'
                },
                {
                    'name': f'Apple iPhone 14 Pro (256GB) - Deep Purple',
                    'base_price': 119900,
                    'brand': 'Apple',
                    'category': 'smartphone'
                }
            ]
        elif 'samsung' in query.lower():
            base_products = [
                {'name': f'Samsung Galaxy S24 Ultra (256GB) - Titanium Gray', 'base_price': 124999, 'brand': 'Samsung', 'category': 'smartphone'},
                {'name': f'Samsung Galaxy S24 (128GB) - Onyx Black', 'base_price': 79999, 'brand': 'Samsung', 'category': 'smartphone'},
                {'name': f'Samsung Galaxy Z Fold5 (256GB) - Phantom Black', 'base_price': 154999, 'brand': 'Samsung', 'category': 'smartphone'},
                {'name': f'Samsung Galaxy A54 5G (128GB) - Awesome Blue', 'base_price': 38999, 'brand': 'Samsung', 'category': 'smartphone'},
                {'name': f'Samsung Galaxy S23 FE (128GB) - Purple', 'base_price': 59999, 'brand': 'Samsung', 'category': 'smartphone'},
                {'name': f'Samsung Galaxy M34 5G (128GB) - Waterfall Blue', 'base_price': 18999, 'brand': 'Samsung', 'category': 'smartphone'},
                {'name': f'Samsung Galaxy Z Flip5 (256GB) - Mint', 'base_price': 99999, 'brand': 'Samsung', 'category': 'smartphone'},
                {'name': f'Samsung Galaxy S24+ (256GB) - Amber Yellow', 'base_price': 99999, 'brand': 'Samsung', 'category': 'smartphone'}
            ]
        elif 'laptop' in query.lower():
            base_products = [
                {'name': f'MacBook Air M2 (256GB) - Midnight', 'base_price': 114900, 'brand': 'Apple', 'category': 'laptop'},
                {'name': f'Dell XPS 13 Intel i7 (512GB SSD)', 'base_price': 124990, 'brand': 'Dell', 'category': 'laptop'},
                {'name': f'HP Pavilion 15 AMD Ryzen 5', 'base_price': 54990, 'brand': 'HP', 'category': 'laptop'},
                {'name': f'Lenovo ThinkPad E14 Intel i5', 'base_price': 65990, 'brand': 'Lenovo', 'category': 'laptop'},
                {'name': f'ASUS VivoBook 15 Intel i3', 'base_price': 39990, 'brand': 'ASUS', 'category': 'laptop'},
                {'name': f'Acer Aspire 5 AMD Ryzen 7', 'base_price': 67990, 'brand': 'Acer', 'category': 'laptop'},
                {'name': f'MSI Modern 14 Intel i7', 'base_price': 84990, 'brand': 'MSI', 'category': 'laptop'},
                {'name': f'Surface Laptop 5 Intel i7', 'base_price': 149990, 'brand': 'Microsoft', 'category': 'laptop'}
            ]
        else:
            # Generic products
            base_products = [
                {'name': f'{query} - Premium Edition', 'base_price': 25000, 'brand': 'Premium', 'category': 'general'},
                {'name': f'{query} - Pro Version', 'base_price': 35000, 'brand': 'Pro', 'category': 'general'},
                {'name': f'{query} - Standard Model', 'base_price': 18000, 'brand': 'Standard', 'category': 'general'},
                {'name': f'{query} - Elite Series', 'base_price': 45000, 'brand': 'Elite', 'category': 'general'},
                {'name': f'{query} - Basic Version', 'base_price': 12000, 'brand': 'Basic', 'category': 'general'},
                {'name': f'{query} - Advanced Model', 'base_price': 55000, 'brand': 'Advanced', 'category': 'general'},
                {'name': f'{query} - Compact Edition', 'base_price': 22000, 'brand': 'Compact', 'category': 'general'},
                {'name': f'{query} - Deluxe Version', 'base_price': 65000, 'brand': 'Deluxe', 'category': 'general'}
            ]
        
        # Site-specific pricing variations
        site_multipliers = {
            'Amazon India': random.uniform(0.95, 1.05),
            'Flipkart': random.uniform(0.92, 1.08),
            'Myntra': random.uniform(0.90, 1.10),
            'Snapdeal': random.uniform(0.88, 1.12)
        }
        
        site_multiplier = site_multipliers.get(self.site_name, 1.0)
        
        for i, base_product in enumerate(base_products[:max_results]):
            # Calculate prices with variations
            base_price = base_product['base_price'] * site_multiplier
            price_variation = random.uniform(0.95, 1.05)
            final_price = base_price * price_variation
            
            # Calculate original price (higher)
            discount_percent = random.uniform(5, 30)
            original_price = final_price / (1 - discount_percent/100)
            savings = original_price - final_price
            
            # Generate realistic ratings and reviews
            rating = round(random.uniform(3.8, 4.8), 1)
            review_count = random.randint(150, 5000)
            
            # Availability based on site and price
            availability_chance = 0.85 if final_price < 100000 else 0.75
            available = random.random() < availability_chance
            
            product = {
                'name': base_product['name'],
                'price': round(final_price, 2),
                'original_price': round(original_price, 2),
                'site': self.site_name,
                'available': available,
                'discount_percentage': round(discount_percent, 1),
                'savings': round(savings, 2),
                'rating': rating,
                'review_count': review_count,
                'brand': base_product['brand'],
                'category': base_product['category'],
                'image_url': f'https://via.placeholder.com/300x300/667eea/ffffff?text={base_product["brand"]}+{i+1}',
                'product_url': f'https://example.com/product/{i+1}',
                'specifications': self._generate_specs(base_product['category']),
                'delivery_info': self._generate_delivery_info(),
                'warranty': self._generate_warranty_info(base_product['category']),
                'timestamp': time.time(),
                'deal_score': 0,  # Will be calculated later
                'seller_rating': round(random.uniform(4.0, 4.9), 1),
                'return_policy': random.choice(['7 days', '10 days', '15 days', '30 days']),
                'emi_available': final_price > 10000,
                'free_delivery': random.choice([True, False]),
                'prime_eligible': self.site_name == 'Amazon India' and random.choice([True, False])
            }
            
            mock_products.append(product)
        
        return mock_products

    def _generate_specs(self, category):
        """Generate category-specific specifications"""
        if category == 'smartphone':
            return [
                f"{random.choice(['6.1', '6.4', '6.7'])}\" Display",
                f"{random.choice(['64MP', '108MP', '200MP'])} Camera",
                f"{random.choice(['4000', '5000', '6000'])}mAh Battery",
                f"{random.choice(['6GB', '8GB', '12GB'])} RAM"
            ]
        elif category == 'laptop':
            return [
                f"{random.choice(['14', '15.6', '16'])}\" Display",
                f"{random.choice(['512GB', '1TB'])} SSD",
                f"{random.choice(['8GB', '16GB', '32GB'])} RAM",
                f"{random.choice(['Intel i5', 'Intel i7', 'AMD Ryzen 5', 'AMD Ryzen 7'])} Processor"
            ]
        else:
            return [f'Feature {i+1}' for i in range(3)]

    def _generate_delivery_info(self):
        """Generate delivery information"""
        return random.choice([
            'Same day delivery',
            'Next day delivery',
            '2-3 business days',
            '3-5 business days',
            'Standard delivery'
        ])

    def _generate_warranty_info(self, category):
        """Generate warranty information"""
        if category == 'smartphone':
            return random.choice(['1 year manufacturer warranty', '2 year extended warranty'])
        elif category == 'laptop':
            return random.choice(['1 year warranty', '2 year warranty', '3 year warranty'])
        else:
            return random.choice(['6 months warranty', '1 year warranty'])

    # Keep existing methods for backward compatibility
    def build_search_url(self, query):
        if not self.search_patterns.get('search_url'):
            return f"{self.base_url}/search?q={quote_plus(query)}"
        
        encoded_query = quote_plus(query)
        return self.search_patterns['search_url'].format(query=encoded_query)

    def find_product_containers(self, soup):
        container_selector = self.search_patterns.get('container_selector', 'div')
        return soup.find_all(container_selector, limit=20)

    def extract_product_data(self, container, soup):
        """Extract enhanced product data"""
        return None  # Using mock data instead