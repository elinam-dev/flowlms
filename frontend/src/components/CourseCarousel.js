import { useCallback, useEffect, useState } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './ui/button';
import { CourseCard } from './CourseCard';

export const CourseCarousel = ({ 
  courses, 
  enrolledCourses = [], 
  onEnroll, 
  enrollingId,
  title,
  subtitle,
  showViewAll = true,
  onViewAll
}) => {
  const [emblaRef, emblaApi] = useEmblaCarousel({
    align: 'start',
    containScroll: 'trimSnaps',
    slidesToScroll: 1,
    dragFree: true,
  });

  const [prevBtnEnabled, setPrevBtnEnabled] = useState(false);
  const [nextBtnEnabled, setNextBtnEnabled] = useState(false);

  const scrollPrev = useCallback(() => emblaApi && emblaApi.scrollPrev(), [emblaApi]);
  const scrollNext = useCallback(() => emblaApi && emblaApi.scrollNext(), [emblaApi]);

  const onSelect = useCallback(() => {
    if (!emblaApi) return;
    setPrevBtnEnabled(emblaApi.canScrollPrev());
    setNextBtnEnabled(emblaApi.canScrollNext());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    onSelect();
    emblaApi.on('select', onSelect);
    emblaApi.on('reInit', onSelect);
  }, [emblaApi, onSelect]);

  const getEnrolledCourse = (courseId) => {
    return enrolledCourses.find(c => c.id === courseId);
  };

  if (!courses || courses.length === 0) return null;

  return (
    <div className="relative" data-testid="course-carousel">
      {/* Header */}
      {(title || subtitle) && (
        <div className="flex items-end justify-between mb-6">
          <div>
            {title && (
              <h2 className="text-2xl font-bold text-slate-900 tracking-tight">{title}</h2>
            )}
            {subtitle && (
              <p className="text-slate-500 mt-1">{subtitle}</p>
            )}
          </div>
          <div className="flex items-center gap-2">
            {/* Navigation Buttons */}
            <Button
              variant="outline"
              size="icon"
              onClick={scrollPrev}
              disabled={!prevBtnEnabled}
              className="h-10 w-10 rounded-full border-slate-200 hover:bg-slate-100 disabled:opacity-30 disabled:cursor-not-allowed"
              data-testid="carousel-prev"
            >
              <ChevronLeft className="h-5 w-5" />
            </Button>
            <Button
              variant="outline"
              size="icon"
              onClick={scrollNext}
              disabled={!nextBtnEnabled}
              className="h-10 w-10 rounded-full border-slate-200 hover:bg-slate-100 disabled:opacity-30 disabled:cursor-not-allowed"
              data-testid="carousel-next"
            >
              <ChevronRight className="h-5 w-5" />
            </Button>
          </div>
        </div>
      )}

      {/* Carousel Container */}
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex gap-6 touch-pan-y">
          {courses.map((course) => (
            <div 
              key={course.id} 
              className="flex-none w-[280px] sm:w-[300px] lg:w-[320px]"
            >
              <CourseCard
                course={course}
                enrolledCourse={getEnrolledCourse(course.id)}
                onEnroll={onEnroll}
                enrollingId={enrollingId}
              />
            </div>
          ))}
        </div>
      </div>

      {/* View All Link */}
      {showViewAll && onViewAll && courses.length > 4 && (
        <div className="mt-6 text-center">
          <Button
            variant="outline"
            onClick={onViewAll}
            className="text-[#095EB1] border-[#095EB1] hover:bg-[#095EB1]/5"
            data-testid="view-all-courses"
          >
            View All Courses
            <ChevronRight className="w-4 h-4 ml-1" />
          </Button>
        </div>
      )}
    </div>
  );
};

export default CourseCarousel;
