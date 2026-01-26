#!/usr/bin/env python3
import requests
import json

def test_admin_users_endpoint():
    """Test the admin users endpoint to verify it returns enrolled courses details"""
    base_url = "https://course-registry-5.preview.emergentagent.com"
    
    print("🔍 Testing Admin Users Endpoint with Enrolled Courses Details")
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
            print(f"   Response: {login_response.text}")
            return False
        
        login_result = login_response.json()
        admin_token = login_result.get('access_token')
        if not admin_token:
            print("❌ No access token received")
            return False
        
        print(f"✅ Admin login successful")
        print(f"   Token: {admin_token[:20]}...")
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False
    
    # Step 2: Call admin users endpoint
    print("\n2. Calling GET /api/admin/users...")
    users_url = f"{base_url}/api/admin/users"
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        users_response = requests.get(users_url, headers=headers, timeout=30)
        if users_response.status_code != 200:
            print(f"❌ Admin users endpoint failed: {users_response.status_code}")
            print(f"   Response: {users_response.text}")
            return False
        
        users_data = users_response.json()
        print(f"✅ Admin users endpoint successful")
        print(f"   Found {len(users_data)} users")
        
    except Exception as e:
        print(f"❌ Users endpoint error: {str(e)}")
        return False
    
    # Step 3: Verify response structure
    print("\n3. Verifying response structure...")
    
    if not isinstance(users_data, list):
        print("❌ Response is not a list")
        return False
    
    users_with_courses = 0
    total_enrolled_courses = 0
    
    for i, user in enumerate(users_data):
        user_email = user.get('email', f'user_{i}')
        
        # Check if enrolled_courses_details field exists
        if "enrolled_courses_details" not in user:
            print(f"❌ User {user_email} missing 'enrolled_courses_details' field")
            return False
        
        enrolled_courses = user["enrolled_courses_details"]
        
        # Verify it's a list
        if not isinstance(enrolled_courses, list):
            print(f"❌ User {user_email} enrolled_courses_details is not a list")
            return False
        
        if enrolled_courses:
            users_with_courses += 1
            total_enrolled_courses += len(enrolled_courses)
            print(f"   ✓ User {user_email} has {len(enrolled_courses)} enrolled courses")
            
            # Verify each course has required fields
            for j, course in enumerate(enrolled_courses):
                if "id" not in course:
                    print(f"❌ Course {j} for user {user_email} missing 'id' field")
                    return False
                
                if "title" not in course:
                    print(f"❌ Course {j} for user {user_email} missing 'title' field")
                    return False
                
                print(f"     - Course: {course['title']} (ID: {course['id']})")
        else:
            print(f"   ✓ User {user_email} has no enrolled courses (empty array)")
    
    # Step 4: Summary
    print("\n4. Test Summary:")
    print(f"   ✅ All {len(users_data)} users have 'enrolled_courses_details' field")
    print(f"   ✅ All enrolled courses have required 'id' and 'title' fields")
    print(f"   📊 {users_with_courses} users have enrolled courses")
    print(f"   📊 Total enrolled courses across all users: {total_enrolled_courses}")
    
    if users_with_courses > 0:
        print("   ✅ Found users with enrolled courses - feature working correctly")
    else:
        print("   ⚠️  No users have enrolled courses - this may be expected if no enrollments exist")
    
    return True

if __name__ == "__main__":
    success = test_admin_users_endpoint()
    if success:
        print("\n🎉 Admin users endpoint test PASSED!")
        exit(0)
    else:
        print("\n❌ Admin users endpoint test FAILED!")
        exit(1)