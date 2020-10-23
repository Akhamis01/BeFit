from django.contrib import admin
from .models import User, Posts, Upvotes, Downvotes, Comments

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Upvotes)
admin.site.register(Downvotes)
admin.site.register(Comments)


