import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { courseApi } from '../../lib/api';
import { Card, CardContent } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { toast } from 'sonner';
import { 
  BookOpen, 
  Search,
  Clock,
  Users,
  ChevronRight,
  Filter,
  CheckCircle
} from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../components/ui/select';

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [enrolledIds, setEnrolledIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
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
      setEnrolledIds(enrolledRes.data.map(c => c.id));
    } catch (error) {
      console.error('Failed to fetch courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async (courseId, e) => {
    e.preventDefault();
    e.stopPropagation();
    setEnrollingId(courseId);
    
    try {
      await courseApi.enroll(courseId);
      setEnrolledIds([...enrolledIds, courseId]);
      toast.success('Successfully enrolled in course!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to enroll');
    } finally {
      setEnrollingId(null);
    }
  };

  const categories = [...new Set(courses.map(c => c.category).filter(Boolean))];
  
  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          course.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = categoryFilter === 'all' || course.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  if (loading) {
    return (
      <Layout>
        <div className="page-container">
          <Skeleton className="h-8 w-64 mb-8" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1,2,3,4,5,6].map(i => <Skeleton key={i} className="h-64" />)}
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page-container" data-testid="courses-page">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#0F172A] mb-2">Course Catalog</h1>
          <p className="text-slate-500">
            Explore our professional courses and start learning today.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input
              placeholder="Search courses..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
              data-testid="search-courses"
            />
          </div>
          <Select value={categoryFilter} onValueChange={setCategoryFilter}>
            <SelectTrigger className="w-full sm:w-48" data-testid="category-filter">
              <Filter className="w-4 h-4 mr-2" />
              <SelectValue placeholder="Category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              {categories.map(cat => (
                <SelectItem key={cat} value={cat}>{cat}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Course Grid */}
        {filteredCourses.length === 0 ? (
          <div className="text-center py-16">
            <BookOpen className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-slate-700 mb-2">No courses found</h3>
            <p className="text-slate-500">Try adjusting your search or filters.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCourses.map((course) => {
              const isEnrolled = enrolledIds.includes(course.id);
              
              return (
                <Link 
                  key={course.id} 
                  to={`/courses/${course.id}`}
                  data-testid={`course-${course.id}`}
                >
                  <Card className="card-base card-interactive h-full group">
                    {/* Thumbnail */}
                    <div className="aspect-video bg-slate-100 relative overflow-hidden">
                      {course.thumbnail ? (
                        <img 
                          src={course.thumbnail} 
                          alt={course.title} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-[#095EB1]/10 to-[#0EA5E9]/10">
                          <BookOpen className="w-12 h-12 text-[#095EB1]/40" />
                        </div>
                      )}
                      {course.category && (
                        <Badge className="absolute top-3 left-3 bg-white/90 text-[#095EB1] hover:bg-white">
                          {course.category}
                        </Badge>
                      )}
                      {isEnrolled && (
                        <Badge className="absolute top-3 right-3 bg-emerald-500 text-white">
                          <CheckCircle className="w-3 h-3 mr-1" />
                          Enrolled
                        </Badge>
                      )}
                    </div>

                    <CardContent className="p-5">
                      <h3 className="font-semibold text-lg text-[#0F172A] mb-2 group-hover:text-[#095EB1] transition-colors line-clamp-2">
                        {course.title}
                      </h3>
                      <p className="text-sm text-slate-500 mb-4 line-clamp-2">
                        {course.description}
                      </p>

                      {/* Meta info */}
                      <div className="flex items-center gap-4 text-sm text-slate-500 mb-4">
                        {course.duration_hours > 0 && (
                          <div className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            <span>{course.duration_hours}h</span>
                          </div>
                        )}
                        <div className="flex items-center gap-1">
                          <Users className="w-4 h-4" />
                          <span>{course.enrolled_users?.length || 0} enrolled</span>
                        </div>
                      </div>

                      {/* Action Button */}
                      {isEnrolled ? (
                        <Button 
                          className="w-full bg-[#095EB1] hover:bg-[#074A8C]"
                          data-testid={`continue-course-${course.id}`}
                        >
                          Continue Learning
                          <ChevronRight className="w-4 h-4 ml-2" />
                        </Button>
                      ) : (
                        <Button
                          className="w-full bg-slate-100 text-slate-700 hover:bg-[#095EB1] hover:text-white"
                          onClick={(e) => handleEnroll(course.id, e)}
                          disabled={enrollingId === course.id}
                          data-testid={`enroll-course-${course.id}`}
                        >
                          {enrollingId === course.id ? 'Enrolling...' : 'Enroll Now'}
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </Layout>
  );
}
