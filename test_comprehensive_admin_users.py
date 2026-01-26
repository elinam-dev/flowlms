#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def comprehensive_admin_users_test():
    """Comprehensive test for admin users endpoint with enrolled courses"""
    base_url = "https://course-registry-5.preview.emergentagent.com"
    
    print("🔍 Comprehensive Admin Users Endpoint Test")
    print("=" * 60)
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    login_url = f"{base_url}/api/auth/login"
    login_data = {
        "identifier": "admin@flowitec.com",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(login_url, json=login_data, timeout=30)
        if login_response.status_code != 200:
            print(f"❌ Admin login failed: {login_response.status_code}")
            return False
        
        login_result = login_response.json()
        admin_token = login_result.get('access_token')
        print(f"✅ Admin login successful")
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False
    
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }
    
    # Step 2: Create a test user
    print("\n2. Creating a test user...")
    timestamp = datetime.now().strftime('%H%M%S')
    user_data = {
        "email": f"testlearner{timestamp}@flowitec.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "Learner",
        "employee_id": f"EMP-{timestamp}",
        "role": "learner"
    }
    
    try:
        create_user_url = f"{base_url}/api/admin/users"
        user_response = requests.post(create_user_url, json=user_data, headers=headers, timeout=30)
        if user_response.status_code != 200:
            print(f"❌ User creation failed: {user_response.status_code}")
            print(f"   Response: {user_response.text}")
            return False
        
        user_result = user_response.json()
        user_id = user_result.get('id')
        print(f"✅ Test user created: {user_data['email']}")
        
    except Exception as e:
        print(f"❌ User creation error: {str(e)}")
        return False
    
    # Step 3: Create a test course
    print("\n3. Creating a test course...")
    course_data = {
        "title": f"Test Course {timestamp}",
        "description": "A test course for enrolled courses verification",
        "category": "Testing",
        "duration_hours": 2.0,
        "is_published": True,
        "course_type": "optional"
    }
    
    try:
        create_course_url = f"{base_url}/api/admin/courses"
        course_response = requests.post(create_course_url, json=course_data, headers=headers, timeout=30)
        if course_response.status_code != 200:
            print(f"❌ Course creation failed: {course_response.status_code}")
            print(f"   Response: {course_response.text}")
            return False
        
        course_result = course_response.json()
        course_id = course_result.get('id')
        print(f"✅ Test course created: {course_data['title']}")
        
    except Exception as e:
        print(f"❌ Course creation error: {str(e)}")
        return False
    
    # Step 4: Login as the test user
    print("\n4. Logging in as test user...")
    user_login_data = {
        "identifier": user_data['email'],
        "password": user_data['password']
    }
    
    try:
        user_login_response = requests.post(login_url, json=user_login_data, timeout=30)
        if user_login_response.status_code != 200:
            print(f"❌ User login failed: {user_login_response.status_code}")
            return False
        
        user_login_result = user_login_response.json()
        user_token = user_login_result.get('access_token')
        print(f"✅ Test user login successful")
        
    except Exception as e:
        print(f"❌ User login error: {str(e)}")
        return False
    
    # Step 5: Enroll user in course
    print("\n5. Enrolling user in course...")
    enrollment_data = {"course_id": course_id}
    user_headers = {
        'Authorization': f'Bearer {user_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        enroll_url = f"{base_url}/api/courses/enroll"
        enroll_response = requests.post(enroll_url, json=enrollment_data, headers=user_headers, timeout=30)
        if enroll_response.status_code != 200:
            print(f"❌ Course enrollment failed: {enroll_response.status_code}")
            print(f"   Response: {enroll_response.text}")
            return False
        
        print(f"✅ User enrolled in course successfully")
        
    except Exception as e:
        print(f"❌ Enrollment error: {str(e)}")
        return False
    
    # Step 6: Test admin users endpoint
    print("\n6. Testing admin users endpoint...")
    try:
        users_url = f"{base_url}/api/admin/users"
        users_response = requests.get(users_url, headers=headers, timeout=30)
        if users_response.status_code != 200:
            print(f"❌ Admin users endpoint failed: {users_response.status_code}")
            return False
        
        users_data = users_response.json()
        print(f"✅ Admin users endpoint successful - Found {len(users_data)} users")
        
    except Exception as e:
        print(f"❌ Users endpoint error: {str(e)}")
        return False
    
    # Step 7: Verify enrolled courses details
    print("\n7. Verifying enrolled courses details...")
    
    test_user_found = False
    enrolled_courses_verified = False
    
    for user in users_data:
        if user.get('email') == user_data['email']:
            test_user_found = True
            print(f"   ✓ Found test user: {user['email']}")
            
            # Check enrolled_courses_details field
            if "enrolled_courses_details" not in user:
                print(f"❌ Test user missing 'enrolled_courses_details' field")
                return False
            
            enrolled_courses = user["enrolled_courses_details"]
            
            if not isinstance(enrolled_courses, list):
                print(f"❌ enrolled_courses_details is not a list")
                return False
            
            if len(enrolled_courses) == 0:
                print(f"❌ Test user has no enrolled courses in details")
                return False
            
            print(f"   ✓ Test user has {len(enrolled_courses)} enrolled courses")
            
            # Verify course details
            for course in enrolled_courses:
                if "id" not in course or "title" not in course:
                    print(f"❌ Course missing required fields: {course}")
                    return False
                
                if course['id'] == course_id and course['title'] == course_data['title']:
                    enrolled_courses_verified = True
                    print(f"   ✅ Found correct course: {course['title']} (ID: {course['id']})")
                else:
                    print(f"   ✓ Found course: {course['title']} (ID: {course['id']})")
            
            break
    
    if not test_user_found:
        print(f"❌ Test user not found in admin users response")
        return False
    
    if not enrolled_courses_verified:
        print(f"❌ Test course not found in user's enrolled courses details")
        return False
    
    # Step 8: Cleanup (delete test user and course)
    print("\n8. Cleaning up test data...")
    try:
        # Delete user
        delete_user_url = f"{base_url}/api/admin/users/{user_id}"
        requests.delete(delete_user_url, headers=headers, timeout=30)
        
        # Delete course
        delete_course_url = f"{base_url}/api/admin/courses/{course_id}"
        requests.delete(delete_course_url, headers=headers, timeout=30)
        
        print("✅ Test data cleaned up")
        
    except Exception as e:
        print(f"⚠️  Cleanup error (non-critical): {str(e)}")
    
    print("\n🎉 COMPREHENSIVE TEST PASSED!")
    print("✅ Admin users endpoint correctly returns enrolled_courses_details")
    print("✅ Each course has required 'id' and 'title' fields")
    print("✅ Enrolled courses are properly populated after enrollment")
    
    return True

if __name__ == "__main__":
    success = comprehensive_admin_users_test()
    if success:
        print("\n🎉 All tests PASSED!")
        exit(0)
    else:
        print("\n❌ Tests FAILED!")
        exit(1)