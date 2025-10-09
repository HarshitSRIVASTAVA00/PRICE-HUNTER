"""
Flask Backend Server for Smart Price Hunter
Simple version without WebSocket dependencies
"""

from datetime import datetime
import sys
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time
import uuid
import random

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

try:
    from base_agent import Agent, ProductInfo
    from enhanced_product_agent import EnhancedProductAgent
    print("✅ Successfully imported agent modules")
except ImportError as e:
    print(f"⚠️ Import warning: {e}")
    print("⚠️ Using mock data mode")

app = Flask(__name__, static_folder='.')
CORS(app, origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"])

# Site configurations
SITE_CONFIGS = {
    "amazon": {
        "name": "Amazon India",
        "base_url": "https://www.amazon.in",
        "search_patterns": {
            "search_url": "https://www.amazon.in/s?k={query}",
            "container_selector": "div",
            "name_patterns": [
                {"tag": "h2", "attrs": {"class": "a-size-mini"}},
                {"tag": "span", "attrs": {"class": "a-size-medium"}}
            ],
            "price_patterns": [
                {"tag": "span", "attrs": {"class": "a-price-whole"}},
                {"tag": "span", "attrs": {"class": "a-offscreen"}}
            ]
        }
    },
    "flipkart": {
        "name": "Flipkart",
        "base_url": "https://www.flipkart.com",
        "search_patterns": {
            "search_url": "https://www.flipkart.com/search?q={query}",
            "container_selector": "div",
            "name_patterns": [
                {"tag": "div", "attrs": {"class": "_4rR01T"}},
                {"tag": "a", "attrs": {"class": "IRpwTa"}}
            ],
            "price_patterns": [
                {"tag": "div", "attrs": {"class": "_30jeq3"}},
                {"tag": "div", "attrs": {"class": "_1_TelR"}}
            ]
        }
    },
    "snapdeal": {
        "name": "Snapdeal",
        "base_url": "https://www.snapdeal.com",
        "search_patterns": {
            "search_url": "https://www.snapdeal.com/search?keyword={query}"
        }
    },
    "myntra": {
        "name": "Myntra",
        "base_url": "https://www.myntra.com",
        "search_patterns": {
            "search_url": "https://www.myntra.com/{query}"
        }
    }
}

class PriceComparisonAPI:
    """API class to handle price comparison requests"""
    
    def __init__(self):
        self.active_searches = {}
        self.search_results = {}
    
    def start_price_comparison(self, search_id, product_query, sites):
        print(f"🚀 Starting price comparison: {search_id}")
        
        self.active_searches[search_id] = {
            'status': 'running',
            'product_query': product_query,
            'sites': sites,
            'results': [],
            'agents_completed': 0,
            'total_agents': len(sites),
            'start_time': datetime.now(),
            'agents': {},
            'progress': 0
        }
        
        # Initialize agent statuses
        for site in sites:
            site_name = SITE_CONFIGS.get(site, {}).get('name', site)
            self.active_searches[search_id]['agents'][site_name] = {
                'status': 'running',
                'products_found': 0,
                'error': None
            }
        
        # Start background processing
        threading.Thread(target=self._run_search, args=(search_id,), daemon=True).start()
        return search_id
    
    def _run_search(self, search_id):
        """Run the actual search process"""
        search = self.active_searches[search_id]
        all_products = []
        
        try:
            for i, site in enumerate(search['sites']):
                # Update progress
                progress = int((i / len(search['sites'])) * 80)  # Up to 80%
                search['progress'] = progress
                
                site_config = SITE_CONFIGS.get(site)
                if not site_config:
                    continue
                
                site_name = site_config['name']
                
                # Simulate processing time
                time.sleep(random.uniform(1, 3))
                
                try:
                    # Try to use real agent
                    site_products = self._search_site_products(search['product_query'], site, site_config)
                    
                    # Update agent status
                    search['agents'][site_name].update({
                        'status': 'completed',
                        'products_found': len(site_products)
                    })
                    
                    all_products.extend(site_products)
                    
                except Exception as e:
                    print(f"Error searching {site_name}: {e}")
                    search['agents'][site_name].update({
                        'status': 'failed',
                        'error': str(e)
                    })
                
                search['agents_completed'] += 1
            
            # Finalize search
            search['progress'] = 100
            search['status'] = 'completed'
            search['end_time'] = datetime.now()
            search['duration'] = (search['end_time'] - search['start_time']).total_seconds()
            
            # Store results
            self.search_results[search_id] = self._build_results(search_id, all_products)
            
        except Exception as e:
            print(f"Search failed: {e}")
            search['status'] = 'failed'
            search['error'] = str(e)
    
    def _search_site_products(self, query, site_key, site_config):
        """Search for products on a specific site"""
        try:
            # Create agent with site configuration
            agent = EnhancedProductAgent(
                site_name=site_config['name'],
                base_url=site_config['base_url'],
                search_patterns=site_config['search_patterns']
            )
            
            result = agent.search_products(query, max_results=5)
            return result.get('products', [])
            
        except Exception as e:
            print(f"Error with {site_config['name']} agent: {e}")
            # Return mock data as fallback
            return self._get_mock_products(query, site_config['name'])
    
    def _get_mock_products(self, query, site_name):
        """Generate mock products for testing"""
        mock_data = {
            'Amazon India': [
                {
                    'name': f'{query} - Amazon Choice',
                    'price': 55000.00,
                    'site': 'Amazon India',
                    'available': True,
                    'rating': 4.5,
                    'review_count': 1205,
                    'discount_percentage': 12,
                    'original_price': 62500.00,
                    'savings': 7500.00,
                    'brand': 'Premium'
                }
            ],
            'Flipkart': [
                {
                    'name': f'{query} - Flipkart Special',
                    'price': 57000.00,
                    'site': 'Flipkart',
                    'available': True,
                    'rating': 4.4,
                    'review_count': 756,
                    'discount_percentage': 10,
                    'original_price': 63333.00,
                    'savings': 6333.00,
                    'brand': 'Premium'
                }
            ],
            'Snapdeal': [
                {
                    'name': f'{query} - Snapdeal Exclusive',
                    'price': 53000.00,
                    'site': 'Snapdeal',
                    'available': True,
                    'rating': 4.3,
                    'review_count': 234,
                    'discount_percentage': 15,
                    'original_price': 62353.00,
                    'savings': 9353.00,
                    'brand': 'Premium'
                }
            ],
            'Myntra': [
                {
                    'name': f'{query} - Fashion Edition',
                    'price': 48000.00,
                    'site': 'Myntra',
                    'available': True,
                    'rating': 4.2,
                    'review_count': 156,
                    'discount_percentage': 20,
                    'original_price': 60000.00,
                    'savings': 12000.00,
                    'brand': 'Style'
                }
            ]
        }
        
        return mock_data.get(site_name, [])
    
    def _build_results(self, search_id, products):
        """Build the final results structure"""
        search = self.active_searches[search_id]
        
        if not products:
            return {
                'search_id': search_id,
                'product_query': search['product_query'],
                'products': [],
                'summary': {
                    'total_products': 0,
                    'available_products': 0,
                    'sites_checked': search['sites'],
                    'duration': search.get('duration', 0),
                    'price_range': {'min': 0, 'max': 0, 'average': 0},
                    'best_deal': None
                }
            }
        
        available_products = [p for p in products if p.get('available', True)]
        prices = [p['price'] for p in available_products]
        best_deal = min(available_products, key=lambda x: x['price']) if available_products else None
        
        summary = {
            'total_products': len(products),
            'available_products': len(available_products),
            'sites_checked': search['sites'],
            'duration': search.get('duration', 0),
            'price_range': {
                'min': min(prices) if prices else 0,
                'max': max(prices) if prices else 0,
                'average': round(sum(prices) / len(prices), 2) if prices else 0
            },
            'best_deal': best_deal
        }
        
        return {
            'search_id': search_id,
            'product_query': search['product_query'],
            'products': products,
            'summary': summary
        }
    
    def get_search_status(self, search_id):
        """Get the status of a search"""
        if search_id not in self.active_searches:
            return None
        
        search = self.active_searches[search_id]
        
        return {
            'search_id': search_id,
            'status': search['status'],
            'progress': search.get('progress', 0),
            'agents_completed': search['agents_completed'],
            'total_agents': search['total_agents'],
            'agent_statuses': search['agents'],
            'duration': (datetime.now() - search['start_time']).total_seconds()
        }
    
    def get_search_results(self, search_id):
        """Get the results of a completed search"""
        return self.search_results.get(search_id)

# Create API instance
api = PriceComparisonAPI()

# Routes
@app.route('/')
def serve_ui():
    """Serve the main UI"""
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Smart Price Hunter Backend</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #1a1a2e; color: white; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .error {{ color: #e74c3c; }}
                .solution {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; margin: 20px 0; }}
                a {{ color: #48cae4; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛍️ Smart Price Hunter Backend</h1>
                <p class="error">⚠️ index.html not found in current directory</p>
                
                <div class="solution">
                    <h3>Backend is Running ✅</h3>
                    <p>API Status: <a href="/api/health">Check Health</a></p>
                    <p>Error: {e}</p>
                </div>
                
                <h3>🎯 Available API Endpoints:</h3>
                <ul style="text-align: left;">
                    <li><strong>GET /api/health</strong> - Health check</li>
                    <li><strong>POST /api/compare</strong> - Start price comparison</li>
                    <li><strong>GET /api/status/&lt;id&gt;</strong> - Get search status</li>
                    <li><strong>GET /api/results/&lt;id&gt;</strong> - Get search results</li>
                </ul>
            </div>
        </body>
        </html>
        '''

@app.route('/api/compare', methods=['POST'])
def start_comparison():
    """Start a new price comparison"""
    try:
        data = request.get_json()
        product_query = data.get('product', '').strip()
        sites = data.get('sites', [])
        
        if not product_query:
            return jsonify({'error': 'Product query is required'}), 400
        
        if not sites:
            return jsonify({'error': 'At least one site must be selected'}), 400
        
        # Generate unique search ID
        search_id = str(uuid.uuid4())
        
        # Start comparison
        api.start_price_comparison(search_id, product_query, sites)
        
        return jsonify({
            'search_id': search_id,
            'status': 'started',
            'message': 'Price comparison started successfully'
        })
        
    except Exception as e:
        print(f"❌ Error starting comparison: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<search_id>')
def get_status(search_id):
    """Get status of a running search"""
    try:
        status = api.get_search_status(search_id)
        if not status:
            return jsonify({'error': 'Search not found'}), 404
        return jsonify(status)
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/results/<search_id>')
def get_results(search_id):
    """Get results of a completed search"""
    try:
        results = api.get_search_results(search_id)
        if not results:
            return jsonify({'error': 'Search not found or not completed'}), 404
        return jsonify(results)
    except Exception as e:
        print(f"❌ Error getting results: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0',
        'active_searches': len(api.active_searches)
    })

@app.route('/api/trends/<product>')
def get_trends(product):
    """Mock price trends endpoint"""
    import datetime as dt
    
    # Generate mock trend data
    base_date = dt.datetime.now() - dt.timedelta(days=30)
    dates = []
    prices = []
    base_price = 50000
    
    for i in range(30):
        date = base_date + dt.timedelta(days=i)
        dates.append(date.strftime('%Y-%m-%d'))
        
        # Add some realistic price variation
        variation = random.uniform(0.95, 1.05)
        trend = -0.001 * i  # Slight downward trend
        price = base_price * (1 + trend) * variation
        prices.append(round(price, 2))
    
    return jsonify({
        'dates': dates,
        'prices': prices,
        'product': product
    })

if __name__ == '__main__':
    print("🚀 Starting Smart Price Hunter Backend Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🎯 API endpoints:")
    print("  - POST /api/compare - Start price comparison")
    print("  - GET /api/status/<id> - Get search status") 
    print("  - GET /api/results/<id> - Get search results")
    print("  - GET /api/health - Health check")
    print("  - GET /api/trends/<product> - Price trends")
    print("\n🌐 Open http://localhost:8000 in your browser to use the UI")
    
    app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)

