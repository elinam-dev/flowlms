#!/usr/bin/env python3
"""
Test script to verify the progress API is working correctly
"""
import asyncio
import aiohttp
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001/api"
TEST_CREDENTIALS = {
    "identifier": "EMP-TEST-01",
    "password": "learner123"
}

async def test_progress_api():
    """Test the progress API functionality"""
    
    async with aiohttp.ClientSession() as session:
        print("🔐 Logging in...")
        
        # Login to get token
        async with session.post(f"{BASE_URL}/auth/login", json=TEST_CREDENTIALS) as resp:
            if resp.status != 200:
                print(f"❌ Login failed: {resp.status}")
                text = await resp.text()
                print(f"Response: {text}")
                return
            
            login_data = await resp.json()
            token = login_data["access_token"]
            user = login_data["user"]
            print(f"✅ Logged in as {user['first_name']} {user['last_name']} ({user['email']})")
        
        # Set authorization header
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n📚 Getting enrolled courses...")
        
        # Get enrolled courses
        async with session.get(f"{BASE_URL}/courses/enrolled", headers=headers) as resp:
            if resp.status != 200:
                print(f"❌ Failed to get courses: {resp.status}")
                return
            
            courses = await resp.json()
            if not courses:
                print("❌ No enrolled courses found")
                return
            
            print(f"✅ Found {len(courses)} enrolled courses")
            course = courses[0]
            print(f"📖 Testing with course: {course['title']}")
        
        print(f"\n🔍 Getting course details...")
        
        # Get course details
        async with session.get(f"{BASE_URL}/courses/{course['id']}", headers=headers) as resp:
            if resp.status != 200:
                print(f"❌ Failed to get course details: {resp.status}")
                return
            
            course_details = await resp.json()
            modules = course_details.get("modules", [])
            if not modules:
                print("❌ No modules found in course")
                return
            
            lessons = []
            for module in modules:
                lessons.extend(module.get("lessons", []))
            
            if not lessons:
                print("❌ No lessons found in course")
                return
            
            print(f"✅ Found {len(lessons)} lessons")
            lesson = lessons[0]
            print(f"📝 Testing with lesson: {lesson['title']}")
        
        print(f"\n⏳ Updating lesson progress...")
        
        # Update lesson progress
        progress_data = {
            "lesson_id": lesson["id"],
            "completed": True
        }
        
        async with session.post(f"{BASE_URL}/progress/lesson", json=progress_data, headers=headers) as resp:
            if resp.status != 200:
                print(f"❌ Failed to update progress: {resp.status}")
                text = await resp.text()
                print(f"Response: {text}")
                return
            
            result = await resp.json()
            print(f"✅ Progress updated successfully!")
            print(f"📊 New percentage: {result.get('percentage', 0)}%")
        
        print(f"\n🔍 Verifying progress update...")
        
        # Verify progress was saved
        async with session.get(f"{BASE_URL}/progress/course/{course['id']}", headers=headers) as resp:
            if resp.status != 200:
                print(f"❌ Failed to get progress: {resp.status}")
                return
            
            progress = await resp.json()
            completed_lessons = progress.get("completed_lessons", [])
            
            if lesson["id"] in completed_lessons:
                print(f"✅ Lesson marked as completed!")
                print(f"📊 Course progress: {progress.get('percentage', 0)}%")
                print(f"📝 Completed lessons: {len(completed_lessons)}")
            else:
                print(f"❌ Lesson not found in completed lessons")
                print(f"Completed lessons: {completed_lessons}")

if __name__ == "__main__":
    print("🧪 Testing Progress API")
    print("=" * 50)
    asyncio.run(test_progress_api())