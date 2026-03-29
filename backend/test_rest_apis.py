import os
import django
from django.test import Client
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

def test_rest():
    c = Client()
    
    print("\n--- Testing Concierge ---")
    r_chat = c.post('/api/concierge/chat/', data=json.dumps({'message': 'hello'}), content_type='application/json')
    print(f"Chat Status: {r_chat.status_code}")
    if r_chat.status_code == 200:
        print(f"Chat Response: {r_chat.json().get('response')[:100]}...")
    else:
        print(f"Chat Error: {r_chat.content.decode()[:500]}")

    print("\n--- Testing Scraper ---")
    r_scrape = c.post('/api/scraper/scrape/', data=json.dumps({'url': 'https://www.google.com'}), content_type='application/json')
    print(f"Scrape Status: {r_scrape.status_code}")
    if r_scrape.status_code == 201:
        print(f"Scrape Success: {r_scrape.json().get('title')}")
    else:
        print(f"Scrape Error: {r_scrape.content.decode()[:500]}")

if __name__ == "__main__":
    test_rest()
