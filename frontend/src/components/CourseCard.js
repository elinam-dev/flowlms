import { Link } from 'react-router-dom';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { 
  Clock, 
  Users, 
  BookOpen, 
  CheckCircle, 
  Award,
  ThumbsUp,
  ChevronRight
} from 'lucide-react';

export const CourseCard = ({ 
  course, 
  enrolledCourse, 
  onEnroll, 
  enrollingId,
  showActions = true,
  variant = 'default' // default, compact, featured
}) => {
  const isEnrolled = !!enrolledCourse;
  const progress = enrolledCourse?.progress || 0;
  const isCompleted = progress >= 100;

  // Get course thumbnail or fallback
  const getThumbnail = () => {
    if (course.thumbnail) return course.thumbnail;
    // Category-based fallback images
    const categoryImages = {
      'International Trade': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=225&fit=crop',
      'Ethics': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&h=225&fit=crop',
      'HR Policy': 'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=400&h=225&fit=crop',
      'Safety': 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=400&h=225&fit=crop',
    };
    return categoryImages[course.category] || 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=225&fit=crop';
  };

  const handleEnrollClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (onEnroll) onEnroll(course.id, e);
  };

  return (
    <div 
      className="group relative bg-white rounded-xl border border-slate-200 overflow-hidden transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl hover:shadow-slate-200/50 h-full flex flex-col"
      data-testid={`course-card-${course.id}`}
    >
      {/* Image Container */}
      <div className="relative aspect-[16/9] overflow-hidden bg-slate-100">
        <img 
          src={getThumbnail()}
          alt={course.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Top Badges */}
        <div className="absolute top-3 left-3 flex flex-wrap gap-2">
          {course.course_type === 'compulsory' && (
            <Badge className="bg-red-500 text-white text-xs font-medium px-2 py-1">
              Required
            </Badge>
          )}
          {course.category && (
            <Badge className="bg-white/95 text-slate-700 text-xs font-medium px-2 py-1 backdrop-blur-sm">
              {course.category}
            </Badge>
          )}
        </div>

        {/* Status Badge */}
        {isCompleted && (
          <Badge className="absolute top-3 right-3 bg-emerald-500 text-white text-xs font-medium px-2 py-1">
            <CheckCircle className="w-3 h-3 mr-1" />
            Completed
          </Badge>
        )}

        {/* Hover Overlay with Actions */}
        {showActions && (
          <div className="absolute inset-0 flex items-end justify-center p-4 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-4 group-hover:translate-y-0">
            <div className="flex gap-2 w-full">
              <Link 
                to={`/courses/${course.id}`}
                className="flex-1"
                onClick={(e) => e.stopPropagation()}
              >
                <Button 
                  variant="outline" 
                  className="w-full bg-white/95 backdrop-blur-sm border-0 text-slate-700 hover:bg-white font-semibold text-sm h-10"
                  data-testid={`more-info-${course.id}`}
                >
                  More Info
                </Button>
              </Link>
              {isCompleted ? (
                <Link to={`/courses/${course.id}`} className="flex-1">
                  <Button 
                    className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-semibold text-sm h-10"
                    data-testid={`review-${course.id}`}
                  >
                    <Award className="w-4 h-4 mr-1" />
                    Review
                  </Button>
                </Link>
              ) : isEnrolled ? (
                <Link to={`/courses/${course.id}`} className="flex-1">
                  <Button 
                    className="w-full bg-[#095EB1] hover:bg-[#074A8C] text-white font-semibold text-sm h-10"
                    data-testid={`continue-${course.id}`}
                  >
                    Continue
                    <ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                </Link>
              ) : (
                <Button 
                  className="flex-1 bg-[#095EB1] hover:bg-[#074A8C] text-white font-semibold text-sm h-10"
                  onClick={handleEnrollClick}
                  disabled={enrollingId === course.id}
                  data-testid={`start-learning-${course.id}`}
                >
                  {enrollingId === course.id ? 'Enrolling...' : 'Start Learning'}
                </Button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col">
        {/* Level Badge */}
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs font-medium text-slate-500 uppercase tracking-wide">
            {course.course_type === 'compulsory' ? 'Required Course' : 'Optional Course'}
          </span>
        </div>

        {/* Title */}
        <h3 className="font-bold text-base text-slate-900 mb-2 line-clamp-2 group-hover:text-[#095EB1] transition-colors">
          {course.title}
        </h3>

        {/* Progress Bar (if enrolled) */}
        {isEnrolled && (
          <div className="mb-3">
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="text-slate-500">Progress</span>
              <span className={`font-bold ${isCompleted ? 'text-emerald-600' : 'text-[#095EB1]'}`}>
                {progress}%
              </span>
            </div>
            <Progress 
              value={progress} 
              className={`h-1.5 ${isCompleted ? '[&>div]:bg-emerald-500' : ''}`} 
            />
          </div>
        )}

        {/* Stats Row */}
        <div className="flex items-center gap-4 text-xs text-slate-500 mt-auto pt-3 border-t border-slate-100">
          {course.duration_hours > 0 && (
            <div className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5" />
              <span>{course.duration_hours}h</span>
            </div>
          )}
          <div className="flex items-center gap-1">
            <Users className="w-3.5 h-3.5" />
            <span>{(course.enrolled_users?.length || 0).toLocaleString()} learners</span>
          </div>
          {course.likes && (
            <div className="flex items-center gap-1">
              <ThumbsUp className="w-3.5 h-3.5" />
              <span>{course.likes}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CourseCard;
