import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { courseApi } from '../../lib/api';
import { Card, CardContent } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { Progress } from '../../components/ui/progress';
import { toast } from 'sonner';
import { 
  BookOpen, 
  Search,
  Clock,
  Users,
  ChevronRight,
  Filter,
  CheckCircle,
  Award
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
  const [enrolledCourses, setEnrolledCourses] = useState([]);
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
      setEnrolledCourses(enrolledRes.data);
    } catch (error) {
      console.error('Failed to fetch courses:', error);
    } finally {
      setLoading(false);
    }
  };

  // Helper to get enrolled course with progress
  const getEnrolledCourse = (courseId) => {
    return enrolledCourses.find(c => c.id === courseId);
  };

  const handleEnroll = async (courseId, e) => {
    e.preventDefault();
    e.stopPropagation();
    setEnrollingId(courseId);
    
    try {
      await courseApi.enroll(courseId);
      // Refresh enrolled courses to get progress data
      const enrolledRes = await courseApi.getEnrolled();
      setEnrolledCourses(enrolledRes.data);
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
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-slate-900 mb-2">Course Catalog</h1>
          <p className="text-slate-600">
            Explore our professional courses and start learning today.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {filteredCourses.map((course) => {
              const enrolledCourse = getEnrolledCourse(course.id);
              const isEnrolled = !!enrolledCourse;
              const progress = enrolledCourse?.progress || 0;
              const isCompleted = progress >= 100;
              
              return (
                <Link 
                  key={course.id} 
                  to={`/courses/${course.id}`}
                  data-testid={`course-${course.id}`}
                >
                  <Card className={`border border-slate-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow duration-200 h-full group ${isCompleted ? 'border-emerald-200' : ''}`}>
                    {/* Thumbnail */}
                    <div className="aspect-video bg-slate-100 relative overflow-hidden">
                      {course.thumbnail ? (
                        <img 
                          src={course.thumbnail} 
                          alt={course.title} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      ) : (
                        <div className={`w-full h-full flex items-center justify-center ${
                          isCompleted 
                            ? 'bg-gradient-to-br from-emerald-100 to-emerald-200' 
                            : 'bg-gradient-to-br from-[#095EB1]/10 to-[#0EA5E9]/10'
                        }`}>
                          {isCompleted ? (
                            <Award className="w-12 h-12 text-emerald-500" />
                          ) : (
                            <BookOpen className="w-12 h-12 text-[#095EB1]/40" />
                          )}
                        </div>
                      )}
                      {course.category && (
                        <Badge className="absolute top-3 left-3 bg-white/90 text-[#095EB1] hover:bg-white">
                          {course.category}
                        </Badge>
                      )}
                      {isCompleted ? (
                        <Badge className="absolute top-3 right-3 bg-emerald-500 text-white">
                          <CheckCircle className="w-3 h-3 mr-1" />
                          Completed
                        </Badge>
                      ) : isEnrolled ? (
                        <Badge className="absolute top-3 right-3 bg-blue-500 text-white">
                          <BookOpen className="w-3 h-3 mr-1" />
                          Enrolled
                        </Badge>
                      ) : null}
                    </div>

                    <CardContent className="p-4">
                      <h3 className="font-semibold text-base text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">
                        {course.title}
                      </h3>
                      
                      {/* Course Type Badge */}
                      <div className="flex items-center gap-2 mb-3">
                        {course.course_type === 'compulsory' && (
                          <Badge className="bg-red-100 text-red-700 text-xs">Required</Badge>
                        )}
                        {course.course_type === 'assigned' && (
                          <Badge className="bg-purple-100 text-purple-700 text-xs">Assigned</Badge>
                        )}
                        {course.category && (
                          <Badge className="bg-slate-100 text-slate-600 text-xs">{course.category}</Badge>
                        )}
                      </div>

                      {/* Progress bar for enrolled courses */}
                      {isEnrolled && (
                        <div className="mb-3">
                          <div className="flex items-center justify-between text-xs mb-1">
                            <span className="text-slate-500">Progress</span>
                            <span className={`font-semibold ${isCompleted ? 'text-emerald-600' : 'text-[#095EB1]'}`}>
                              {progress}%
                            </span>
                          </div>
                          <Progress 
                            value={progress} 
                            className={`h-1.5 ${isCompleted ? '[&>div]:bg-emerald-500' : ''}`} 
                          />
                        </div>
                      )}

                      {/* Meta info */}
                      <div className="flex items-center gap-3 text-xs text-slate-500 mb-3">
                        {course.duration_hours > 0 && (
                          <div className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            <span>{course.duration_hours}h</span>
                          </div>
                        )}
                        <div className="flex items-center gap-1">
                          <Users className="w-3 h-3" />
                          <span>{course.enrolled_users?.length || 0}</span>
                        </div>
                      </div>

                      {/* Action Button */}
                      {isCompleted ? (
                        <Button 
                          className="w-full bg-emerald-500 hover:bg-emerald-600 text-white text-sm py-2"
                          data-testid={`completed-course-${course.id}`}
                        >
                          <CheckCircle className="w-4 h-4 mr-2" />
                          Completed
                        </Button>
                      ) : isEnrolled ? (
                        <Button 
                          className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm py-2"
                          data-testid={`continue-course-${course.id}`}
                        >
                          Continue
                          <ChevronRight className="w-4 h-4 ml-2" />
                        </Button>
                      ) : (
                        <Button
                          className="w-full bg-green-600 hover:bg-green-700 text-white text-sm py-2"
                          onClick={(e) => handleEnroll(course.id, e)}
                          disabled={enrollingId === course.id}
                          data-testid={`enroll-course-${course.id}`}
                        >
                          {enrollingId === course.id ? 'Enrolling...' : 'Enroll Free'}
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
