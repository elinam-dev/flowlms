import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { useAuth } from '../../context/AuthContext';
import { courseApi, certificateApi } from '../../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Progress } from '../../components/ui/progress';
import { Skeleton } from '../../components/ui/skeleton';
import { 
  BookOpen, 
  Award, 
  Clock, 
  TrendingUp, 
  ChevronRight,
  PlayCircle,
  GraduationCap
} from 'lucide-react';

export default function LearnerDashboard() {
  const { user } = useAuth();
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [coursesRes, certsRes] = await Promise.all([
        courseApi.getEnrolled(),
        certificateApi.getAll()
      ]);
      setEnrolledCourses(coursesRes.data);
      setCertificates(certsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const completedCourses = enrolledCourses.filter(c => c.progress >= 100);
  const inProgressCourses = enrolledCourses.filter(c => c.progress > 0 && c.progress < 100);
  const avgProgress = enrolledCourses.length > 0 
    ? Math.round(enrolledCourses.reduce((acc, c) => acc + c.progress, 0) / enrolledCourses.length)
    : 0;

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
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#0F172A] mb-2">
            Welcome back, {user?.first_name}!
          </h1>
          <p className="text-slate-500">
            Continue your learning journey and track your progress.
          </p>
        </div>

        {/* Stats Grid - Bento Style */}
        <div className="bento-grid mb-8">
          {/* Total Courses */}
          <div className="col-span-1 md:col-span-3">
            <Card className="card-base h-full">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-14 h-14 bg-[#095EB1]/10 rounded-xl flex items-center justify-center">
                  <BookOpen className="w-7 h-7 text-[#095EB1]" />
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
            <Card className="card-base h-full">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-14 h-14 bg-[#0EA5E9]/10 rounded-xl flex items-center justify-center">
                  <PlayCircle className="w-7 h-7 text-[#0EA5E9]" />
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
            <Card className="card-base h-full">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-14 h-14 bg-emerald-50 rounded-xl flex items-center justify-center">
                  <GraduationCap className="w-7 h-7 text-emerald-600" />
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
            <Card className="card-base h-full">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-14 h-14 bg-amber-50 rounded-xl flex items-center justify-center">
                  <Award className="w-7 h-7 text-amber-600" />
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
          {/* Continue Learning - Larger Section */}
          <div className="col-span-1 md:col-span-8">
            <Card className="card-base">
              <CardHeader className="border-b border-slate-100 bg-slate-50/50">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-semibold flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-[#095EB1]" />
                    Continue Learning
                  </CardTitle>
                  <Link to="/courses">
                    <Button variant="ghost" size="sm" className="text-[#095EB1]" data-testid="view-all-courses">
                      View All <ChevronRight className="w-4 h-4 ml-1" />
                    </Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent className="p-6">
                {inProgressCourses.length === 0 ? (
                  <div className="text-center py-12">
                    <BookOpen className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                    <p className="text-slate-500 mb-4">No courses in progress</p>
                    <Link to="/courses">
                      <Button className="bg-[#095EB1] hover:bg-[#074A8C]" data-testid="browse-courses-btn">
                        Browse Courses
                      </Button>
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {inProgressCourses.slice(0, 3).map((course) => (
                      <Link 
                        key={course.id} 
                        to={`/courses/${course.id}`}
                        className="block"
                        data-testid={`course-card-${course.id}`}
                      >
                        <div className="p-4 border border-slate-200 rounded-lg hover:border-[#095EB1]/30 hover:shadow-md transition-all group">
                          <div className="flex items-start gap-4">
                            <div className="w-20 h-14 bg-slate-100 rounded-md overflow-hidden flex-shrink-0">
                              {course.thumbnail ? (
                                <img src={course.thumbnail} alt={course.title} className="w-full h-full object-cover" />
                              ) : (
                                <div className="w-full h-full flex items-center justify-center">
                                  <BookOpen className="w-6 h-6 text-slate-400" />
                                </div>
                              )}
                            </div>
                            <div className="flex-1 min-w-0">
                              <h3 className="font-semibold text-[#0F172A] group-hover:text-[#095EB1] transition-colors truncate">
                                {course.title}
                              </h3>
                              <p className="text-sm text-slate-500 truncate">{course.description}</p>
                              <div className="mt-2 flex items-center gap-3">
                                <Progress value={course.progress} className="flex-1 h-2" />
                                <span className="text-sm font-medium text-[#095EB1]">{course.progress}%</span>
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
            <Card className="card-base">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-500">Overall Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-end gap-2 mb-3">
                  <span className="text-4xl font-bold text-[#095EB1]">{avgProgress}%</span>
                  <span className="text-sm text-slate-500 mb-1">average</span>
                </div>
                <Progress value={avgProgress} className="h-3" />
              </CardContent>
            </Card>

            {/* Recent Certificates */}
            <Card className="card-base">
              <CardHeader className="border-b border-slate-100 bg-slate-50/50">
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
                        className="flex items-center gap-3 p-2 rounded-md hover:bg-slate-50 transition-colors"
                        data-testid={`cert-${cert.id}`}
                      >
                        <Award className="w-8 h-8 text-amber-500" />
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
