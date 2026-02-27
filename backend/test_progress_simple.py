#!/usr/bin/env python3
"""
Test script to verify the progress API is working correctly
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8001/api"
TEST_CREDENTIALS = {
    "identifier": "EMP-TEST-01",
    "password": "learner123"
}

def test_progress_api():
    """Test the progress API functionality"""
    
    print("Logging in...")
    
    # Login to get token
    resp = requests.post(f"{BASE_URL}/auth/login", json=TEST_CREDENTIALS)
    if resp.status_code != 200:
        print(f"Login failed: {resp.status_code}")
        print(f"Response: {resp.text}")
        return
    
    login_data = resp.json()
    token = login_data["access_token"]
    user = login_data["user"]
    print(f"Logged in as {user['first_name']} {user['last_name']} ({user['email']})")
    
    # Set authorization header
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\nGetting enrolled courses...")
    
    # Get enrolled courses
    resp = requests.get(f"{BASE_URL}/courses/enrolled", headers=headers)
    if resp.status_code != 200:
        print(f"Failed to get courses: {resp.status_code}")
        print(f"Response: {resp.text}")
        return
    
    courses = resp.json()
    if not courses:
        print("No enrolled courses found")
        return
    
    print(f"Found {len(courses)} enrolled courses")
    course = courses[0]
    print(f"Testing with course: {course['title']}")
    
    print(f"\nGetting course details...")
    
    # Get course details
    resp = requests.get(f"{BASE_URL}/courses/{course['id']}", headers=headers)
    if resp.status_code != 200:
        print(f"Failed to get course details: {resp.status_code}")
        print(f"Response: {resp.text}")
        return
    
    course_details = resp.json()
    modules = course_details.get("modules", [])
    if not modules:
        print("No modules found in course")
        return
    
    lessons = []
    for module in modules:
        lessons.extend(module.get("lessons", []))
    
    if not lessons:
        print("No lessons found in course")
        return
    
    print(f"Found {len(lessons)} lessons")
    lesson = lessons[0]
    print(f"Testing with lesson: {lesson['title']}")
    
    print(f"\nUpdating lesson progress...")
    
    # Update lesson progress
    progress_data = {
        "lesson_id": lesson["id"],
        "completed": True
    }
    
    resp = requests.post(f"{BASE_URL}/progress/lesson", json=progress_data, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to update progress: {resp.status_code}")
        print(f"Response: {resp.text}")
        return
    
    result = resp.json()
    print(f"Progress updated successfully!")
    print(f"New percentage: {result.get('percentage', 0)}%")
    
    print(f"\nVerifying progress update...")
    
    # Verify progress was saved
    resp = requests.get(f"{BASE_URL}/progress/course/{course['id']}", headers=headers)
    if resp.status_code != 200:
        print(f"Failed to get progress: {resp.status_code}")
        print(f"Response: {resp.text}")
        return
    
    progress = resp.json()
    completed_lessons = progress.get("completed_lessons", [])
    
    if lesson["id"] in completed_lessons:
        print(f"Lesson marked as completed!")
        print(f"Course progress: {progress.get('percentage', 0)}%")
        print(f"Completed lessons: {len(completed_lessons)}")
    else:
        print(f"Lesson not found in completed lessons")
        print(f"Completed lessons: {completed_lessons}")

if __name__ == "__main__":
    print("Testing Progress API")
    print("=" * 50)
    test_progress_api()