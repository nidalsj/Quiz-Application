from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Quiz, Option, Question
import random
from random import shuffle


# Create your views here.

def home(request):

    categories = Category.objects.all()

    if request.method=='POST':
        candidate_name=request.POST.get('candidate_name')
        category_id=request.POST.get('category')
        difficulty=request.POST.get('difficulty')

        if not candidate_name or not category_id or not difficulty:
            return render(request, 'home.html', {'categories': categories, 'error_message': 'All fields are required.'})

        #new quiz instance for the user
        selected_category = Category.objects.get(id=category_id)
        quiz=Quiz.objects.create(
            candidate_name=candidate_name,
            category=selected_category,
            difficulty=difficulty
        )

        return redirect('quiz',quiz_id=quiz.id)

    context={'categories': categories,}

    return render(request, 'index.html', context)

def quiz(request, quiz_id):
    quiz_instance = get_object_or_404(Quiz, id=quiz_id)

    questions = Question.objects.filter(
        category=quiz_instance.category,
        difficulty=quiz_instance.difficulty
    ).order_by('?')[:10]

    # store the questions in the session to keep track of progress
    request.session['questions'] = [question.id for question in questions]
    request.session['current_question_index'] = 0
    request.session['quiz_id'] = quiz_id

    current_question_id = request.session['questions'][0]
    current_question = get_object_or_404(Question, id=current_question_id)

    context = {
        'quiz_instance': quiz_instance,
        'current_question': current_question,
        'question_number': 1,
    }

    return render(request, 'quiz.html', context)



def submit_answer(request):
    if request.method == 'POST':
        quiz_id = request.session.get('quiz_id')
        current_question_index = request.session.get('current_question_index', 0)
        selected_option_id = request.POST.get('answer')

        # retrieve the quiz and current question
        quiz_instance = get_object_or_404(Quiz, id=quiz_id)
        current_question_id = request.session['questions'][current_question_index]
        current_question = get_object_or_404(Question, id=current_question_id)

        # check if the selected option is correct
        selected_option = get_object_or_404(Option, id=selected_option_id)
        if selected_option.is_correct:
            quiz_instance.score += 1

        # move to the next question
        current_question_index += 1
        request.session['current_question_index'] = current_question_index

        # check if all questions have been answered
        if current_question_index < len(request.session['questions']):
            next_question_id = request.session['questions'][current_question_index]
            next_question = get_object_or_404(Question, id=next_question_id)

            context = {
                'quiz_instance': quiz_instance,
                'current_question': next_question,
                'question_number': current_question_index + 1,  # Adjusted to display the correct question number
            }

            return render(request, 'quiz.html', context)
        else:
            # all questions answered, redirect to the result page
            quiz_instance.save()
            return redirect('result', quiz_id=quiz_id)




def result(request, quiz_id):
    quiz_instance = get_object_or_404(Quiz, id=quiz_id)

    context = {
        'quiz_instance': quiz_instance,
    }

    return render(request, 'result.html', context)

