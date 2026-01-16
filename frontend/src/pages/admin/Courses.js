import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { adminApi, courseApi } from '../../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { Switch } from '../../components/ui/switch';
import { toast } from 'sonner';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../../components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '../../components/ui/alert-dialog';
import { 
  BookOpen, 
  Plus,
  Pencil,
  Trash2,
  Users,
  Clock,
  Search,
  Eye,
  Loader2
} from 'lucide-react';

export default function AdminCourses() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [saving, setSaving] = useState(false);
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    thumbnail: '',
    category: '',
    duration_hours: 0,
    is_published: false,
    course_type: 'optional'
  });

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await courseApi.getAll();
      setCourses(response.data);
    } catch (error) {
      console.error('Failed to fetch courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      thumbnail: '',
      category: '',
      duration_hours: 0,
      is_published: false
    });
  };

  const handleCreate = async () => {
    if (!formData.title.trim()) {
      toast.error('Course title is required');
      return;
    }
    
    setSaving(true);
    try {
      await adminApi.createCourse(formData);
      toast.success('Course created successfully');
      setShowCreateModal(false);
      resetForm();
      fetchCourses();
    } catch (error) {
      toast.error('Failed to create course');
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = async () => {
    if (!formData.title.trim()) {
      toast.error('Course title is required');
      return;
    }
    
    setSaving(true);
    try {
      await adminApi.updateCourse(selectedCourse.id, formData);
      toast.success('Course updated successfully');
      setShowEditModal(false);
      setSelectedCourse(null);
      resetForm();
      fetchCourses();
    } catch (error) {
      toast.error('Failed to update course');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    try {
      await adminApi.deleteCourse(selectedCourse.id);
      toast.success('Course deleted');
      setShowDeleteDialog(false);
      setSelectedCourse(null);
      fetchCourses();
    } catch (error) {
      toast.error('Failed to delete course');
    }
  };

  const openEditModal = (course) => {
    setSelectedCourse(course);
    setFormData({
      title: course.title,
      description: course.description || '',
      thumbnail: course.thumbnail || '',
      category: course.category || '',
      duration_hours: course.duration_hours || 0,
      is_published: course.is_published || false
    });
    setShowEditModal(true);
  };

  const openDeleteDialog = (course) => {
    setSelectedCourse(course);
    setShowDeleteDialog(true);
  };

  const filteredCourses = courses.filter(course =>
    course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    course.category?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <Layout>
        <div className="page-container">
          <Skeleton className="h-8 w-64 mb-8" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1,2,3].map(i => <Skeleton key={i} className="h-64" />)}
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page-container" data-testid="admin-courses">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-[#0F172A] mb-2">Course Management</h1>
            <p className="text-slate-500">
              Create, edit, and manage your training courses.
            </p>
          </div>
          <Button 
            className="bg-[#095EB1] hover:bg-[#074A8C]"
            onClick={() => { resetForm(); setShowCreateModal(true); }}
            data-testid="create-course-btn"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create Course
          </Button>
        </div>

        {/* Search */}
        <div className="mb-6">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input
              placeholder="Search courses..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
              data-testid="search-courses"
            />
          </div>
        </div>

        {/* Courses Grid */}
        {filteredCourses.length === 0 ? (
          <Card className="card-base">
            <CardContent className="p-16 text-center">
              <BookOpen className="w-16 h-16 text-slate-200 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-700 mb-2">No courses yet</h3>
              <p className="text-slate-500 mb-4">Create your first course to get started.</p>
              <Button 
                className="bg-[#095EB1] hover:bg-[#074A8C]"
                onClick={() => { resetForm(); setShowCreateModal(true); }}
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Course
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCourses.map((course) => (
              <Card key={course.id} className="card-base group" data-testid={`course-${course.id}`}>
                {/* Thumbnail */}
                <div className="aspect-video bg-slate-100 relative overflow-hidden">
                  {course.thumbnail ? (
                    <img src={course.thumbnail} alt={course.title} className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-[#095EB1]/10 to-[#0EA5E9]/10">
                      <BookOpen className="w-12 h-12 text-[#095EB1]/40" />
                    </div>
                  )}
                  <Badge 
                    className={`absolute top-3 right-3 ${course.is_published ? 'bg-emerald-500' : 'bg-slate-500'}`}
                  >
                    {course.is_published ? 'Published' : 'Draft'}
                  </Badge>
                </div>

                <CardContent className="p-5">
                  <h3 className="font-semibold text-lg text-[#0F172A] mb-2 line-clamp-1">
                    {course.title}
                  </h3>
                  <p className="text-sm text-slate-500 mb-4 line-clamp-2">
                    {course.description || 'No description'}
                  </p>

                  <div className="flex items-center gap-4 text-sm text-slate-500 mb-4">
                    <div className="flex items-center gap-1">
                      <Users className="w-4 h-4" />
                      <span>{course.enrolled_users?.length || 0}</span>
                    </div>
                    {course.duration_hours > 0 && (
                      <div className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        <span>{course.duration_hours}h</span>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="flex-1"
                      onClick={() => navigate(`/admin/courses/${course.id}`)}
                      data-testid={`manage-course-${course.id}`}
                    >
                      <Eye className="w-4 h-4 mr-1" />
                      Manage
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => openEditModal(course)}
                      data-testid={`edit-course-${course.id}`}
                    >
                      <Pencil className="w-4 h-4" />
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      onClick={() => openDeleteDialog(course)}
                      data-testid={`delete-course-${course.id}`}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Create/Edit Modal */}
        <Dialog open={showCreateModal || showEditModal} onOpenChange={() => { setShowCreateModal(false); setShowEditModal(false); }}>
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>{showEditModal ? 'Edit Course' : 'Create New Course'}</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label>Title *</Label>
                <Input
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Course title"
                  data-testid="course-title-input"
                />
              </div>
              <div className="space-y-2">
                <Label>Description</Label>
                <Textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Course description"
                  rows={3}
                  data-testid="course-description-input"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Category</Label>
                  <Input
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    placeholder="e.g., Engineering"
                    data-testid="course-category-input"
                  />
                </div>
                <div className="space-y-2">
                  <Label>Duration (hours)</Label>
                  <Input
                    type="number"
                    value={formData.duration_hours}
                    onChange={(e) => setFormData({ ...formData, duration_hours: parseFloat(e.target.value) || 0 })}
                    min={0}
                    data-testid="course-duration-input"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Thumbnail URL</Label>
                <Input
                  value={formData.thumbnail}
                  onChange={(e) => setFormData({ ...formData, thumbnail: e.target.value })}
                  placeholder="https://example.com/image.jpg"
                  data-testid="course-thumbnail-input"
                />
              </div>
              <div className="flex items-center justify-between">
                <Label>Publish Course</Label>
                <Switch
                  checked={formData.is_published}
                  onCheckedChange={(checked) => setFormData({ ...formData, is_published: checked })}
                  data-testid="course-publish-toggle"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => { setShowCreateModal(false); setShowEditModal(false); }}>
                Cancel
              </Button>
              <Button 
                className="bg-[#095EB1] hover:bg-[#074A8C]"
                onClick={showEditModal ? handleEdit : handleCreate}
                disabled={saving}
                data-testid="save-course-btn"
              >
                {saving && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                {showEditModal ? 'Save Changes' : 'Create Course'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Delete Confirmation */}
        <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Delete Course</AlertDialogTitle>
              <AlertDialogDescription>
                Are you sure you want to delete "{selectedCourse?.title}"? This action cannot be undone 
                and will remove all modules, lessons, and learner progress.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction
                onClick={handleDelete}
                className="bg-red-600 hover:bg-red-700"
                data-testid="confirm-delete-course"
              >
                Delete
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </Layout>
  );
}
