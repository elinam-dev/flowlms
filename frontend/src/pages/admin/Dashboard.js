import { useState, useEffect } from 'react';
import { Layout } from '../../components/layout/Layout';
import { adminApi } from '../../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Skeleton } from '../../components/ui/skeleton';
import { 
  Users, 
  BookOpen, 
  GraduationCap, 
  Award,
  TrendingUp,
  Activity
} from 'lucide-react';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await adminApi.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
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
            {[1,2,3,4].map(i => <Skeleton key={i} className="h-32" />)}
          </div>
        </div>
      </Layout>
    );
  }

  const statCards = [
    {
      title: 'Total Learners',
      value: stats?.total_users || 0,
      icon: Users,
      color: 'bg-blue-500',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Total Courses',
      value: stats?.total_courses || 0,
      icon: BookOpen,
      color: 'bg-emerald-500',
      bgColor: 'bg-emerald-50'
    },
    {
      title: 'Total Enrollments',
      value: stats?.total_enrollments || 0,
      icon: GraduationCap,
      color: 'bg-violet-500',
      bgColor: 'bg-violet-50'
    },
    {
      title: 'Certificates Issued',
      value: stats?.total_certificates || 0,
      icon: Award,
      color: 'bg-amber-500',
      bgColor: 'bg-amber-50'
    }
  ];

  return (
    <Layout>
      <div className="page-container" data-testid="admin-dashboard">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#0F172A] mb-2">Admin Dashboard</h1>
          <p className="text-slate-500">
            Overview of your learning management system.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat, index) => (
            <Card key={index} className="card-base" data-testid={`stat-${stat.title.toLowerCase().replace(' ', '-')}`}>
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm text-slate-500 font-medium mb-1">{stat.title}</p>
                    <p className="text-3xl font-bold text-[#0F172A]">{stat.value}</p>
                  </div>
                  <div className={`w-12 h-12 ${stat.bgColor} rounded-xl flex items-center justify-center`}>
                    <stat.icon className={`w-6 h-6 ${stat.color.replace('bg-', 'text-')}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="bento-grid">
          <Card className="col-span-1 md:col-span-8 card-base">
            <CardHeader className="bg-slate-50 border-b">
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5 text-[#095EB1]" />
                Quick Actions
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <a 
                  href="/admin/courses" 
                  className="p-4 bg-slate-50 rounded-lg hover:bg-[#095EB1]/10 transition-colors group"
                  data-testid="quick-action-courses"
                >
                  <BookOpen className="w-8 h-8 text-[#095EB1] mb-3" />
                  <h3 className="font-semibold text-[#0F172A] group-hover:text-[#095EB1]">Manage Courses</h3>
                  <p className="text-sm text-slate-500">Create and edit courses</p>
                </a>
                <a 
                  href="/admin/users" 
                  className="p-4 bg-slate-50 rounded-lg hover:bg-[#095EB1]/10 transition-colors group"
                  data-testid="quick-action-users"
                >
                  <Users className="w-8 h-8 text-[#095EB1] mb-3" />
                  <h3 className="font-semibold text-[#0F172A] group-hover:text-[#095EB1]">Manage Users</h3>
                  <p className="text-sm text-slate-500">View and manage learners</p>
                </a>
                <a 
                  href="/admin/courses" 
                  className="p-4 bg-slate-50 rounded-lg hover:bg-[#095EB1]/10 transition-colors group"
                  data-testid="quick-action-assign"
                >
                  <TrendingUp className="w-8 h-8 text-[#095EB1] mb-3" />
                  <h3 className="font-semibold text-[#0F172A] group-hover:text-[#095EB1]">Track Progress</h3>
                  <p className="text-sm text-slate-500">Monitor learner progress</p>
                </a>
              </div>
            </CardContent>
          </Card>

          <Card className="col-span-1 md:col-span-4 card-base">
            <CardHeader className="bg-slate-50 border-b">
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-[#095EB1]" />
                System Health
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center justify-between p-3 bg-emerald-50 rounded-lg">
                <span className="text-sm font-medium text-emerald-700">Database</span>
                <span className="text-sm text-emerald-600">Connected</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-emerald-50 rounded-lg">
                <span className="text-sm font-medium text-emerald-700">API</span>
                <span className="text-sm text-emerald-600">Operational</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-emerald-50 rounded-lg">
                <span className="text-sm font-medium text-emerald-700">Storage</span>
                <span className="text-sm text-emerald-600">Available</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
