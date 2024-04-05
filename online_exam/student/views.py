from datetime import date, timedelta
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from register_login.models import *
from Admin.models import *
from django.contrib import messages
import random


# Create your views here.

def student_dash(request):
  if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)

        return render(request, 'student_dash.html',{'student_det':student_det})


def exam_list(request):
  if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)

        all_exams = Exams.objects.filter(exam_date = date.today()).order_by('-id')

        attempted_exams = ExamResults.objects.filter(student=student_det).values_list('exam_id', flat=True)
        current_date = date.today()

        context= {
            'all_exams':all_exams,
            'student_det':student_det,
            'attempted_exams':attempted_exams,
            'current_date':current_date
            }

        return render(request, 'exam_list.html',context)


def exam_introduction(request,examid):
  if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)

        exam = Exams.objects.get(id = examid)

        context= {
            'exam':exam,
            'student_det':student_det
        }

        return render(request, 'exam_introduction.html',context)




def start_exam(request, examid):
    if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)

        exam = Exams.objects.get(id=examid)
        all_questions = Questions.objects.filter(exam=exam)

        qn_atmpted_without_exam_submission =  QuestionsAttended.objects.filter(exam=exam, student=student_det) 
        qn_atmpted_without_exam_submission.delete()

        # Shuffle options for each question
        for question in all_questions:
            options = [question.choice1, question.choice2, question.choice3, question.answer]
            random.shuffle(options)
            question.shuffled_options = options

        attempted_questions = QuestionsAttended.objects.filter(exam=exam, student=student_det).values_list('question_id', flat=True)

        context= {
            'exam': exam,
            'student_det': student_det,
            'all_questions': all_questions,
            'attempted_questions':attempted_questions
        }

        return render(request, 'start_exam.html', context)
    else:
        return redirect('/')  # Redirect to login page if user is not logged in
    



def submit_answer(request):

    if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)

        if request.method == 'POST':
            qid = request.POST.get('qid')
            selected_option = request.POST.get('choice')

            

            question = Questions.objects.get(id = qid)
            exam = Exams.objects.get(id=question.exam_id)
            all_questions = Questions.objects.filter(exam=exam)

            if selected_option == question.answer:
                status = 'True'
            else:
                status = 'False'

            if QuestionsAttended.objects.filter(question=question,exam=exam, student=student_det).exists():
                qa = QuestionsAttended.objects.get(question=question,exam=exam, student=student_det)
                qa.answer=selected_option
                qa.answer_status=status
                qa.save()

            else:
                result = QuestionsAttended(exam=exam,
                                        question=question,
                                        student=student_det,
                                        answer=selected_option,
                                        answer_status=status)
                result.save()

            attempted_questions = QuestionsAttended.objects.filter(exam=exam, student=student_det).values_list('question__id', flat=True)

            return JsonResponse({'success': True, 'message': 'Answer submitted successfully', 'attempted_questions': list(attempted_questions)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})



def submit_exam(request, examid):
    if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)
        
        exam = Exams.objects.get(id=examid)

        attempted = QuestionsAttended.objects.filter(exam=exam, student=student_det).count()

        correct_answers = QuestionsAttended.objects.filter(exam=exam, student=student_det, answer_status= 'True').count()

        if correct_answers >= exam.passing_score:
            exam_status = 'Passed'
        else:
            exam_status = 'Failed'

        total_score = exam.no_of_questions
        score = correct_answers
        percentage_score = (score / total_score) * 100 if total_score != 0 else 0

        print(total_score)
        print(score)
        print(percentage_score)

        if ExamResults.objects.filter(exam=exam,student=student_det).exists():

            exam_result = ExamResults.objects.get(exam=exam,student=student_det)
            re_submit = 1
        
        else:
            exam_result = ExamResults(exam=exam,
                                    student=student_det,
                                    questions_attempted=attempted,
                                    score=correct_answers,
                                    exam_status=exam_status)
            exam_result.save()
            re_submit = 0
        

        context= {
            'exam': exam,
            'student_det': student_det,
            'exam_result':exam_result,
            'percentage_score':percentage_score,
            're_submit':re_submit
        }

        return render(request, 'submit_exam.html', context)
    else:
        return redirect('/') 


def review_result(request, examid):
    if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)
        
        exam = Exams.objects.get(id=examid)
        all_questions = Questions.objects.filter(exam=exam)

        attempted = QuestionsAttended.objects.filter(exam=exam, student=student_det)

        for aq in all_questions:
            try:
                question_attended = QuestionsAttended.objects.get(exam=exam, student=student_det, question=aq)
                aq.marked_ans = question_attended.answer
            except QuestionsAttended.DoesNotExist:
                aq.marked_ans = 'not answered'

        context= {
            'exam': exam,
            'student_det': student_det,
            'all_questions':all_questions
        }

        return render(request, 'review_result.html', context)
    else:
        return redirect('/') 


def exam_attended(request):
  if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)


        attempted_exams = ExamResults.objects.filter(student=student_det).order_by('-id')

        for a in attempted_exams:
            a.percentage = (a.score/a.exam.no_of_questions) * 100 if a.exam.passing_score != 0 else 0

        context= {
            'student_det':student_det,
            'attempted_exams':attempted_exams
            }

        return render(request, 'exam_attended.html',context)



def all_exam_list(request):
  if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)

        all_exams = Exams.objects.all().order_by('-id')

        attempted_exams = ExamResults.objects.filter(student=student_det).values_list('exam_id', flat=True)

        current_date = date.today()

        context= {
            'all_exams':all_exams,
            'student_det':student_det,
            'attempted_exams':attempted_exams,
            'current_date':current_date
            }

        return render(request, 'exam_list.html',context)


def add_feedback(request,examid):

    if 'login_id' in request.session:
        login_id = request.session['login_id']

        if 'login_id' not in request.session:
            return redirect('/') 
        
        student_det = StudentDetails.objects.get(id=login_id)

        exam = Exams.objects.get(id=examid)

        if request.method == 'POST':
            text = request.POST.get('feedback')

            feedback = ExamFeedback(exam = exam,
                                    student = student_det,
                                    feedback = text,
                                    date = date.today())
            feedback.save()

            all_questions = Questions.objects.filter(exam=exam)

            attempted = QuestionsAttended.objects.filter(exam=exam, student=student_det)

            for aq in all_questions:
                try:
                    question_attended = QuestionsAttended.objects.get(exam=exam, student=student_det, question=aq)
                    aq.marked_ans = question_attended.answer
                except QuestionsAttended.DoesNotExist:
                    aq.marked_ans = 'not answered'

            context= {
                'exam': exam,
                'student_det': student_det,
                'all_questions':all_questions
            }

            messages.info(request, 'Feedback sent!')
            return render(request, 'review_result.html', context)
        else:
            return redirect('/') 




