from django.urls import path
from Student import views
app_name="Student"

urlpatterns = [
    path('Homepage/',views.Homepage,name="Homepage"),
    path('Myprofile/',views.Myprofile,name="Myprofile"),
    path('Editprofile/',views.Editprofile,name="Editprofile"),
    path('Changepass/',views.Changepass,name="Changepass"),
    path('Viewnotes/',views.Viewnotes,name="Viewnotes"),
    path('AjaxSubject/',views.AjaxSubject,name="AjaxSubject"),
    path('Ajaxnotes/',views.Ajaxnotes,name="Ajaxnotes"),
    path('Viewassignment/',views.Viewassignment,name="Viewassignment"),
    path('Submitassignment/<int:aid>/',views.Submitassignment,name="Submitassignment"),
    path('delassign/<int:did>/<aid>/',views.delassign,name="delassign"),
    path('Myassignments/',views.Myassignments,name="Myassignments"),
    path("ViewTimeTable/", views.ViewTimeTable, name="ViewTimeTable"),
    path("Complaint/", views.Complaint, name="Complaint"),
    path('delcomplaint/<int:did>/',views.delcomplaint,name="delcomplaint"),
    path("viewattendance/", views.viewattendance, name="viewattendance"),
    path("leaveapplication/", views.leaveapplication, name="leaveapplication"),
    path('delleave/<int:did>/',views.delleave,name="delleave"),
    path('dutyleave/',views.dutyleave,name="dutyleave"),
    path('logout/', views.logout, name="logout"),
    path('deldutyleave/<int:did>/',views.deldutyleave,name="deldutyleave"),
    path('chat/',views.chat,name="chat"),
]