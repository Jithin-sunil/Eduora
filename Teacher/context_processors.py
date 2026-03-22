from Admin.models import tbl_assignclass
from Teacher.models import tbl_teacher


def teacher_sidebar_context(request):
    is_class_teacher = False
    tid = request.session.get('tid')
    if tid:
        try:
            teacher = tbl_teacher.objects.get(id=tid)
            is_class_teacher = tbl_assignclass.objects.filter(teacher=teacher).exists()
        except tbl_teacher.DoesNotExist:
            is_class_teacher = False

    return {
        'is_class_teacher': is_class_teacher
    }
