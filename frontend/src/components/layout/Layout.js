import { Navbar } from './Navbar';
import { Toaster } from '../ui/sonner';

export const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <main className="animate-fade-in">
        {children}
      </main>
      <Toaster position="top-right" />
    </div>
  );
};
