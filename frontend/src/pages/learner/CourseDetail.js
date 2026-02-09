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

// CSS for professional lesson content styling
const policyStyles = `
  /* Base Lesson Content Styles */
  .lesson-content, .policy-page {
    max-width: 900px;
    margin: 0 auto;
    line-height: 1.8;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  }
  
  /* Typography */
  .lesson-content h2, .policy-page h2 {
    color: #095EB1;
    font-size: 2rem;
    font-weight: 700;
    margin: 2rem 0 1.5rem;
    border-bottom: 3px solid #095EB1;
    padding-bottom: 0.75rem;
  }
  .lesson-content h3, .policy-page h3 {
    color: #1e293b;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 2rem 0 1rem;
  }
  .lesson-content h4, .policy-page h4 {
    color: #475569;
    font-size: 1.125rem;
    font-weight: 600;
    margin: 1.5rem 0 0.75rem;
  }
  .lesson-content p, .policy-page p {
    color: #334155;
    margin-bottom: 1.25rem;
    font-size: 1.0625rem;
  }
  .lesson-content ul, .policy-page ul {
    list-style-type: disc;
    padding-left: 2rem;
    margin-bottom: 1.5rem;
  }
  .lesson-content ol, .policy-page ol {
    list-style-type: decimal;
    padding-left: 2rem;
    margin-bottom: 1.5rem;
  }
  .lesson-content li, .policy-page li {
    color: #334155;
    margin-bottom: 0.75rem;
    line-height: 1.7;
  }
  .lesson-content strong, .policy-page strong {
    color: #0F172A;
    font-weight: 600;
  }
  .lesson-content em, .policy-page em {
    font-style: italic;
    color: #64748b;
  }
  
  /* Tables */
  .lesson-content table, .policy-page table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-radius: 0.5rem;
    overflow: hidden;
  }
  .lesson-content th, .policy-page th {
    background: linear-gradient(135deg, #095EB1 0%, #0369A1 100%);
    color: white;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.9375rem;
  }
  .lesson-content td, .policy-page td {
    padding: 1rem;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
  }
  .lesson-content tr:last-child td, .policy-page tr:last-child td {
    border-bottom: none;
  }
  .lesson-content tr:nth-child(even), .policy-page tr:nth-child(even) {
    background: #f8fafc;
  }
  
  /* Highlight Boxes */
  .lesson-content .highlight-box, .policy-page .highlight-box {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border-left: 4px solid #095EB1;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin: 2rem 0;
    box-shadow: 0 2px 4px rgba(9, 94, 177, 0.1);
  }
  .lesson-content .warning-box, .policy-page .warning-box {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    border-left: 4px solid #F59E0B;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin: 2rem 0;
    box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
  }
  .lesson-content .info-box, .policy-page .info-box {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border-left: 4px solid #10B981;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin: 2rem 0;
    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.1);
  }
  .lesson-content .example-box, .policy-page .example-box {
    background: #F8FAFC;
    border: 2px solid #e2e8f0;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin: 2rem 0;
  }
  
  /* Cards and Grids */
  .lesson-content .responsibilities-grid, .lesson-content .functions-grid,
  .lesson-content .advantages, .lesson-content .applications {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }
  .lesson-content .resp-card, .lesson-content .function-card,
  .lesson-content .advantage-card, .lesson-content .app-card,
  .lesson-content .principle-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
  }
  .lesson-content .resp-card:hover, .lesson-content .function-card:hover,
  .lesson-content .advantage-card:hover, .lesson-content .app-card:hover {
    box-shadow: 0 4px 12px rgba(9, 94, 177, 0.15);
    transform: translateY(-2px);
  }
  .lesson-content .advantage-card.highlight {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 2px solid #095EB1;
  }
  .lesson-content .principle-card.warning, .policy-page .principle-card.warning {
    background: #FEF3C7;
    border-left: 4px solid #F59E0B;
  }
  .lesson-content .principle-card.highlight, .policy-page .principle-card.highlight {
    background: #EFF6FF;
    border: 2px solid #095EB1;
  }
  
  /* Numbered Items */
  .lesson-content .purpose-item, .lesson-content .guideline-item,
  .lesson-content .procedure-item, .lesson-content .training-item,
  .policy-page .purpose-item, .policy-page .guideline-item,
  .policy-page .procedure-item, .policy-page .training-item {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    background: #F8FAFC;
    padding: 1.25rem;
    border-radius: 0.75rem;
    margin-bottom: 1rem;
    border: 1px solid #e2e8f0;
  }
  .lesson-content .purpose-item .number, .lesson-content .guideline-item .number,
  .lesson-content .procedure-item .number, .lesson-content .training-item .number,
  .policy-page .purpose-item .number, .policy-page .guideline-item .number,
  .policy-page .procedure-item .number, .policy-page .training-item .number {
    background: linear-gradient(135deg, #095EB1 0%, #0369A1 100%);
    color: white;
    min-width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    flex-shrink: 0;
    box-shadow: 0 2px 4px rgba(9, 94, 177, 0.2);
  }
  .lesson-content .guideline-item.important, .policy-page .guideline-item.important {
    background: #FEF3C7;
    border-left: 4px solid #F59E0B;
  }
  .lesson-content .procedure-item.important, .policy-page .procedure-item.important {
    background: #FEE2E2;
    border-left: 4px solid #EF4444;
  }
  
  /* Special Sections */
  .lesson-content .summary-box, .policy-page .summary-box,
  .lesson-content .conclusion-box, .policy-page .conclusion-box,
  .lesson-content .declaration-box, .policy-page .declaration-box {
    background: linear-gradient(135deg, #095EB1 0%, #0369A1 100%);
    color: white;
    padding: 2rem;
    border-radius: 1rem;
    margin: 2rem 0;
    box-shadow: 0 4px 12px rgba(9, 94, 177, 0.3);
  }
  .lesson-content .summary-box h4, .lesson-content .conclusion-box h4,
  .policy-page .summary-box h4, .policy-page .conclusion-box h4,
  .policy-page .declaration-box h3 {
    color: white;
    margin-top: 0;
  }
  .lesson-content .summary-box p, .lesson-content .conclusion-box p,
  .policy-page .summary-box p, .policy-page .conclusion-box p,
  .policy-page .declaration-box p {
    color: rgba(255,255,255,0.95);
  }
  .lesson-content .summary-box li, .policy-page .summary-box li {
    color: rgba(255,255,255,0.9);
  }
  
  /* Leave Types & Badges */
  .policy-page .leave-type {
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 1rem;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
  .policy-page .days-badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: linear-gradient(135deg, #095EB1 0%, #0369A1 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 0.9375rem;
    box-shadow: 0 2px 4px rgba(9, 94, 177, 0.3);
  }
  .policy-page .days-badge.special {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  }
  
  /* Misconduct & Behavior Grids */
  .policy-page .misconduct-grid, .policy-page .behavior-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
  }
  .policy-page .misconduct-item {
    background: #FEE2E2;
    padding: 1.25rem;
    border-radius: 0.75rem;
    border-left: 4px solid #EF4444;
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
  }
  .policy-page .misconduct-item .number {
    background: #EF4444;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    font-weight: 700;
    font-size: 0.75rem;
    flex-shrink: 0;
  }
  .policy-page .behavior-item {
    background: #FEF3C7;
    padding: 1.25rem;
    border-radius: 0.75rem;
    border-left: 4px solid #F59E0B;
  }
  
  /* Penalty Sections */
  .policy-page .penalty-section {
    background: #F8FAFC;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 1.5rem;
    border: 1px solid #e2e8f0;
  }
  .policy-page .penalty-section.moderate {
    background: #FEF3C7;
    border-left: 4px solid #F59E0B;
  }
  .policy-page .penalty-section.severe {
    background: #FEE2E2;
    border-left: 4px solid #EF4444;
  }
  .policy-page .penalty-section .examples {
    font-size: 0.9375rem;
    color: #64748b;
    font-style: italic;
    margin-bottom: 0.75rem;
  }
  
  /* Role Sections */
  .policy-page .role-section {
    background: white;
    border: 2px solid #e2e8f0;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 1.5rem;
  }
  
  /* Misc */
  .policy-page .legal-note {
    font-style: italic;
    color: #64748b;
    border-top: 2px solid #e2e8f0;
    padding-top: 1.5rem;
    margin-top: 2rem;
    font-size: 0.9375rem;
  }
  .policy-page .document-code {
    color: #64748b;
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
    font-weight: 500;
  }
  .policy-page .purpose-box {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 2rem;
    border: 2px solid #095EB1;
  }
  .policy-page .policy-statement {
    font-size: 1.125rem;
    font-weight: 500;
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .lesson-content, .policy-page {
      padding: 0 1rem;
    }
    .lesson-content h2, .policy-page h2 {
      font-size: 1.5rem;
    }
    .lesson-content .responsibilities-grid, .lesson-content .functions-grid,
    .lesson-content .advantages, .lesson-content .applications {
      grid-template-columns: 1fr;
    }
  }
`;

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
        <style>{policyStyles}</style>
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
      <style>{policyStyles}</style>
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
                  className="prose prose-slate max-w-none lesson-content"
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
