# Fitness Blog Website

*In this project, I created a website that helps users, as the title suggests, **BeFit!**. So, essentially the website gives users the option to either check out recipes of any types of food wanted, create a fitness log, or enter a discussions forum with other users. Also, the user has the option to either register as a 'Free', 'Special', or 'Professional' user.*

[Here is a Demo of my project](https://youtu.be/pv9qL7vmrKE)

>*There are 6 main elements in my webpage (The **Landing Page**, **Profile Page**, **Nutrition Page**, **Fitness Logs Page**, and **Discussions Page**). Also, all files included use `'layoutt.css'` for CSS properties.*

# Files:
### Please note, all files have been well commented
static Folder: `registration.js, nutrition01.js, discussions.js, layoutt.css, (Images_used).`

- `Images_used Folder:` Stores all images used for the 'fitness.html' file

- `Layoutt.css:` Includes the styling of all elements in all .html files, and incluces the mobile responsiveness attibutes.

- `registration.js:` Includes the dynamic validation checks for the register.html file. It checks if user already exists, and if passwords are incorrect without user having to submit page. Also adds client-side PayPal integration.
- `nutrition01.js:` Used for the 'recipe.html' file, to create the interactive PieChart, and swtching items in carousel, and for fetching the Edamam API. Also implements dynamic reloading functionality, so when user scrolls down, the cards start to reload. Also, adds some loading sequences to a few functions.
- `discussions.js:` This file is used to allow for upvote/downvote and deleting posts functionality.

---

media Folder: Has `profile_pics` directory, and `default.jpg`. 'default.jpg' is the default profile picture for a new user. The 'profile_pics' directory stores all profile pictures used by existing users.

---

templates folder: `(index, login, register, profile, recipe, fitness, discussions, spec_post).html.`

>Note: All .html files are explained in further detail in the Elements section of the README.md file

- `profile.html:` User can edit information, and add profile picture

- `recipe.html:` Includes food imformation in carousel, weight goal piechart, and food recipe search
- `fitness.html:` Includes Fitness Logs which are generated as CSV files, which users can download
- `discussions.html:` Includes page to add posts, upvote/downvote posts, add comments, and video embedding.

- `spec_post.html:` This is part of the 'discussions.html' file. This file is used to display an invidual post, to show the comments made on that specific post. This can be accessed by clicking the 'comments' icon from the discussions page.

---

`settings.py:` Has the neccessary API ID and API Key to be used for the Edamam API. Note: if you would like to clone this project and run it for yourself, you must have your own edamam API ID and Key. It can be easily generated [here](https://developer.edamam.com/)

---
# Elements:

## Landing Page:
>File(s) and Views Used: **`index.html, views.index`**

This is where the user finds himself/herself redirected to when logging into the webpage, or registering as a new user.

---

## Login Page:
>File(s) and Views Used: **`login.html, views.login`**

In this page, an existing user can regularly login to the website.

---

## Register Page:
>File(s) and Views Used: **`register.html, registration.js, views.register`**

>API Used: **PayPal API**

In this page, an interested user can create a new account. In this page, the user can either pick to be a 'Free', 'Special', or 'Professional' user. Each user has different accesses and privileges in the website. This page also takes advantage of the PayPal API to allow for secure payments.

* To register as a 'Free' user, the client can register like normal, and pick 'normal user' from the dropdown menu

* To register as a 'Special' user, the client must pay $2.99 through PayPal **(I have created a sandbox account for use if needed.)**

* To register as a 'Professional' user, the client must put a link to their CV, or their LinkedIn profile. From there, the user will not be able to login until it has been authenticated by an admin. The admin can then add him as an 'active user' if they feel is appropriate.

* This page also uses dynamic validation, so the user knows if information being input is incorrect before they register.

---

## Profile Page:
>File(s) and Views Used: **`profile.html, views.profile, views.member_upgrade`**

>API Used:  **PayPal API**

*This is where the user can change basic information about himself/herself, and also add important info such as **height, weight, and age** which is later used to calculate the BMI (Body Mass Index) and BMR (Body Mass Ratio) to help determine the right nutritional information, which is used in the `Nutrition` Page.* You can also add a profile picture, which uses the **Pillow** Library in Python. Also, a 'free' user can upgrade their membership to a 'special' user from this page.

---

## Nutrition Page:
>File(s) and Views Used: **`recipe.html, nutrition01.js, views.recipe`**

>API Used: **Edamam API**

This page has many components, which are all focused on giving the user tips to gain/lose weight, and gives the user nutritional information about different types of food that may interest them. This page also takes advantage of the Edamam API, which allows the webpage to gather nutritional information, such as Calories, Diet Labels, Health Labels, etc. 

* At the top of the page, there's a carousel labeled 'Meal Of The Day' which shows the suggested meals, displaying the appropriate picture, and nutritional information (Which is fetched by the Edamam API). This carousel also takes into account the user's BMI, BMR, and age (Fetched from the `Profile` Page) to suggest what it thinks is most appropriate meal for the user.

* Also, there's another element which asks the user to input their weight goal. Then is then used to calculate the amount of nutrients needed to intake per day to eventually achieve this goal. It gives you a PieChart with each nutrient, and gives you a small card showing you methods to either gain/lose weight, depending on your current weight.

* Furthermore, there's a search recipe input at the bottom of the page, which can be used by the user to search for a certain food's recipe. This will give a detailed information card for each food, displaying the calories, nutrients, and more! Also, it uses dynamic reloading, so when scrolled to the end of the page, more foods will be loaded. You can also filter out your search results using the filter button. Overall, this also takes advantage of the **Edamam API**.

---

## Fitness Logs Page:
>File(s) and Views Used: **`fitness.html, views.fitness, views.export, views.custom_export`**

This page is used to help the user create a fitness log, for the neccessary exercises needed to be performed per week.

* The user has the option to download a CSV file of some pre-made fitness logs created by the website.

* Also, if the user would like to create a fitness log from scratch, they can go to the bottom of the page, where they can choose how many days a week they'd like to exercise, and can download the appropriate fitness log CSV file for further use.

* This page can ONLY be accessed by special and professional users to give them some exclusivity. A free user would have to upgrade their membership.

---

## Discussions Page:
>File(s) and Views Used: **`discussions.html, spec_post.html, discussions.js, views.(create_post, create_comment, upvote, downvote, delete, delete_comment)`**

This page is a small forum, where users can create small posts asking either general questions, or creating informative posts.

* The textarea for adding a post takes advantage of the 'CKEditor' Library, which allows the user to customize the text being entered into the textarea.

* Users have the ability to upvote and downvote posts, similar to the popular website, 'Reddit'.

* Professional users have the ability to add a Youtube link, which is embedded into the post, to further create informative posts, and to give them some exclusivity.

* The type of users are highlighted on hover of the image icon of the user, or by the borders shown to the right of the profile image.

* Users can press the 'comments' icon, to see the specific post made, and see comments made by other users. Also, they have the option to delete a post/comment if wanted.

---

# Additional Information:
To run this project, you need to:

- Install the appropriate libraries from the 'requirements.txt' file. It includes the *Pillow, Django-Crispy-Forms, and Request Libraries*

- The Edamam API Requires an **API ID** and **API Key** to be used. I have left some indications on where to put the API ID and API Key in the `settings.py` file (Line 131-132), the `nutrition01.js` file (Lines 46, 169, and 195).

- To create a special user, you must pay $2.99 through PayPal in either the registration page, or profile page. If you'd like to create a special user, you can use the sandbox PayPal account I have created to pay $2.99 fee. If you'd like to use it, you must have created a PayPal sandbox account:
