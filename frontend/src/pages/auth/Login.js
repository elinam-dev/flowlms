import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { toast } from 'sonner';
import { Loader2, User, Lock, ArrowRight, Sparkles } from 'lucide-react';

export default function Login() {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const user = await login(identifier, password);
      
      // Show welcome back toast with animation
      toast.success(
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-[#095EB1] to-[#0EA5E9] rounded-full flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="font-semibold">Welcome back, {user.first_name}!</p>
            <p className="text-sm text-slate-500">Ready to continue learning?</p>
          </div>
        </div>,
        { duration: 4000 }
      );
      
      navigate(user.role === 'admin' ? '/admin' : '/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex" data-testid="login-page">
      {/* Left side - Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-white relative overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-[#095EB1]/5 rounded-full blur-3xl animate-pulse" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-[#0EA5E9]/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        </div>
        
        <div className="w-full max-w-md relative z-10">
          {/* Logo */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-20 h-20 flex items-center justify-center">
                <img 
                  src="/images/flowitec-logo.png" 
                  alt="Flowitec Logo" 
                  className="w-20 h-20 object-contain"
                />
              </div>
              <div>
                <span className="font-bold text-[#0F172A] text-2xl">Flowitec</span>
                <span className="text-[#095EB1] font-bold ml-1 text-2xl">Go & Grow</span>
              </div>
            </div>
            <p className="text-slate-500 text-sm mt-2">Learning Management System</p>
          </div>

          <Card className="border-0 shadow-none">
            <CardHeader className="px-0">
              <CardTitle className="text-3xl font-bold text-[#0F172A]">Welcome back</CardTitle>
              <CardDescription className="text-slate-500 text-base">
                Sign in with your Employee ID or Email
              </CardDescription>
            </CardHeader>
            <CardContent className="px-0">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label htmlFor="identifier" className="text-slate-700 font-medium">Employee ID or Email</Label>
                  <div className="relative group">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-[#095EB1] transition-colors" />
                    <Input
                      id="identifier"
                      type="text"
                      value={identifier}
                      onChange={(e) => setIdentifier(e.target.value)}
                      placeholder="EMP-001 or you@company.com"
                      className="pl-11 h-12 text-base border-slate-200 focus:border-[#095EB1] focus:ring-[#095EB1]"
                      required
                      data-testid="login-identifier"
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-slate-700 font-medium">Password</Label>
                  <div className="relative group">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-[#095EB1] transition-colors" />
                    <Input
                      id="password"
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter your password"
                      className="pl-11 h-12 text-base border-slate-200 focus:border-[#095EB1] focus:ring-[#095EB1]"
                      required
                      data-testid="login-password"
                    />
                  </div>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-gradient-to-r from-[#095EB1] to-[#0EA5E9] hover:from-[#074A8C] hover:to-[#0284C7] h-12 text-base font-semibold shadow-lg shadow-[#095EB1]/25 transition-all hover:shadow-xl hover:shadow-[#095EB1]/30"
                  disabled={loading}
                  data-testid="login-submit"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>
                      Sign In
                      <ArrowRight className="w-5 h-5 ml-2" />
                    </>
                  )}
                </Button>
              </form>

              <div className="mt-8 p-4 bg-gradient-to-r from-slate-50 to-slate-100 rounded-xl border border-slate-200">
                <p className="text-xs font-semibold text-slate-600 mb-2 flex items-center gap-2">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
                  Need an account?
                </p>
                <p className="text-xs text-slate-500">
                  Contact your administrator to create an account for you.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Right side - Image */}
      <div className="hidden lg:flex flex-1 relative bg-slate-900">
        <img
          src="https://images.pexels.com/photos/380768/pexels-photo-380768.jpeg"
          alt="Corporate office"
          className="absolute inset-0 w-full h-full object-cover opacity-50"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-[#095EB1]/90 via-[#095EB1]/70 to-slate-900/95" />
        
        {/* Floating elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-20 right-20 w-32 h-32 border border-white/20 rounded-2xl rotate-12 animate-float" />
          <div className="absolute bottom-40 left-20 w-24 h-24 border border-white/20 rounded-2xl -rotate-12 animate-float" style={{ animationDelay: '0.5s' }} />
          <div className="absolute top-1/2 right-40 w-16 h-16 bg-white/10 rounded-xl rotate-45 animate-float" style={{ animationDelay: '1s' }} />
        </div>
        
        <div className="relative z-10 flex flex-col justify-end p-12 text-white">
          <div className="mb-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full mb-6">
              <Sparkles className="w-4 h-4" />
              <span className="text-sm font-medium">Corporate Training Platform</span>
            </div>
          </div>
          <h2 className="text-5xl font-bold mb-4 leading-tight">
            Empower Your<br />
            <span className="text-[#0EA5E9]">Team's Growth</span>
          </h2>
          <p className="text-lg text-white/80 max-w-md leading-relaxed">
            Flowitec Go & Grow provides comprehensive training solutions for engineers, 
            technicians, and corporate professionals.
          </p>
        </div>
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0) rotate(var(--rotate, 12deg)); }
          50% { transform: translateY(-20px) rotate(var(--rotate, 12deg)); }
        }
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}
