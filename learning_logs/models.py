from django.db import models
from django.contrib.auth.models import User
# Created Topic model here.
class Topic(models.Model):
    """docstring for Topic."""
    text=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE)#default is added because without it we are getting error
    def __str__(self):
        return self.text

# Created Entry models
class Entry(models.Model):
    '''specific learned about a topic
    multiple entries associated with a Topic'''
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    #Meta class holds the extra information for managing a model
    class Meta:
        verbose_name_plural='entries'

    def __str__(self):
        '''Return the string representation of the model'''
        if len(self.text)>50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text[:50]}"
