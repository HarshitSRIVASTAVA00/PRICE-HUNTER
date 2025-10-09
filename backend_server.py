"""
Enhanced Simple Backend Server with BETTER mock data that varies by product
"""

import os
import sys
import json
import time
import uuid
import threading
import random
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global storage for search results
search_results = {}
search_status = {}

class EnhancedMockAgent:
    """Enhanced Mock agent with realistic, varied data based on search query"""
    def __init__(self, site_name):
        self.site_name = site_name
        
    def search_products(self, query, max_results=8):
        return self._get_realistic_mock_data(query, max_results)
    
    def _get_realistic_mock_data(self, query, max_results):
        """Generate realistic mock data that varies significantly by product type"""
        products = []
        query_lower = query.lower()
        
        # Product databases with realistic pricing and variations
        if any(term in query_lower for term in ['iphone', 'iphone 15', 'apple phone']):
            base_products = self._get_iphone_products()
        elif any(term in query_lower for term in ['samsung', 'galaxy', 'samsung phone']):
            base_products = self._get_samsung_products()
        elif any(term in query_lower for term in ['laptop', 'computer', 'macbook', 'dell', 'hp']):
            base_products = self._get_laptop_products()
        elif any(term in query_lower for term in ['adidas', 'nike', 'shoe', 'sneaker', 'running']):
            base_products = self._get_shoe_products(query)
        elif any(term in query_lower for term in ['knife', 'kitchen knife', 'chef knife', 'cutting']):
            base_products = self._get_knife_products()
        elif any(term in query_lower for term in ['headphone', 'earphone', 'audio', 'beats', 'sony']):
            base_products = self._get_headphone_products()
        elif any(term in query_lower for term in ['watch', 'smartwatch', 'apple watch', 'fitness']):
            base_products = self._get_watch_products()
        elif any(term in query_lower for term in ['tv', 'television', 'smart tv', 'led', 'oled']):
            base_products = self._get_tv_products()
        else:
            # Generic products with query-specific naming
            base_products = self._get_generic_products(query)
        
        # Site-specific pricing multipliers (each site has different pricing strategies)
        site_multipliers = {
            'Amazon India': random.uniform(0.95, 1.08),
            'Flipkart': random.uniform(0.90, 1.05),  # Often cheaper
            'Myntra': random.uniform(1.02, 1.15),    # Premium pricing
            'Snapdeal': random.uniform(0.85, 1.10)   # Most variable pricing
        }
        
        site_multiplier = site_multipliers.get(self.site_name, 1.0)
        
        # Generate products with unique variations per site
        for i, base_product in enumerate(base_products[:max_results]):
            # Add randomness based on site + product + time to ensure uniqueness
            random.seed(hash(f"{self.site_name}_{base_product['name']}_{i}_{time.time()//10}"))
            
            # Calculate varied prices
            base_price = base_product['base_price'] * site_multiplier
            price_variation = random.uniform(0.92, 1.08)
            final_price = base_price * price_variation
            
            # Varied discount percentages by site
            site_discount_ranges = {
                'Amazon India': (5, 25),
                'Flipkart': (8, 30),
                'Myntra': (10, 40),  # Fashion site - higher discounts
                'Snapdeal': (15, 45)   # Budget site - highest discounts
            }
            
            discount_range = site_discount_ranges.get(self.site_name, (5, 25))
            discount_percent = random.uniform(*discount_range)
            original_price = final_price / (1 - discount_percent/100)
            savings = original_price - final_price
            
            # Generate varied ratings (better products have better ratings)
            base_rating = base_product.get('base_rating', 4.0)
            rating_variation = random.uniform(-0.3, 0.5)
            rating = max(3.0, min(5.0, base_rating + rating_variation))
            
            # Review count varies by popularity and site
            base_reviews = base_product.get('base_reviews', 500)
            review_multiplier = random.uniform(0.3, 2.5)
            review_count = int(base_reviews * review_multiplier)
            
            # Availability varies by site and price point
            availability_chance = 0.90 if final_price < 50000 else 0.75
            if self.site_name == 'Snapdeal':
                availability_chance -= 0.1  # Snapdeal has slightly lower availability
            available = random.random() < availability_chance
            
            product = {
                'name': base_product['name'],
                'price': round(final_price, 2),
                'original_price': round(original_price, 2),
                'site': self.site_name,
                'available': available,
                'discount_percentage': round(discount_percent, 1),
                'savings': round(savings, 2),
                'rating': round(rating, 1),
                'review_count': review_count,
                'brand': base_product['brand'],
                'image_url': f'https://via.placeholder.com/300x300/{self._get_site_color()}/ffffff?text={base_product["brand"]}+{i+1}',
                'product_url': f'https://example.com/product/{hash(base_product["name"]) % 10000}',
                'specifications': base_product.get('specs', [f'Feature {j+1}' for j in range(3)]),
                'delivery_info': self._get_delivery_info(),
                'warranty': base_product.get('warranty', '1 year warranty'),
                'timestamp': time.time(),
                'deal_score': 0,
                'seller_rating': round(random.uniform(4.0, 4.9), 1),
                'return_policy': random.choice(['7 days', '10 days', '15 days', '30 days']),
                'emi_available': final_price > 10000,
                'free_delivery': random.choice([True, False]),
                'prime_eligible': self.site_name == 'Amazon India' and random.choice([True, False])
            }
            
            products.append(product)
            
            # Reset random seed to ensure different results for next product
            random.seed()
        
        return products
    
    def _get_iphone_products(self):
        return [
            {'name': 'Apple iPhone 15 (128GB) - Blue', 'base_price': 79900, 'brand': 'Apple', 'base_rating': 4.5, 'base_reviews': 2500},
            {'name': 'Apple iPhone 15 Pro (256GB) - Natural Titanium', 'base_price': 134900, 'brand': 'Apple', 'base_rating': 4.7, 'base_reviews': 1800},
            {'name': 'Apple iPhone 15 Plus (128GB) - Pink', 'base_price': 89900, 'brand': 'Apple', 'base_rating': 4.4, 'base_reviews': 1200},
            {'name': 'Apple iPhone 14 (128GB) - Midnight', 'base_price': 69900, 'brand': 'Apple', 'base_rating': 4.6, 'base_reviews': 3500},
            {'name': 'Apple iPhone 13 (128GB) - Red', 'base_price': 59900, 'brand': 'Apple', 'base_rating': 4.5, 'base_reviews': 4500},
            {'name': 'Apple iPhone 15 Pro Max (256GB) - Blue Titanium', 'base_price': 159900, 'brand': 'Apple', 'base_rating': 4.8, 'base_reviews': 1500},
            {'name': 'Apple iPhone 14 Pro (256GB) - Deep Purple', 'base_price': 119900, 'brand': 'Apple', 'base_rating': 4.7, 'base_reviews': 2200},
            {'name': 'Apple iPhone 12 (64GB) - White', 'base_price': 49900, 'brand': 'Apple', 'base_rating': 4.4, 'base_reviews': 5000}
        ]
    
    def _get_samsung_products(self):
        return [
            {'name': 'Samsung Galaxy S24 Ultra (256GB) - Titanium Gray', 'base_price': 124999, 'brand': 'Samsung', 'base_rating': 4.4, 'base_reviews': 1800},
            {'name': 'Samsung Galaxy S24 (128GB) - Onyx Black', 'base_price': 79999, 'brand': 'Samsung', 'base_rating': 4.3, 'base_reviews': 2200},
            {'name': 'Samsung Galaxy Z Fold5 (256GB) - Phantom Black', 'base_price': 154999, 'brand': 'Samsung', 'base_rating': 4.2, 'base_reviews': 800},
            {'name': 'Samsung Galaxy A54 5G (128GB) - Awesome Blue', 'base_price': 38999, 'brand': 'Samsung', 'base_rating': 4.1, 'base_reviews': 3200},
            {'name': 'Samsung Galaxy S23 FE (128GB) - Purple', 'base_price': 59999, 'brand': 'Samsung', 'base_rating': 4.2, 'base_reviews': 1500},
            {'name': 'Samsung Galaxy M34 5G (128GB) - Waterfall Blue', 'base_price': 18999, 'brand': 'Samsung', 'base_rating': 4.0, 'base_reviews': 2800},
            {'name': 'Samsung Galaxy Z Flip5 (256GB) - Mint', 'base_price': 99999, 'brand': 'Samsung', 'base_rating': 4.1, 'base_reviews': 600},
            {'name': 'Samsung Galaxy Note 20 Ultra (256GB) - Mystic Bronze', 'base_price': 89999, 'brand': 'Samsung', 'base_rating': 4.3, 'base_reviews': 1200}
        ]
    
    def _get_laptop_products(self):
        return [
            {'name': 'MacBook Air M2 (256GB) - Midnight', 'base_price': 114900, 'brand': 'Apple', 'base_rating': 4.6, 'base_reviews': 1200},
            {'name': 'Dell XPS 13 Intel i7 (512GB SSD)', 'base_price': 124990, 'brand': 'Dell', 'base_rating': 4.3, 'base_reviews': 800},
            {'name': 'HP Pavilion 15 AMD Ryzen 5', 'base_price': 54990, 'brand': 'HP', 'base_rating': 4.1, 'base_reviews': 1500},
            {'name': 'Lenovo ThinkPad E14 Intel i5', 'base_price': 65990, 'brand': 'Lenovo', 'base_rating': 4.2, 'base_reviews': 900},
            {'name': 'ASUS VivoBook 15 Intel i3', 'base_price': 39990, 'brand': 'ASUS', 'base_rating': 4.0, 'base_reviews': 2200},
            {'name': 'Acer Aspire 5 AMD Ryzen 7', 'base_price': 67990, 'brand': 'Acer', 'base_rating': 4.1, 'base_reviews': 1100},
            {'name': 'MSI Modern 14 Intel i7', 'base_price': 84990, 'brand': 'MSI', 'base_rating': 4.2, 'base_reviews': 600},
            {'name': 'Surface Laptop 5 Intel i7', 'base_price': 149990, 'brand': 'Microsoft', 'base_rating': 4.4, 'base_reviews': 400}
        ]
    
    def _get_shoe_products(self, query):
        brand = 'Adidas' if 'adidas' in query.lower() else 'Nike' if 'nike' in query.lower() else 'Generic'
        return [
            {'name': f'{brand} Ultraboost 22 Running Shoes - Black', 'base_price': 16999, 'brand': brand, 'base_rating': 4.3, 'base_reviews': 850},
            {'name': f'{brand} Air Max 270 - White/Blue', 'base_price': 12999, 'brand': brand, 'base_rating': 4.2, 'base_reviews': 1200},
            {'name': f'{brand} Stan Smith Casual Sneakers - White', 'base_price': 8999, 'brand': brand, 'base_rating': 4.4, 'base_reviews': 2100},
            {'name': f'{brand} Football Boots - Black/Orange', 'base_price': 7999, 'brand': brand, 'base_rating': 4.1, 'base_reviews': 650},
            {'name': f'{brand} Training Shoes - Gray', 'base_price': 5999, 'brand': brand, 'base_rating': 4.0, 'base_reviews': 980},
            {'name': f'{brand} Basketball High-Tops - Red', 'base_price': 14999, 'brand': brand, 'base_rating': 4.2, 'base_reviews': 420},
            {'name': f'{brand} Hiking Boots - Brown', 'base_price': 11999, 'brand': brand, 'base_rating': 4.3, 'base_reviews': 330},
            {'name': f'{brand} Casual Slip-On - Navy', 'base_price': 6999, 'brand': brand, 'base_rating': 4.1, 'base_reviews': 1100}
        ]
    
    def _get_knife_products(self):
        return [
            {'name': 'Chef\'s Knife 8-inch German Steel', 'base_price': 2999, 'brand': 'KitchenPro', 'base_rating': 4.5, 'base_reviews': 420},
            {'name': 'Santoku Knife Japanese Carbon Steel', 'base_price': 4999, 'brand': 'Yamato', 'base_rating': 4.7, 'base_reviews': 280},
            {'name': 'Paring Knife Set (3-piece)', 'base_price': 1999, 'brand': 'SharpEdge', 'base_rating': 4.2, 'base_reviews': 650},
            {'name': 'Bread Knife Serrated 9-inch', 'base_price': 1799, 'brand': 'BreadMaster', 'base_rating': 4.1, 'base_reviews': 380},
            {'name': 'Utility Knife 6-inch Stainless Steel', 'base_price': 1499, 'brand': 'KitchenAce', 'base_rating': 4.0, 'base_reviews': 520},
            {'name': 'Butcher Knife Heavy Duty', 'base_price': 3499, 'brand': 'MeatPro', 'base_rating': 4.3, 'base_reviews': 210},
            {'name': 'Kitchen Knife Set (5-piece) with Block', 'base_price': 7999, 'brand': 'ChefSet', 'base_rating': 4.4, 'base_reviews': 890},
            {'name': 'Fillet Knife Flexible Blade', 'base_price': 2499, 'brand': 'FishPro', 'base_rating': 4.2, 'base_reviews': 150}
        ]
    
    def _get_headphone_products(self):
        return [
            {'name': 'Sony WH-1000XM4 Wireless Noise Cancelling', 'base_price': 29990, 'brand': 'Sony', 'base_rating': 4.6, 'base_reviews': 1800},
            {'name': 'Apple AirPods Pro (2nd Gen)', 'base_price': 26900, 'brand': 'Apple', 'base_rating': 4.5, 'base_reviews': 2200},
            {'name': 'Bose QuietComfort 45', 'base_price': 32900, 'brand': 'Bose', 'base_rating': 4.4, 'base_reviews': 950},
            {'name': 'JBL Tune 760NC Wireless', 'base_price': 7999, 'brand': 'JBL', 'base_rating': 4.1, 'base_reviews': 1500},
            {'name': 'Sennheiser HD 450BT', 'base_price': 12999, 'brand': 'Sennheiser', 'base_rating': 4.3, 'base_reviews': 680},
            {'name': 'Beats Studio3 Wireless', 'base_price': 22900, 'brand': 'Beats', 'base_rating': 4.2, 'base_reviews': 1100},
            {'name': 'Audio-Technica ATH-M50xBT2', 'base_price': 18999, 'brand': 'Audio-Technica', 'base_rating': 4.4, 'base_reviews': 420},
            {'name': 'Skullcandy Crusher Wireless', 'base_price': 8999, 'brand': 'Skullcandy', 'base_rating': 4.0, 'base_reviews': 890}
        ]
    
    def _get_watch_products(self):
        return [
            {'name': 'Apple Watch Series 9 (45mm) GPS', 'base_price': 45900, 'brand': 'Apple', 'base_rating': 4.5, 'base_reviews': 1200},
            {'name': 'Samsung Galaxy Watch6 Classic', 'base_price': 39999, 'brand': 'Samsung', 'base_rating': 4.3, 'base_reviews': 800},
            {'name': 'Fitbit Charge 5 Fitness Tracker', 'base_price': 14999, 'brand': 'Fitbit', 'base_rating': 4.1, 'base_reviews': 1500},
            {'name': 'Garmin Venu 2 Plus Smartwatch', 'base_price': 44990, 'brand': 'Garmin', 'base_rating': 4.4, 'base_reviews': 450},
            {'name': 'Amazfit GTR 4 Smartwatch', 'base_price': 17999, 'brand': 'Amazfit', 'base_rating': 4.2, 'base_reviews': 920},
            {'name': 'Fossil Gen 6 Smartwatch', 'base_price': 22995, 'brand': 'Fossil', 'base_rating': 4.0, 'base_reviews': 380},
            {'name': 'Huawei Watch GT 3 Pro', 'base_price': 32999, 'brand': 'Huawei', 'base_rating': 4.2, 'base_reviews': 280},
            {'name': 'Noise ColorFit Pro 4 Alpha', 'base_price': 4999, 'brand': 'Noise', 'base_rating': 3.9, 'base_reviews': 2100}
        ]
    
    def _get_tv_products(self):
        return [
            {'name': 'Samsung 55" Neo QLED 4K Smart TV', 'base_price': 89990, 'brand': 'Samsung', 'base_rating': 4.4, 'base_reviews': 650},
            {'name': 'LG 65" OLED C3 4K Smart TV', 'base_price': 139990, 'brand': 'LG', 'base_rating': 4.6, 'base_reviews': 420},
            {'name': 'Sony Bravia 55" 4K LED Google TV', 'base_price': 74990, 'brand': 'Sony', 'base_rating': 4.3, 'base_reviews': 880},
            {'name': 'TCL 43" 4K Android TV', 'base_price': 28999, 'brand': 'TCL', 'base_rating': 4.0, 'base_reviews': 1200},
            {'name': 'Mi TV 5X 50" 4K Ultra HD Smart TV', 'base_price': 39999, 'brand': 'Xiaomi', 'base_rating': 4.1, 'base_reviews': 1800},
            {'name': 'OnePlus TV 55" U1S 4K LED', 'base_price': 44999, 'brand': 'OnePlus', 'base_rating': 4.2, 'base_reviews': 520},
            {'name': 'Hisense 65" ULED 4K Smart TV', 'base_price': 79999, 'brand': 'Hisense', 'base_rating': 4.1, 'base_reviews': 280},
            {'name': 'VU 32" HD Ready Smart TV', 'base_price': 16999, 'brand': 'VU', 'base_rating': 3.9, 'base_reviews': 950}
        ]
    
    def _get_generic_products(self, query):
        # Create varied generic products based on query
        variations = [
            'Premium Edition', 'Pro Version', 'Standard Model', 'Elite Series',
            'Basic Version', 'Advanced Model', 'Compact Edition', 'Deluxe Version'
        ]
        
        return [
            {
                'name': f'{query.title()} - {variation}',
                'base_price': random.randint(5000, 50000),
                'brand': random.choice(['Premium', 'Pro', 'Elite', 'Standard', 'Advanced']),
                'base_rating': round(random.uniform(3.5, 4.5), 1),
                'base_reviews': random.randint(100, 1500)
            }
            for variation in variations
        ]
    
    def _get_site_color(self):
        colors = {
            'Amazon India': 'FF9500',
            'Flipkart': '2874F0',
            'Myntra': 'FF3F6C',
            'Snapdeal': 'E53E3E'
        }
        return colors.get(self.site_name, '667EEA')
    
    def _get_delivery_info(self):
        options = {
            'Amazon India': ['Same day delivery', 'Next day delivery', '2 days delivery'],
            'Flipkart': ['Next day delivery', '2-3 days delivery', 'Express delivery'],
            'Myntra': ['2-3 days delivery', '3-5 days delivery', 'Standard delivery'],
            'Snapdeal': ['3-5 days delivery', '5-7 days delivery', 'Standard delivery']
        }
        return random.choice(options.get(self.site_name, ['Standard delivery', '2-3 days']))

def create_agent(site_name):
    """Create enhanced mock agent"""
    return EnhancedMockAgent(site_name)

def run_agent_search(agent, query, search_id, max_results=8):
    """Run agent search in background with better error handling"""
    try:
        search_status[search_id]['agent_statuses'][agent.site_name] = {
            'status': 'running',
            'products_found': 0,
            'error': None
        }
        
        # Simulate processing time with variation
        processing_time = random.uniform(1.5, 4.0)
        time.sleep(processing_time)
        
        products = agent.search_products(query, max_results)
        
        search_results[search_id]['products'].extend(products)
        search_status[search_id]['agent_statuses'][agent.site_name] = {
            'status': 'completed',
            'products_found': len(products),
            'error': None
        }
        
        # Update overall progress
        completed_agents = sum(1 for status in search_status[search_id]['agent_statuses'].values() 
                              if status['status'] in ['completed', 'failed'])
        total_agents = search_status[search_id]['total_agents']
        search_status[search_id]['progress'] = (completed_agents / total_agents) * 100
        search_status[search_id]['agents_completed'] = completed_agents
        
        if completed_agents == total_agents:
            search_status[search_id]['status'] = 'completed'
            search_status[search_id]['end_time'] = time.time()
            search_status[search_id]['duration'] = search_status[search_id]['end_time'] - search_status[search_id]['start_time']
            
    except Exception as e:
        print(f"Error with {agent.site_name} agent: {e}")
        search_status[search_id]['agent_statuses'][agent.site_name] = {
            'status': 'failed',
            'products_found': 0,
            'error': str(e)
        }

@app.route('/')
def serve_frontend():
    """Serve the main HTML file"""
    try:
        return send_from_directory('.', 'index.html')
    except FileNotFoundError:
        return jsonify({
            'status': 'Backend Running ✅',
            'message': 'index.html not found in current directory',
            'error': '404 Not Found: The requested URL was not found on the server.',
            'available_endpoints': [
                'GET /api/health - Health check',
                'POST /api/compare - Start price comparison',
                'GET /api/status/<id> - Get search status', 
                'GET /api/results/<id> - Get search results',
                'GET /api/trends/<product> - Price trends'
            ]
        }), 404

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'server': 'Smart Price Hunter Backend - Enhanced',
        'version': '2.1',
        'features': ['Enhanced Mock Data', 'Varied Products', 'Realistic Pricing']
    })

@app.route('/api/compare', methods=['POST'])
def start_comparison():
    """Start price comparison across multiple sites"""
    try:
        data = request.json
        product_query = data.get('product', '')
        selected_sites = data.get('sites', [])
        
        if not product_query or not selected_sites:
            return jsonify({'error': 'Missing product query or sites'}), 400
        
        search_id = str(uuid.uuid4())
        print(f"🚀 Starting price comparison: {search_id} for '{product_query}'")
        
        # Map site codes to full names
        site_mapping = {
            'amazon': 'Amazon India',
            'flipkart': 'Flipkart',
            'myntra': 'Myntra',
            'snapdeal': 'Snapdeal'
        }
        
        selected_site_names = [site_mapping.get(site, site) for site in selected_sites]
        
        # Initialize search results
        search_results[search_id] = {
            'product_query': product_query,
            'sites': selected_site_names,
            'products': [],
            'created_at': datetime.now().isoformat()
        }
        
        search_status[search_id] = {
            'status': 'running',
            'progress': 0,
            'start_time': time.time(),
            'end_time': None,
            'duration': 0,
            'total_agents': len(selected_site_names),
            'agents_completed': 0,
            'agent_statuses': {}
        }
        
        # Create and start agents
        threads = []
        for site_name in selected_site_names:
            agent = create_agent(site_name)
            thread = threading.Thread(
                target=run_agent_search,
                args=(agent, product_query, search_id, 8)
            )
            thread.start()
            threads.append(thread)
        
        return jsonify({
            'search_id': search_id,
            'status': 'started',
            'sites': selected_site_names,
            'message': f'Scanning {len(selected_site_names)} sites for "{product_query}"'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<search_id>')
def get_search_status(search_id):
    """Get search status"""
    if search_id not in search_status:
        return jsonify({'error': 'Search not found'}), 404
    
    status = search_status[search_id].copy()
    if status['start_time']:
        current_time = status['end_time'] if status['end_time'] else time.time()
        status['duration'] = current_time - status['start_time']
    
    return jsonify(status)

@app.route('/api/results/<search_id>')
def get_search_results(search_id):
    """Get search results"""
    if search_id not in search_results:
        return jsonify({'error': 'Search not found'}), 404
    
    if search_status[search_id]['status'] != 'completed':
        return jsonify({'error': 'Search still in progress'}), 202
    
    results = search_results[search_id]
    
    # Calculate enhanced summary statistics
    products = results['products']
    available_products = [p for p in products if p.get('available', True)]
    
    if available_products:
        prices = [p['price'] for p in available_products]
        best_deal = min(available_products, key=lambda x: x['price'])
        
        summary = {
            'total_products': len(products),
            'available_products': len(available_products),
            'sites_checked': list(set(p['site'] for p in products)),
            'price_range': {
                'min': min(prices),
                'max': max(prices),
                'average': sum(prices) / len(prices)
            },
            'best_deal': {
                'name': best_deal['name'],
                'price': best_deal['price'],
                'site': best_deal['site'],
                'savings': best_deal.get('savings', 0),
                'discount_percentage': best_deal.get('discount_percentage', 0)
            },
            'duration': search_status[search_id].get('duration', 0),
            'total_savings': sum(p.get('savings', 0) for p in products),
            'average_rating': sum(p.get('rating', 0) for p in products if p.get('rating', 0) > 0) / len([p for p in products if p.get('rating', 0) > 0]) if any(p.get('rating', 0) > 0 for p in products) else 0
        }
    else:
        summary = {
            'total_products': len(products),
            'available_products': 0,
            'sites_checked': list(set(p['site'] for p in products)),
            'price_range': {'min': 0, 'max': 0, 'average': 0},
            'best_deal': None,
            'duration': search_status[search_id].get('duration', 0),
            'total_savings': 0,
            'average_rating': 0
        }
    
    return jsonify({
        'search_id': search_id,
        'product_query': results['product_query'],
        'products': products,
        'summary': summary,
        'created_at': results['created_at'],
        'status': search_status[search_id]['status']
    })

@app.route('/api/trends/<product>')
def get_price_trends(product):
    """Get realistic price trends for charts"""
    # Generate more realistic trend data based on product type
    dates = []
    prices = []
    
    # Base price varies by product type
    if 'iphone' in product.lower():
        base_price = random.randint(60000, 120000)
    elif 'laptop' in product.lower():
        base_price = random.randint(40000, 100000)
    elif 'shoe' in product.lower() or 'adidas' in product.lower():
        base_price = random.randint(5000, 20000)
    elif 'knife' in product.lower():
        base_price = random.randint(1000, 8000)
    else:
        base_price = random.randint(10000, 50000)
    
    # Generate 30 days of realistic price trends
    current_price = base_price
    for i in range(30):
        dates.append(f"Day {i+1}")
        
        # Add realistic price fluctuations
        daily_change = random.uniform(-0.05, 0.03)  # Slight downward trend (sales/discounts)
        seasonal_factor = 1 + 0.1 * random.sin(i / 30 * 2 * 3.14159)  # Seasonal variation
        
        current_price = current_price * (1 + daily_change) * seasonal_factor
        prices.append(round(current_price, 2))
    
    return jsonify({
        'product': product,
        'dates': dates,
        'prices': prices,
        'currency': 'INR',
        'trend': 'downward' if prices[-1] < prices[0] else 'upward',
        'volatility': 'moderate'
    })

if __name__ == '__main__':
    print("🚀 Starting Enhanced Smart Price Hunter Backend Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🎯 API endpoints:")
    print("  - POST /api/compare - Start price comparison")
    print("  - GET /api/status/<id> - Get search status")
    print("  - GET /api/results/<id> - Get search results")
    print("  - GET /api/health - Health check")
    print("  - GET /api/trends/<product> - Price trends")
    print("🌟 Features: Enhanced Mock Data, Varied Products, Realistic Pricing")
    print("🌐 Open http://localhost:8000 in your browser to use the UI")
    
    app.run(host='0.0.0.0', port=8000, debug=True)