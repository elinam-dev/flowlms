import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { useAuth } from '../../context/AuthContext';
import { courseApi, progressApi, quizApi } from '../../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Progress } from '../../components/ui/progress';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { toast } from 'sonner';
import { 
  BookOpen, 
  PlayCircle,
  CheckCircle,
  ChevronRight,
  ChevronLeft,
  Clock,
  Users,
  Award,
  ArrowLeft,
  FileText,
  ClipboardList,
  Target,
  BarChart3
} from 'lucide-react';

export default function CourseDetail() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  const [completingPage, setCompletingPage] = useState(false);
  const [activeQuiz, setActiveQuiz] = useState(null);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizSubmitting, setQuizSubmitting] = useState(false);
  const [quizResults, setQuizResults] = useState(null);

  const isEnrolled = user && course?.enrolled_users?.includes(user.id);
  
  // Check URL for action parameter
  const urlParams = new URLSearchParams(window.location.search);
  const action = urlParams.get('action');
  const [showOverview, setShowOverview] = useState(action !== 'learn');
  const userProgress = course?.user_progress;
  const progressPercentage = userProgress?.percentage || 0;
  const isCompleted = progressPercentage >= 100;

  // Get all lessons (pages) from all modules
  const getAllPages = () => {
    if (!course?.modules) return [];
    return course.modules.flatMap(m => m.lessons || []).sort((a, b) => a.order - b.order);
  };

  const pages = getAllPages();
  const currentPage = pages[currentPageIndex];
  const totalPages = pages.length;

  useEffect(() => {
    fetchCourse();
  }, [courseId]);

  // Scroll to top when page changes
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [currentPageIndex]);

  const fetchCourse = async () => {
    try {
      const response = await courseApi.getById(courseId);
      setCourse(response.data);
      
      // Find the first incomplete page to start from
      const allPages = response.data.modules?.flatMap(m => m.lessons || []).sort((a, b) => a.order - b.order) || [];
      const completedLessons = response.data.user_progress?.completed_lessons || [];
      const firstIncompleteIndex = allPages.findIndex(p => !completedLessons.includes(p.id));
      if (firstIncompleteIndex > 0) {
        setCurrentPageIndex(firstIncompleteIndex);
      }
    } catch (error) {
      console.error('Failed to fetch course:', error);
      toast.error('Failed to load course');
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async () => {
    setEnrolling(true);
    try {
      await courseApi.enroll(courseId);
      toast.success('Successfully enrolled! Let\'s begin learning.');
      fetchCourse();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to enroll');
    } finally {
      setEnrolling(false);
    }
  };

  const handleCompletePage = async () => {
    if (!currentPage) return;
    setCompletingPage(true);
    
    try {
      await progressApi.updateLesson(currentPage.id, true);
      
      // Move to next page
      if (currentPageIndex < totalPages - 1) {
        setCurrentPageIndex(currentPageIndex + 1);
        toast.success('Page completed! Moving to next page.');
      } else {
        toast.success('Congratulations! You\'ve completed this course!');
      }
      
      fetchCourse();
    } catch (error) {
      toast.error('Failed to save progress');
    } finally {
      setCompletingPage(false);
    }
  };

  const isPageCompleted = (pageId) => {
    return userProgress?.completed_lessons?.includes(pageId);
  };

  const goToPage = (index) => {
    if (index >= 0 && index < totalPages) {
      setCurrentPageIndex(index);
    }
  };

  // Get learning outcomes
  const getLearningOutcomes = () => {
    if (course?.category === 'Safety') {
      return [
        'Identify workplace hazards and safety risks',
        'Apply proper safety protocols and procedures',
        'Understand emergency response procedures',
        'Maintain compliance with safety regulations'
      ];
    }
    if (course?.category === 'HR Policy') {
      return [
        'Understand company policies and procedures',
        'Apply HR guidelines in daily operations',
        'Navigate employee relations effectively',
        'Ensure compliance with organizational standards'
      ];
    }
    if (course?.category === 'Ethics') {
      return [
        'Recognize ethical dilemmas in the workplace',
        'Apply ethical decision-making frameworks',
        'Understand corporate governance principles',
        'Maintain professional integrity standards'
      ];
    }
    return [
      'Understand the key concepts and principles',
      'Apply practical knowledge to real-world scenarios',
      'Demonstrate competency through assessments',
      'Earn a certificate upon completion'
    ];
  };

  if (loading) {
    return (
      <Layout>
        <div className="bg-slate-50 min-h-screen py-8">
          <div className="max-w-5xl mx-auto px-4">
            <Skeleton className="h-8 w-64 mb-4" />
            <Skeleton className="h-96 rounded-xl" />
          </div>
        </div>
      </Layout>
    );
  }

  if (!course) {
    return (
      <Layout>
        <div className="py-20 text-center">
          <BookOpen className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-4">Course not found</h2>
          <Button onClick={() => navigate('/courses')} variant="outline">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Courses
          </Button>
        </div>
      </Layout>
    );
  }

  // If showing overview or not enrolled, show course overview
  if (showOverview || !isEnrolled) {
    return (
      <Layout>
        <div data-testid="course-detail" className="bg-slate-50 min-h-screen">
          {/* Breadcrumb */}
          <div className="bg-white border-b border-slate-200">
            <div className="max-w-5xl mx-auto px-4 py-4">
              <nav className="flex items-center gap-2 text-sm">
                <Link to="/courses" className="text-slate-500 hover:text-[#095EB1]">Courses</Link>
                <ChevronRight className="w-4 h-4 text-slate-400" />
                <span className="text-slate-900 font-medium truncate">{course.title}</span>
              </nav>
            </div>
          </div>

          <div className="max-w-5xl mx-auto px-4 py-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Main Content */}
              <div className="lg:col-span-2 space-y-6">
                {/* Course Header */}
                <div className="bg-white rounded-xl p-8 border border-slate-200">
                  <div className="flex flex-wrap gap-2 mb-4">
                    {course.course_type === 'compulsory' && (
                      <Badge className="bg-red-100 text-red-700">Required</Badge>
                    )}
                    {course.category && (
                      <Badge className="bg-slate-100 text-slate-700">{course.category}</Badge>
                    )}
                    {course.code && (
                      <Badge variant="outline">{course.code}</Badge>
                    )}
                  </div>
                  <h1 className="text-3xl font-bold text-slate-900 mb-4">{course.title}</h1>
                  <p className="text-lg text-slate-600 leading-relaxed">{course.description}</p>
                  
                  <div className="flex flex-wrap gap-6 mt-6 pt-6 border-t border-slate-100">
                    <div className="flex items-center gap-2 text-slate-600">
                      <FileText className="w-5 h-5 text-slate-400" />
                      <span>{totalPages} pages</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-600">
                      <Clock className="w-5 h-5 text-slate-400" />
                      <span>{course.duration_hours || 1} hour{course.duration_hours !== 1 ? 's' : ''}</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-600">
                      <Users className="w-5 h-5 text-slate-400" />
                      <span>{(course.enrolled_users?.length || 0).toLocaleString()} enrolled</span>
                    </div>
                  </div>
                </div>

                {/* What You'll Learn */}
                <div className="bg-white rounded-xl p-8 border border-slate-200">
                  <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                    <Target className="w-5 h-5 text-[#095EB1]" />
                    What You'll Learn
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {getLearningOutcomes().map((outcome, i) => (
                      <div key={i} className="flex items-start gap-3">
                        <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                        <span className="text-slate-600">{outcome}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Course Content Preview */}
                <div className="bg-white rounded-xl p-8 border border-slate-200">
                  <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                    <BookOpen className="w-5 h-5 text-[#095EB1]" />
                    Course Content
                  </h2>
                  <div className="space-y-2">
                    {pages.slice(0, 5).map((page, i) => (
                      <div key={page.id} className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                        <span className="w-8 h-8 bg-[#095EB1] text-white rounded-lg flex items-center justify-center text-sm font-bold">
                          {i + 1}
                        </span>
                        <span className="text-slate-700">{page.title}</span>
                      </div>
                    ))}
                    {pages.length > 5 && (
                      <p className="text-sm text-slate-500 pl-11">+ {pages.length - 5} more pages</p>
                    )}
                  </div>
                </div>
              </div>

              {/* Sidebar */}
              <div className="lg:col-span-1">
                <Card className="sticky top-24 shadow-xl border-slate-200">
                  {course.thumbnail && (
                    <div className="aspect-video overflow-hidden rounded-t-xl">
                      <img src={course.thumbnail} alt={course.title} className="w-full h-full object-cover" />
                    </div>
                  )}
                  <CardContent className="p-6">
                    <div className="text-center py-4">
                      <p className="text-3xl font-bold text-[#095EB1] mb-1">Free</p>
                      <p className="text-slate-500 text-sm">Enroll to start learning</p>
                    </div>

                    <Button 
                      className="w-full h-12 rounded-xl font-semibold bg-[#095EB1] hover:bg-[#074A8C]"
                      onClick={isEnrolled ? () => setShowOverview(false) : handleEnroll}
                      disabled={enrolling}
                      data-testid="enroll-btn"
                    >
                      {enrolling ? 'Enrolling...' : isEnrolled ? 'Start Learning' : 'Start Course'}
                    </Button>

                    <div className="mt-6 pt-6 border-t border-slate-100 space-y-3">
                      <div className="flex items-center gap-3 text-sm text-slate-600">
                        <CheckCircle className="w-4 h-4 text-emerald-500" />
                        <span>Full access to all content</span>
                      </div>
                      <div className="flex items-center gap-3 text-sm text-slate-600">
                        <CheckCircle className="w-4 h-4 text-emerald-500" />
                        <span>Certificate on completion</span>
                      </div>
                      <div className="flex items-center gap-3 text-sm text-slate-600">
                        <CheckCircle className="w-4 h-4 text-emerald-500" />
                        <span>Track your progress</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  // Enrolled - Show page-based content viewer
  return (
    <Layout>
      <div data-testid="course-detail" className="bg-slate-50 min-h-screen">
        {/* Top Progress Bar */}
        <div className="bg-white border-b border-slate-200 sticky top-16 z-40">
          <div className="max-w-5xl mx-auto px-4">
            {/* Breadcrumb & Title */}
            <div className="flex items-center justify-between py-3">
              <div className="flex items-center gap-4">
                <Link to="/courses" className="p-2 hover:bg-slate-100 rounded-lg transition-colors">
                  <ArrowLeft className="w-5 h-5 text-slate-600" />
                </Link>
                <div>
                  <h1 className="font-semibold text-slate-900 line-clamp-1">{course.title}</h1>
                  <p className="text-sm text-slate-500">
                    Page {currentPageIndex + 1} of {totalPages}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span className={`text-lg font-bold ${isCompleted ? 'text-emerald-600' : 'text-[#095EB1]'}`}>
                  {Math.round(progressPercentage)}%
                </span>
                {isCompleted && (
                  <Badge className="bg-emerald-100 text-emerald-700">
                    <CheckCircle className="w-3 h-3 mr-1" />
                    Complete
                  </Badge>
                )}
              </div>
            </div>
            
            {/* Progress Bar */}
            <div className="pb-3">
              <Progress value={progressPercentage} className={`h-2 ${isCompleted ? '[&>div]:bg-emerald-500' : ''}`} />
            </div>

            {/* Page Dots Navigation */}
            <div className="flex items-center justify-center gap-2 pb-4">
              {pages.map((page, index) => (
                <button
                  key={page.id}
                  onClick={() => goToPage(index)}
                  className={`w-3 h-3 rounded-full transition-all ${
                    index === currentPageIndex 
                      ? 'bg-[#095EB1] w-6' 
                      : isPageCompleted(page.id)
                        ? 'bg-emerald-500'
                        : 'bg-slate-300 hover:bg-slate-400'
                  }`}
                  title={page.title}
                  data-testid={`page-dot-${index}`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Page Content */}
        <div className="max-w-5xl mx-auto px-4 py-8">
          {currentPage ? (
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
              {/* Page Header */}
              <div className="bg-gradient-to-r from-[#095EB1] to-[#0369A1] px-8 py-6 text-white">
                <div className="flex items-center gap-2 text-white/70 text-sm mb-2">
                  <span>Page {currentPageIndex + 1}</span>
                  <span>•</span>
                  <span>{course.title}</span>
                </div>
                <h2 className="text-2xl font-bold">{currentPage.title}</h2>
              </div>

              {/* Page Content */}
              <div className="p-8 bg-white">
                <div 
                  className="lesson-content"
                  dangerouslySetInnerHTML={{ __html: currentPage.content }}
                />
              </div>

              {/* Navigation Footer */}
              <div className="border-t border-slate-200 bg-slate-50 px-8 py-6">
                <div className="flex items-center justify-between">
                  {/* Previous Button */}
                  <Button
                    variant="outline"
                    onClick={() => goToPage(currentPageIndex - 1)}
                    disabled={currentPageIndex === 0}
                    className="h-12 px-6 rounded-xl"
                    data-testid="prev-page-btn"
                  >
                    <ChevronLeft className="w-5 h-5 mr-2" />
                    Previous
                  </Button>

                  {/* Page Status */}
                  <div className="flex items-center gap-2">
                    {isPageCompleted(currentPage.id) ? (
                      <Badge className="bg-emerald-100 text-emerald-700 py-2 px-4">
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Completed
                      </Badge>
                    ) : (
                      <span className="text-slate-500">
                        Mark as complete to continue
                      </span>
                    )}
                  </div>

                  {/* Next/Complete Button */}
                  {currentPageIndex < totalPages - 1 ? (
                    isPageCompleted(currentPage.id) ? (
                      <Button
                        onClick={() => goToPage(currentPageIndex + 1)}
                        className="h-12 px-6 rounded-xl bg-[#095EB1] hover:bg-[#074A8C]"
                        data-testid="next-page-btn"
                      >
                        Next Page
                        <ChevronRight className="w-5 h-5 ml-2" />
                      </Button>
                    ) : (
                      <Button
                        onClick={handleCompletePage}
                        disabled={completingPage}
                        className="h-12 px-6 rounded-xl bg-emerald-600 hover:bg-emerald-700"
                        data-testid="complete-page-btn"
                      >
                        {completingPage ? 'Saving...' : 'Complete & Continue'}
                        <ChevronRight className="w-5 h-5 ml-2" />
                      </Button>
                    )
                  ) : (
                    isPageCompleted(currentPage.id) ? (
                      <Link to="/courses">
                        <Button className="h-12 px-6 rounded-xl bg-emerald-600 hover:bg-emerald-700">
                          <Award className="w-5 h-5 mr-2" />
                          Course Complete!
                        </Button>
                      </Link>
                    ) : (
                      <Button
                        onClick={handleCompletePage}
                        disabled={completingPage}
                        className="h-12 px-6 rounded-xl bg-emerald-600 hover:bg-emerald-700"
                        data-testid="finish-course-btn"
                      >
                        {completingPage ? 'Saving...' : 'Finish Course'}
                        <CheckCircle className="w-5 h-5 ml-2" />
                      </Button>
                    )
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-20">
              <BookOpen className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-500">No content available</p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
