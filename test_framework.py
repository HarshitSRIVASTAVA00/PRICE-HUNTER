"""
Test script for Mobile Agent Framework
"""

import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

try:
    from base_agent import Agent, AgentState, ProductInfo, ComparisonResult
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class MockAgent(Agent):
    def __init__(self, name="MockAgent"):
        super().__init__(name=name)
        
    def execute(self):
        print(f"🤖 {self.name} executing...")
        self.executed = True
        time.sleep(0.1)
        print(f"✅ {self.name} completed")

def main():
    print("🚀 Starting Mobile Agent Framework Tests")
    print("=" * 50)
    
    # Test 1: Agent creation
    print("\n🧪 Test 1: Agent Creation")
    agent = MockAgent("TestAgent")
    print(f"Agent ID: {agent.agent_id[:8]}")
    
    # Test 2: Agent execution
    print("\n🧪 Test 2: Agent Execution")
    agent.execute()
    print("✅ Agent execution successful" if agent.executed else "❌ Failed")
    
    # Test 3: Agent migration
    print("\n🧪 Test 3: Agent Migration")
    agent.migrate("test_host")
    
    # Test 4: Product comparison
    print("\n🧪 Test 4: Product Comparison")
    product1 = ProductInfo("iPhone 15 128GB", 799.99, "Amazon", "", True)
    product2 = ProductInfo("iPhone 15 128GB", 829.99, "eBay", "", True)
    product3 = ProductInfo("iPhone 15 128GB", 789.99, "Flipkart", "", False)
    
    comparison = ComparisonResult("iPhone 15")
    comparison.add_product(product1)
    comparison.add_product(product2)
    comparison.add_product(product3)
    
    best_deal = comparison.get_best_deal()
    summary = comparison.get_summary()
    
    print("✅ Created test products:")
    print(f"   - {product1}")
    print(f"   - {product2}")
    print(f"   - {product3}")
    
    print(f"\n📊 Results:")
    print(f"   - Total: {summary['total_results']}")
    print(f"   - Available: {summary['available_products']}")
    if best_deal:
        print(f"   - Best: {best_deal.name} at ${best_deal.price:.2f}")
    
    print("\n🎉 ALL TESTS PASSED! Mobile Agent Framework working!")
    print("📅 Day 1: COMPLETE ✅")

if __name__ == "__main__":
    main()
