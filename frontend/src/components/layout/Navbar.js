import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../ui/dropdown-menu';
import { User, LogOut, Settings, BookOpen, Award, LayoutDashboard, Menu, X } from 'lucide-react';
import { useState } from 'react';

export const Navbar = () => {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navLinks = isAdmin() ? [
    { href: '/admin', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/admin/courses', label: 'Courses', icon: BookOpen },
    { href: '/admin/users', label: 'Users', icon: User },
  ] : [
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/courses', label: 'Courses', icon: BookOpen },
    { href: '/certificates', label: 'Certificates', icon: Award },
  ];

  const isActive = (path) => location.pathname === path || location.pathname.startsWith(path + '/');

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-50" data-testid="navbar">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to={isAdmin() ? '/admin' : '/dashboard'} className="flex items-center gap-3" data-testid="navbar-logo">
            <div className="w-10 h-10 bg-[#095EB1] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">F</span>
            </div>
            <div className="hidden sm:block">
              <span className="font-semibold text-[#0F172A] text-lg">Flowitec</span>
              <span className="text-[#095EB1] font-bold ml-1">Go & Grow</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className={`nav-link ${isActive(link.href) ? 'nav-link-active' : ''}`}
                data-testid={`nav-${link.label.toLowerCase()}`}
              >
                <link.icon className="w-4 h-4" />
                <span>{link.label}</span>
              </Link>
            ))}
          </div>

          {/* User Menu */}
          <div className="flex items-center gap-3">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="flex items-center gap-2" data-testid="user-menu-trigger">
                  <div className="w-8 h-8 bg-slate-100 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-slate-600" />
                  </div>
                  <span className="hidden sm:block text-sm font-medium text-slate-700">
                    {user?.first_name} {user?.last_name}
                  </span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <div className="px-2 py-1.5">
                  <p className="text-sm font-medium">{user?.first_name} {user?.last_name}</p>
                  <p className="text-xs text-slate-500">{user?.email}</p>
                  <p className="text-xs text-[#095EB1] mt-0.5 capitalize">{user?.role}</p>
                </div>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => navigate('/profile')} data-testid="menu-profile">
                  <Settings className="w-4 h-4 mr-2" />
                  Profile Settings
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="text-red-600" data-testid="menu-logout">
                  <LogOut className="w-4 h-4 mr-2" />
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Mobile menu button */}
            <button
              className="md:hidden p-2 rounded-md hover:bg-slate-100"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              data-testid="mobile-menu-toggle"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden py-3 border-t border-slate-100 animate-slide-up">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className={`nav-link ${isActive(link.href) ? 'nav-link-active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <link.icon className="w-4 h-4" />
                <span>{link.label}</span>
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};
