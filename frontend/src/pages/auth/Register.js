import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { toast } from 'sonner';
import { Loader2, Mail, Lock, User, Building, ArrowRight } from 'lucide-react';

export default function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    employee_id: ''
  });
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const user = await register(formData);
      toast.success(`Welcome to Flowitec Go & Grow, ${user.first_name}!`);
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex" data-testid="register-page">
      {/* Left side - Image */}
      <div className="hidden lg:flex flex-1 relative bg-slate-900">
        <img
          src="https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg"
          alt="Technology"
          className="absolute inset-0 w-full h-full object-cover opacity-60"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-[#095EB1]/80 to-slate-900/90" />
        <div className="relative z-10 flex flex-col justify-end p-12 text-white">
          <h2 className="text-4xl font-bold mb-4">Start Learning Today</h2>
          <p className="text-lg text-white/80 max-w-md">
            Join thousands of professionals advancing their skills with 
            industry-leading courses and certifications.
          </p>
        </div>
      </div>

      {/* Right side - Form */}
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
              <CardTitle className="text-2xl font-bold text-[#0F172A]">Create account</CardTitle>
              <CardDescription className="text-slate-500">
                Get started with your learning journey
              </CardDescription>
            </CardHeader>
            <CardContent className="px-0">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="first_name" className="text-slate-700">First Name</Label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <Input
                        id="first_name"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        placeholder="John"
                        className="pl-10"
                        required
                        data-testid="register-first-name"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="last_name" className="text-slate-700">Last Name</Label>
                    <Input
                      id="last_name"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                      placeholder="Doe"
                      required
                      data-testid="register-last-name"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email" className="text-slate-700">Email</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="you@company.com"
                      className="pl-10"
                      required
                      data-testid="register-email"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="employee_id" className="text-slate-700">Employee ID (Optional)</Label>
                  <div className="relative">
                    <Building className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      id="employee_id"
                      name="employee_id"
                      value={formData.employee_id}
                      onChange={handleChange}
                      placeholder="EMP-001"
                      className="pl-10"
                      data-testid="register-employee-id"
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-slate-700">Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      id="password"
                      name="password"
                      type="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Create a strong password"
                      className="pl-10"
                      required
                      minLength={6}
                      data-testid="register-password"
                    />
                  </div>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-[#095EB1] hover:bg-[#074A8C] h-11 mt-2"
                  disabled={loading}
                  data-testid="register-submit"
                >
                  {loading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <>
                      Create Account
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </>
                  )}
                </Button>
              </form>

              <div className="mt-6 text-center">
                <p className="text-sm text-slate-500">
                  Already have an account?{' '}
                  <Link to="/login" className="text-[#095EB1] hover:underline font-medium" data-testid="login-link">
                    Sign in
                  </Link>
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
