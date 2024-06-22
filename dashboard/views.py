from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.contrib import messages
from .models import Test, Question, Choice, UserTestResult
from django.db.models import Count
# Create your views here.



def dashboard(request):
    tests = Test.objects.all().annotate(question_count=Count("question"))
    context = {"tests": tests}
    return render(request, 'dashboard/test.html', context=context)


@login_required(login_url="/auth/login/")
def profile(request):
    user = request.user

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")

        if not full_name:
            messages.error(request, "Full name is required.")
        elif not username:
            messages.error(request, "Username is required.")
        else:
            user.first_name = full_name
            user.username = username
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after the update
            messages.success(request, "Profile updated successfully.")

        return redirect('profile')

    context = {
        'user': user
    }
    return render(request, 'dashboard/profile.html', context)

@login_required(login_url="/auth/login/")
def test_add(request):
    test_name = ''
    test_description = ''
    question_choices = []  # Initialize an empty list for question_choices
    
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        test_description = request.POST.get('test_description')
        action = request.POST.get('action')
        question_text = request.POST.get('question')
        
        if not test_name.strip():  # Check if test_name is empty or contains only whitespace
            messages.error(request, 'Test Name is required.')
            return render(request, 'dashboard/test_add.html', {
                'test_name': test_name,
                'test_description': test_description,
                'question_choices': question_choices
            })
        # Retrieve or create the test
        test_id = request.POST.get('test_id')
        if test_id:
            new_test = Test.objects.get(id=test_id)
        else:
            new_test = Test.objects.create(name=test_name, description=test_description, owner=request.user)
        
        # Save the question only if it's not empty
        if question_text.strip():  # Check if the question text is not empty or contains only whitespace
            new_question = Question(test=new_test, question=question_text)
            new_question.save()
        
            # Save the choices associated with the question
            for option in ['a', 'b', 'c', 'd']:  # Use lowercase to match the form field names
                choice_text = request.POST.get(f'choice_text_{option}')
                is_correct = request.POST.get(f'is_correct_{option}') == 'on'  # Check for 'on' since it's a checkbox
                if choice_text:
                    choice = Choice(question=new_question, choice=choice_text, is_correct=is_correct, option=option.upper())
                    choice.save()
        
        if action == 'save_info':
            return redirect('dashboard')
        
        elif action == 'save_add_another':
            # Retrieve the questions associated with the current test
            questions = Question.objects.filter(test=new_test)
            
            # Retrieve the choices associated with each question
            for question in questions:
                choices = Choice.objects.filter(question=question)
                # Ensure all options 'a', 'b', 'c', 'd' are included
                all_choices = {choice.option.lower(): choice for choice in choices}
                complete_choices = []
                for option in ['a', 'b', 'c', 'd']:
                    if option in all_choices:
                        complete_choices.append(all_choices[option])
                    else:
                        complete_choices.append(Choice(option=option.upper(), question=question, choice='', is_correct=False))
                question_choices.append((question, complete_choices))
        
            # Pass the test name, description, and question_choices back to the template
            return render(request, 'dashboard/test_add.html', {
                'test_name': test_name,
                'test_description': test_description,
                'question_choices': question_choices,
                'test_id': new_test.id
            })
    
    # Pass the test name and description to the template for the initial rendering
    return render(request, 'dashboard/test_add.html', {
        'test_name': test_name,
        'test_description': test_description,
        'question_choices': question_choices  # Pass the empty question_choices list
    })

@login_required(login_url="/auth/login/")
def test_edit(request, test_id):

    test = Test.objects.get(id=test_id)
    if test.owner != request.user:
        messages.error(request, "You don't have permission to access this test.")
        return redirect("dashboard")
    questions = Question.objects.filter(test_id=test.id)

    #other edit code
    if request.method == "POST":
        name = request.POST.get("test_name")
        description = request.POST.get("test_description")

        question_choices = []
        for question in questions:
            choices = Choice.objects.filter(question=question)
            # Ensure all options 'a', 'b', 'c', 'd' are included
            all_choices = {choice.option.lower(): choice for choice in choices}
            
            complete_choices = []
            for option in ['a', 'b', 'c', 'd']:
                choice_text = request.POST.get(f"choice_text_{question.id}_{option}")
                is_correct = request.POST.get(f"is_correct_{question.id}_{option}") == "on"
                
                # Check if the choice text is not empty
                if choice_text:
                    choice = all_choices.get(option.lower())
                    # If choice already exists, update it
                    if choice:
                        choice.choice = choice_text
                        choice.is_correct = is_correct
                        choice.save()
                    # If choice doesn't exist, create and save it
                    else:
                        new_choice = Choice(option=option.upper(), question=question, choice=choice_text, is_correct=is_correct)
                        new_choice.save()
                        # Append new_choice to complete_choices
                        complete_choices.append(new_choice)
                else:
                    # If choice text is empty, append None to complete_choices
                    complete_choices.append(None)
            
            question_choices.append((question, complete_choices))





        test.name = name
        test.description = description
        test.save()

        return redirect("dashboard")

    question_choices = []
    for question in questions:
        choices = Choice.objects.filter(question=question)
        # Ensure all options 'a', 'b', 'c', 'd' are included
        all_choices = {choice.option.lower(): choice for choice in choices}
        complete_choices = []
        for option in ['a', 'b', 'c', 'd']:
            if option in all_choices:
                complete_choices.append(all_choices[option])
            else:
                complete_choices.append(Choice(option=option.upper(), question=question, choice='', is_correct=False))
        question_choices.append((question, complete_choices))
       

    return render(
        request,
        "dashboard/test_edit.html",
        context={
            "test": test,
            "question_choices": question_choices,
        },
    )


@login_required(login_url="/auth/login/")
def test_delete(request, test_id):
    test = Test.objects.get(id=test_id)
    if test.owner != request.user:
        messages.error(request, "You don't have permission to access this test.")
        return redirect("dashboard")
    if request.method == "POST":
        test.delete()
        return redirect("dashboard")

    return render(request, 'dashboard/test_delete.html', context={"test": test})


@login_required(login_url="/auth/login/")
def test_solve(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = Question.objects.filter(test=test)

    if request.method == "POST":
        user_answers = {}
        for question in questions:
            selected_options = request.POST.getlist(f'question{question.id}')
            user_answers[question.id] = [int(opt) for opt in selected_options]
        
        # Evaluate the answers
        score = 0
        for question_id, selected_options in user_answers.items():
            correct_options = set(Choice.objects.filter(question_id=question_id, is_correct=True).values_list('id', flat=True))
            if set(selected_options) == correct_options:
                score += 1

        # Build the URL with query parameters
        result_url = reverse('test_result', args=[test_id])
        result_url += f'?score={score}&total={len(questions)}'

        return redirect(result_url)

    return render(request, 'dashboard/test_solve.html', context={'test': test, 'questions': questions})

@login_required(login_url="/auth/login/")
def test_result(request, test_id):
    test = Test.objects.get(id=test_id)
    user = request.user

    show_previous_results = False
    score = int(request.GET.get('score', 0))
    total = int(request.GET.get('total', 1))
    percentage = (score / total) * 100 if total != 0 else 0

    if request.method == 'POST':
        if 'try_again' in request.POST:
            return redirect(reverse('test_solve', kwargs={'test_id': test_id}))
        elif 'view_results' in request.POST:
            # Filter for the first attempt result
            first_result = UserTestResult.objects.filter(user=user, test=test).order_by('date').first()
            previous_results = [first_result] if first_result else []
            show_previous_results = True
            context = {
                'test': test,
                'previous_results': previous_results,
                'test_id': test_id,
                'score': score,
                'total': total,
                'show_previous_results': show_previous_results,
                'user_name': user.get_full_name() or user.username,  # Using full name if available, otherwise username
            }
            return render(request, 'dashboard/result.html', context)



    # Save the result
    UserTestResult.objects.create(user=user, test=test, score=score, total=total, percentage=percentage)

    previous_results = UserTestResult.objects.filter(user=user, test=test).order_by('date').first()
    previous_results = [previous_results] if previous_results else []

    context = {
        'test': test,
        'score': score,
        'total': total,
        'percentage': percentage,
        'test_id': test_id,
        'previous_results': previous_results,
        'show_previous_results': show_previous_results,
        'user_name': user.get_full_name() or user.username,  # Using full name if available, otherwise username
    }
    return render(request, 'dashboard/result.html', context)

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))