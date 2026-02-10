import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { adminApi, courseApi } from '../../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { toast } from 'sonner';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../../components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../components/ui/select';
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
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '../../components/ui/collapsible';
import { 
  ArrowLeft,
  Plus,
  Pencil,
  Trash2,
  ChevronDown,
  ChevronUp,
  PlayCircle,
  FileText,
  BookOpen,
  ClipboardList,
  GripVertical,
  Loader2,
  Users
} from 'lucide-react';

export default function AdminCourseDetail() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [openModules, setOpenModules] = useState({});
  
  // Modal states
  const [showModuleModal, setShowModuleModal] = useState(false);
  const [showLessonModal, setShowLessonModal] = useState(false);
  const [showQuizModal, setShowQuizModal] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  
  const [editingModule, setEditingModule] = useState(null);
  const [editingLesson, setEditingLesson] = useState(null);
  const [editingQuiz, setEditingQuiz] = useState(null);
  const [selectedModuleId, setSelectedModuleId] = useState(null);
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [saving, setSaving] = useState(false);

  // Form data
  const [moduleForm, setModuleForm] = useState({ title: '', description: '', order: 0 });
  const [lessonForm, setLessonForm] = useState({ title: '', content_type: 'text', content: '', duration_minutes: 0, order: 0 });
  const [quizForm, setQuizForm] = useState({ 
    title: '', 
    description: '', 
    passing_score: 70, 
    questions: [{ question: '', question_type: 'multiple_choice', options: ['', '', '', ''], correct_answer: '', points: 1 }]
  });

  useEffect(() => {
    fetchCourse();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseId]);

  const fetchCourse = async () => {
    try {
      const response = await courseApi.getById(courseId);
      setCourse(response.data);
      // Open all modules by default
      const openState = {};
      response.data.modules?.forEach(m => { openState[m.id] = true; });
      setOpenModules(openState);
    } catch (error) {
      toast.error('Failed to load course');
      navigate('/admin/courses');
    } finally {
      setLoading(false);
    }
  };

  const toggleModule = (moduleId) => {
    setOpenModules(prev => ({ ...prev, [moduleId]: !prev[moduleId] }));
  };

  // Module operations
  const openAddModule = () => {
    setEditingModule(null);
    setModuleForm({ title: '', description: '', order: (course?.modules?.length || 0) });
    setShowModuleModal(true);
  };

  const openEditModule = (module) => {
    setEditingModule(module);
    setModuleForm({ title: module.title, description: module.description || '', order: module.order });
    setShowModuleModal(true);
  };

  const saveModule = async () => {
    if (!moduleForm.title.trim()) {
      toast.error('Module title is required');
      return;
    }
    setSaving(true);
    try {
      if (editingModule) {
        await adminApi.updateModule(editingModule.id, moduleForm);
        toast.success('Module updated');
      } else {
        await adminApi.createModule(courseId, moduleForm);
        toast.success('Module created');
      }
      setShowModuleModal(false);
      fetchCourse();
    } catch (error) {
      toast.error('Failed to save module');
    } finally {
      setSaving(false);
    }
  };

  // Lesson operations
  const openAddLesson = (moduleId) => {
    setSelectedModuleId(moduleId);
    setEditingLesson(null);
    const module = course.modules.find(m => m.id === moduleId);
    setLessonForm({ title: '', content_type: 'text', content: '', duration_minutes: 0, order: module?.lessons?.length || 0 });
    setShowLessonModal(true);
  };

  const openEditLesson = (lesson, moduleId) => {
    setSelectedModuleId(moduleId);
    setEditingLesson(lesson);
    setLessonForm({ 
      title: lesson.title, 
      content_type: lesson.content_type, 
      content: lesson.content, 
      duration_minutes: lesson.duration_minutes || 0, 
      order: lesson.order 
    });
    setShowLessonModal(true);
  };

  const saveLesson = async () => {
    if (!lessonForm.title.trim()) {
      toast.error('Lesson title is required');
      return;
    }
    setSaving(true);
    try {
      if (editingLesson) {
        await adminApi.updateLesson(editingLesson.id, lessonForm);
        toast.success('Lesson updated');
      } else {
        await adminApi.createLesson(selectedModuleId, lessonForm);
        toast.success('Lesson created');
      }
      setShowLessonModal(false);
      fetchCourse();
    } catch (error) {
      toast.error('Failed to save lesson');
    } finally {
      setSaving(false);
    }
  };

  // Quiz operations
  const openAddQuiz = (moduleId) => {
    setSelectedModuleId(moduleId);
    setEditingQuiz(null);
    setQuizForm({ 
      title: '', 
      description: '', 
      passing_score: 70, 
      questions: [{ question: '', question_type: 'multiple_choice', options: ['', '', '', ''], correct_answer: '', points: 1 }]
    });
    setShowQuizModal(true);
  };

  const openEditQuiz = (quiz, moduleId) => {
    setSelectedModuleId(moduleId);
    setEditingQuiz(quiz);
    setQuizForm({ 
      title: quiz.title, 
      description: quiz.description || '', 
      passing_score: quiz.passing_score, 
      questions: quiz.questions || []
    });
    setShowQuizModal(true);
  };

  const addQuestion = () => {
    setQuizForm({
      ...quizForm,
      questions: [...quizForm.questions, { question: '', question_type: 'multiple_choice', options: ['', '', '', ''], correct_answer: '', points: 1 }]
    });
  };

  const updateQuestion = (index, field, value) => {
    const newQuestions = [...quizForm.questions];
    newQuestions[index] = { ...newQuestions[index], [field]: value };
    setQuizForm({ ...quizForm, questions: newQuestions });
  };

  const updateQuestionOption = (qIndex, oIndex, value) => {
    const newQuestions = [...quizForm.questions];
    newQuestions[qIndex].options[oIndex] = value;
    setQuizForm({ ...quizForm, questions: newQuestions });
  };

  const removeQuestion = (index) => {
    if (quizForm.questions.length === 1) {
      toast.error('Quiz must have at least one question');
      return;
    }
    const newQuestions = quizForm.questions.filter((_, i) => i !== index);
    setQuizForm({ ...quizForm, questions: newQuestions });
  };

  const saveQuiz = async () => {
    if (!quizForm.title.trim()) {
      toast.error('Quiz title is required');
      return;
    }
    if (quizForm.questions.some(q => !q.question.trim() || !q.correct_answer.trim())) {
      toast.error('All questions must have content and correct answer');
      return;
    }
    setSaving(true);
    try {
      if (editingQuiz) {
        await adminApi.updateQuiz(editingQuiz.id, quizForm);
        toast.success('Quiz updated');
      } else {
        await adminApi.createQuiz(selectedModuleId, quizForm);
        toast.success('Quiz created');
      }
      setShowQuizModal(false);
      fetchCourse();
    } catch (error) {
      toast.error('Failed to save quiz');
    } finally {
      setSaving(false);
    }
  };

  // Delete operations
  const openDeleteDialog = (type, item, moduleId = null) => {
    setDeleteTarget({ type, item, moduleId });
    setShowDeleteDialog(true);
  };

  const handleDelete = async () => {
    try {
      switch (deleteTarget.type) {
        case 'module':
          await adminApi.deleteModule(deleteTarget.item.id);
          toast.success('Module deleted');
          break;
        case 'lesson':
          await adminApi.deleteLesson(deleteTarget.item.id);
          toast.success('Lesson deleted');
          break;
        case 'quiz':
          await adminApi.deleteQuiz(deleteTarget.item.id);
          toast.success('Quiz deleted');
          break;
      }
      setShowDeleteDialog(false);
      setDeleteTarget(null);
      fetchCourse();
    } catch (error) {
      toast.error('Failed to delete');
    }
  };

  const getContentIcon = (type) => {
    switch (type) {
      case 'video':
      case 'embed':
        return <PlayCircle className="w-4 h-4 text-blue-500" />;
      case 'pdf':
        return <FileText className="w-4 h-4 text-red-500" />;
      default:
        return <BookOpen className="w-4 h-4 text-slate-500" />;
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="page-container">
          <Skeleton className="h-8 w-64 mb-8" />
          <Skeleton className="h-96" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page-container" data-testid="admin-course-detail">
        {/* Back Button */}
        <Button variant="ghost" onClick={() => navigate('/admin/courses')} className="mb-4">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Courses
        </Button>

        {/* Course Header */}
        <div className="flex flex-col md:flex-row justify-between items-start gap-4 mb-8">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold text-[#0F172A]">{course?.title}</h1>
              <Badge className={course?.is_published ? 'bg-emerald-500' : 'bg-slate-500'}>
                {course?.is_published ? 'Published' : 'Draft'}
              </Badge>
            </div>
            <p className="text-slate-500">{course?.description}</p>
            <div className="flex items-center gap-4 mt-2 text-sm text-slate-500">
              <span className="flex items-center gap-1">
                <Users className="w-4 h-4" />
                {course?.enrolled_users?.length || 0} enrolled
              </span>
              <span>{course?.modules?.length || 0} modules</span>
            </div>
          </div>
          <Button className="bg-[#095EB1] hover:bg-[#074A8C]" onClick={openAddModule} data-testid="add-module-btn">
            <Plus className="w-4 h-4 mr-2" />
            Add Module
          </Button>
        </div>

        {/* Modules */}
        <div className="space-y-4">
          {course?.modules?.length === 0 ? (
            <Card className="card-base">
              <CardContent className="p-12 text-center">
                <BookOpen className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-slate-700 mb-2">No modules yet</h3>
                <p className="text-slate-500 mb-4">Add modules to organize your course content.</p>
                <Button className="bg-[#095EB1] hover:bg-[#074A8C]" onClick={openAddModule}>
                  <Plus className="w-4 h-4 mr-2" />
                  Add First Module
                </Button>
              </CardContent>
            </Card>
          ) : (
            course?.modules?.map((module, mIndex) => (
              <Card key={module.id} className="card-base" data-testid={`module-${module.id}`}>
                <Collapsible open={openModules[module.id]} onOpenChange={() => toggleModule(module.id)}>
                  <CollapsibleTrigger className="w-full">
                    <CardHeader className="bg-slate-50 border-b hover:bg-slate-100 transition-colors cursor-pointer">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <span className="w-8 h-8 bg-[#095EB1] text-white rounded-full flex items-center justify-center text-sm font-semibold">
                            {mIndex + 1}
                          </span>
                          <div className="text-left">
                            <CardTitle className="text-lg">{module.title}</CardTitle>
                            {module.description && (
                              <p className="text-sm text-slate-500 font-normal">{module.description}</p>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline">{module.lessons?.length || 0} lessons</Badge>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            onClick={(e) => { e.stopPropagation(); openEditModule(module); }}
                            data-testid={`edit-module-${module.id}`}
                          >
                            <Pencil className="w-4 h-4" />
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="text-red-600"
                            onClick={(e) => { e.stopPropagation(); openDeleteDialog('module', module); }}
                            data-testid={`delete-module-${module.id}`}
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                          {openModules[module.id] ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                        </div>
                      </div>
                    </CardHeader>
                  </CollapsibleTrigger>
                  
                  <CollapsibleContent>
                    <CardContent className="p-4 space-y-3">
                      {/* Lessons */}
                      {module.lessons?.map((lesson, lIndex) => (
                        <div 
                          key={lesson.id} 
                          className="flex items-center gap-3 p-3 bg-white border rounded-lg"
                          data-testid={`lesson-${lesson.id}`}
                        >
                          <GripVertical className="w-4 h-4 text-slate-300" />
                          {getContentIcon(lesson.content_type)}
                          <div className="flex-1">
                            <p className="font-medium">{lesson.title}</p>
                            <p className="text-xs text-slate-500 capitalize">{lesson.content_type} • {lesson.duration_minutes || 0} min</p>
                          </div>
                          <div className="flex gap-1">
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => openEditLesson(lesson, module.id)}
                            >
                              <Pencil className="w-4 h-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              className="text-red-600"
                              onClick={() => openDeleteDialog('lesson', lesson, module.id)}
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      ))}

                      {/* Quizzes */}
                      {module.quizzes?.map((quiz) => (
                        <div 
                          key={quiz.id} 
                          className="flex items-center gap-3 p-3 bg-amber-50 border border-amber-200 rounded-lg"
                          data-testid={`quiz-${quiz.id}`}
                        >
                          <ClipboardList className="w-4 h-4 text-amber-500" />
                          <div className="flex-1">
                            <p className="font-medium">{quiz.title}</p>
                            <p className="text-xs text-slate-500">{quiz.questions?.length || 0} questions • Pass: {quiz.passing_score}%</p>
                          </div>
                          <div className="flex gap-1">
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => openEditQuiz(quiz, module.id)}
                            >
                              <Pencil className="w-4 h-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              className="text-red-600"
                              onClick={() => openDeleteDialog('quiz', quiz, module.id)}
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      ))}

                      {/* Add buttons */}
                      <div className="flex gap-2 pt-2">
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => openAddLesson(module.id)}
                          data-testid={`add-lesson-${module.id}`}
                        >
                          <Plus className="w-4 h-4 mr-1" />
                          Add Lesson
                        </Button>
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => openAddQuiz(module.id)}
                          data-testid={`add-quiz-${module.id}`}
                        >
                          <Plus className="w-4 h-4 mr-1" />
                          Add Quiz
                        </Button>
                      </div>
                    </CardContent>
                  </CollapsibleContent>
                </Collapsible>
              </Card>
            ))
          )}
        </div>

        {/* Module Modal */}
        <Dialog open={showModuleModal} onOpenChange={setShowModuleModal}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{editingModule ? 'Edit Module' : 'Add Module'}</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label>Title *</Label>
                <Input
                  value={moduleForm.title}
                  onChange={(e) => setModuleForm({ ...moduleForm, title: e.target.value })}
                  placeholder="Module title"
                  data-testid="module-title-input"
                />
              </div>
              <div className="space-y-2">
                <Label>Description</Label>
                <Textarea
                  value={moduleForm.description}
                  onChange={(e) => setModuleForm({ ...moduleForm, description: e.target.value })}
                  placeholder="Module description"
                  rows={2}
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowModuleModal(false)}>Cancel</Button>
              <Button className="bg-[#095EB1] hover:bg-[#074A8C]" onClick={saveModule} disabled={saving} data-testid="save-module-btn">
                {saving && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                Save Module
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Lesson Modal */}
        <Dialog open={showLessonModal} onOpenChange={setShowLessonModal}>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>{editingLesson ? 'Edit Lesson' : 'Add Lesson'}</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4 max-h-[60vh] overflow-y-auto">
              <div className="space-y-2">
                <Label>Title *</Label>
                <Input
                  value={lessonForm.title}
                  onChange={(e) => setLessonForm({ ...lessonForm, title: e.target.value })}
                  placeholder="Lesson title"
                  data-testid="lesson-title-input"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Content Type</Label>
                  <Select 
                    value={lessonForm.content_type} 
                    onValueChange={(value) => setLessonForm({ ...lessonForm, content_type: value })}
                  >
                    <SelectTrigger data-testid="lesson-type-select">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="text">Text</SelectItem>
                      <SelectItem value="video">Video (Upload URL)</SelectItem>
                      <SelectItem value="embed">Video (Embed)</SelectItem>
                      <SelectItem value="pdf">PDF</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Duration (minutes)</Label>
                  <Input
                    type="number"
                    value={lessonForm.duration_minutes}
                    onChange={(e) => setLessonForm({ ...lessonForm, duration_minutes: parseInt(e.target.value) || 0 })}
                    min={0}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Content *</Label>
                {lessonForm.content_type === 'text' ? (
                  <Textarea
                    value={lessonForm.content}
                    onChange={(e) => setLessonForm({ ...lessonForm, content: e.target.value })}
                    placeholder="Enter lesson content (HTML supported)"
                    rows={6}
                    data-testid="lesson-content-input"
                  />
                ) : (
                  <Input
                    value={lessonForm.content}
                    onChange={(e) => setLessonForm({ ...lessonForm, content: e.target.value })}
                    placeholder={lessonForm.content_type === 'embed' ? 'YouTube/Vimeo embed URL' : 'File URL'}
                    data-testid="lesson-content-input"
                  />
                )}
                {lessonForm.content_type === 'embed' && (
                  <p className="text-xs text-slate-500">Enter a YouTube or Vimeo embed URL (e.g., https://www.youtube.com/embed/VIDEO_ID)</p>
                )}
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowLessonModal(false)}>Cancel</Button>
              <Button className="bg-[#095EB1] hover:bg-[#074A8C]" onClick={saveLesson} disabled={saving} data-testid="save-lesson-btn">
                {saving && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                Save Lesson
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Quiz Modal */}
        <Dialog open={showQuizModal} onOpenChange={setShowQuizModal}>
          <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-hidden flex flex-col">
            <DialogHeader>
              <DialogTitle>{editingQuiz ? 'Edit Quiz' : 'Add Quiz'}</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4 overflow-y-auto flex-1">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Title *</Label>
                  <Input
                    value={quizForm.title}
                    onChange={(e) => setQuizForm({ ...quizForm, title: e.target.value })}
                    placeholder="Quiz title"
                    data-testid="quiz-title-input"
                  />
                </div>
                <div className="space-y-2">
                  <Label>Passing Score (%)</Label>
                  <Input
                    type="number"
                    value={quizForm.passing_score}
                    onChange={(e) => setQuizForm({ ...quizForm, passing_score: parseInt(e.target.value) || 70 })}
                    min={0}
                    max={100}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Description</Label>
                <Textarea
                  value={quizForm.description}
                  onChange={(e) => setQuizForm({ ...quizForm, description: e.target.value })}
                  placeholder="Quiz description"
                  rows={2}
                />
              </div>

              {/* Questions */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <Label className="text-base">Questions</Label>
                  <Button variant="outline" size="sm" onClick={addQuestion}>
                    <Plus className="w-4 h-4 mr-1" />
                    Add Question
                  </Button>
                </div>

                {quizForm.questions.map((q, qIndex) => (
                  <Card key={qIndex} className="p-4 bg-slate-50">
                    <div className="space-y-3">
                      <div className="flex items-start justify-between">
                        <span className="font-medium">Question {qIndex + 1}</span>
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          className="text-red-600"
                          onClick={() => removeQuestion(qIndex)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                      
                      <Input
                        value={q.question}
                        onChange={(e) => updateQuestion(qIndex, 'question', e.target.value)}
                        placeholder="Enter question"
                      />
                      
                      <div className="grid grid-cols-2 gap-3">
                        <Select 
                          value={q.question_type} 
                          onValueChange={(value) => updateQuestion(qIndex, 'question_type', value)}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="multiple_choice">Multiple Choice</SelectItem>
                            <SelectItem value="true_false">True/False</SelectItem>
                            <SelectItem value="short_answer">Short Answer</SelectItem>
                          </SelectContent>
                        </Select>
                        <Input
                          type="number"
                          value={q.points}
                          onChange={(e) => updateQuestion(qIndex, 'points', parseInt(e.target.value) || 1)}
                          placeholder="Points"
                          min={1}
                        />
                      </div>

                      {q.question_type === 'multiple_choice' && (
                        <div className="space-y-2">
                          <Label className="text-sm">Options</Label>
                          {q.options.map((opt, oIndex) => (
                            <Input
                              key={oIndex}
                              value={opt}
                              onChange={(e) => updateQuestionOption(qIndex, oIndex, e.target.value)}
                              placeholder={`Option ${oIndex + 1}`}
                            />
                          ))}
                        </div>
                      )}

                      <div className="space-y-2">
                        <Label className="text-sm">Correct Answer *</Label>
                        {q.question_type === 'true_false' ? (
                          <Select 
                            value={q.correct_answer} 
                            onValueChange={(value) => updateQuestion(qIndex, 'correct_answer', value)}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Select answer" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="True">True</SelectItem>
                              <SelectItem value="False">False</SelectItem>
                            </SelectContent>
                          </Select>
                        ) : (
                          <Input
                            value={q.correct_answer}
                            onChange={(e) => updateQuestion(qIndex, 'correct_answer', e.target.value)}
                            placeholder="Enter correct answer"
                          />
                        )}
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowQuizModal(false)}>Cancel</Button>
              <Button className="bg-[#095EB1] hover:bg-[#074A8C]" onClick={saveQuiz} disabled={saving} data-testid="save-quiz-btn">
                {saving && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                Save Quiz
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Delete Dialog */}
        <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Delete {deleteTarget?.type}</AlertDialogTitle>
              <AlertDialogDescription>
                Are you sure you want to delete "{deleteTarget?.item?.title}"? This action cannot be undone.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction onClick={handleDelete} className="bg-red-600 hover:bg-red-700">
                Delete
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </Layout>
  );
}
