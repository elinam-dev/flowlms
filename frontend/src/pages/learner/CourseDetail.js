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
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { 
  BookOpen, 
  PlayCircle,
  FileText,
  CheckCircle,
  ChevronRight,
  Clock,
  Users,
  Award,
  ArrowLeft,
  Lock,
  ChevronDown,
  ChevronUp,
  ClipboardList,
  Target,
  GraduationCap,
  ThumbsUp,
  Share2,
  Calendar,
  BarChart3
} from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '../../components/ui/collapsible';

export default function CourseDetail() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [activeLesson, setActiveLesson] = useState(null);
  const [openModules, setOpenModules] = useState({});
  const [completingLesson, setCompletingLesson] = useState(null);
  const [activeQuiz, setActiveQuiz] = useState(null);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizSubmitting, setQuizSubmitting] = useState(false);
  const [quizResults, setQuizResults] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  const isEnrolled = user && course?.enrolled_users?.includes(user.id);
  const userProgress = course?.user_progress;
  const progressPercentage = userProgress?.percentage || 0;
  const isCompleted = progressPercentage >= 100;

  useEffect(() => {
    fetchCourse();
  }, [courseId]);

  const fetchCourse = async () => {
    try {
      const response = await courseApi.getById(courseId);
      setCourse(response.data);
      
      if (response.data.modules?.length > 0) {
        setOpenModules({ [response.data.modules[0].id]: true });
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
      toast.success('Successfully enrolled!');
      fetchCourse();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to enroll');
    } finally {
      setEnrolling(false);
    }
  };

  const handleCompleteLesson = async (lessonId) => {
    setCompletingLesson(lessonId);
    try {
      await progressApi.updateLesson(lessonId, true);
      toast.success('Lesson marked as complete!');
      fetchCourse();
    } catch (error) {
      toast.error('Failed to update progress');
    } finally {
      setCompletingLesson(null);
    }
  };

  const toggleModule = (moduleId) => {
    setOpenModules(prev => ({ ...prev, [moduleId]: !prev[moduleId] }));
  };

  const isLessonCompleted = (lessonId) => {
    return userProgress?.completed_lessons?.includes(lessonId);
  };

  const startQuiz = async (quiz) => {
    try {
      const response = await quizApi.getById(quiz.id);
      setActiveQuiz(response.data);
      setQuizAnswers({});
      setQuizResults(null);
      setActiveLesson(null);
      setActiveTab('content');
    } catch (error) {
      toast.error('Failed to load quiz');
    }
  };

  const submitQuiz = async () => {
    setQuizSubmitting(true);
    try {
      const response = await quizApi.submit(activeQuiz.id, quizAnswers);
      setQuizResults(response.data);
      if (response.data.passed) {
        toast.success(`Congratulations! You passed with ${response.data.score}%`);
      } else {
        toast.error(`You scored ${response.data.score}%. Required: ${activeQuiz.passing_score}%`);
      }
      fetchCourse();
    } catch (error) {
      toast.error('Failed to submit quiz');
    } finally {
      setQuizSubmitting(false);
    }
  };

  const getContentIcon = (type, content) => {
    const contentLower = (content || '').toLowerCase();
    const isDocument = contentLower.endsWith('.pdf') || contentLower.endsWith('.docx') || contentLower.endsWith('.doc');
    
    if (isDocument || type === 'pdf') {
      return <FileText className="w-4 h-4" />;
    }
    
    switch (type) {
      case 'video':
      case 'embed':
        return <PlayCircle className="w-4 h-4" />;
      default:
        return <BookOpen className="w-4 h-4" />;
    }
  };

  // Get total lessons count
  const getTotalLessons = () => {
    return course?.modules?.reduce((acc, m) => acc + (m.lessons?.length || 0), 0) || 0;
  };

  // Get completed lessons count
  const getCompletedLessons = () => {
    return userProgress?.completed_lessons?.length || 0;
  };

  // Generate learning outcomes from course
  const getLearningOutcomes = () => {
    const outcomes = [
      'Understand the key concepts and principles covered in this course',
      'Apply practical knowledge to real-world scenarios',
      'Demonstrate competency through assessments and quizzes',
      'Earn a certificate upon successful completion'
    ];
    
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
    
    return outcomes;
  };

  const renderLessonContent = () => {
    if (!activeLesson) return null;

    const getContentUrl = () => {
      if (activeLesson.content.startsWith('/')) {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
        return `${backendUrl}${activeLesson.content}`;
      }
      return activeLesson.content;
    };

    const getViewerUrl = () => {
      if (activeLesson.content.startsWith('/api/uploads/documents/')) {
        const filename = activeLesson.content.split('/').pop();
        const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
        return `${backendUrl}/api/upload/view/${filename}`;
      }
      return getContentUrl();
    };

    const getPdfUrl = () => {
      const url = getContentUrl();
      return `${url}#toolbar=0&navpanes=0&scrollbar=0&view=FitH&zoom=page-width`;
    };

    const contentLower = activeLesson.content.toLowerCase();
    const isWordDoc = contentLower.endsWith('.docx') || contentLower.endsWith('.doc');
    const isPdf = contentLower.endsWith('.pdf');
    const isDocument = isWordDoc || isPdf;

    switch (activeLesson.content_type) {
      case 'video':
        return (
          <div className="video-container rounded-xl overflow-hidden bg-black">
            <video src={getContentUrl()} controls className="w-full" />
          </div>
        );
      case 'embed':
        return (
          <div className="video-container rounded-xl overflow-hidden">
            <iframe src={activeLesson.content} title={activeLesson.title} allowFullScreen className="w-full h-full" />
          </div>
        );
      case 'pdf':
        if (isDocument) {
          return (
            <div className="rounded-xl overflow-hidden border bg-white" style={{ height: '80vh' }}>
              <iframe src={getViewerUrl()} title={activeLesson.title} className="w-full h-full" frameBorder="0" style={{ border: 'none' }} />
            </div>
          );
        }
        return (
          <div className="rounded-xl overflow-hidden border bg-white" style={{ height: '80vh' }}>
            <iframe src={isPdf ? getPdfUrl() : getContentUrl()} title={activeLesson.title} className="w-full h-full" frameBorder="0" sandbox="allow-same-origin allow-scripts" />
          </div>
        );
      default:
        return (
          <div className="prose max-w-none p-8 bg-white rounded-xl border">
            <div dangerouslySetInnerHTML={{ __html: activeLesson.content }} />
          </div>
        );
    }
  };

  const renderQuizContent = () => {
    if (!activeQuiz) return null;

    if (quizResults) {
      return (
        <div className="space-y-6">
          <Card className={`border-2 ${quizResults.passed ? 'border-emerald-500 bg-emerald-50/50' : 'border-red-500 bg-red-50/50'}`}>
            <CardContent className="p-8 text-center">
              <div className={`w-20 h-20 mx-auto mb-6 rounded-full flex items-center justify-center ${quizResults.passed ? 'bg-emerald-100' : 'bg-red-100'}`}>
                {quizResults.passed ? (
                  <CheckCircle className="w-10 h-10 text-emerald-600" />
                ) : (
                  <ClipboardList className="w-10 h-10 text-red-600" />
                )}
              </div>
              <h3 className="text-3xl font-bold mb-2">{quizResults.passed ? 'Congratulations!' : 'Keep Trying!'}</h3>
              <p className="text-5xl font-bold text-[#095EB1] mb-4">{quizResults.score}%</p>
              <p className="text-slate-500">You scored {quizResults.earned_points} out of {quizResults.total_points} points</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Review Answers</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {quizResults.results.map((result, index) => (
                <div key={index} className={`p-4 rounded-xl border ${result.correct ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'}`}>
                  <p className="font-medium mb-2">Q{index + 1}: {result.question}</p>
                  <p className="text-sm">
                    <span className="text-slate-500">Your answer:</span>{' '}
                    <span className={result.correct ? 'text-emerald-600 font-medium' : 'text-red-600 font-medium'}>{result.user_answer || '(no answer)'}</span>
                  </p>
                  {!result.correct && (
                    <p className="text-sm mt-1">
                      <span className="text-slate-500">Correct answer:</span>{' '}
                      <span className="text-emerald-600 font-medium">{result.correct_answer}</span>
                    </p>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>

          <Button onClick={() => { setActiveQuiz(null); setQuizResults(null); }} variant="outline" className="w-full h-12 rounded-xl">
            Back to Course
          </Button>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <Card>
          <CardHeader className="bg-slate-50 border-b">
            <CardTitle className="flex items-center gap-2">
              <ClipboardList className="w-5 h-5 text-[#095EB1]" />
              {activeQuiz.title}
            </CardTitle>
            {activeQuiz.description && <p className="text-sm text-slate-500 mt-1">{activeQuiz.description}</p>}
            <Badge className="w-fit mt-2 bg-[#095EB1]/10 text-[#095EB1]">Passing Score: {activeQuiz.passing_score}%</Badge>
          </CardHeader>
          <CardContent className="p-6 space-y-6">
            {activeQuiz.questions?.map((question, qIndex) => (
              <div key={qIndex} className="p-5 bg-slate-50 rounded-xl">
                <p className="font-semibold mb-4">
                  Q{qIndex + 1}: {question.question}
                  <span className="text-sm text-slate-500 font-normal ml-2">({question.points} pt{question.points > 1 ? 's' : ''})</span>
                </p>
                
                {question.question_type === 'multiple_choice' && (
                  <div className="space-y-2">
                    {question.options?.map((option, oIndex) => (
                      <label key={oIndex} className={`flex items-center gap-3 p-4 rounded-lg border cursor-pointer transition-all ${quizAnswers[qIndex] === option ? 'bg-[#095EB1]/10 border-[#095EB1] shadow-sm' : 'bg-white border-slate-200 hover:border-slate-300'}`}>
                        <input type="radio" name={`q${qIndex}`} value={option} checked={quizAnswers[qIndex] === option} onChange={() => setQuizAnswers({ ...quizAnswers, [qIndex]: option })} className="w-4 h-4 text-[#095EB1]" />
                        <span>{option}</span>
                      </label>
                    ))}
                  </div>
                )}

                {question.question_type === 'true_false' && (
                  <div className="flex gap-4">
                    {['True', 'False'].map((option) => (
                      <label key={option} className={`flex-1 flex items-center justify-center gap-2 p-4 rounded-lg border cursor-pointer transition-all ${quizAnswers[qIndex] === option ? 'bg-[#095EB1]/10 border-[#095EB1] shadow-sm' : 'bg-white border-slate-200 hover:border-slate-300'}`}>
                        <input type="radio" name={`q${qIndex}`} value={option} checked={quizAnswers[qIndex] === option} onChange={() => setQuizAnswers({ ...quizAnswers, [qIndex]: option })} className="w-4 h-4 text-[#095EB1]" />
                        <span className="font-medium">{option}</span>
                      </label>
                    ))}
                  </div>
                )}

                {question.question_type === 'short_answer' && (
                  <input type="text" value={quizAnswers[qIndex] || ''} onChange={(e) => setQuizAnswers({ ...quizAnswers, [qIndex]: e.target.value })} className="w-full p-4 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[#095EB1]/20 focus:border-[#095EB1]" placeholder="Type your answer..." />
                )}
              </div>
            ))}
          </CardContent>
        </Card>

        <div className="flex gap-4">
          <Button variant="outline" onClick={() => setActiveQuiz(null)} className="flex-1 h-12 rounded-xl">Cancel</Button>
          <Button onClick={submitQuiz} disabled={quizSubmitting} className="flex-1 h-12 rounded-xl bg-[#095EB1] hover:bg-[#074A8C]">
            {quizSubmitting ? 'Submitting...' : 'Submit Quiz'}
          </Button>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <Layout>
        <div className="bg-slate-50 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <Skeleton className="h-8 w-32 mb-6" />
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              <div className="lg:col-span-8">
                <Skeleton className="h-64 rounded-xl mb-4" />
                <Skeleton className="h-8 w-3/4 mb-2" />
                <Skeleton className="h-4 w-full mb-4" />
              </div>
              <div className="lg:col-span-4">
                <Skeleton className="h-96 rounded-xl" />
              </div>
            </div>
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

  return (
    <Layout>
      <div data-testid="course-detail" className="bg-slate-50 min-h-screen">
        {/* Breadcrumb */}
        <div className="bg-white border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <nav className="flex items-center gap-2 text-sm">
              <Link to="/courses" className="text-slate-500 hover:text-[#095EB1] transition-colors">Courses</Link>
              <ChevronRight className="w-4 h-4 text-slate-400" />
              <span className="text-slate-900 font-medium truncate max-w-xs">{course.title}</span>
            </nav>
          </div>
        </div>

        {/* Course Header - Alison Style */}
        <div className="bg-white border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* Left Content */}
              <div className="lg:col-span-8">
                {/* Badges */}
                <div className="flex flex-wrap items-center gap-2 mb-4">
                  {course.course_type === 'compulsory' && (
                    <Badge className="bg-red-100 text-red-700 font-medium">Required Course</Badge>
                  )}
                  {course.category && (
                    <Badge className="bg-slate-100 text-slate-700">{course.category}</Badge>
                  )}
                  {isCompleted && (
                    <Badge className="bg-emerald-100 text-emerald-700">
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Completed
                    </Badge>
                  )}
                </div>

                {/* Title */}
                <h1 className="text-3xl md:text-4xl font-bold text-slate-900 tracking-tight mb-4">
                  {course.title}
                </h1>

                {/* Description */}
                <p className="text-lg text-slate-600 mb-6 leading-relaxed">
                  {course.description}
                </p>

                {/* Stats Row - Alison Style */}
                <div className="flex flex-wrap items-center gap-6 text-sm">
                  {course.duration_hours > 0 && (
                    <div className="flex items-center gap-2 text-slate-600">
                      <Clock className="w-4 h-4 text-slate-400" />
                      <span>{course.duration_hours} hours</span>
                    </div>
                  )}
                  <div className="flex items-center gap-2 text-slate-600">
                    <Users className="w-4 h-4 text-slate-400" />
                    <span>{(course.enrolled_users?.length || 0).toLocaleString()} learners</span>
                  </div>
                  <div className="flex items-center gap-2 text-slate-600">
                    <BookOpen className="w-4 h-4 text-slate-400" />
                    <span>{getTotalLessons()} lessons</span>
                  </div>
                  <div className="flex items-center gap-2 text-slate-600">
                    <BarChart3 className="w-4 h-4 text-slate-400" />
                    <span>{course.modules?.length || 0} modules</span>
                  </div>
                </div>
              </div>

              {/* Right Sidebar - Enrollment Card */}
              <div className="lg:col-span-4">
                <Card className="sticky top-24 shadow-xl shadow-slate-200/50 border-slate-200 overflow-hidden">
                  {/* Course Thumbnail */}
                  {course.thumbnail && (
                    <div className="aspect-video overflow-hidden">
                      <img src={course.thumbnail} alt={course.title} className="w-full h-full object-cover" />
                    </div>
                  )}
                  
                  <CardContent className="p-6">
                    {isEnrolled ? (
                      <div className="space-y-4">
                        {/* Progress Circle */}
                        <div className="text-center py-4">
                          <div className="relative w-24 h-24 mx-auto mb-3">
                            <svg className="w-full h-full transform -rotate-90">
                              <circle cx="48" cy="48" r="42" fill="none" stroke="#E2E8F0" strokeWidth="8" />
                              <circle cx="48" cy="48" r="42" fill="none" stroke={isCompleted ? '#10B981' : '#095EB1'} strokeWidth="8" strokeLinecap="round" strokeDasharray={`${progressPercentage * 2.64} 264`} />
                            </svg>
                            <div className="absolute inset-0 flex items-center justify-center">
                              <span className={`text-2xl font-bold ${isCompleted ? 'text-emerald-600' : 'text-[#095EB1]'}`}>{progressPercentage}%</span>
                            </div>
                          </div>
                          <p className="text-slate-500 text-sm">{getCompletedLessons()} of {getTotalLessons()} lessons completed</p>
                        </div>

                        <Button 
                          className={`w-full h-12 rounded-xl font-semibold ${isCompleted ? 'bg-emerald-500 hover:bg-emerald-600' : 'bg-[#095EB1] hover:bg-[#074A8C]'}`}
                          onClick={() => setActiveTab('content')}
                          data-testid="continue-learning-btn"
                        >
                          {isCompleted ? (
                            <>
                              <Award className="w-5 h-5 mr-2" />
                              Review Course
                            </>
                          ) : (
                            <>
                              <PlayCircle className="w-5 h-5 mr-2" />
                              Continue Learning
                            </>
                          )}
                        </Button>

                        {isCompleted && (
                          <p className="text-center text-sm text-emerald-600 font-medium">
                            <CheckCircle className="w-4 h-4 inline mr-1" />
                            You've completed this course!
                          </p>
                        )}
                      </div>
                    ) : (
                      <div className="space-y-4">
                        <div className="text-center py-4">
                          <p className="text-3xl font-bold text-[#095EB1] mb-1">Free</p>
                          <p className="text-slate-500 text-sm">Enroll to start learning</p>
                        </div>

                        <Button 
                          className="w-full h-12 rounded-xl font-semibold bg-[#095EB1] hover:bg-[#074A8C] animate-pulse-ring"
                          onClick={handleEnroll}
                          disabled={enrolling}
                          data-testid="enroll-btn"
                        >
                          {enrolling ? 'Enrolling...' : 'Start Learning'}
                        </Button>

                        <div className="pt-4 border-t border-slate-100 space-y-3">
                          <div className="flex items-center gap-3 text-sm text-slate-600">
                            <CheckCircle className="w-4 h-4 text-emerald-500" />
                            <span>Full lifetime access</span>
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
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs Navigation */}
        <div className="bg-white border-b border-slate-200 sticky top-16 z-30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="bg-transparent h-auto p-0 border-b-0">
                <TabsTrigger 
                  value="overview" 
                  className="px-6 py-4 rounded-none border-b-2 border-transparent data-[state=active]:border-[#095EB1] data-[state=active]:text-[#095EB1] font-medium"
                  data-testid="tab-overview"
                >
                  Overview
                </TabsTrigger>
                <TabsTrigger 
                  value="content" 
                  className="px-6 py-4 rounded-none border-b-2 border-transparent data-[state=active]:border-[#095EB1] data-[state=active]:text-[#095EB1] font-medium"
                  data-testid="tab-content"
                >
                  Course Content
                </TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
        </div>

        {/* Tab Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {activeTab === 'overview' ? (
            /* Overview Tab - Alison Style */
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              <div className="lg:col-span-8 space-y-8">
                {/* You Will Learn Section */}
                <Card className="border-slate-200">
                  <CardHeader className="bg-gradient-to-r from-[#095EB1]/5 to-transparent">
                    <CardTitle className="flex items-center gap-2 text-xl">
                      <Target className="w-5 h-5 text-[#095EB1]" />
                      What You Will Learn
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {getLearningOutcomes().map((outcome, index) => (
                        <div key={index} className="flex items-start gap-3">
                          <div className="w-6 h-6 bg-emerald-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <CheckCircle className="w-4 h-4 text-emerald-600" />
                          </div>
                          <p className="text-slate-600">{outcome}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Course Curriculum Preview */}
                <Card className="border-slate-200">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-xl">
                      <BookOpen className="w-5 h-5 text-[#095EB1]" />
                      Course Curriculum
                    </CardTitle>
                    <p className="text-slate-500 text-sm mt-1">
                      {course.modules?.length || 0} modules · {getTotalLessons()} lessons
                    </p>
                  </CardHeader>
                  <CardContent className="p-0">
                    <div className="divide-y divide-slate-100">
                      {course.modules?.slice(0, 3).map((module, mIndex) => (
                        <div key={module.id} className="p-4">
                          <div className="flex items-center gap-3">
                            <span className="w-8 h-8 bg-[#095EB1] text-white rounded-lg flex items-center justify-center text-sm font-bold">
                              {mIndex + 1}
                            </span>
                            <div>
                              <h4 className="font-semibold text-slate-900">{module.title}</h4>
                              <p className="text-sm text-slate-500">{module.lessons?.length || 0} lessons</p>
                            </div>
                          </div>
                        </div>
                      ))}
                      {course.modules?.length > 3 && (
                        <div className="p-4 text-center">
                          <Button variant="ghost" onClick={() => setActiveTab('content')} className="text-[#095EB1]">
                            View all {course.modules.length} modules
                            <ChevronRight className="w-4 h-4 ml-1" />
                          </Button>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Right Column */}
              <div className="lg:col-span-4 space-y-6">
                {/* Course Details */}
                <Card className="border-slate-200">
                  <CardHeader>
                    <CardTitle className="text-lg">Course Details</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between py-2 border-b border-slate-100">
                      <span className="text-slate-500 flex items-center gap-2">
                        <Clock className="w-4 h-4" />
                        Duration
                      </span>
                      <span className="font-medium">{course.duration_hours || 1} hours</span>
                    </div>
                    <div className="flex items-center justify-between py-2 border-b border-slate-100">
                      <span className="text-slate-500 flex items-center gap-2">
                        <BookOpen className="w-4 h-4" />
                        Modules
                      </span>
                      <span className="font-medium">{course.modules?.length || 0}</span>
                    </div>
                    <div className="flex items-center justify-between py-2 border-b border-slate-100">
                      <span className="text-slate-500 flex items-center gap-2">
                        <FileText className="w-4 h-4" />
                        Lessons
                      </span>
                      <span className="font-medium">{getTotalLessons()}</span>
                    </div>
                    <div className="flex items-center justify-between py-2 border-b border-slate-100">
                      <span className="text-slate-500 flex items-center gap-2">
                        <Users className="w-4 h-4" />
                        Enrolled
                      </span>
                      <span className="font-medium">{(course.enrolled_users?.length || 0).toLocaleString()}</span>
                    </div>
                    <div className="flex items-center justify-between py-2">
                      <span className="text-slate-500 flex items-center gap-2">
                        <Award className="w-4 h-4" />
                        Certificate
                      </span>
                      <span className="font-medium text-emerald-600">Yes</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          ) : (
            /* Content Tab - Course Player */
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Content Viewer */}
              <div className="lg:col-span-8">
                {activeQuiz ? (
                  renderQuizContent()
                ) : activeLesson ? (
                  <div className="space-y-4">
                    <Card className="border-slate-200 overflow-hidden">
                      <CardHeader className="bg-slate-50 border-b">
                        <div className="flex items-center justify-between">
                          <CardTitle className="flex items-center gap-2">
                            {getContentIcon(activeLesson.content_type, activeLesson.content)}
                            {activeLesson.title}
                          </CardTitle>
                          {activeLesson.duration_minutes > 0 && (
                            <Badge variant="outline">{activeLesson.duration_minutes} min</Badge>
                          )}
                        </div>
                      </CardHeader>
                      <CardContent className="p-6">
                        {renderLessonContent()}
                      </CardContent>
                    </Card>

                    {isEnrolled && !isLessonCompleted(activeLesson.id) && (
                      <Button 
                        className="w-full h-12 rounded-xl bg-[#095EB1] hover:bg-[#074A8C] font-semibold"
                        onClick={() => handleCompleteLesson(activeLesson.id)}
                        disabled={completingLesson === activeLesson.id}
                        data-testid="complete-lesson-btn"
                      >
                        {completingLesson === activeLesson.id ? 'Marking...' : 'Mark as Complete'}
                        <CheckCircle className="w-5 h-5 ml-2" />
                      </Button>
                    )}
                  </div>
                ) : (
                  <Card className="border-slate-200">
                    <CardContent className="p-16 text-center">
                      <div className="w-20 h-20 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                        <PlayCircle className="w-10 h-10 text-slate-400" />
                      </div>
                      <h3 className="text-xl font-semibold text-slate-700 mb-2">Select a lesson to start</h3>
                      <p className="text-slate-500 max-w-md mx-auto">
                        Choose a lesson from the curriculum on the right to begin learning.
                      </p>
                    </CardContent>
                  </Card>
                )}
              </div>

              {/* Curriculum Sidebar */}
              <div className="lg:col-span-4">
                <Card className="border-slate-200 sticky top-32">
                  <CardHeader className="bg-slate-50 border-b">
                    <CardTitle className="text-lg">Course Content</CardTitle>
                    {isEnrolled && (
                      <div className="mt-2">
                        <div className="flex items-center justify-between text-sm mb-1">
                          <span className="text-slate-500">Progress</span>
                          <span className={`font-bold ${isCompleted ? 'text-emerald-600' : 'text-[#095EB1]'}`}>{progressPercentage}%</span>
                        </div>
                        <Progress value={progressPercentage} className={`h-2 ${isCompleted ? '[&>div]:bg-emerald-500' : ''}`} />
                      </div>
                    )}
                  </CardHeader>
                  <CardContent className="p-0 max-h-[60vh] overflow-y-auto">
                    {course.modules?.length === 0 ? (
                      <div className="p-6 text-center text-slate-500">No content available yet</div>
                    ) : (
                      <div className="divide-y divide-slate-100">
                        {course.modules?.map((module, mIndex) => (
                          <Collapsible key={module.id} open={openModules[module.id]} onOpenChange={() => toggleModule(module.id)}>
                            <CollapsibleTrigger className="w-full p-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                              <div className="flex items-center gap-3">
                                <span className="w-7 h-7 bg-[#095EB1] text-white rounded-lg flex items-center justify-center text-xs font-bold">
                                  {mIndex + 1}
                                </span>
                                <span className="font-medium text-left text-sm">{module.title}</span>
                              </div>
                              {openModules[module.id] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                            </CollapsibleTrigger>
                            <CollapsibleContent>
                              <div className="pl-4 pr-2 pb-3 space-y-1">
                                {module.lessons?.map((lesson) => {
                                  const completed = isLessonCompleted(lesson.id);
                                  const isActive = activeLesson?.id === lesson.id;
                                  
                                  return (
                                    <button
                                      key={lesson.id}
                                      onClick={() => { setActiveLesson(lesson); setActiveQuiz(null); }}
                                      disabled={!isEnrolled}
                                      className={`w-full flex items-center gap-3 p-3 rounded-lg text-left transition-all ${
                                        isActive 
                                          ? 'bg-[#095EB1]/10 text-[#095EB1] shadow-sm' 
                                          : isEnrolled 
                                            ? 'hover:bg-slate-50' 
                                            : 'opacity-60 cursor-not-allowed'
                                      }`}
                                      data-testid={`lesson-${lesson.id}`}
                                    >
                                      {completed ? (
                                        <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                                      ) : isEnrolled ? (
                                        getContentIcon(lesson.content_type, lesson.content)
                                      ) : (
                                        <Lock className="w-4 h-4 text-slate-400 flex-shrink-0" />
                                      )}
                                      <span className="flex-1 text-sm truncate">{lesson.title}</span>
                                      {lesson.duration_minutes > 0 && (
                                        <span className="text-xs text-slate-400">{lesson.duration_minutes}m</span>
                                      )}
                                    </button>
                                  );
                                })}
                                
                                {module.quizzes?.map((quiz) => {
                                  const quizScore = userProgress?.quiz_scores?.[quiz.id];
                                  const passed = quizScore?.passed;
                                  
                                  return (
                                    <button
                                      key={quiz.id}
                                      onClick={() => startQuiz(quiz)}
                                      disabled={!isEnrolled}
                                      className={`w-full flex items-center gap-3 p-3 rounded-lg text-left transition-all ${
                                        activeQuiz?.id === quiz.id 
                                          ? 'bg-[#095EB1]/10 text-[#095EB1] shadow-sm' 
                                          : isEnrolled 
                                            ? 'hover:bg-slate-50' 
                                            : 'opacity-60 cursor-not-allowed'
                                      }`}
                                      data-testid={`quiz-${quiz.id}`}
                                    >
                                      {passed ? (
                                        <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                                      ) : isEnrolled ? (
                                        <ClipboardList className="w-4 h-4 text-amber-500 flex-shrink-0" />
                                      ) : (
                                        <Lock className="w-4 h-4 text-slate-400 flex-shrink-0" />
                                      )}
                                      <span className="flex-1 text-sm truncate">{quiz.title}</span>
                                      {quizScore && (
                                        <Badge className={`text-xs ${passed ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
                                          {quizScore.score}%
                                        </Badge>
                                      )}
                                    </button>
                                  );
                                })}
                              </div>
                            </CollapsibleContent>
                          </Collapsible>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
