import requests

try:
    response = requests.get("http://localhost:8000/api/courses/incoterms_2024")
    if response.status_code == 200:
        course = response.json()
        print(f"Course: {course.get('title')}")
        print(f"Modules: {len(course.get('modules', []))}")
        
        for module in course.get('modules', []):
            print(f"\nModule: {module.get('title')}")
            lessons = module.get('lessons', [])
            print(f"Lessons: {len(lessons)}")
            
            if lessons:
                print("\nFirst 3 lessons:")
                for i, lesson in enumerate(lessons[:3], 1):
                    print(f"{i}. {lesson.get('title')}")
                    content = lesson.get('content', '')
                    if 'src=' in content:
                        start = content.find('src="') + 5
                        end = content.find('"', start)
                        img_url = content[start:end]
                        print(f"   Image: {img_url}")
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
