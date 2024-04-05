from django.urls import path
from . import views

urlpatterns = [

  path('Student_Dashboard',views.student_dash,name='student_dash'),
  path('exam_list',views.exam_list,name='exam_list'),
  path('exam_introduction/<int:examid>',views.exam_introduction,name='exam_introduction'),
  path('start_exam/<int:examid>',views.start_exam,name='start_exam'),
  path('submit_answer',views.submit_answer,name='submit_answer'),
  path('submit_exam/<int:examid>',views.submit_exam,name='submit_exam'),
  path('exam_attended',views.exam_attended,name='exam_attended'),
  path('all_exam_list',views.all_exam_list,name='all_exam_list'),
  path('review_result/<int:examid>',views.review_result,name='review_result'),
  path('add_feedback/<int:examid>',views.add_feedback,name='add_feedback'),


]