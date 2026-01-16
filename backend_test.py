import requests
import sys
import json
from datetime import datetime

class FlowitecLMSTester:
    def __init__(self, base_url="https://flowitec-lms.preview.emergentagent.com"):
        self.base_url = base_url
        self.admin_token = None
        self.learner_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.created_resources = {
            'courses': [],
            'modules': [],
            'lessons': [],
            'quizzes': [],
            'users': []
        }

    def run_test(self, name, method, endpoint, expected_status, data=None, token=None, description=""):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        if description:
            print(f"   Description: {description}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json() if response.content else {}
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Response: {response.text[:200]}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_admin_login(self):
        """Test admin login and get token"""
        print("\n" + "="*50)
        print("TESTING AUTHENTICATION")
        print("="*50)
        
        success, response = self.run_test(
            "Admin Login",
            "POST",
            "auth/login",
            200,
            data={"email": "admin@flowitec.com", "password": "admin123"},
            description="Login with admin credentials"
        )
        if success and 'access_token' in response:
            self.admin_token = response['access_token']
            print(f"   Admin token obtained: {self.admin_token[:20]}...")
            return True
        return False

    def test_user_registration_disabled(self):
        """Test that user registration is disabled"""
        timestamp = datetime.now().strftime('%H%M%S')
        user_data = {
            "email": f"testuser{timestamp}@flowitec.com",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User"
        }
        
        success, response = self.run_test(
            "User Registration (Should be Disabled)",
            "POST",
            "auth/register",
            403,  # Expecting 403 Forbidden
            data=user_data,
            description="Verify registration is disabled - only admin can create users"
        )
        return success

    def test_learner_login(self):
        """Test learner login with existing credentials"""
        success, response = self.run_test(
            "Learner Login",
            "POST",
            "auth/login",
            200,
            data={"email": "learner@flowitec.com", "password": "learner123"},
            description="Login with learner credentials"
        )
        if success and 'access_token' in response:
            self.learner_token = response['access_token']
            print(f"   Learner token obtained: {self.learner_token[:20]}...")
            return True
        return False

    def test_auth_me(self):
        """Test getting current user info"""
        success, response = self.run_test(
            "Get Current User (Admin)",
            "GET",
            "auth/me",
            200,
            token=self.admin_token,
            description="Get admin user profile"
        )
        return success

    def test_admin_stats(self):
        """Test admin stats endpoint"""
        print("\n" + "="*50)
        print("TESTING ADMIN ENDPOINTS")
        print("="*50)
        
        success, response = self.run_test(
            "Admin Stats",
            "GET",
            "admin/stats",
            200,
            token=self.admin_token,
            description="Get system statistics"
        )
        if success:
            print(f"   Stats: {response}")
        return success

    def test_course_creation(self):
        """Test course creation"""
        course_data = {
            "title": "Test Engineering Course",
            "description": "A comprehensive test course for engineering professionals",
            "category": "Engineering",
            "duration_hours": 10.5,
            "is_published": True
        }
        
        success, response = self.run_test(
            "Create Course",
            "POST",
            "admin/courses",
            200,
            data=course_data,
            token=self.admin_token,
            description="Create a new course"
        )
        if success and 'id' in response:
            self.created_resources['courses'].append(response['id'])
            print(f"   Course created with ID: {response['id']}")
            return response['id']
        return None

    def test_module_creation(self, course_id):
        """Test module creation"""
        module_data = {
            "title": "Introduction to Safety",
            "description": "Basic safety protocols and procedures",
            "order": 0
        }
        
        success, response = self.run_test(
            "Create Module",
            "POST",
            f"admin/courses/{course_id}/modules",
            200,
            data=module_data,
            token=self.admin_token,
            description="Create a module in the course"
        )
        if success and 'id' in response:
            self.created_resources['modules'].append(response['id'])
            print(f"   Module created with ID: {response['id']}")
            return response['id']
        return None

    def test_lesson_creation(self, module_id):
        """Test lesson creation"""
        lesson_data = {
            "title": "Safety Fundamentals",
            "content_type": "text",
            "content": "<h2>Safety First</h2><p>This lesson covers the fundamental principles of workplace safety.</p>",
            "duration_minutes": 15,
            "order": 0
        }
        
        success, response = self.run_test(
            "Create Lesson",
            "POST",
            f"admin/modules/{module_id}/lessons",
            200,
            data=lesson_data,
            token=self.admin_token,
            description="Create a text lesson"
        )
        if success and 'id' in response:
            self.created_resources['lessons'].append(response['id'])
            print(f"   Lesson created with ID: {response['id']}")
            return response['id']
        return None

    def test_quiz_creation(self, module_id):
        """Test quiz creation"""
        quiz_data = {
            "title": "Safety Knowledge Check",
            "description": "Test your understanding of safety fundamentals",
            "passing_score": 70,
            "questions": [
                {
                    "question": "What is the first priority in any workplace?",
                    "question_type": "multiple_choice",
                    "options": ["Productivity", "Safety", "Efficiency", "Cost"],
                    "correct_answer": "Safety",
                    "points": 1
                },
                {
                    "question": "Personal Protective Equipment (PPE) is mandatory in hazardous areas.",
                    "question_type": "true_false",
                    "correct_answer": "True",
                    "points": 1
                }
            ]
        }
        
        success, response = self.run_test(
            "Create Quiz",
            "POST",
            f"admin/modules/{module_id}/quizzes",
            200,
            data=quiz_data,
            token=self.admin_token,
            description="Create a quiz with multiple question types"
        )
        if success and 'id' in response:
            self.created_resources['quizzes'].append(response['id'])
            print(f"   Quiz created with ID: {response['id']}")
            return response['id']
        return None

    def test_course_listing(self):
        """Test course listing"""
        print("\n" + "="*50)
        print("TESTING COURSE ENDPOINTS")
        print("="*50)
        
        success, response = self.run_test(
            "List Courses (Admin)",
            "GET",
            "courses/",
            200,
            token=self.admin_token,
            description="Get all courses as admin"
        )
        return success

    def test_course_enrollment(self, course_id):
        """Test course enrollment"""
        enrollment_data = {"course_id": course_id}
        
        success, response = self.run_test(
            "Enroll in Course",
            "POST",
            "courses/enroll",
            200,
            data=enrollment_data,
            token=self.learner_token,
            description="Enroll learner in course"
        )
        return success

    def test_enrolled_courses(self):
        """Test getting enrolled courses"""
        success, response = self.run_test(
            "Get Enrolled Courses",
            "GET",
            "courses/enrolled",
            200,
            token=self.learner_token,
            description="Get learner's enrolled courses"
        )
        return success

    def test_course_detail(self, course_id):
        """Test getting course details"""
        success, response = self.run_test(
            "Get Course Detail",
            "GET",
            f"courses/{course_id}",
            200,
            token=self.learner_token,
            description="Get detailed course information"
        )
        if success:
            print(f"   Course has {len(response.get('modules', []))} modules")
        return success

    def test_lesson_progress(self, lesson_id):
        """Test lesson progress update"""
        print("\n" + "="*50)
        print("TESTING PROGRESS ENDPOINTS")
        print("="*50)
        
        progress_data = {
            "lesson_id": lesson_id,
            "completed": True
        }
        
        success, response = self.run_test(
            "Update Lesson Progress",
            "POST",
            "progress/lesson",
            200,
            data=progress_data,
            token=self.learner_token,
            description="Mark lesson as completed"
        )
        return success

    def test_quiz_taking(self, quiz_id):
        """Test taking a quiz"""
        print("\n" + "="*50)
        print("TESTING QUIZ ENDPOINTS")
        print("="*50)
        
        # First get the quiz
        success, quiz_data = self.run_test(
            "Get Quiz",
            "GET",
            f"quizzes/{quiz_id}",
            200,
            token=self.learner_token,
            description="Get quiz questions"
        )
        
        if not success:
            return False
            
        # Submit quiz answers
        answers = {
            "0": "Safety",  # First question answer
            "1": "True"     # Second question answer
        }
        
        success, response = self.run_test(
            "Submit Quiz",
            "POST",
            f"quizzes/{quiz_id}/submit",
            200,
            data={"answers": answers},
            token=self.learner_token,
            description="Submit quiz with correct answers"
        )
        
        if success:
            print(f"   Quiz score: {response.get('score', 0)}%")
            print(f"   Passed: {response.get('passed', False)}")
        
        return success

    def test_certificates(self):
        """Test certificate endpoints"""
        print("\n" + "="*50)
        print("TESTING CERTIFICATE ENDPOINTS")
        print("="*50)
        
        success, response = self.run_test(
            "Get Certificates",
            "GET",
            "certificates/",
            200,
            token=self.learner_token,
            description="Get learner's certificates"
        )
        
        if success:
            print(f"   Found {len(response)} certificates")
        
        return success

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Flowitec LMS Backend Testing")
        print("="*60)
        
        # Authentication tests
        if not self.test_admin_login():
            print("❌ Admin login failed, stopping tests")
            return False
            
        if not self.test_user_registration():
            print("❌ User registration failed, stopping tests")
            return False
            
        self.test_auth_me()
        
        # Admin functionality tests
        self.test_admin_stats()
        
        course_id = self.test_course_creation()
        if not course_id:
            print("❌ Course creation failed, stopping tests")
            return False
            
        module_id = self.test_module_creation(course_id)
        if not module_id:
            print("❌ Module creation failed, stopping tests")
            return False
            
        lesson_id = self.test_lesson_creation(module_id)
        quiz_id = self.test_quiz_creation(module_id)
        
        # Course and enrollment tests
        self.test_course_listing()
        self.test_course_enrollment(course_id)
        self.test_enrolled_courses()
        self.test_course_detail(course_id)
        
        # Progress and quiz tests
        if lesson_id:
            self.test_lesson_progress(lesson_id)
            
        if quiz_id:
            self.test_quiz_taking(quiz_id)
            
        # Certificate tests
        self.test_certificates()
        
        # Print final results
        print("\n" + "="*60)
        print("📊 FINAL TEST RESULTS")
        print("="*60)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return True
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return False

def main():
    tester = FlowitecLMSTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())