import requests

try:
    response = requests.get("http://localhost:8000/api/courses")
    if response.status_code == 200:
        courses = response.json()
        print(f"API returned {len(courses)} courses")
        
        # Find Incoterms
        incoterms = [c for c in courses if 'incoterms' in c.get('title', '').lower()]
        if incoterms:
            print(f"\nIncoterms course found:")
            for c in incoterms:
                print(f"  Title: {c.get('title')}")
                print(f"  Category: {c.get('category')}")
                print(f"  Published: {c.get('published')}")
        else:
            print("\nIncoterms course NOT found in API response")
    else:
        print(f"API error: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
