import { useState, useEffect } from 'react';
import { Layout } from '../../components/layout/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import axios from 'axios';
import { toast } from 'sonner';
import { 
  TrendingUp, 
  Users, 
  Briefcase, 
  GraduationCap,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  Target,
  Clock,
  Award,
  Building2,
  Sparkles,
  ArrowRight,
  CheckCircle
} from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '../../components/ui/collapsible';

const API = process.env.REACT_APP_BACKEND_URL ? `${process.env.REACT_APP_BACKEND_URL}/api` : '/api';

// Department icons mapping
const departmentIcons = {
  sales: Briefcase,
  supply_chain: TrendingUp,
  finance: Building2,
  hr: Users,
  facilities: Building2
};

// Level colors
const levelColors = {
  'Entry level': 'bg-emerald-100 text-emerald-700',
  'Intermediate': 'bg-blue-100 text-blue-700',
  'Mid level': 'bg-cyan-100 text-cyan-700',
  'First Level': 'bg-purple-100 text-purple-700',
  'Senior Mgt.': 'bg-amber-100 text-amber-700',
  'Senior Level': 'bg-red-100 text-red-700'
};

export default function CareerBeetle() {
  const [careerData, setCareerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedDept, setSelectedDept] = useState(null);
  const [expandedRoles, setExpandedRoles] = useState({});

  useEffect(() => {
    fetchCareerData();
  }, []);

  const fetchCareerData = async () => {
    try {
      const token = localStorage.getItem('flowitec_token');
      const response = await axios.get(`${API}/career-beetle`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCareerData(response.data);
      if (response.data.departments?.length > 0) {
        setSelectedDept(response.data.departments[0]);
      }
    } catch (error) {
      console.error('Failed to fetch career data:', error);
      toast.error('Failed to load career data');
    } finally {
      setLoading(false);
    }
  };

  const toggleRole = (roleId) => {
    setExpandedRoles(prev => ({
      ...prev,
      [roleId]: !prev[roleId]
    }));
  };

  const getLevelIndex = (level) => {
    const levels = ['Entry level', 'Intermediate', 'Mid level', 'First Level', 'Senior Mgt.', 'Senior Level'];
    return levels.indexOf(level);
  };

  if (loading) {
    return (
      <Layout>
        <div className="hero-pattern py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <Skeleton className="h-12 w-64 mb-4" />
            <Skeleton className="h-6 w-96 mb-8" />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1,2,3,4,5,6].map(i => <Skeleton key={i} className="h-40 rounded-xl" />)}
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div data-testid="career-beetle-page">
        {/* Hero Section */}
        <section className="hero-pattern py-16 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-[#095EB1]/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-amber-500/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
          
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <Badge className="bg-amber-100 text-amber-700 mb-4 py-1.5 px-3">
              <Sparkles className="w-3.5 h-3.5 mr-1.5" />
              Career Development
            </Badge>
            <h1 className="text-4xl md:text-5xl font-bold text-slate-900 tracking-tight mb-4">
              Career <span className="text-amber-600">Beetle</span>
            </h1>
            <p className="text-lg text-slate-600 max-w-2xl">
              Explore your career progression path at Flowitec. Discover the skills, qualifications, 
              and timelines needed to advance in your chosen career track.
            </p>

            {/* Quick Stats */}
            <div className="flex flex-wrap gap-6 mt-8">
              <div className="flex items-center gap-3 bg-white/80 backdrop-blur-sm rounded-xl px-4 py-3 shadow-sm">
                <div className="w-10 h-10 bg-[#095EB1]/10 rounded-lg flex items-center justify-center">
                  <Building2 className="w-5 h-5 text-[#095EB1]" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">{careerData?.departments?.length || 0}</p>
                  <p className="text-sm text-slate-500">Departments</p>
                </div>
              </div>
              <div className="flex items-center gap-3 bg-white/80 backdrop-blur-sm rounded-xl px-4 py-3 shadow-sm">
                <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
                  <Briefcase className="w-5 h-5 text-amber-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">
                    {careerData?.departments?.reduce((acc, d) => acc + (d.roles?.length || 0), 0) || 0}
                  </p>
                  <p className="text-sm text-slate-500">Career Roles</p>
                </div>
              </div>
              <div className="flex items-center gap-3 bg-white/80 backdrop-blur-sm rounded-xl px-4 py-3 shadow-sm">
                <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-5 h-5 text-emerald-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">6</p>
                  <p className="text-sm text-slate-500">Career Levels</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Department Selection */}
        <section className="border-b border-slate-200 bg-white sticky top-16 z-40">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex overflow-x-auto scrollbar-hide py-4 gap-2">
              {careerData?.departments?.map((dept) => {
                const Icon = departmentIcons[dept.id] || Building2;
                return (
                  <Button
                    key={dept.id}
                    variant={selectedDept?.id === dept.id ? "default" : "outline"}
                    className={`flex-shrink-0 rounded-full h-11 px-5 ${
                      selectedDept?.id === dept.id 
                        ? 'bg-[#095EB1] text-white' 
                        : 'hover:bg-slate-100'
                    }`}
                    onClick={() => setSelectedDept(dept)}
                    data-testid={`dept-${dept.id}`}
                  >
                    <Icon className="w-4 h-4 mr-2" />
                    {dept.name}
                  </Button>
                );
              })}
            </div>
          </div>
        </section>

        {/* Career Path Content */}
        <section className="py-12 bg-slate-50/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {selectedDept && (
              <div className="space-y-8">
                {/* Department Header */}
                <div className="text-center">
                  <h2 className="text-3xl font-bold text-slate-900 mb-2">{selectedDept.name}</h2>
                  <p className="text-slate-500">
                    {selectedDept.roles?.length || 0} career positions • Click on a role to see details
                  </p>
                </div>

                {/* Career Ladder Visualization */}
                <div className="relative">
                  {/* Vertical Line */}
                  <div className="absolute left-1/2 top-0 bottom-0 w-1 bg-gradient-to-b from-emerald-500 via-[#095EB1] to-amber-500 transform -translate-x-1/2 hidden lg:block" />

                  {/* Roles */}
                  <div className="space-y-6">
                    {selectedDept.roles?.sort((a, b) => getLevelIndex(b.level) - getLevelIndex(a.level)).map((role, index) => {
                      const isExpanded = expandedRoles[role.id];
                      const isLeftSide = index % 2 === 0;
                      
                      return (
                        <div 
                          key={role.id} 
                          className={`flex ${isLeftSide ? 'lg:flex-row' : 'lg:flex-row-reverse'} items-center gap-4`}
                        >
                          {/* Role Card */}
                          <div className={`flex-1 max-w-xl ${isLeftSide ? 'lg:text-right' : 'lg:text-left'}`}>
                            <Collapsible open={isExpanded} onOpenChange={() => toggleRole(role.id)}>
                              <CollapsibleTrigger asChild>
                                <Card 
                                  className={`cursor-pointer transition-all hover:shadow-lg hover:-translate-y-1 border-slate-200 ${
                                    isExpanded ? 'ring-2 ring-[#095EB1] shadow-lg' : ''
                                  }`}
                                  data-testid={`role-card-${role.id}`}
                                >
                                  <CardContent className="p-6">
                                    <div className={`flex items-start gap-4 ${isLeftSide ? 'lg:flex-row-reverse' : ''}`}>
                                      <div className={`flex-1 ${isLeftSide ? 'lg:text-right' : ''}`}>
                                        <Badge className={`mb-2 ${levelColors[role.level] || 'bg-slate-100 text-slate-700'}`}>
                                          {role.level}
                                        </Badge>
                                        <h3 className="text-xl font-bold text-slate-900 mb-2">{role.title}</h3>
                                        <div className={`flex items-center gap-4 text-sm text-slate-500 ${isLeftSide ? 'lg:justify-end' : ''}`}>
                                          {role.timeline && role.timeline !== 'N/A' && (
                                            <span className="flex items-center gap-1">
                                              <Clock className="w-4 h-4" />
                                              {role.timeline}
                                            </span>
                                          )}
                                        </div>
                                      </div>
                                      <div className={`${isExpanded ? 'rotate-180' : ''} transition-transform`}>
                                        <ChevronDown className="w-5 h-5 text-slate-400" />
                                      </div>
                                    </div>
                                  </CardContent>
                                </Card>
                              </CollapsibleTrigger>
                              
                              <CollapsibleContent>
                                <Card className="mt-2 bg-slate-50 border-slate-200">
                                  <CardContent className="p-6 space-y-4">
                                    <div>
                                      <h4 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                                        <Target className="w-4 h-4 text-[#095EB1]" />
                                        Key Skills & Development Focus
                                      </h4>
                                      <p className="text-slate-600">{role.key_skills}</p>
                                    </div>
                                    <div>
                                      <h4 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                                        <GraduationCap className="w-4 h-4 text-[#095EB1]" />
                                        Qualifications Required
                                      </h4>
                                      <p className="text-slate-600">{role.qualifications}</p>
                                    </div>
                                    {role.timeline && role.timeline !== 'N/A' && (
                                      <div>
                                        <h4 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                                          <Clock className="w-4 h-4 text-[#095EB1]" />
                                          Expected Timeline
                                        </h4>
                                        <p className="text-slate-600">{role.timeline} in this position before advancement</p>
                                      </div>
                                    )}
                                  </CardContent>
                                </Card>
                              </CollapsibleContent>
                            </Collapsible>
                          </div>

                          {/* Center Dot (Desktop) */}
                          <div className="hidden lg:flex items-center justify-center w-8">
                            <div className={`w-4 h-4 rounded-full border-4 border-white shadow-lg ${
                              getLevelIndex(role.level) >= 4 
                                ? 'bg-amber-500' 
                                : getLevelIndex(role.level) >= 2 
                                  ? 'bg-[#095EB1]' 
                                  : 'bg-emerald-500'
                            }`} />
                          </div>

                          {/* Spacer for alternating layout */}
                          <div className="hidden lg:block flex-1 max-w-xl" />
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Career Levels Legend */}
                <Card className="mt-12 border-slate-200">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Award className="w-5 h-5 text-amber-500" />
                      Career Levels at Flowitec
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                      {['Entry level', 'Intermediate', 'Mid level', 'First Level', 'Senior Mgt.', 'Senior Level'].map((level, index) => (
                        <div key={level} className="text-center">
                          <div className={`w-12 h-12 rounded-xl ${levelColors[level] || 'bg-slate-100'} flex items-center justify-center mx-auto mb-2`}>
                            <span className="font-bold text-lg">{index + 1}</span>
                          </div>
                          <p className="text-sm font-medium text-slate-700">{level}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-gradient-to-r from-amber-500 to-orange-500">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to advance your career?
            </h2>
            <p className="text-white/90 mb-8 max-w-2xl mx-auto">
              Talk to your manager or HR about your career aspirations and create a personalized 
              development plan to reach your goals.
            </p>
            <Button 
              className="bg-white text-amber-600 hover:bg-white/90 font-semibold px-8 h-12 rounded-xl"
              onClick={() => window.location.href = '/courses'}
            >
              Start Learning
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </section>
      </div>
    </Layout>
  );
}
