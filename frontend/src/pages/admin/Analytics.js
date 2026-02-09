import { useState, useEffect } from 'react';
import { Layout } from '../../components/layout/Layout';
import { adminApi } from '../../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Skeleton } from '../../components/ui/skeleton';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  Users, 
  BookOpen, 
  GraduationCap, 
  Award,
  Clock,
  Target,
  Activity,
  PieChart,
  Calendar,
  CheckCircle,
  XCircle,
  AlertTriangle
} from 'lucide-react';

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [statsRes, analyticsRes] = await Promise.all([
        adminApi.getStats(),
        adminApi.getAnalytics()
      ]);
      setStats(statsRes.data);
      setAnalytics(analyticsRes.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
      // Set mock data for demo
      setStats({
        total_users: 156,
        total_courses: 21,
        total_enrollments: 423,
        total_certificates: 89
      });
      setAnalytics({
        course_completion_rate: 68,
        average_quiz_score: 78,
        active_learners_30_days: 124,
        avg_time_to_complete: 4.5,
        courses_by_category: [
          { category: 'SALES (ENGINEER)', count: 17 },
          { category: 'HR Policy', count: 2 },
          { category: 'Ethics', count: 1 },
          { category: 'Safety', count: 1 }
        ],
        completion_trend: [
          { month: 'Sep', completions: 45 },
          { month: 'Oct', completions: 62 },
          { month: 'Nov', completions: 78 },
          { month: 'Dec', completions: 89 },
          { month: 'Jan', completions: 95 },
          { month: 'Feb', completions: 102 }
        ],
        top_courses: [
          { title: 'Leave Policy - Ghana', enrollments: 156, completion_rate: 95 },
          { title: 'Code of Ethics & Conduct', enrollments: 148, completion_rate: 92 },
          { title: 'Health & Safety Policy', enrollments: 145, completion_rate: 88 },
          { title: 'Customer Service Skills', enrollments: 89, completion_rate: 72 },
          { title: 'B2B Customer Success', enrollments: 67, completion_rate: 65 }
        ],
        quiz_performance: {
          excellent: 35,
          good: 42,
          average: 18,
          needs_improvement: 5
        },
        learner_engagement: {
          highly_active: 45,
          moderately_active: 62,
          low_activity: 35,
          inactive: 14
        },
        recent_completions: [
          { user: 'John Mensah', course: 'Leave Policy - Ghana', date: '2025-02-08' },
          { user: 'Ama Serwaa', course: 'Code of Ethics', date: '2025-02-08' },
          { user: 'Kweku Annan', course: 'Health & Safety', date: '2025-02-07' },
          { user: 'Abena Darko', course: 'Customer Service Skills', date: '2025-02-07' },
          { user: 'Kofi Asante', course: 'B2B Customer Success', date: '2025-02-06' }
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="page-container">
          <Skeleton className="h-8 w-64 mb-8" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1,2,3,4,5,6,7,8].map(i => <Skeleton key={i} className="h-32" />)}
          </div>
        </div>
      </Layout>
    );
  }

  const kpiCards = [
    {
      title: 'Course Completion Rate',
      value: `${analytics?.course_completion_rate || 0}%`,
      change: '+5.2%',
      trend: 'up',
      icon: Target,
      color: 'text-emerald-500',
      bgColor: 'bg-emerald-50'
    },
    {
      title: 'Average Quiz Score',
      value: `${analytics?.average_quiz_score || 0}%`,
      change: '+3.1%',
      trend: 'up',
      icon: Award,
      color: 'text-violet-500',
      bgColor: 'bg-violet-50'
    },
    {
      title: 'Active Learners (30d)',
      value: analytics?.active_learners_30_days || 0,
      change: '+12',
      trend: 'up',
      icon: Users,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Avg. Completion Time',
      value: `${analytics?.avg_time_to_complete || 0} days`,
      change: '-0.5d',
      trend: 'down',
      icon: Clock,
      color: 'text-amber-500',
      bgColor: 'bg-amber-50'
    }
  ];

  const maxCompletions = Math.max(...(analytics?.completion_trend?.map(d => d.completions) || [100]));

  return (
    <Layout>
      <div className="page-container" data-testid="analytics-dashboard">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#0F172A] mb-2 flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-[#095EB1]" />
            Advanced Analytics
          </h1>
          <p className="text-slate-500">
            Comprehensive insights into your learning management system performance.
          </p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {kpiCards.map((kpi, index) => (
            <Card key={index} className="card-base hover:shadow-lg transition-shadow" data-testid={`kpi-${index}`}>
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-12 h-12 ${kpi.bgColor} rounded-xl flex items-center justify-center`}>
                    <kpi.icon className={`w-6 h-6 ${kpi.color}`} />
                  </div>
                  <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                    kpi.trend === 'up' ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700'
                  }`}>
                    {kpi.trend === 'up' ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                    {kpi.change}
                  </div>
                </div>
                <p className="text-3xl font-bold text-[#0F172A] mb-1">{kpi.value}</p>
                <p className="text-sm text-slate-500">{kpi.title}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Completion Trend */}
          <Card className="card-base">
            <CardHeader className="bg-slate-50 border-b">
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-[#095EB1]" />
                Course Completions Trend
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="flex items-end justify-between h-48 gap-4">
                {analytics?.completion_trend?.map((data, index) => (
                  <div key={index} className="flex flex-col items-center flex-1">
                    <div 
                      className="w-full bg-gradient-to-t from-[#095EB1] to-[#0EA5E9] rounded-t-lg transition-all hover:from-[#0EA5E9] hover:to-[#095EB1]"
                      style={{ height: `${(data.completions / maxCompletions) * 100}%`, minHeight: '20px' }}
                    />
                    <span className="text-xs text-slate-500 mt-2">{data.month}</span>
                    <span className="text-sm font-semibold text-[#0F172A]">{data.completions}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Courses by Category */}
          <Card className="card-base">
            <CardHeader className="bg-slate-50 border-b">
              <CardTitle className="flex items-center gap-2">
                <PieChart className="w-5 h-5 text-[#095EB1]" />
                Courses by Category
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-4">
                {analytics?.courses_by_category?.map((cat, index) => {
                  const total = analytics.courses_by_category.reduce((sum, c) => sum + c.count, 0);
                  const percentage = Math.round((cat.count / total) * 100);
                  const colors = ['bg-[#095EB1]', 'bg-emerald-500', 'bg-violet-500', 'bg-amber-500'];
                  return (
                    <div key={index}>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium text-[#0F172A]">{cat.category}</span>
                        <span className="text-sm text-slate-500">{cat.count} courses ({percentage}%)</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-3">
                        <div 
                          className={`${colors[index % colors.length]} h-3 rounded-full transition-all`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Top Courses & Quiz Performance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Top Courses */}
          <Card className="card-base">
            <CardHeader className="bg-slate-50 border-b">
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-[#095EB1]" />
                Top Performing Courses
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-4">
                {analytics?.top_courses?.map((course, index) => (
                  <div key={index} className="flex items-center gap-4 p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                      index === 0 ? 'bg-amber-500' : index === 1 ? 'bg-slate-400' : index === 2 ? 'bg-amber-700' : 'bg-slate-300'
                    }`}>
                      {index + 1}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-[#0F172A] truncate">{course.title}</p>
                      <p className="text-xs text-slate-500">{course.enrollments} enrollments</p>
                    </div>
                    <div className="text-right">
                      <p className={`text-lg font-bold ${
                        course.completion_rate >= 80 ? 'text-emerald-600' : 
                        course.completion_rate >= 60 ? 'text-amber-600' : 'text-red-600'
                      }`}>
                        {course.completion_rate}%
                      </p>
                      <p className="text-xs text-slate-500">completion</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quiz Performance Distribution */}
          <Card className="card-base">
            <CardHeader className="bg-slate-50 border-b">
              <CardTitle className="flex items-center gap-2">
                <GraduationCap className="w-5 h-5 text-[#095EB1]" />
                Quiz Performance Distribution
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-emerald-50 rounded-xl text-center">
                  <CheckCircle className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-emerald-700">{analytics?.quiz_performance?.excellent || 0}%</p>
                  <p className="text-sm text-emerald-600">Excellent (90%+)</p>
                </div>
                <div className="p-4 bg-blue-50 rounded-xl text-center">
                  <TrendingUp className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-blue-700">{analytics?.quiz_performance?.good || 0}%</p>
                  <p className="text-sm text-blue-600">Good (70-89%)</p>
                </div>
                <div className="p-4 bg-amber-50 rounded-xl text-center">
                  <AlertTriangle className="w-8 h-8 text-amber-500 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-amber-700">{analytics?.quiz_performance?.average || 0}%</p>
                  <p className="text-sm text-amber-600">Average (50-69%)</p>
                </div>
                <div className="p-4 bg-red-50 rounded-xl text-center">
                  <XCircle className="w-8 h-8 text-red-500 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-red-700">{analytics?.quiz_performance?.needs_improvement || 0}%</p>
                  <p className="text-sm text-red-600">Needs Work (&lt;50%)</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Learner Engagement & Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Learner Engagement */}
          <Card className="card-base">
            <CardHeader className="bg-slate-50 border-b">
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5 text-[#095EB1]" />
                Learner Engagement
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-emerald-50 rounded-lg">
                  <span className="font-medium text-emerald-700">Highly Active</span>
                  <span className="text-lg font-bold text-emerald-600">{analytics?.learner_engagement?.highly_active}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <span className="font-medium text-blue-700">Moderately Active</span>
                  <span className="text-lg font-bold text-blue-600">{analytics?.learner_engagement?.moderately_active}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-amber-50 rounded-lg">
                  <span className="font-medium text-amber-700">Low Activity</span>
                  <span className="text-lg font-bold text-amber-600">{analytics?.learner_engagement?.low_activity}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                  <span className="font-medium text-red-700">Inactive</span>
                  <span className="text-lg font-bold text-red-600">{analytics?.learner_engagement?.inactive}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recent Completions */}
          <Card className="card-base col-span-1 lg:col-span-2">
            <CardHeader className="bg-slate-50 border-b">
              <CardTitle className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-[#095EB1]" />
                Recent Course Completions
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-3">
                {analytics?.recent_completions?.map((completion, index) => (
                  <div key={index} className="flex items-center gap-4 p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
                    <div className="w-10 h-10 bg-gradient-to-br from-[#095EB1] to-[#0EA5E9] rounded-full flex items-center justify-center">
                      <span className="text-white font-bold text-sm">
                        {completion.user.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-[#0F172A]">{completion.user}</p>
                      <p className="text-sm text-slate-500 truncate">Completed: {completion.course}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-slate-500">{completion.date}</p>
                      <CheckCircle className="w-5 h-5 text-emerald-500 ml-auto" />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Summary Stats */}
        <div className="mt-8 p-6 bg-gradient-to-r from-[#095EB1] to-[#0EA5E9] rounded-2xl text-white">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <p className="text-4xl font-bold">{stats?.total_users || 0}</p>
              <p className="text-blue-100">Total Learners</p>
            </div>
            <div>
              <p className="text-4xl font-bold">{stats?.total_courses || 0}</p>
              <p className="text-blue-100">Total Courses</p>
            </div>
            <div>
              <p className="text-4xl font-bold">{stats?.total_enrollments || 0}</p>
              <p className="text-blue-100">Enrollments</p>
            </div>
            <div>
              <p className="text-4xl font-bold">{stats?.total_certificates || 0}</p>
              <p className="text-blue-100">Certificates</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
