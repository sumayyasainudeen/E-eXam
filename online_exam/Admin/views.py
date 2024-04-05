from datetime import date, timedelta
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from Admin.models import *
from student.models import *
from register_login.models import *
from django.contrib import messages

# Create your views here.

@login_required(login_url='login_page')
def admindash(request):
  return render(request, 'admindash.html')

@login_required(login_url='login_page')
def create_exam_page(request):
  exams_obj = Exams.objects.all()
  return render(request, 'create_exam_page.html',{'exams_obj':exams_obj})

def save_exam(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        number = request.POST.get('no_of_qn')
        duration = request.POST.get('duration')
        # score = request.POST.get('total_score')
        passing_score = request.POST.get('passing_score')

        exam_obj = Exams(
            exam_name=name,
            exam_date=date,
            no_of_questions=number,
            total_score=number,
            duration=duration,
            passing_score=passing_score

        )
        exam_obj.save()

        messages.info(request, 'Exam saved!')

        return redirect('create_exam_page')

    return render(request, 'create_exam_page.html')

def delete_exam(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        try:
            exam = Exams.objects.get(id=exam_id)
            all_questions = Questions.objects.filter(exam = exam)
            all_questions.delete()
            exam.delete()
            return JsonResponse({'success': True})
        except exam.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Exam does not exist.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
    

@login_required(login_url='login_page')
def add_questions_page(request):
  exams_obj = Exams.objects.all()
  return render(request, 'add_questions_page.html',{'exams_obj':exams_obj})

def get_exam_data(request):
  print('view')
  examid = request.POST['ex_id']
  exam = Exams.objects.get(id=examid)

  questions = Questions.objects.filter(exam=exam).values('id','question', 'answer', 'choice1', 'choice2', 'choice3')

  total_no_of_questions = exam.no_of_questions 
  questions_added = Questions.objects.filter(exam=exam).count()
  
  diff = int(total_no_of_questions) - questions_added
  next_qno = questions_added + 1

  return JsonResponse({'next_qno':next_qno,'total_no_of_questions':total_no_of_questions,'questions_added':questions_added,'questions':list(questions)})

def delete_question(request):
    if request.method == 'POST':
        print('delete')
        question_id = request.POST['question_Id']
        print(question_id)
        try:
            question = Questions.objects.get(id=question_id)
            question.delete()
            return JsonResponse({'success': True})
        except question.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Question does not exist.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def save_question(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam')
        qn = request.POST.get('question')
        ans = request.POST.get('answer')
        ch1 = request.POST.get('ch1')
        ch2 = request.POST.get('ch2')
        ch3 = request.POST.get('ch3')

        question_obj = Questions(
            exam_id=exam_id,
            question=qn,
            answer=ans,
            choice1=ch1,
            choice2=ch2,
            choice3=ch3
        )
        question_obj.save()

        messages.info(request, 'Question saved!')

        return redirect('add_questions_page')

    return render(request, 'add_questions_page.html')


@login_required(login_url='login_page')
def admin_all_exam_list(request):
 
    all_exams = Exams.objects.all().order_by('-id')

    for e in all_exams:
        e.students = ExamResults.objects.filter(exam=e).count()


    context= {
        'all_exams':all_exams,
        
        }

    return render(request, 'admin_all_exam_list.html',context)


def students(request):
 
    students = StudentDetails.objects.all().order_by('-id')

    for s in students:
        s.no_of_exam_atnded = ExamResults.objects.filter(student=s).count()

    context= {
        'students':students,
        
        }

    return render(request, 'students.html',context)


def exam_results(request):
 
    all_exam = Exams.objects.all().order_by('-id')

    context= {
        'all_exam':all_exam,
        
        }

    return render(request, 'exam_results.html',context)

def exam_wise_results(request,examid):
 
    exam_wise = ExamResults.objects.filter(exam_id = examid).order_by('-id')

    context= {
        'exam_wise':exam_wise,
        
        }

    return render(request, 'exam_wise_results.html',context)


def view_feedback(request):
 
    feedbacks = ExamFeedback.objects.all().order_by('-id')

    context= {
        'feedbacks':feedbacks,
        
        }

    return render(request, 'view_feedback.html',context)






