from django.urls import path
from . import views

urlpatterns = [

  path('Admin_Dashboard',views.admindash,name='admindash'),
  path('create_exam_page',views.create_exam_page,name='create_exam_page'),
  path('save_exam',views.save_exam,name='save_exam'),
  path('delete_exam',views.delete_exam,name='delete_exam'),

  path('add_questions_page',views.add_questions_page,name='add_questions_page'),
  path('get_exam_data',views.get_exam_data,name='get_exam_data'),
  path('delete_question',views.delete_question,name='delete_question'),

  path('save_question',views.save_question,name='save_question'),
  path('admin_all_exam_list',views.admin_all_exam_list,name='admin_all_exam_list'),
  path('students',views.students,name='students'),
  path('exam_results',views.exam_results,name='exam_results'),
  path('exam_wise_results\<int:examid>',views.exam_wise_results,name='exam_wise_results'),
  path('view_feedback',views.view_feedback,name='view_feedback'),



]