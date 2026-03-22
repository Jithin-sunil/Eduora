import numpy as np
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Admin.models import *
from Teacher.models import *
from Student.models import *

class EduBot:
    def __init__(self):
        self.intents = [
            {
                "id": "attendance",
                "patterns": [
                    "attendance", "my attendance", "attendance percentage",
                    "how much attendance do i have", "am i below 75",
                    "attendance status", "present absent"
                ],
                "response_type": "dynamic",
                "context": "attendance"
            },
            {
                "id": "marks",
                "patterns": [
                    "marks", "internal marks", "score", "result",
                    "my marks", "exam result", "performance"
                ],
                "response_type": "dynamic",
                "context": "marks"
            },
            {
                "id": "assignments",
                "patterns": [
                    "assignment", "homework", "pending assignment",
                    "any tasks", "submission", "assignment due"
                ],
                "response_type": "dynamic",
                "context": "assignments"
            },
            {
                "id": "timetable",
                "patterns": [
                    "timetable", "schedule", "today class",
                    "next class", "class today", "lecture"
                ],
                "response_type": "dynamic",
                "context": "timetable"
            },
            {
                "id": "notifications",
                "patterns": [
                    "notifications", "announcements", "news",
                    "events", "college updates"
                ],
                "response_type": "dynamic",
                "context": "notifications"
            },
            {
                "id": "profile",
                "patterns": [
                    "my details", "my profile", "student info",
                    "my course", "my class"
                ],
                "response_type": "dynamic",
                "context": "profile"
            },
            {
                "id": "greetings",
                "patterns": ["hi", "hello", "hey"],
                "response": "Hi 👋 I'm EduBot! Ask me about attendance, marks, timetable, assignments, or notifications."
            },
            {
                "id": "leave",
                "patterns": ["leave", "apply leave", "sick leave"],
                "response": "You can apply leave from the Leave section in your dashboard."
            },
            {
                "id": "complaint",
                "patterns": ["complaint", "issue", "problem", "report"],
                "response": "Please use the Complaint section to submit your issue."
            }
        ]

        self.patterns = []
        self.intent_map = []

        for intent in self.intents:
            for p in intent["patterns"]:
                self.patterns.append(p)
                self.intent_map.append(intent)

        self.vectorizer = TfidfVectorizer().fit(self.patterns)
        self.matrix = self.vectorizer.transform(self.patterns)

    def get_response(self, query, student):
        query = query.lower()
        vec = self.vectorizer.transform([query])
        sim = cosine_similarity(vec, self.matrix).flatten()
        idx = np.argmax(sim)

        if sim[idx] < 0.25:
            return self.fallback()

        intent = self.intent_map[idx]

        if intent.get("response_type") == "dynamic":
            return self.handle_dynamic(intent["context"], student)
        return intent.get("response")

    def fallback(self):
        return ("I'm not sure I understood that 🤔\n"
                "Try asking things like:\n"
                "- My attendance\n"
                "- My marks\n"
                "- Today's timetable\n"
                "- Any assignments")

    def handle_dynamic(self, context, student):

        # ✅ ATTENDANCE
        if context == "attendance":
            attendance = tbl_attendance.objects.filter(student=student)

            total = attendance.count()
            present = attendance.filter(status=1).count()

            if total == 0:
                return "No attendance data found."

            percent = (present / total) * 100

            status_msg = "Good 👍"
            if percent < 75:
                status_msg = "Warning ⚠️ You are below 75%!"

            return f"Attendance: {percent:.2f}%\nPresent: {present}/{total}\n{status_msg}"

        # ✅ MARKS
        elif context == "marks":
            marks = tbl_internalmark.objects.filter(student=student)

            if not marks.exists():
                return "Marks not uploaded yet."

            reply = "📊 Your Marks:\n"
            for m in marks:
                reply += f"- {m.subject.subject_name}: {m.internal_score}\n"
            return reply

        # ✅ ASSIGNMENTS
        elif context == "assignments":
            course = student.assignclass.Class.course

            assignments = tbl_assignment.objects.filter(
                subject__course=course
            ).order_by('-assignment_duedate')[:5]

            if not assignments.exists():
                return "No assignments found."

            reply = "📝 Assignments:\n"
            for a in assignments:
                reply += f"- {a.assignment_title} ({a.subject.subject_name})\nDue: {a.assignment_duedate}\n"
            return reply

        # ✅ TIMETABLE
        elif context == "timetable":
            today = datetime.datetime.now().strftime("%A")

            course = student.assignclass.Class.course

            timetable = tbl_timetable.objects.filter(
                course=course,
                day=today
            ).order_by('hour')

            if not timetable.exists():
                return f"No classes today ({today}) 🎉"

            reply = f"📅 {today} Schedule:\n"
            for t in timetable:
                reply += f"- Hour {t.hour}: {t.subject.subject_name} ({t.teacher_id.teacher_name})\n"
            return reply

        # ✅ NOTIFICATIONS
        elif context == "notifications":
            notes = tbl_notification.objects.all().order_by('-id')[:3]

            if not notes.exists():
                return "No notifications available."

            reply = "📢 Latest Updates:\n"
            for n in notes:
                reply += f"- {n.notification_title}\n"
            return reply

        # ✅ PROFILE
        elif context == "profile":
            return (
                f"👤 Name: {student.student_name}\n"
                f"📚 Course: {student.assignclass.Class.course.course_name}\n"
                f"🏫 Class: {student.assignclass.Class.class_name}"
            )

        return "Processing..."
        

# GLOBAL INSTANCE
edubot_instance = EduBot()