from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django import forms
from .models import User
import json
import requests
import csv
from random import randint, choice
from .models import User, Posts, Upvotes, Downvotes, Comments

# Landing page view
def index(request):
    return render(request, "final_project/index.html")


# Nutrition Page 
def recipe(request):
    if request.user.is_authenticated:
        # If user authenticated, all information is taken from his profile
        logged_in = 'true'
        current_user = get_object_or_404(User, username=request.user)
        height = current_user.height/100
        weight = current_user.weight
        age = current_user.age
        # Info gathered used to calculate BMI and BMR to calculate maintenance calories
        BMI = weight/pow(height,2)
        BMR = (10*weight) + (625*height) - (5*age) + 5
        recom_calories = (BMR * 1.575) + 600

        # This is used to decide if user is underweight, normal, or overweight, depending on the BMI of the user
        if BMI < 18.5:
            diet_label = 'high-protein'
        elif BMI >= 18.5 and BMI < 25:
            diet_label = 'balanced'
        elif BMI >=25 and BMI < 30:
            diet_label = 'low-carb'
        elif BMI >= 30:
            diet_label = 'low-fat'
    else:
        logged_in = 'false'
        weight = 60
        recom_calories = 3000
        diet_label = 'high-protein'

    
    # Small random list is used to ensure each time user goes to the nutrition page, the 'Meal of the day' is unique
    list_of_foods = ['egg', 'meat', 'chicken', 'fish']
    random_food = choice(list_of_foods)

    # Random integer used to get random item from the Edamam API
    rand_int = randint(0,12)

    res = requests.get("https://api.edamam.com/search", params={
        'app_id': settings.APP_ID,
        'app_key':settings.API_KEY,
        'q': random_food,
        'from': rand_int,
        'diet': diet_label
    })
    data = res.json()

    img = data['hits'][0]['recipe']['image']
    label = data['hits'][0]['recipe']['label']
    calories = data['hits'][0]['recipe']['calories']
    diet = data['hits'][0]['recipe']['dietLabels'][0]

    context={
        'img': img,
        'label':label,
        'calories':float("{:.2f}".format(calories)),
        'diet':diet,
        'recom_calories': float("{:.2f}".format(recom_calories)),
        'weight': weight,
        'logged_in': logged_in
    }

    return render(request, "final_project/recipe.html", context)




# View for gym logs, only special and professional users can access this
@login_required(login_url='/login')
@user_passes_test(lambda u: u.special_user or u.professional, login_url='/profile')
def fitness(request):
    return render(request, "final_project/fitness.html")



# This is used to create a CSV file of a gym log the user chooses to download
@login_required(login_url='/login')
@csrf_exempt
@user_passes_test(lambda u: u.special_user or u.professional, login_url='/profile')
def export(request, id):
    # Each id is for each different pre-made gym log
    if id == 1:
        # These all use the 'csv' library to create each row with the appropriate gym logs
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="PPL.csv"'

        writer = csv.writer(response)
        writer.writerow(['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'])
        writer.writerow(['Bench Press', 'Cable-Pull', 'Squat', 'Rest', 'Bench Press', 'Cable-Pull', 'Squat'])
        writer.writerow(['Incline Press', 'T-bar Row', 'Deadlift', 'Rest', 'Incline Press', 'T-bar Row', 'Deadlift'])
        writer.writerow(['Shoulder Press', 'Pull-Up', 'Leg Curl', 'Rest', 'Shoulder Press', 'Pull-Up', 'Leg Curl'])
        writer.writerow(['Lateral Raises', 'Hammer Curl', 'Leg Raises', 'Rest', 'Lateral Raises', 'Hammer Curl', 'Leg Raises'])
        writer.writerow(['Tricep Extension', 'Facepull', 'Ab Crunch', 'Rest', 'Tricep Extension', 'Facepull', 'Ab Crunch'])
    
    elif id == 2:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Upper-Lower.csv"'

        writer = csv.writer(response)
        writer.writerow(['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'])
        writer.writerow(['Bench Press', 'Squat', 'Rest', 'Rest', 'Bench Press', 'Squat', 'Rest'])
        writer.writerow(['Incline Press', 'Deadlift', '', '-', 'Incline Press', 'Deadlift', '-'])
        writer.writerow(['Cable Pulley', 'Leg Curl', '-', '-', 'Shoulder Press', 'Leg Curl', '-'])
        writer.writerow(['T-bar Row', 'Leg Raises', '-', '-', 'Cable Pulley', 'Leg Raises', '-'])
        writer.writerow(['Pull-up', 'Ab Crunch', '-', '-', 'T-bar Row', 'Ab Crunch', '-'])
        writer.writerow(['Shoulder Press', '-', '-', '-', 'Pull-Up', '-', '-'])

    elif id == 3:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Bro-Split.csv"'

        writer = csv.writer(response)
        writer.writerow(['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'])
        writer.writerow(['Bench Press', 'Shoulder Press', 'Lat Pulldown', 'Hammer Curls', 'Squat', 'Ab Crunches', 'Rest'])
        writer.writerow(['Incline Press', 'Lateral Raises', 'Cable Pulley', 'Spider Curls', 'Deadlift', 'Leg Raises', '-'])
        writer.writerow(['Chest Flys', 'Front Raises', 'T-bar Row', 'Tricep Extension', 'Lunges', 'Plank', '-'])
        writer.writerow(['-', '-', '-', 'Close-Grip Bench', 'Leg Curls', '-', '-'])

    return response



# This is used to create a gym log from scratch, rather than downloading a pre-made one
@login_required(login_url='/login')
@csrf_exempt
@user_passes_test(lambda u: u.special_user or u.professional, login_url='/profile')
def custom_export(request):
    if request.method == 'POST':
        days = int(request.POST["days"])

        if days == 3:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{days}day-Split.csv"'

            writer = csv.writer(response)
            writer.writerow(['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'])

            writer.writerow(['Bench Press', 'Rest', 'Hammer Curls', 'Rest', 'Lat Pulldown', 'Rest', 'Rest'])
            writer.writerow(['Incline Press', '-', 'Spider Curls', '-', 'Cable Pulley', '-', '-'])
            writer.writerow(['Day1', '-', 'Squat', '-', 'T-bar Rows', '-', '-'])
            writer.writerow(['Day1', '-', 'Deadlift', '-', 'Pull-ups', '-', '-'])
            writer.writerow(['Day1', '-', 'Lunges', '-', 'Triceps Extensions', '-', '-'])
            writer.writerow(['Day1', '-', 'Leg Curls', '-', 'Close-Grip Press', '-', '-'])

            return response
        
        elif days == 4:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{days}day-Split.csv"'

            writer = csv.writer(response)
            writer.writerow(['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'])

            writer.writerow(['Bench Press', 'Lat Pulldown', 'Rest', 'Hammer Curls', 'Squat', 'Rest', 'Rest'])
            writer.writerow(['Incline Press', 'Cable Pulley', '-', 'Spider Curls', 'Deadlift', '-', '-'])
            writer.writerow(['Chest Flys', 'T-Bar Rows', '-', 'Tricep Extensions', 'Lunges', '-', '-'])
            writer.writerow(['Soulder Press', 'Pull-ups', '-', 'Close-Grip Bench', 'Leg Curls', '-', '-'])
            writer.writerow(['Lateral Raises', 'Leg Raises', '-', 'Plank', '-', '-', '-'])
            writer.writerow(['Front Raises', 'Jumping Jacks', '-', '-', '-', '-', '-'])


            return response

        elif days == 5:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{days}day-Split.csv"'

            writer = csv.writer(response)
            writer.writerow(['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'])

            writer.writerow(['Bench Press', 'Lat Pulldown', 'Rest', 'Hammer Curls', 'Squat', 'Plank', 'Rest'])
            writer.writerow(['Incline Press', 'Cable Pulley', '-', 'Spider Curls', 'Deadlift', 'Leg Raises', '-'])
            writer.writerow(['Chest Flys', 'T-Bar Rows', '-', 'Tricep Extensions', 'Lunges', 'Jumping Jacks', '-'])
            writer.writerow(['Shoulder Press', 'Pull-ups', '-', 'Close-Grip Press', 'Leg Curls', '-', '-'])
            writer.writerow(['Lateral Raises', '-', '-', '-', '-', '-', '-'])
            writer.writerow(['Front Raises', '-', '-', '-', '-', '-', '-'])

            return response

        elif days == 6:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{days}day-Split.csv"'

            writer = csv.writer(response)
            writer.writerow(['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'])

            writer.writerow(['Bench Press', 'Shoulder Press', 'Lat Pulldown', 'Hammer Curls', 'Squat', 'Plank', 'Rest'])
            writer.writerow(['Incline Press', 'Lateral Raises', 'Cable Pulley', 'Spider Curls', 'Deadlift', 'Leg Raises', '-'])
            writer.writerow(['Chest Flys', 'Front Raises', 'T-Bar Rows', 'Tricep Extensions', 'Lunges', 'Jumping Jacks', '-'])
            writer.writerow(['-', '-', '-', 'Close-Grip Press', 'Leg Curls', '-', '-'])

            return response

    return HttpResponseRedirect(reverse("fitness"))



# This link is used to check if a certain user exists. This is used for the 'Register' Page, and is fetched by the JavaScript used
# This is to allow for dynamic validation checking
@csrf_exempt
def user_exist(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        username = data.get('username')
        user_check = User.objects.filter(username=username).exists()

        return JsonResponse({'user_exists': user_check})

    else:
        return JsonResponse({"error": "PUT request required!"}, status=400)




# This is used if a 'free' member wants to upgrade to a 'special' user. Can only be done if user pays $2.99 through PayPal
@csrf_exempt
def member_upgrade(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        username = data.get('username')
        username_update = get_object_or_404(User, username=username)
        username_update.special_user = True
        username_update.save()
        return JsonResponse({'complete': 'complete'})

    else:
        return JsonResponse({"error": "PUT request required!"}, status=400)




#This class based view is used for the 'discussions' page
class Discussions(ListView):
    template_name = 'final_project/discussions.html'
    model = Posts
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5

    # Function used for context data for the 'discussions.html' file
    def get_context_data(self, **kwargs):
        context = super(Discussions, self).get_context_data(**kwargs)
        upvoted_posts = []
        downvoted_posts = []

        if not self.request.user.is_authenticated:
            liked_posts = False
        else:
            current_user = self.request.user
            upvoted_list = Upvotes.objects.filter(liker=current_user).all()
            downvoted_list = Downvotes.objects.filter(liker=current_user).all()

            for upvoted in upvoted_list:
                upvoted_posts.append(upvoted.post)

            for downvoted in downvoted_list:
                downvoted_posts.append(downvoted.post)

        # Upvoted and Downvoted posts are stored into different arrays to be used by the html. This is to correctly put the votes of the user for the appropriate posts
        context.update({'upvoted_posts': upvoted_posts,'downvoted_posts': downvoted_posts})
        return context




# This view is used to check an individual post, to see the comments made on the post
def spec_post(request, id):
    post = Posts.objects.get(pk=id)
    spec_posts = Comments.objects.filter(post=post).all().order_by('-date')
    comments_exist = Comments.objects.filter(post=post).exists()

    context = {
        'post':post,
        'spec_posts':spec_posts,
        'comments_exist':comments_exist
    }

    return render(request, "final_project/spec_post.html", context)




# This link is used to create a post, this is also where a professional user can upload a reference Youtube video.
@login_required(login_url='/login')
def create_post(request, username):
    if request.method == 'POST':
        post_username = get_object_or_404(User, username=username)
        post_text = request.POST['post_text']
        flare = request.POST['flare']
        url = request.POST['url']

        # This is to help parse the link, remove the unnecessary parts, and replace with 'embed' to allow to be used in the HTML
        if 'https://www.youtube.com/watch?v=' in url:
            url = url.replace('watch?v=', 'embed/')
        else:
            url = 'None'


        if len(post_text) == 0:
            messages.warning(request, 'Cant post empty text!')
            return HttpResponseRedirect(reverse("discussions"))

        new_post = Posts.objects.create(content=post_text, author=post_username, flare=flare, video_url=url)
        new_post.save()
        return HttpResponseRedirect(reverse("discussions"))
    
    # Prevents accessing '/createpost/username' link directly
    messages.warning(request, 'Please write your post in the textarea below!')
    return HttpResponseRedirect(reverse("discussions"))



# This link is used for the creation of a comment, for each individual post
@login_required(login_url='/login')
def create_comment(request, username):
    if request.method == 'POST':
        commenter = get_object_or_404(User, username=username)
        comment = request.POST['comment']
        post_id = int(request.POST['post-id'])

        post = Posts.objects.get(pk=post_id)

        if len(comment) == 0:
            messages.warning(request, 'Cant comment empty text!')
            return redirect(f'/spec_post/{post_id}')

        new_comment = Comments.objects.create(post=post, commenter=commenter, comment=comment)
        new_comment.save()

        post.comment_count = Comments.objects.filter(post=post).count()
        post.save()
        return redirect(f'/spec_post/{post_id}')
    
    # Prevents accessing '/create_comment/username' link directly
    messages.warning(request, 'Please write your post in the textarea below!')
    return redirect(f'/spec_post/{post_id}')





# Function for the upvote button
@login_required(login_url='/login')
@csrf_exempt
def upvote(request):

    # Update whether post is liked
    if request.method == 'PUT':
        data = json.loads(request.body)
        post_id = data.get('id')
        upvoted = data.get('upvoted')
        downvoted = data.get('downvoted')

        post = Posts.objects.get(pk=post_id)


        # If both upvote and downvote is false, create a new upvote model
        if upvoted == 'false' and downvoted == 'false':
            upvote_complete = Upvotes.objects.create(liker=request.user, post=post)
            upvote_complete.save()
            count = (Upvotes.objects.filter(post=post_id).count()) - (Downvotes.objects.filter(post=post_id).count())
            post.likes = count
            post.save()

            return JsonResponse({'upvoted': True, 'downvoted': False, 'vote_count': count})

        # If downvote is true, delete the downvote model, and create an upvote model
        elif upvoted == 'false' and downvoted == 'true':
            upvote_complete = Upvotes.objects.create(liker=request.user, post=post)
            upvote_complete.save()

            downvote_complete = Downvotes.objects.get(liker=request.user, post=post)
            downvote_complete.delete()

            count = (Upvotes.objects.filter(post=post_id).count()) - (Downvotes.objects.filter(post=post_id).count())
            post.likes = count
            post.save()

            return JsonResponse({'upvoted': True, 'downvoted': False, 'vote_count': count})
        
        # If upvote is true, but downvote is false, delete the upvote
        elif upvoted == 'true' and downvoted == 'false':
            Upvote_complete = Upvotes.objects.get(liker=request.user, post=post)
            Upvote_complete.delete()

            count = (Upvotes.objects.filter(post=post_id).count()) - (Downvotes.objects.filter(post=post_id).count())
            post.likes = count
            post.save()

            return JsonResponse({'upvoted': False, 'downvoted': False, 'vote_count': count})
    
    else:
        return JsonResponse({"error": "PUT request required!"}, status=400)






# Function for downvote button (Similar to upvote function)
@login_required(login_url='/login')
@csrf_exempt
def downvote(request):

    # Update whether post is liked
    if request.method == 'PUT':
        data = json.loads(request.body)
        post_id = data.get('id')
        upvoted = data.get('upvoted')
        downvoted = data.get('downvoted')

        post = Posts.objects.get(pk=post_id)

        # If both upvote and downvote is false, create a new downvote model
        if upvoted == 'false' and downvoted == 'false':
            downvote_complete = Downvotes.objects.create(liker=request.user, post=post)
            downvote_complete.save()
            count = (Upvotes.objects.filter(post=post_id).count()) - (Downvotes.objects.filter(post=post_id).count())
            post.likes = count
            post.save()

            return JsonResponse({'upvoted': False, 'downvoted': True, 'vote_count': count})

        # If upvote is true, delete the upvote model, and create an downvote model
        elif upvoted == 'true' and downvoted == 'false':
            downvote_complete = Downvotes.objects.create(liker=request.user, post=post)
            downvote_complete.save()

            upvote_complete = Upvotes.objects.get(liker=request.user, post=post)
            upvote_complete.delete()

            count = (Upvotes.objects.filter(post=post_id).count()) - (Downvotes.objects.filter(post=post_id).count())
            post.likes = count
            post.save()

            return JsonResponse({'upvoted': False, 'downvoted': True, 'vote_count': count})
        
        # If upvote is false, but downvote is true, delete the downvote
        elif upvoted == 'false' and downvoted == 'true':
            downvote_complete = Downvotes.objects.get(liker=request.user, post=post)
            downvote_complete.delete()

            count = (Upvotes.objects.filter(post=post_id).count()) - (Downvotes.objects.filter(post=post_id).count())
            post.likes = count
            post.save()

            return JsonResponse({'upvoted': False, 'downvoted': False, 'vote_count': count})
    
    else:
        return JsonResponse({"error": "PUT request required!"}, status=400)





# Function is used for deletion of posts. Only the user who created the post can delete that post
@login_required(login_url='/login')
@csrf_exempt
def delete(request):

    # Update whether post is liked
    if request.method == 'PUT':
        data = json.loads(request.body)
        post_id = data.get('id')

        post = Posts.objects.get(pk=post_id)

        if request.user == post.author:
            post.delete()
            return JsonResponse({'alert': 'success'})

        else:
            return JsonResponse({'alert':'failed to delete post'})
    
    else:
        return JsonResponse({"error": "PUT request required!"}, status=400)




# Function similar to the delete function, but used for comments on specific posts
@login_required(login_url='/login')
@csrf_exempt
def delete_comment(request):

    # Update whether post is liked
    if request.method == 'PUT':
        data = json.loads(request.body)
        comment_id = data.get('id')

        comment = Comments.objects.get(pk=comment_id)

        if request.user == comment.commenter:
            comment.delete()
            return JsonResponse({'alert': 'success'})

        else:
            return JsonResponse({'alert':'failed to delete post'})
    
    else:
        return JsonResponse({"error": "PUT request required!"}, status=400)















# Used for creating the update form for the profile page, helps when paired with the 'crispy-forms' library used in 'profile.html'
class UserUpdate(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'height', 'weight', 'age', 'pic']


# Link for the profile view
@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        form = UserUpdate(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated!')
            return redirect('profile')
        else:
            messages.warning(request, 'Something went wrong! Please double check your values.')

        return render(request, "final_project/profile.html", {
            'form':form,
        })

    form = UserUpdate(instance=request.user)
    return render(request, "final_project/profile.html", {
        'form':form
    })



# Login function based view
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "final_project/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "final_project/login.html")


# Register function based view
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        type_user = request.POST['pick-user']

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "final_project/register.html", {
                "message": "Passwords must match."
            })

        # Checks the type of user chosen in the registration, and creates the appropriate user
        if type_user == 'Free':
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "final_project/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        elif type_user == 'Paid':
            try:
                user = User.objects.create_user(username, email, password)
                user.special_user = True
                user.save()
            except IntegrityError:
                return render(request, "final_project/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        elif type_user == 'Professional':
            try:
                cv_link = request.POST['cv']
                user = User.objects.create_user(username, email, password)
                user.cv = cv_link
                user.professional = True
                user.is_active = False
                user.save()
            except IntegrityError:
                return render(request, "final_project/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "final_project/register.html")



# Function used for the logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))