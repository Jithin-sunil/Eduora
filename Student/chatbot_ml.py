import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Admin.models import *
from Teacher.models import *
from Student.models import *

class EduBot:
    def __init__(self):
        # Define Intents: (Question Patterns, Response Type/Logic)
        self.intents = [
            {
                "id": "attendance",
                "patterns": ["how is my attendance", "my attendance percentage", "attendance status", "absent", "present"],
                "response_type": "dynamic",
                "context": "attendance"
            },
            {
                "id": "marks",
                "patterns": ["my internal marks", "exam score", "marks", "result", "grade", "performance"],
                "response_type": "dynamic",
                "context": "marks"
            },
            {
                "id": "assignments",
                "patterns": ["any assignments", "pending tasks", "homework", "submissions", "assignment deadline"],
                "response_type": "dynamic",
                "context": "assignments"
            },
            {
                "id": "timetable",
                "patterns": ["what is my timetable", "next class", "today schedule", "when is the lecture", "my classes"],
                "response_type": "dynamic",
                "context": "timetable"
            },
            {
                "id": "notifications",
                "patterns": ["college news", "announcements", "notifications", "what's happening", "events"],
                "response_type": "dynamic",
                "context": "notifications"
            },
            {
                "id": "greetings",
                "patterns": ["hi", "hello", "hey", "who are you", "what can you do"],
                "response": "Hello! I'm EduBot, your personal academic assistant. You can ask me about your attendance, internal marks, assignments, or today's timetable."
            },
            {
                "id": "leave",
                "patterns": ["how to apply for leave", "sick leave", "absent application"],
                "response": "You can apply for leave from the 'Leaves' section in your dashboard. Just provide the reason and travel/duration dates."
            },
            {
                "id": "complaint",
                "patterns": ["i want to complain", "issue with class", "feedback", "reporting issue"],
                "response": "If you have any academic or infrastructure issues, please use the 'Complaints' section to submit your feedback to the administration."
            }
        ]
        
        # Prepare training data
        self.all_patterns = []
        self.pattern_to_intent = []
        
        for intent in self.intents:
            for pattern in intent["patterns"]:
                self.all_patterns.append(pattern)
                self.pattern_to_intent.append(intent)
        
        # Initialize Vectorizer
        self.vectorizer = TfidfVectorizer().fit(self.all_patterns)
        self.feature_matrix = self.vectorizer.transform(self.all_patterns)

    def get_response(self, user_query, student):
        user_query = user_query.lower()
        query_vec = self.vectorizer.transform([user_query])
        
        # Calculate Cosine Similarity
        similarities = cosine_similarity(query_vec, self.feature_matrix).flatten()
        max_idx = np.argmax(similarities)
        
        if similarities[max_idx] < 0.3:
            return "I'm sorry, I'm not quite sure how to help with that yet. Feel free to ask about your attendance, marks, or timetable!"

        intent = self.pattern_to_intent[max_idx]
        
        if intent.get("response_type") == "dynamic":
            return self._handle_dynamic_intent(intent["context"], student)
        else:
            return intent.get("response", "I'm processing your request, please hold on.")

    def _handle_dynamic_intent(self, context, student):
        if context == "attendance":
            attendance = tbl_attendance.objects.filter(student=student)
            total = attendance.count()
            present = attendance.filter(status=1).count()
            if total > 0:
                percentage = (present / total) * 100
                return f"Your current attendance is {percentage:.2f}%. You have attended {present} out of {total} classes. Keep it up!"
            return "I couldn't find any attendance logs for you. Try checking later!"
            
        elif context == "marks":
            marks = tbl_internalmark.objects.filter(student=student)
            if marks.exists():
                reply = "Here are your latest internal assessment scores:\n"
                for m in marks:
                    reply += f"\n- {m.subject.subject_name}: {m.internal_score}"
                return reply
            return "Your internal marks haven't been uploaded yet."
            
        elif context == "assignments":
            course = student.assignclass.Class.course
            assignments = tbl_assignment.objects.filter(subject__course=course).order_by('-id')[:3]
            if assignments.exists():
                reply = "Recent/Upcoming assignments:\n"
                for a in assignments:
                    reply += f"\n- {a.assignment_title} for {a.subject.subject_name} (Due: {a.assignment_duedate})"
                return reply
            return "No active assignments found for your current course curriculum."
            
        elif context == "timetable":
            import datetime
            today_day = datetime.datetime.now().strftime("%A")
            course = student.assignclass.Class.course
            timetable = tbl_timetable.objects.filter(course=course, day=today_day).order_by('hour')
            if timetable.exists():
                reply = f"Today's ({today_day}) class schedule:\n"
                for t in timetable:
                    reply += f"\n- Hour {t.hour}: {t.subject.subject_name} ({t.teacher_id.teacher_name})"
                return reply
            return f"Great news! No classes are scheduled for you today ({today_day})."
            
        elif context == "notifications":
            notifications = tbl_notification.objects.all().order_by('-id')[:2]
            if notifications.exists():
                reply = "Latest college announcements:\n"
                for n in notifications:
                    reply += f"\n- {n.notification_title}: {n.notification_content[:50]}..."
                return reply
            return "Stay tuned! No official announcements have been posted recently."
            
        return "I'm processing your request, please hold on."

# Global Instance
edubot_instance = EduBot()
