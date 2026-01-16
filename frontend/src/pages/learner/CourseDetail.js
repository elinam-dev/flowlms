import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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
  ClipboardList
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

  const isEnrolled = user && course?.enrolled_users?.includes(user.id);
  const userProgress = course?.user_progress;

  useEffect(() => {
    fetchCourse();
  }, [courseId]);

  const fetchCourse = async () => {
    try {
      const response = await courseApi.getById(courseId);
      setCourse(response.data);
      
      // Open first module by default
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
      const response = await progressApi.updateLesson(lessonId, true);
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

  const getContentIcon = (type) => {
    switch (type) {
      case 'video':
      case 'embed':
        return <PlayCircle className="w-4 h-4" />;
      case 'pdf':
        return <FileText className="w-4 h-4" />;
      default:
        return <BookOpen className="w-4 h-4" />;
    }
  };

  const renderLessonContent = () => {
    if (!activeLesson) return null;

    switch (activeLesson.content_type) {
      case 'video':
        return (
          <div className="video-container rounded-lg overflow-hidden bg-black">
            <video 
              src={activeLesson.content.startsWith('/') ? `${process.env.REACT_APP_BACKEND_URL}${activeLesson.content}` : activeLesson.content}
              controls 
              className="w-full"
            />
          </div>
        );
      case 'embed':
        return (
          <div className="video-container rounded-lg overflow-hidden">
            <iframe
              src={activeLesson.content}
              title={activeLesson.title}
              allowFullScreen
              className="w-full h-full"
            />
          </div>
        );
      case 'pdf':
        return (
          <div className="aspect-[4/3] rounded-lg overflow-hidden">
            <iframe
              src={activeLesson.content.startsWith('/') ? `${process.env.REACT_APP_BACKEND_URL}${activeLesson.content}` : activeLesson.content}
              title={activeLesson.title}
              className="w-full h-full"
            />
          </div>
        );
      default:
        return (
          <div className="prose max-w-none p-6 bg-white rounded-lg border">
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
          <Card className={`card-base ${quizResults.passed ? 'border-emerald-500' : 'border-red-500'}`}>
            <CardContent className="p-6 text-center">
              <div className={`w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center ${quizResults.passed ? 'bg-emerald-100' : 'bg-red-100'}`}>
                {quizResults.passed ? (
                  <CheckCircle className="w-8 h-8 text-emerald-600" />
                ) : (
                  <ClipboardList className="w-8 h-8 text-red-600" />
                )}
              </div>
              <h3 className="text-2xl font-bold mb-2">{quizResults.passed ? 'Congratulations!' : 'Keep Trying!'}</h3>
              <p className="text-4xl font-bold text-[#095EB1] mb-2">{quizResults.score}%</p>
              <p className="text-slate-500">
                You scored {quizResults.earned_points} out of {quizResults.total_points} points
              </p>
            </CardContent>
          </Card>

          <Card className="card-base">
            <CardHeader>
              <CardTitle>Review Answers</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {quizResults.results.map((result, index) => (
                <div 
                  key={index} 
                  className={`p-4 rounded-lg border ${result.correct ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'}`}
                >
                  <p className="font-medium mb-2">Q{index + 1}: {result.question}</p>
                  <p className="text-sm">
                    <span className="text-slate-500">Your answer:</span>{' '}
                    <span className={result.correct ? 'text-emerald-600' : 'text-red-600'}>{result.user_answer || '(no answer)'}</span>
                  </p>
                  {!result.correct && (
                    <p className="text-sm">
                      <span className="text-slate-500">Correct answer:</span>{' '}
                      <span className="text-emerald-600">{result.correct_answer}</span>
                    </p>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>

          <Button onClick={() => { setActiveQuiz(null); setQuizResults(null); }} variant="outline" className="w-full">
            Back to Course
          </Button>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <Card className="card-base">
          <CardHeader className="bg-slate-50 border-b">
            <CardTitle>{activeQuiz.title}</CardTitle>
            {activeQuiz.description && (
              <p className="text-sm text-slate-500">{activeQuiz.description}</p>
            )}
            <Badge className="w-fit">Passing Score: {activeQuiz.passing_score}%</Badge>
          </CardHeader>
          <CardContent className="p-6 space-y-6">
            {activeQuiz.questions?.map((question, qIndex) => (
              <div key={qIndex} className="p-4 bg-slate-50 rounded-lg">
                <p className="font-medium mb-3">
                  Q{qIndex + 1}: {question.question}
                  <span className="text-sm text-slate-500 ml-2">({question.points} pt{question.points > 1 ? 's' : ''})</span>
                </p>
                
                {question.question_type === 'multiple_choice' && (
                  <div className="space-y-2">
                    {question.options?.map((option, oIndex) => (
                      <label 
                        key={oIndex} 
                        className={`flex items-center gap-3 p-3 rounded-md border cursor-pointer transition-colors ${
                          quizAnswers[qIndex] === option ? 'bg-[#095EB1]/10 border-[#095EB1]' : 'bg-white border-slate-200 hover:border-slate-300'
                        }`}
                      >
                        <input
                          type="radio"
                          name={`q${qIndex}`}
                          value={option}
                          checked={quizAnswers[qIndex] === option}
                          onChange={() => setQuizAnswers({ ...quizAnswers, [qIndex]: option })}
                          className="w-4 h-4 text-[#095EB1]"
                        />
                        <span>{option}</span>
                      </label>
                    ))}
                  </div>
                )}

                {question.question_type === 'true_false' && (
                  <div className="flex gap-4">
                    {['True', 'False'].map((option) => (
                      <label 
                        key={option} 
                        className={`flex-1 flex items-center justify-center gap-2 p-3 rounded-md border cursor-pointer transition-colors ${
                          quizAnswers[qIndex] === option ? 'bg-[#095EB1]/10 border-[#095EB1]' : 'bg-white border-slate-200 hover:border-slate-300'
                        }`}
                      >
                        <input
                          type="radio"
                          name={`q${qIndex}`}
                          value={option}
                          checked={quizAnswers[qIndex] === option}
                          onChange={() => setQuizAnswers({ ...quizAnswers, [qIndex]: option })}
                          className="w-4 h-4 text-[#095EB1]"
                        />
                        <span>{option}</span>
                      </label>
                    ))}
                  </div>
                )}

                {question.question_type === 'short_answer' && (
                  <input
                    type="text"
                    value={quizAnswers[qIndex] || ''}
                    onChange={(e) => setQuizAnswers({ ...quizAnswers, [qIndex]: e.target.value })}
                    className="w-full p-3 rounded-md border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[#095EB1]"
                    placeholder="Type your answer..."
                  />
                )}
              </div>
            ))}
          </CardContent>
        </Card>

        <div className="flex gap-4">
          <Button variant="outline" onClick={() => setActiveQuiz(null)} className="flex-1">
            Cancel
          </Button>
          <Button 
            onClick={submitQuiz} 
            disabled={quizSubmitting}
            className="flex-1 bg-[#095EB1] hover:bg-[#074A8C]"
          >
            {quizSubmitting ? 'Submitting...' : 'Submit Quiz'}
          </Button>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <Layout>
        <div className="page-container">
          <Skeleton className="h-8 w-64 mb-4" />
          <Skeleton className="h-64 mb-8" />
        </div>
      </Layout>
    );
  }

  if (!course) {
    return (
      <Layout>
        <div className="page-container text-center py-16">
          <BookOpen className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Course not found</h2>
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
      <div className="page-container" data-testid="course-detail">
        {/* Back Button */}
        <Button 
          variant="ghost" 
          onClick={() => navigate('/courses')} 
          className="mb-4"
          data-testid="back-to-courses"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Courses
        </Button>

        {/* Course Header */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <div className="lg:col-span-2">
            <div className="flex items-start gap-4 mb-4">
              {course.category && (
                <Badge className="bg-[#095EB1]/10 text-[#095EB1]">{course.category}</Badge>
              )}
            </div>
            <h1 className="text-3xl font-bold text-[#0F172A] mb-4">{course.title}</h1>
            <p className="text-slate-600 mb-6">{course.description}</p>
            
            <div className="flex flex-wrap items-center gap-6 text-sm text-slate-500">
              {course.duration_hours > 0 && (
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  <span>{course.duration_hours} hours</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                <span>{course.enrolled_users?.length || 0} enrolled</span>
              </div>
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                <span>{course.modules?.length || 0} modules</span>
              </div>
            </div>
          </div>

          {/* Enrollment Card */}
          <Card className="card-base">
            <CardContent className="p-6">
              {course.thumbnail && (
                <img src={course.thumbnail} alt={course.title} className="w-full aspect-video object-cover rounded-lg mb-4" />
              )}
              
              {isEnrolled ? (
                <div className="space-y-4">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-500">Progress</span>
                    <span className="font-semibold text-[#095EB1]">{userProgress?.percentage || 0}%</span>
                  </div>
                  <Progress value={userProgress?.percentage || 0} className="h-2" />
                  <Badge className="bg-emerald-100 text-emerald-700 w-full justify-center py-2">
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Enrolled
                  </Badge>
                </div>
              ) : (
                <Button 
                  className="w-full bg-[#095EB1] hover:bg-[#074A8C]" 
                  onClick={handleEnroll}
                  disabled={enrolling}
                  data-testid="enroll-btn"
                >
                  {enrolling ? 'Enrolling...' : 'Enroll in Course'}
                </Button>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Course Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Content Viewer */}
          <div className="lg:col-span-2 order-2 lg:order-1">
            {activeQuiz ? (
              renderQuizContent()
            ) : activeLesson ? (
              <div className="space-y-4">
                <Card className="card-base">
                  <CardHeader className="bg-slate-50 border-b">
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center gap-2">
                        {getContentIcon(activeLesson.content_type)}
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
                    className="w-full bg-[#095EB1] hover:bg-[#074A8C]"
                    onClick={() => handleCompleteLesson(activeLesson.id)}
                    disabled={completingLesson === activeLesson.id}
                    data-testid="complete-lesson-btn"
                  >
                    {completingLesson === activeLesson.id ? 'Marking...' : 'Mark as Complete'}
                    <CheckCircle className="w-4 h-4 ml-2" />
                  </Button>
                )}
              </div>
            ) : (
              <Card className="card-base">
                <CardContent className="p-12 text-center">
                  <PlayCircle className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-700 mb-2">Select a lesson to start</h3>
                  <p className="text-slate-500">Choose a lesson from the curriculum to begin learning.</p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Curriculum Sidebar */}
          <div className="order-1 lg:order-2">
            <Card className="card-base sticky top-24">
              <CardHeader className="bg-slate-50 border-b">
                <CardTitle>Course Content</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                {course.modules?.length === 0 ? (
                  <div className="p-6 text-center text-slate-500">
                    No content available yet
                  </div>
                ) : (
                  <div className="divide-y">
                    {course.modules?.map((module, mIndex) => (
                      <Collapsible 
                        key={module.id} 
                        open={openModules[module.id]}
                        onOpenChange={() => toggleModule(module.id)}
                      >
                        <CollapsibleTrigger className="w-full p-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                          <div className="flex items-center gap-3">
                            <span className="w-6 h-6 bg-[#095EB1] text-white rounded-full flex items-center justify-center text-xs font-medium">
                              {mIndex + 1}
                            </span>
                            <span className="font-medium text-left">{module.title}</span>
                          </div>
                          {openModules[module.id] ? (
                            <ChevronUp className="w-4 h-4 text-slate-400" />
                          ) : (
                            <ChevronDown className="w-4 h-4 text-slate-400" />
                          )}
                        </CollapsibleTrigger>
                        <CollapsibleContent>
                          <div className="pl-4 pr-2 pb-2 space-y-1">
                            {module.lessons?.map((lesson) => {
                              const completed = isLessonCompleted(lesson.id);
                              const isActive = activeLesson?.id === lesson.id;
                              
                              return (
                                <button
                                  key={lesson.id}
                                  onClick={() => { setActiveLesson(lesson); setActiveQuiz(null); }}
                                  disabled={!isEnrolled}
                                  className={`w-full flex items-center gap-3 p-3 rounded-md text-left transition-colors ${
                                    isActive 
                                      ? 'bg-[#095EB1]/10 text-[#095EB1]' 
                                      : isEnrolled 
                                        ? 'hover:bg-slate-50' 
                                        : 'opacity-60 cursor-not-allowed'
                                  }`}
                                  data-testid={`lesson-${lesson.id}`}
                                >
                                  {completed ? (
                                    <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                                  ) : isEnrolled ? (
                                    getContentIcon(lesson.content_type)
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
                            
                            {/* Quizzes */}
                            {module.quizzes?.map((quiz) => {
                              const quizScore = userProgress?.quiz_scores?.[quiz.id];
                              const passed = quizScore?.passed;
                              
                              return (
                                <button
                                  key={quiz.id}
                                  onClick={() => startQuiz(quiz)}
                                  disabled={!isEnrolled}
                                  className={`w-full flex items-center gap-3 p-3 rounded-md text-left transition-colors ${
                                    activeQuiz?.id === quiz.id 
                                      ? 'bg-[#095EB1]/10 text-[#095EB1]' 
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
                                    <Badge className={passed ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}>
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
      </div>
    </Layout>
  );
}
