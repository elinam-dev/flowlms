import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { toast } from 'sonner';
import { Loader2, Mail, Lock, ArrowRight } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const user = await login(email, password);
      toast.success(`Welcome back, ${user.first_name}!`);
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
      <div className="flex-1 flex items-center justify-center p-8 bg-white">
        <div className="w-full max-w-md">
          {/* Logo */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-[#095EB1] rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-xl">F</span>
              </div>
              <div>
                <span className="font-semibold text-[#0F172A] text-xl">Flowitec</span>
                <span className="text-[#095EB1] font-bold ml-1 text-xl">Go & Grow</span>
              </div>
            </div>
            <p className="text-slate-500 text-sm mt-1">Learning Management System</p>
          </div>

          <Card className="border-0 shadow-none">
            <CardHeader className="px-0">
              <CardTitle className="text-2xl font-bold text-[#0F172A]">Welcome back</CardTitle>
              <CardDescription className="text-slate-500">
                Sign in to continue your learning journey
              </CardDescription>
            </CardHeader>
            <CardContent className="px-0">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-slate-700">Email</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="you@company.com"
                      className="pl-10"
                      required
                      data-testid="login-email"
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-slate-700">Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      id="password"
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter your password"
                      className="pl-10"
                      required
                      data-testid="login-password"
                    />
                  </div>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-[#095EB1] hover:bg-[#074A8C] h-11"
                  disabled={loading}
                  data-testid="login-submit"
                >
                  {loading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <>
                      Sign In
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </>
                  )}
                </Button>
              </form>

              <div className="mt-6 text-center">
                <p className="text-sm text-slate-500">
                  Don't have an account?{' '}
                  <Link to="/register" className="text-[#095EB1] hover:underline font-medium" data-testid="register-link">
                    Create account
                  </Link>
                </p>
              </div>

              {/* Demo credentials */}
              <div className="mt-8 p-4 bg-slate-50 rounded-lg border border-slate-200">
                <p className="text-xs font-medium text-slate-700 mb-2">Demo Credentials:</p>
                <div className="space-y-1 text-xs text-slate-600">
                  <p><span className="font-medium">Admin:</span> admin@flowitec.com / admin123</p>
                </div>
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
          className="absolute inset-0 w-full h-full object-cover opacity-60"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-[#095EB1]/80 to-slate-900/90" />
        <div className="relative z-10 flex flex-col justify-end p-12 text-white">
          <h2 className="text-4xl font-bold mb-4">Empower Your Team</h2>
          <p className="text-lg text-white/80 max-w-md">
            Flowitec Go & Grow provides comprehensive training solutions for engineers, 
            technicians, and corporate professionals.
          </p>
        </div>
      </div>
    </div>
  );
}
