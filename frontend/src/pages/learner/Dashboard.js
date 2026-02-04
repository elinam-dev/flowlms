import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { useAuth } from '../../context/AuthContext';
import { courseApi, certificateApi, userApi } from '../../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Progress } from '../../components/ui/progress';
import { Skeleton } from '../../components/ui/skeleton';
import { Badge } from '../../components/ui/badge';
import { CourseCarousel } from '../../components/CourseCarousel';
import { toast } from 'sonner';
import { 
  BookOpen, 
  Award, 
  Clock, 
  TrendingUp, 
  ChevronRight,
  PlayCircle,
  GraduationCap,
  Flame,
  Calendar,
  CheckCircle,
  Sparkles,
  Target,
  ArrowRight,
  Users
} from 'lucide-react';

export default function LearnerDashboard() {
  const { user } = useAuth();
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [allCourses, setAllCourses] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [checkInStatus, setCheckInStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [checkingIn, setCheckingIn] = useState(false);
  const [enrollingId, setEnrollingId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [coursesRes, enrolledRes, certsRes, checkInRes] = await Promise.all([
        courseApi.getAll(),
        courseApi.getEnrolled(),
        certificateApi.getAll(),
        userApi.getCheckInStatus()
      ]);
      setAllCourses(coursesRes.data);
      setEnrolledCourses(enrolledRes.data);
      setCertificates(certsRes.data);
      setCheckInStatus(checkInRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckIn = async () => {
    setCheckingIn(true);
    try {
      const response = await userApi.checkIn();
      setCheckInStatus(response.data);
      
      if (response.data.already_checked_in) {
        toast.info("You've already checked in today!");
      } else {
        toast.success(
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center">
              <Flame className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="font-semibold">Check-in successful!</p>
              <p className="text-sm">{response.data.streak} day streak!</p>
            </div>
          </div>,
          { duration: 4000 }
        );
      }
    } catch (error) {
      toast.error('Failed to check in');
    } finally {
      setCheckingIn(false);
    }
  };

  const handleEnroll = async (courseId, e) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    setEnrollingId(courseId);
    
    try {
      await courseApi.enroll(courseId);
      const enrolledRes = await courseApi.getEnrolled();
      setEnrolledCourses(enrolledRes.data);
      toast.success('Successfully enrolled in course!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to enroll');
    } finally {
      setEnrollingId(null);
    }
  };

  const completedCourses = enrolledCourses.filter(c => c.progress >= 100);
  const inProgressCourses = enrolledCourses.filter(c => c.progress > 0 && c.progress < 100);
  const avgProgress = enrolledCourses.length > 0 
    ? Math.round(enrolledCourses.reduce((acc, c) => acc + c.progress, 0) / enrolledCourses.length)
    : 0;

  // Get courses not yet enrolled
  const availableCourses = allCourses.filter(
    course => !enrolledCourses.some(ec => ec.id === course.id)
  );

  // Get last 7 days for check-in calendar
  const getLast7Days = () => {
    const days = [];
    for (let i = 6; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      days.push(date.toISOString().split('T')[0]);
    }
    return days;
  };

  // Get greeting based on time
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  if (loading) {
    return (
      <Layout>
        <div className="hero-pattern py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <Skeleton className="h-12 w-64 mb-4" />
            <Skeleton className="h-6 w-96 mb-8" />
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[1,2,3,4].map(i => <Skeleton key={i} className="h-32 rounded-xl" />)}
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div data-testid="learner-dashboard">
        {/* Hero Section */}
        <section className="hero-pattern py-12 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-[#095EB1]/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-[#0EA5E9]/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
          
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-8">
              {/* Welcome Message */}
              <div className="animate-fade-up">
                <Badge className="bg-[#095EB1]/10 text-[#095EB1] mb-3 py-1.5 px-3">
                  <Sparkles className="w-3.5 h-3.5 mr-1.5" />
                  {getGreeting()}
                </Badge>
                <h1 className="text-4xl md:text-5xl font-bold text-slate-900 tracking-tight mb-3">
                  Welcome back, <span className="text-[#095EB1]">{user?.first_name}!</span>
                </h1>
                <p className="text-lg text-slate-600 max-w-xl">
                  Continue your learning journey. You have {inProgressCourses.length} courses in progress.
                </p>
              </div>

              {/* Daily Check-in Card */}
              <div className="animate-fade-up stagger-2">
                <Card className="bg-gradient-to-br from-[#095EB1] to-[#074A8C] text-white border-0 shadow-xl shadow-[#095EB1]/25 overflow-hidden">
                  <CardContent className="p-6 relative">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
                    <div className="relative z-10">
                      <div className="flex items-center gap-2 mb-4">
                        <Flame className="w-5 h-5 text-orange-300" />
                        <span className="font-semibold">Daily Check-in</span>
                      </div>
                      <div className="flex items-baseline gap-2 mb-4">
                        <span className="text-5xl font-bold">{checkInStatus?.streak || 0}</span>
                        <span className="text-white/80">day streak</span>
                      </div>
                      <Button
                        onClick={handleCheckIn}
                        disabled={checkingIn || checkInStatus?.checked_in_today}
                        className={`w-full ${
                          checkInStatus?.checked_in_today 
                            ? 'bg-white/20 text-white cursor-default hover:bg-white/20' 
                            : 'bg-white text-[#095EB1] hover:bg-white/90'
                        } font-semibold h-11 rounded-xl`}
                        data-testid="check-in-btn"
                      >
                        {checkInStatus?.checked_in_today ? (
                          <>
                            <CheckCircle className="w-4 h-4 mr-2" />
                            Checked In Today
                          </>
                        ) : checkingIn ? (
                          'Checking in...'
                        ) : (
                          <>
                            <Target className="w-4 h-4 mr-2" />
                            Check In Now
                          </>
                        )}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Check-in Calendar Row */}
            <div className="mt-8 animate-fade-up stagger-3">
              <Card className="bg-white/80 backdrop-blur-sm border-slate-200">
                <CardContent className="p-4">
                  <div className="flex items-center gap-6">
                    <div className="flex items-center gap-2 text-slate-600">
                      <Calendar className="w-5 h-5 text-[#095EB1]" />
                      <span className="font-medium">Last 7 Days</span>
                    </div>
                    <div className="flex gap-2">
                      {getLast7Days().map((date) => {
                        const isCheckedIn = checkInStatus?.check_ins?.includes(date);
                        const isToday = date === new Date().toISOString().split('T')[0];
                        const dayName = new Date(date).toLocaleDateString('en', { weekday: 'short' });
                        return (
                          <div 
                            key={date} 
                            className={`w-12 h-14 rounded-xl flex flex-col items-center justify-center text-xs transition-all ${
                              isCheckedIn 
                                ? 'bg-gradient-to-br from-orange-400 to-red-500 text-white shadow-lg shadow-orange-200' 
                                : isToday 
                                  ? 'bg-[#095EB1]/10 border-2 border-dashed border-[#095EB1] text-[#095EB1]'
                                  : 'bg-slate-100 text-slate-400'
                            }`}
                          >
                            <span className="text-[10px] uppercase font-medium opacity-75">{dayName}</span>
                            <span className="font-bold text-sm">{new Date(date).getDate()}</span>
                            {isCheckedIn && <Flame className="w-3 h-3 mt-0.5" />}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-8 bg-white border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {/* Enrolled */}
              <div className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-br from-blue-50 to-white border border-blue-100">
                <div className="w-12 h-12 bg-gradient-to-br from-[#095EB1] to-[#0EA5E9] rounded-xl flex items-center justify-center shadow-lg shadow-blue-200">
                  <BookOpen className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">{enrolledCourses.length}</p>
                  <p className="text-sm text-slate-500">Enrolled</p>
                </div>
              </div>

              {/* In Progress */}
              <div className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-br from-cyan-50 to-white border border-cyan-100">
                <div className="w-12 h-12 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-200">
                  <PlayCircle className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">{inProgressCourses.length}</p>
                  <p className="text-sm text-slate-500">In Progress</p>
                </div>
              </div>

              {/* Completed */}
              <div className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-br from-emerald-50 to-white border border-emerald-100">
                <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-green-500 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-200">
                  <GraduationCap className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">{completedCourses.length}</p>
                  <p className="text-sm text-slate-500">Completed</p>
                </div>
              </div>

              {/* Certificates */}
              <div className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-br from-amber-50 to-white border border-amber-100">
                <div className="w-12 h-12 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center shadow-lg shadow-amber-200">
                  <Award className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">{certificates.length}</p>
                  <p className="text-sm text-slate-500">Certificates</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Continue Learning Section */}
        {inProgressCourses.length > 0 && (
          <section className="py-12 bg-slate-50/50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <CourseCarousel
                title="Continue Learning"
                subtitle="Pick up where you left off"
                courses={inProgressCourses}
                enrolledCourses={enrolledCourses}
                onEnroll={handleEnroll}
                enrollingId={enrollingId}
                showViewAll={false}
              />
            </div>
          </section>
        )}

        {/* Main Content */}
        <section className="py-12 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* My Courses List */}
              <div className="lg:col-span-8">
                <Card className="border-slate-200 shadow-sm">
                  <CardHeader className="border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-xl font-bold flex items-center gap-2">
                        <BookOpen className="w-5 h-5 text-[#095EB1]" />
                        My Enrolled Courses
                      </CardTitle>
                      <Link to="/courses">
                        <Button variant="ghost" size="sm" className="text-[#095EB1] font-medium" data-testid="view-all-courses">
                          View All <ChevronRight className="w-4 h-4 ml-1" />
                        </Button>
                      </Link>
                    </div>
                  </CardHeader>
                  <CardContent className="p-0">
                    {enrolledCourses.length === 0 ? (
                      <div className="text-center py-16 px-6">
                        <div className="w-20 h-20 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                          <BookOpen className="w-10 h-10 text-slate-400" />
                        </div>
                        <h3 className="text-xl font-semibold text-slate-700 mb-2">No courses enrolled yet</h3>
                        <p className="text-slate-500 mb-6 max-w-md mx-auto">
                          Start your learning journey by exploring our course catalog.
                        </p>
                        <Link to="/courses">
                          <Button className="bg-[#095EB1] hover:bg-[#074A8C] font-semibold px-6" data-testid="browse-courses-btn">
                            Browse Courses
                            <ArrowRight className="w-4 h-4 ml-2" />
                          </Button>
                        </Link>
                      </div>
                    ) : (
                      <div className="divide-y divide-slate-100">
                        {enrolledCourses.slice(0, 5).map((course) => {
                          const isCompleted = course.progress >= 100;
                          
                          return (
                            <Link 
                              key={course.id} 
                              to={`/courses/${course.id}`}
                              className="block"
                              data-testid={`course-card-${course.id}`}
                            >
                              <div className={`p-5 hover:bg-slate-50 transition-colors group`}>
                                <div className="flex items-start gap-4">
                                  {/* Thumbnail */}
                                  <div className={`w-24 h-16 rounded-lg overflow-hidden flex-shrink-0 ${
                                    isCompleted 
                                      ? 'bg-gradient-to-br from-emerald-100 to-emerald-200' 
                                      : 'bg-gradient-to-br from-[#095EB1]/10 to-[#0EA5E9]/10'
                                  } flex items-center justify-center`}>
                                    {course.thumbnail ? (
                                      <img src={course.thumbnail} alt={course.title} className="w-full h-full object-cover" />
                                    ) : isCompleted ? (
                                      <CheckCircle className="w-6 h-6 text-emerald-600" />
                                    ) : (
                                      <BookOpen className="w-6 h-6 text-[#095EB1]" />
                                    )}
                                  </div>

                                  {/* Content */}
                                  <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                                      {isCompleted ? (
                                        <Badge className="bg-emerald-100 text-emerald-700 text-xs font-medium">
                                          <CheckCircle className="w-3 h-3 mr-1" />
                                          Completed
                                        </Badge>
                                      ) : course.progress > 0 ? (
                                        <Badge className="bg-blue-100 text-blue-700 text-xs font-medium">
                                          In Progress
                                        </Badge>
                                      ) : (
                                        <Badge className="bg-slate-100 text-slate-600 text-xs font-medium">
                                          Not Started
                                        </Badge>
                                      )}
                                      {course.course_type === 'compulsory' && (
                                        <Badge className="bg-red-100 text-red-700 text-xs font-medium">Required</Badge>
                                      )}
                                    </div>
                                    <h3 className={`font-semibold transition-colors ${
                                      isCompleted 
                                        ? 'text-emerald-800 group-hover:text-emerald-600' 
                                        : 'text-slate-900 group-hover:text-[#095EB1]'
                                    }`}>
                                      {course.title}
                                    </h3>
                                    <div className="mt-3 flex items-center gap-3">
                                      <Progress 
                                        value={course.progress} 
                                        className={`flex-1 h-2 ${isCompleted ? '[&>div]:bg-emerald-500' : ''}`} 
                                      />
                                      <span className={`text-sm font-bold min-w-[3rem] text-right ${isCompleted ? 'text-emerald-600' : 'text-[#095EB1]'}`}>
                                        {course.progress}%
                                      </span>
                                    </div>
                                  </div>

                                  {/* Action */}
                                  <div className="flex-shrink-0">
                                    {isCompleted ? (
                                      <Award className="w-5 h-5 text-emerald-500" />
                                    ) : (
                                      <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-[#095EB1] transition-colors" />
                                    )}
                                  </div>
                                </div>
                              </div>
                            </Link>
                          );
                        })}
                        {enrolledCourses.length > 5 && (
                          <div className="p-4 text-center bg-slate-50">
                            <Link to="/courses">
                              <Button variant="ghost" className="text-[#095EB1] font-medium">
                                View all {enrolledCourses.length} courses
                                <ChevronRight className="w-4 h-4 ml-1" />
                              </Button>
                            </Link>
                          </div>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>

              {/* Sidebar */}
              <div className="lg:col-span-4 space-y-6">
                {/* Overall Progress */}
                <Card className="border-slate-200 shadow-sm overflow-hidden">
                  <div className="h-1.5 bg-gradient-to-r from-[#095EB1] to-[#0EA5E9]" style={{ width: `${avgProgress}%` }} />
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium text-slate-500 flex items-center gap-2">
                      <TrendingUp className="w-4 h-4" />
                      Overall Progress
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-end gap-2 mb-4">
                      <span className="text-5xl font-bold bg-gradient-to-r from-[#095EB1] to-[#0EA5E9] bg-clip-text text-transparent">{avgProgress}%</span>
                      <span className="text-slate-500 mb-1">average</span>
                    </div>
                    <Progress value={avgProgress} className="h-3" />
                  </CardContent>
                </Card>

                {/* Recent Certificates */}
                <Card className="border-slate-200 shadow-sm">
                  <CardHeader className="border-b border-slate-100 bg-gradient-to-r from-amber-50 to-white">
                    <CardTitle className="text-sm font-medium flex items-center gap-2">
                      <Award className="w-4 h-4 text-amber-500" />
                      Recent Certificates
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="p-4">
                    {certificates.length === 0 ? (
                      <p className="text-sm text-slate-500 text-center py-6">
                        Complete courses to earn certificates
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {certificates.slice(0, 3).map((cert) => (
                          <Link 
                            key={cert.id} 
                            to="/certificates"
                            className="flex items-center gap-3 p-3 rounded-xl hover:bg-amber-50 transition-colors"
                            data-testid={`cert-${cert.id}`}
                          >
                            <div className="w-10 h-10 bg-gradient-to-br from-amber-400 to-orange-500 rounded-lg flex items-center justify-center shadow-sm">
                              <Award className="w-5 h-5 text-white" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-slate-900 truncate">{cert.course_title}</p>
                              <p className="text-xs text-slate-500">
                                {new Date(cert.issued_at).toLocaleDateString()}
                              </p>
                            </div>
                          </Link>
                        ))}
                      </div>
                    )}
                    {certificates.length > 0 && (
                      <Link to="/certificates" className="block mt-4">
                        <Button variant="ghost" size="sm" className="w-full text-[#095EB1] font-medium" data-testid="view-all-certs">
                          View All Certificates
                          <ChevronRight className="w-4 h-4 ml-1" />
                        </Button>
                      </Link>
                    )}
                  </CardContent>
                </Card>

                {/* Explore More */}
                {availableCourses.length > 0 && (
                  <Card className="border-slate-200 shadow-sm bg-gradient-to-br from-[#095EB1]/5 to-transparent">
                    <CardContent className="p-6 text-center">
                      <div className="w-12 h-12 bg-[#095EB1]/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                        <Sparkles className="w-6 h-6 text-[#095EB1]" />
                      </div>
                      <h3 className="font-semibold text-slate-900 mb-2">Explore More Courses</h3>
                      <p className="text-sm text-slate-500 mb-4">
                        {availableCourses.length} more courses available to enroll
                      </p>
                      <Link to="/courses">
                        <Button className="w-full bg-[#095EB1] hover:bg-[#074A8C] font-semibold">
                          Browse Catalog
                          <ArrowRight className="w-4 h-4 ml-2" />
                        </Button>
                      </Link>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* Recommended Courses */}
        {availableCourses.length > 0 && (
          <section className="py-12 bg-slate-50/50 border-t border-slate-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <CourseCarousel
                title="Recommended For You"
                subtitle="Courses you might be interested in"
                courses={availableCourses.slice(0, 8)}
                enrolledCourses={enrolledCourses}
                onEnroll={handleEnroll}
                enrollingId={enrollingId}
                showViewAll={false}
              />
            </div>
          </section>
        )}
      </div>
    </Layout>
  );
}
