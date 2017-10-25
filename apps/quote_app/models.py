from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[^\W_]+(-[^\W_]+)?$', re.U)

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = []
        if len(self.filter(email=postData['email'])) > 0:
            # check this user's password
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')
        if errors:
            return errors
        return user

    def register_validator(self,postData):
        errors = []
        # check name and last name length
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors.append("User name/last name should be more than 2 characters")
        # check password
        if len(postData['password']) < 8:
            errors.append("Password should have more than 8 characters")    
        #check name for character
        if not re.match(NAME_REGEX, postData['first_name']) or not re.match(NAME_REGEX, postData['last_name']):
            errors.append("User name/last name should contains only letters")
        # check email 
        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append("Invalid email format")
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("email already in use")
        # check password
        if postData['password'] != postData['confirm']:
            errors.append("Password doesn't match")
        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
            print "hashed code: ", hashed
            new_user = self.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed
            )
            return new_user
        return errors

# class QuoteManager(models.Manager):
#     def quote_validator(self, postData):
#         errors = []
#         # check quote and messange length
#         if len(postData['author']) < 3:
#             errors.append("'quoted by' requires more than 3 characters")
#         if len(postData['content']) < 10:
#             errors.append("'message' requires more than 10 characters")
        # if errors:
#         #     return errors
#         # if not errors:
#         #     # user = User.objects.get(id=request.session['user_id'])
#         #     quote = Quote.objects.create(
#         #         content = postData['content'],
#         #         author = postData['author'],
#         #         uploader = postData['user'],
#         #         favBoolean = False 
#         #     )
#         #     return quote
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.TextField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    def __repr__(self):
        return "User: --{}".format(self.first_name)

class Quote(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name='uploaded_quote')
    favorite = models.ManyToManyField(User, related_name='liked_quotes')
    favBoolean = models.BooleanField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # objects = QuoteManager()
    def __repr__(self):
        return "Quote: --{}, --uploader {}".format(self.content, self.uploader)