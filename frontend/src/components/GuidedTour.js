import { useEffect } from 'react';
import { driver } from 'driver.js';
import 'driver.js/dist/driver.css';

export default function GuidedTour({ run, onFinish }) {
  useEffect(() => {
    if (!run) return;

    const driverObj = driver({
      showProgress: true,
      animate: true,
      overlayOpacity: 0.6,
      smoothScroll: true,
      allowClose: true,
      progressText: '{{current}} of {{total}}',
      nextBtnText: 'Next →',
      prevBtnText: '← Back',
      doneBtnText: 'Done!',
      onDestroyStarted: () => {
        driverObj.destroy();
        onFinish?.();
      },
      steps: [
        {
          element: '[data-tour="greeting"]',
          popover: {
            title: '👋 Welcome to Flowitec Go & Grow!',
            description: 'This is your personal learning dashboard. Everything you need to grow professionally is right here. Let us show you around!',
            side: 'bottom',
            align: 'start',
          },
        },
        {
          element: '[data-tour="checkin"]',
          popover: {
            title: '🔥 Daily Check-In',
            description: 'Click "Check In Now" every day you log in to build your streak. The more consistent you are, the higher your streak grows!',
            side: 'left',
            align: 'start',
          },
        },
        {
          element: '[data-tour="streak-calendar"]',
          popover: {
            title: '📅 Your Streak Calendar',
            description: 'This shows your check-in history for the last 7 days. Orange flames mean you checked in that day. Keep the streak alive!',
            side: 'bottom',
            align: 'start',
          },
        },
        {
          element: '[data-tour="stats"]',
          popover: {
            title: '📊 Your Learning Stats',
            description: 'Track how many courses you are enrolled in, how many are in progress, completed, and how many certificates you have earned.',
            side: 'bottom',
            align: 'start',
          },
        },
        {
          element: '[data-tour="enrolled-courses"]',
          popover: {
            title: '📚 My Enrolled Courses',
            description: 'All your enrolled courses appear here. Click any course to open it and start or continue learning. Courses marked "Required" must be completed.',
            side: 'top',
            align: 'start',
          },
        },
        {
          element: '[data-tour="overall-progress"]',
          popover: {
            title: '📈 Overall Progress',
            description: 'This shows your average progress across all enrolled courses. Keep completing lessons to push this number up!',
            side: 'left',
            align: 'start',
          },
        },
        {
          element: '[data-tour="certificates"]',
          popover: {
            title: '🏆 Certificates',
            description: 'When you complete 100% of a course, you automatically earn a certificate. You can download it as a PDF to share with your employer or on LinkedIn.',
            side: 'left',
            align: 'start',
          },
        },
        {
          element: '[data-tour="nav-courses"]',
          popover: {
            title: '🔍 Browse All Courses',
            description: 'Click here to explore the full course catalog. You can browse by category and enroll in any course that interests you.',
            side: 'bottom',
            align: 'start',
          },
        },
        {
          element: '[data-tour="nav-career"]',
          popover: {
            title: '🪲 Career Beetle',
            description: 'The Career Beetle shows your career progression path within the company — the roles, skills, and qualifications needed to advance.',
            side: 'bottom',
            align: 'start',
          },
        },
        {
          element: '[data-tour="nav-certificates"]',
          popover: {
            title: '🎓 Certificates Page',
            description: 'All your earned certificates live here. Click any certificate to view or download it as a PDF.',
            side: 'bottom',
            align: 'start',
          },
        },
      ],
    });

    // Small delay to ensure DOM is ready
    setTimeout(() => driverObj.drive(), 300);

    return () => driverObj.destroy();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [run]);

  return null;
}
