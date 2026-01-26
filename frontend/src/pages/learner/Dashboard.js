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
  Target
} from 'lucide-react';

export default function LearnerDashboard() {
  const { user } = useAuth();
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [checkInStatus, setCheckInStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [checkingIn, setCheckingIn] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [coursesRes, certsRes, checkInRes] = await Promise.all([
        courseApi.getEnrolled(),
        certificateApi.getAll(),
        userApi.getCheckInStatus()
      ]);
      setEnrolledCourses(coursesRes.data);
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
              <p className="text-sm">🔥 {response.data.streak} day streak!</p>
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

  const completedCourses = enrolledCourses.filter(c => c.progress >= 100);
  const inProgressCourses = enrolledCourses.filter(c => c.progress > 0 && c.progress < 100);
  const avgProgress = enrolledCourses.length > 0 
    ? Math.round(enrolledCourses.reduce((acc, c) => acc + c.progress, 0) / enrolledCourses.length)
    : 0;

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

  if (loading) {
    return (
      <Layout>
        <div className="page-container">
          <Skeleton className="h-8 w-64 mb-8" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[1,2,3,4].map(i => <Skeleton key={i} className="h-32" />)}
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page-container" data-testid="learner-dashboard">
        {/* Welcome Section with Gradient Background */}
        <div className="relative mb-8 p-6 rounded-2xl bg-gradient-to-r from-[#095EB1] to-[#0EA5E9] text-white overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-white/10 rounded-full translate-y-1/2 -translate-x-1/2" />
          
          <div className="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-5 h-5 text-yellow-300" />
                <span className="text-sm font-medium text-white/80">Welcome back</span>
              </div>
              <h1 className="text-3xl font-bold mb-1">
                Hello, {user?.first_name}! 👋
              </h1>
              <p className="text-white/80">
                Ready to continue your learning journey?
              </p>
            </div>
            
            {/* Daily Check-in */}
            <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4 min-w-[200px]">
              <div className="flex items-center gap-2 mb-3">
                <Flame className="w-5 h-5 text-orange-300" />
                <span className="font-semibold">Daily Check-in</span>
              </div>
              <div className="flex items-center gap-3 mb-3">
                <span className="text-3xl font-bold">{checkInStatus?.streak || 0}</span>
                <span className="text-sm text-white/80">day streak</span>
              </div>
              <Button
                onClick={handleCheckIn}
                disabled={checkingIn || checkInStatus?.checked_in_today}
                className={`w-full ${
                  checkInStatus?.checked_in_today 
                    ? 'bg-white/30 text-white cursor-default' 
                    : 'bg-white text-[#095EB1] hover:bg-white/90'
                }`}
                data-testid="check-in-btn"
              >
                {checkInStatus?.checked_in_today ? (
                  <>
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Checked In!
                  </>
                ) : checkingIn ? (
                  'Checking in...'
                ) : (
                  <>
                    <Target className="w-4 h-4 mr-2" />
                    Check In
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>

        {/* Check-in Calendar */}
        <Card className="card-base mb-8">
          <CardContent className="p-4">
            <div className="flex items-center gap-4">
              <Calendar className="w-5 h-5 text-[#095EB1]" />
              <span className="font-medium text-slate-700">Last 7 Days</span>
              <div className="flex gap-2 ml-auto">
                {getLast7Days().map((date) => {
                  const isCheckedIn = checkInStatus?.check_ins?.includes(date);
                  const isToday = date === new Date().toISOString().split('T')[0];
                  return (
                    <div 
                      key={date} 
                      className={`w-10 h-10 rounded-lg flex flex-col items-center justify-center text-xs ${
                        isCheckedIn 
                          ? 'bg-gradient-to-br from-orange-400 to-red-500 text-white' 
                          : isToday 
                            ? 'bg-[#095EB1]/10 border-2 border-dashed border-[#095EB1] text-[#095EB1]'
                            : 'bg-slate-100 text-slate-400'
                      }`}
                    >
                      <span className="font-semibold">{new Date(date).getDate()}</span>
                      {isCheckedIn && <Flame className="w-3 h-3" />}
                    </div>
                  );
                })}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats Grid - Bento Style */}
        <div className="bento-grid mb-8">
          {/* Total Courses */}
          <div className="col-span-1 md:col-span-3">
            <Card className="card-base h-full bg-gradient-to-br from-blue-50 to-white border-blue-100">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-14 h-14 bg-gradient-to-br from-[#095EB1] to-[#0EA5E9] rounded-xl flex items-center justify-center shadow-lg shadow-blue-200">
                  <BookOpen className="w-7 h-7 text-white" />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Enrolled Courses</p>
                  <p className="text-3xl font-bold text-[#0F172A]">{enrolledCourses.length}</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* In Progress */}
          <div className="col-span-1 md:col-span-3">
            <Card className="card-base h-full bg-gradient-to-br from-cyan-50 to-white border-cyan-100">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-14 h-14 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-200">
                  <PlayCircle className="w-7 h-7 text-white" />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">In Progress</p>
                  <p className="text-3xl font-bold text-[#0F172A]">{inProgressCourses.length}</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Completed */}
          <div className="col-span-1 md:col-span-3">
            <Card className="card-base h-full bg-gradient-to-br from-emerald-50 to-white border-emerald-100">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-14 h-14 bg-gradient-to-br from-emerald-500 to-green-500 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-200">
                  <GraduationCap className="w-7 h-7 text-white" />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Completed</p>
                  <p className="text-3xl font-bold text-[#0F172A]">{completedCourses.length}</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Certificates */}
          <div className="col-span-1 md:col-span-3">
            <Card className="card-base h-full bg-gradient-to-br from-amber-50 to-white border-amber-100">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-14 h-14 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center shadow-lg shadow-amber-200">
                  <Award className="w-7 h-7 text-white" />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Certificates</p>
                  <p className="text-3xl font-bold text-[#0F172A]">{certificates.length}</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="bento-grid">
          {/* All Enrolled Courses with Progress - Larger Section */}
          <div className="col-span-1 md:col-span-8">
            <Card className="card-base">
              <CardHeader className="border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-semibold flex items-center gap-2">
                    <BookOpen className="w-5 h-5 text-[#095EB1]" />
                    My Enrolled Courses
                  </CardTitle>
                  <Link to="/courses">
                    <Button variant="ghost" size="sm" className="text-[#095EB1]" data-testid="view-all-courses">
                      View All <ChevronRight className="w-4 h-4 ml-1" />
                    </Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent className="p-6">
                {enrolledCourses.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="w-20 h-20 bg-gradient-to-br from-slate-100 to-slate-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
                      <BookOpen className="w-10 h-10 text-slate-400" />
                    </div>
                    <p className="text-slate-500 mb-4">No courses enrolled yet</p>
                    <Link to="/courses">
                      <Button className="bg-gradient-to-r from-[#095EB1] to-[#0EA5E9] hover:from-[#074A8C] hover:to-[#0284C7]" data-testid="browse-courses-btn">
                        Browse Courses
                      </Button>
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {enrolledCourses.map((course) => (
                      <Link 
                        key={course.id} 
                        to={`/courses/${course.id}`}
                        className="block"
                        data-testid={`course-card-${course.id}`}
                      >
                        <div className="p-4 border border-slate-200 rounded-xl hover:border-[#095EB1]/30 hover:shadow-lg hover:shadow-blue-100 transition-all group">
                          <div className="flex items-start gap-4">
                            <div className="w-20 h-14 bg-gradient-to-br from-[#095EB1]/10 to-[#0EA5E9]/10 rounded-lg overflow-hidden flex-shrink-0 flex items-center justify-center">
                              {course.thumbnail ? (
                                <img src={course.thumbnail} alt={course.title} className="w-full h-full object-cover" />
                              ) : (
                                <BookOpen className="w-6 h-6 text-[#095EB1]" />
                              )}
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                {course.course_type === 'compulsory' && (
                                  <Badge className="bg-red-100 text-red-700 text-xs">Required</Badge>
                                )}
                                {course.course_type === 'assigned' && (
                                  <Badge className="bg-purple-100 text-purple-700 text-xs">Assigned</Badge>
                                )}
                                <Badge className="bg-emerald-100 text-emerald-700 text-xs">
                                  <CheckCircle className="w-3 h-3 mr-1" />
                                  Enrolled
                                </Badge>
                              </div>
                              <h3 className="font-semibold text-[#0F172A] group-hover:text-[#095EB1] transition-colors truncate">
                                {course.title}
                              </h3>
                              <p className="text-sm text-slate-500 truncate">{course.description}</p>
                              <div className="mt-2 flex items-center gap-3">
                                <Progress value={course.progress} className="flex-1 h-2" />
                                <span className={`text-sm font-semibold ${course.progress >= 100 ? 'text-emerald-600' : 'text-[#095EB1]'}`}>
                                  {course.progress}%
                                </span>
                                {course.progress >= 100 && (
                                  <Badge className="bg-emerald-100 text-emerald-700 text-xs">
                                    <CheckCircle className="w-3 h-3 mr-1" />
                                    Completed
                                  </Badge>
                                )}
                              </div>
                            </div>
                            <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-[#095EB1] transition-colors" />
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Quick Stats Sidebar */}
          <div className="col-span-1 md:col-span-4 space-y-6">
            {/* Overall Progress */}
            <Card className="card-base overflow-hidden">
              <div className="h-2 bg-gradient-to-r from-[#095EB1] to-[#0EA5E9]" style={{ width: `${avgProgress}%` }} />
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-500">Overall Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-end gap-2 mb-3">
                  <span className="text-4xl font-bold bg-gradient-to-r from-[#095EB1] to-[#0EA5E9] bg-clip-text text-transparent">{avgProgress}%</span>
                  <span className="text-sm text-slate-500 mb-1">average</span>
                </div>
                <Progress value={avgProgress} className="h-3" />
              </CardContent>
            </Card>

            {/* Recent Certificates */}
            <Card className="card-base">
              <CardHeader className="border-b border-slate-100 bg-gradient-to-r from-amber-50 to-white">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Award className="w-4 h-4 text-amber-500" />
                    Recent Certificates
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent className="p-4">
                {certificates.length === 0 ? (
                  <p className="text-sm text-slate-500 text-center py-4">
                    Complete courses to earn certificates
                  </p>
                ) : (
                  <div className="space-y-3">
                    {certificates.slice(0, 3).map((cert) => (
                      <Link 
                        key={cert.id} 
                        to={`/certificates/${cert.id}`}
                        className="flex items-center gap-3 p-2 rounded-lg hover:bg-amber-50 transition-colors"
                        data-testid={`cert-${cert.id}`}
                      >
                        <div className="w-10 h-10 bg-gradient-to-br from-amber-400 to-orange-500 rounded-lg flex items-center justify-center">
                          <Award className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-[#0F172A] truncate">{cert.course_title}</p>
                          <p className="text-xs text-slate-500">
                            {new Date(cert.issued_at).toLocaleDateString()}
                          </p>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
                {certificates.length > 0 && (
                  <Link to="/certificates" className="block mt-3">
                    <Button variant="ghost" size="sm" className="w-full text-[#095EB1]" data-testid="view-all-certs">
                      View All Certificates
                    </Button>
                  </Link>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
}
