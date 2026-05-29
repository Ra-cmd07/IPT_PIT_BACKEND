"""
Simple test script to verify chatbot setup
Run: python test_chatbot_setup.py
"""

import os
import sys
import django

# Load environment variables manually to avoid python-dotenv dependency issues
base_dir = os.path.dirname(os.path.abspath(__file__))
env_paths = ['.env', '.env.txt', 'env.txt']
loaded = False
for p in env_paths:
    env_path = os.path.join(base_dir, p)
    if os.path.exists(env_path):
        loaded = True
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        k, v = line.split('=', 1)
                        if k.strip() == 'OPENAI_API_KEY':
                            os.environ['OPENAI_API_KEY'] = v.strip().strip("'\"")
                    elif line.startswith('sk-') or line.startswith('gsk_') or line.startswith('AIza'):
                        os.environ['OPENAI_API_KEY'] = line.strip()

if not loaded:
    print(f"\n⚠️  Warning: No .env file found in {base_dir}")

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitchen_system.settings')
django.setup()

from chatbot.models import ChatMessage, ChatFAQ
from django.contrib.auth.models import User

def test_database():
    """Test database connectivity"""
    print("✓ Testing database connectivity...")
    try:
        count = ChatFAQ.objects.count()
        print(f"  Found {count} FAQs in database")
        return True
    except Exception as e:
        print(f"  ✗ Database error: {e}")
        return False

def test_models():
    """Test model creation"""
    print("\n✓ Testing model creation...")
    try:
        # Check ChatFAQ model
        faq_count = ChatFAQ.objects.count()
        print(f"  ChatFAQ model: OK ({faq_count} records)")
        
        # Check ChatMessage model
        msg_count = ChatMessage.objects.count()
        print(f"  ChatMessage model: OK ({msg_count} records)")
        
        return True
    except Exception as e:
        print(f"  ✗ Model error: {e}")
        return False

def test_openai_key():
    """Test OpenAI API key"""
    print("\n✓ Testing OpenAI API key...")
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("  ✗ OPENAI_API_KEY not set in environment")
        
        print("\n  💡 Let's fix this! Please paste your OpenAI API key below.")
        print("  (It should start with 'sk-' for OpenAI, 'gsk_' for Groq, or 'AIza' for Gemini)")
        user_input = input("  API Key (or press Enter to skip): ").strip()
        
        if user_input.startswith('sk-') or user_input.startswith('gsk_') or user_input.startswith('AIza'):
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
            with open(env_path, 'a') as f:
                f.write(f"\nOPENAI_API_KEY={user_input}\n")
            print(f"  ✓ Saved your key correctly to {env_path}")
            os.environ['OPENAI_API_KEY'] = user_input
            api_key = user_input
        else:
            return False
    
    if api_key.startswith('sk-') or api_key.startswith('gsk_') or api_key.startswith('AIza'):
        print(f"  API key found: {api_key[:20]}...")
        return True
    else:
        print("  ✗ Invalid API key format (should start with 'sk-', 'gsk_', or 'AIza')")
        return False

def test_faq_data():
    """Test FAQ data"""
    print("\n✓ Testing FAQ data...")
    
    categories = dict(ChatFAQ._meta.get_field('category').choices)
    print(f"  Available categories: {', '.join(categories.values())}")
    
    try:
        by_category = {}
        for cat_code in categories.keys():
            count = ChatFAQ.objects.filter(category=cat_code).count()
            if count > 0:
                by_category[cat_code] = count
        
        if by_category:
            for cat, count in by_category.items():
                print(f"  Category '{cat}': {count} FAQs")
            return True
        else:
            print("  ⚠ No FAQs found. Run: python manage.py init_faqs")
            return False
    except Exception as e:
        print(f"  ✗ FAQ error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints are registered"""
    print("\n✓ Testing API endpoints...")
    
    from django.urls import reverse
    
    endpoints = [
        'chatbot',
        'api-root',
    ]
    
    for endpoint in endpoints:
        try:
            url = reverse(endpoint)
            print(f"  ✓ {endpoint}: {url}")
        except Exception as e:
            print(f"  ✗ {endpoint}: {e}")
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("🤖 Customer Support Chatbot - Setup Verification")
    print("=" * 60)
    
    results = []
    
    results.append(("Database Connection", test_database()))
    results.append(("Django Models", test_models()))
    results.append(("OpenAI API Key", test_openai_key()))
    results.append(("FAQ Data", test_faq_data()))
    results.append(("API Endpoints", test_api_endpoints()))
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All systems ready! Your chatbot is configured correctly.")
        print("\nNext steps:")
        print("1. Start Django: python manage.py runserver 8000")
        print("2. Start React: cd frontend && npm run dev")
        print("3. Open browser and click the chat widget!")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
