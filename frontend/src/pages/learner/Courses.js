import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { courseApi } from '../../lib/api';
import { CourseCard } from '../../components/CourseCard';
import { CourseCarousel } from '../../components/CourseCarousel';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { Tabs, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { toast } from 'sonner';
import { 
  Search,
  BookOpen,
  Award,
  GraduationCap,
  Sparkles,
  Users,
  TrendingUp,
  Clock,
  ChevronRight,
  Filter
} from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../components/ui/select';

export default function Courses() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [enrollingId, setEnrollingId] = useState(null);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const [allCoursesRes, enrolledRes] = await Promise.all([
        courseApi.getAll(),
        courseApi.getEnrolled()
      ]);
      setCourses(allCoursesRes.data);
      setEnrolledCourses(enrolledRes.data);
    } catch (error) {
      console.error('Failed to fetch courses:', error);
    } finally {
      setLoading(false);
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

  const handleSearch = (e) => {
    e.preventDefault();
    // Search is already reactive
  };

  // Get unique categories
  const categories = [...new Set(courses.map(c => c.category).filter(Boolean))];

  // Filter courses based on active tab and search
  const getFilteredCourses = () => {
    let filtered = courses;

    // Apply search filter
    if (searchQuery) {
      filtered = filtered.filter(course =>
        course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        course.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        course.category?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Apply category filter
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(course => course.category === categoryFilter);
    }

    return filtered;
  };

  // Get courses by category for tab filtering
  const getTabCourses = () => {
    const filtered = getFilteredCourses();
    
    switch (activeTab) {
      case 'popular':
        return filtered.sort((a, b) => (b.enrolled_users?.length || 0) - (a.enrolled_users?.length || 0));
      case 'required':
        return filtered.filter(c => c.course_type === 'compulsory');
      case 'optional':
        return filtered.filter(c => c.course_type === 'optional' || c.course_type === 'assigned');
      case 'enrolled':
        return filtered.filter(c => enrolledCourses.some(ec => ec.id === c.id));
      default:
        return filtered;
    }
  };

  // Group courses by category for carousels
  const getCoursesByCategory = () => {
    const grouped = {};
    courses.forEach(course => {
      const cat = course.category || 'Other';
      if (!grouped[cat]) grouped[cat] = [];
      grouped[cat].push(course);
    });
    return grouped;
  };

  // Stats
  const totalLearners = courses.reduce((acc, c) => acc + (c.enrolled_users?.length || 0), 0);
  const completedCount = enrolledCourses.filter(c => c.progress >= 100).length;

  const filteredCourses = getTabCourses();
  const coursesByCategory = getCoursesByCategory();

  if (loading) {
    return (
      <Layout>
        <div className="hero-pattern py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <Skeleton className="h-12 w-96 mb-4" />
            <Skeleton className="h-6 w-64 mb-8" />
            <Skeleton className="h-14 w-full max-w-2xl" />
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1,2,3,4,5,6,7,8].map(i => <Skeleton key={i} className="h-80 rounded-xl" />)}
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div data-testid="courses-page">
        {/* Hero Section - Alison Style */}
        <section className="hero-pattern py-16 lg:py-20 relative overflow-hidden">
          {/* Background decorations */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-[#095EB1]/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-[#0EA5E9]/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
          
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Left Content */}
              <div className="animate-fade-up">
                <Badge className="bg-[#095EB1]/10 text-[#095EB1] mb-4 py-1.5 px-3">
                  <Sparkles className="w-3.5 h-3.5 mr-1.5" />
                  Professional Development
                </Badge>
                <h1 className="text-4xl md:text-5xl font-bold text-slate-900 tracking-tight mb-4 leading-tight">
                  Explore Our<br />
                  <span className="text-[#095EB1]">Training Courses</span>
                </h1>
                <p className="text-lg text-slate-600 mb-8 max-w-lg">
                  Enhance your skills with our comprehensive corporate training programs. 
                  Learn at your own pace and earn certificates.
                </p>

                {/* Search Bar */}
                <form onSubmit={handleSearch} className="relative max-w-xl">
                  <div className="flex gap-2">
                    <div className="relative flex-1">
                      <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                      <Input
                        type="text"
                        placeholder="What do you want to learn today?"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-12 h-14 text-base rounded-xl border-slate-200 shadow-sm focus:ring-2 focus:ring-[#095EB1]/20 focus:border-[#095EB1]"
                        data-testid="search-courses"
                      />
                    </div>
                    <Button 
                      type="submit"
                      className="h-14 px-8 bg-[#095EB1] hover:bg-[#074A8C] rounded-xl font-semibold shadow-lg shadow-[#095EB1]/25"
                      data-testid="search-btn"
                    >
                      Search
                    </Button>
                  </div>
                </form>

                {/* Quick Stats */}
                <div className="flex items-center gap-8 mt-8 pt-8 border-t border-slate-200">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-[#095EB1]/10 rounded-lg flex items-center justify-center">
                      <BookOpen className="w-5 h-5 text-[#095EB1]" />
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-slate-900">{courses.length}</p>
                      <p className="text-sm text-slate-500">Courses</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
                      <Users className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-slate-900">{totalLearners.toLocaleString()}</p>
                      <p className="text-sm text-slate-500">Enrollments</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
                      <Award className="w-5 h-5 text-amber-600" />
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-slate-900">{completedCount}</p>
                      <p className="text-sm text-slate-500">Completed</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right - Featured Image */}
              <div className="hidden lg:block animate-fade-up stagger-2">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-br from-[#095EB1]/20 to-[#0EA5E9]/20 rounded-2xl transform rotate-3" />
                  <img 
                    src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&h=400&fit=crop"
                    alt="Team learning"
                    className="relative rounded-2xl shadow-2xl w-full object-cover"
                  />
                  {/* Floating card */}
                  <div className="absolute -bottom-6 -left-6 bg-white rounded-xl shadow-xl p-4 animate-fade-up stagger-3">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center">
                        <TrendingUp className="w-6 h-6 text-emerald-600" />
                      </div>
                      <div>
                        <p className="font-bold text-slate-900">Track Progress</p>
                        <p className="text-sm text-slate-500">Learn at your pace</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Category Tabs - Alison Style */}
        <section className="border-b border-slate-200 bg-white sticky top-16 z-40">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between py-4">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="bg-transparent h-auto p-0 gap-1">
                  <TabsTrigger 
                    value="all" 
                    className="px-4 py-2.5 rounded-full data-[state=active]:bg-[#095EB1] data-[state=active]:text-white data-[state=active]:shadow-md font-medium transition-all"
                    data-testid="tab-all"
                  >
                    All Courses
                  </TabsTrigger>
                  <TabsTrigger 
                    value="popular" 
                    className="px-4 py-2.5 rounded-full data-[state=active]:bg-[#095EB1] data-[state=active]:text-white data-[state=active]:shadow-md font-medium transition-all"
                    data-testid="tab-popular"
                  >
                    <TrendingUp className="w-4 h-4 mr-1.5" />
                    Popular
                  </TabsTrigger>
                  <TabsTrigger 
                    value="required" 
                    className="px-4 py-2.5 rounded-full data-[state=active]:bg-[#095EB1] data-[state=active]:text-white data-[state=active]:shadow-md font-medium transition-all"
                    data-testid="tab-required"
                  >
                    <GraduationCap className="w-4 h-4 mr-1.5" />
                    Required
                  </TabsTrigger>
                  <TabsTrigger 
                    value="optional" 
                    className="px-4 py-2.5 rounded-full data-[state=active]:bg-[#095EB1] data-[state=active]:text-white data-[state=active]:shadow-md font-medium transition-all"
                    data-testid="tab-optional"
                  >
                    <BookOpen className="w-4 h-4 mr-1.5" />
                    Optional
                  </TabsTrigger>
                  <TabsTrigger 
                    value="enrolled" 
                    className="px-4 py-2.5 rounded-full data-[state=active]:bg-[#095EB1] data-[state=active]:text-white data-[state=active]:shadow-md font-medium transition-all"
                    data-testid="tab-enrolled"
                  >
                    <Award className="w-4 h-4 mr-1.5" />
                    My Courses
                  </TabsTrigger>
                </TabsList>
              </Tabs>

              {/* Category Filter */}
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger className="w-48 ml-4" data-testid="category-filter">
                  <Filter className="w-4 h-4 mr-2" />
                  <SelectValue placeholder="All Categories" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  {categories.map(cat => (
                    <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </section>

        {/* Course Content */}
        <section className="py-12 bg-slate-50/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Show carousels on "All" tab without search */}
            {activeTab === 'all' && !searchQuery && categoryFilter === 'all' ? (
              <div className="space-y-16">
                {/* Popular Courses Carousel */}
                <CourseCarousel
                  title="Popular Courses"
                  subtitle="Most enrolled courses by our learners"
                  courses={courses.sort((a, b) => (b.enrolled_users?.length || 0) - (a.enrolled_users?.length || 0)).slice(0, 8)}
                  enrolledCourses={enrolledCourses}
                  onEnroll={handleEnroll}
                  enrollingId={enrollingId}
                  showViewAll={false}
                />

                {/* Required Courses */}
                {courses.filter(c => c.course_type === 'compulsory').length > 0 && (
                  <CourseCarousel
                    title="Required Courses"
                    subtitle="Complete these courses to maintain compliance"
                    courses={courses.filter(c => c.course_type === 'compulsory')}
                    enrolledCourses={enrolledCourses}
                    onEnroll={handleEnroll}
                    enrollingId={enrollingId}
                    showViewAll={false}
                  />
                )}

                {/* Courses by Category */}
                {Object.entries(coursesByCategory).map(([category, categoryCourses]) => (
                  <CourseCarousel
                    key={category}
                    title={category}
                    subtitle={`${categoryCourses.length} courses available`}
                    courses={categoryCourses}
                    enrolledCourses={enrolledCourses}
                    onEnroll={handleEnroll}
                    enrollingId={enrollingId}
                    showViewAll={false}
                  />
                ))}
              </div>
            ) : (
              /* Grid View for filtered/searched results */
              <div>
                <div className="flex items-center justify-between mb-8">
                  <div>
                    <h2 className="text-2xl font-bold text-slate-900">
                      {activeTab === 'enrolled' ? 'My Enrolled Courses' : 
                       activeTab === 'required' ? 'Required Courses' :
                       activeTab === 'optional' ? 'Optional Courses' :
                       activeTab === 'popular' ? 'Popular Courses' : 'All Courses'}
                    </h2>
                    <p className="text-slate-500 mt-1">
                      {filteredCourses.length} course{filteredCourses.length !== 1 ? 's' : ''} found
                    </p>
                  </div>
                </div>

                {filteredCourses.length === 0 ? (
                  <div className="text-center py-20 bg-white rounded-2xl border border-slate-200">
                    <div className="w-20 h-20 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                      <BookOpen className="w-10 h-10 text-slate-400" />
                    </div>
                    <h3 className="text-xl font-semibold text-slate-700 mb-2">No courses found</h3>
                    <p className="text-slate-500 mb-6 max-w-md mx-auto">
                      {searchQuery 
                        ? `No courses match "${searchQuery}". Try a different search term.`
                        : 'No courses available in this category yet.'}
                    </p>
                    <Button 
                      variant="outline"
                      onClick={() => { setSearchQuery(''); setActiveTab('all'); setCategoryFilter('all'); }}
                      data-testid="clear-filters"
                    >
                      Clear Filters
                    </Button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {filteredCourses.map((course) => (
                      <CourseCard
                        key={course.id}
                        course={course}
                        enrolledCourse={enrolledCourses.find(c => c.id === course.id)}
                        onEnroll={handleEnroll}
                        enrollingId={enrollingId}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-gradient-to-r from-[#095EB1] to-[#074A8C]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to start your learning journey?
            </h2>
            <p className="text-white/80 mb-8 max-w-2xl mx-auto">
              Enroll in courses today and take your career to the next level with our 
              professional development programs.
            </p>
            <div className="flex items-center justify-center gap-4">
              <Button 
                className="bg-white text-[#095EB1] hover:bg-slate-100 font-semibold px-8 h-12 rounded-xl"
                onClick={() => setActiveTab('all')}
                data-testid="browse-all-cta"
              >
                Browse All Courses
              </Button>
              <Link to="/dashboard">
                <Button 
                  variant="outline" 
                  className="border-white/30 text-white hover:bg-white/10 font-semibold px-8 h-12 rounded-xl"
                  data-testid="go-dashboard-cta"
                >
                  Go to Dashboard
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
}
