import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { certificateApi } from '../../lib/api';
import { Card, CardContent } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Skeleton } from '../../components/ui/skeleton';
import { toast } from 'sonner';
import { Award, Download, Eye, Calendar } from 'lucide-react';

export default function Certificates() {
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(null);

  useEffect(() => {
    fetchCertificates();
  }, []);

  const fetchCertificates = async () => {
    try {
      const response = await certificateApi.getAll();
      setCertificates(response.data);
    } catch (error) {
      console.error('Failed to fetch certificates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (certId) => {
    setDownloading(certId);
    try {
      const response = await certificateApi.downloadPdf(certId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `certificate-${certId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success('Certificate downloaded!');
    } catch (error) {
      toast.error('Failed to download certificate');
    } finally {
      setDownloading(null);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="page-container">
          <Skeleton className="h-8 w-64 mb-8" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1,2,3].map(i => <Skeleton key={i} className="h-48" />)}
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page-container" data-testid="certificates-page">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#0F172A] mb-2">My Certificates</h1>
          <p className="text-slate-500">
            Your achievements and completed certifications.
          </p>
        </div>

        {/* Certificates Grid */}
        {certificates.length === 0 ? (
          <Card className="card-base">
            <CardContent className="p-16 text-center">
              <Award className="w-20 h-20 text-slate-200 mx-auto mb-6" />
              <h3 className="text-xl font-semibold text-slate-700 mb-2">No certificates yet</h3>
              <p className="text-slate-500 mb-6">
                Complete courses to earn certificates and showcase your achievements.
              </p>
              <Link to="/courses">
                <Button className="bg-[#095EB1] hover:bg-[#074A8C]">
                  Browse Courses
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {certificates.map((cert) => (
              <Card key={cert.id} className="card-base overflow-hidden group" data-testid={`certificate-${cert.id}`}>
                {/* Certificate Preview */}
                <div className="relative bg-gradient-to-br from-[#095EB1]/5 to-[#0EA5E9]/10 p-6 border-b">
                  <div className="absolute top-0 left-0 w-full h-full opacity-5">
                    <div className="absolute inset-4 border-2 border-[#095EB1] rounded-lg" />
                    <div className="absolute inset-6 border border-[#0EA5E9] rounded-lg" />
                  </div>
                  <div className="relative text-center">
                    <Award className="w-12 h-12 text-amber-500 mx-auto mb-3" />
                    <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Certificate of Completion</p>
                    <h3 className="font-bold text-[#0F172A]">{cert.course_title}</h3>
                  </div>
                </div>

                <CardContent className="p-4">
                  <div className="flex items-center gap-2 text-sm text-slate-500 mb-4">
                    <Calendar className="w-4 h-4" />
                    <span>Issued {new Date(cert.issued_at).toLocaleDateString()}</span>
                  </div>
                  
                  <p className="text-xs text-slate-400 mb-4 font-mono">
                    {cert.certificate_number}
                  </p>

                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="flex-1"
                      onClick={() => handleDownload(cert.id)}
                      disabled={downloading === cert.id}
                      data-testid={`download-cert-${cert.id}`}
                    >
                      <Download className="w-4 h-4 mr-2" />
                      {downloading === cert.id ? 'Downloading...' : 'Download'}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
