from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['text']
        labels={'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        lables={'text':'Entry:'}
        #widgets are HTML form element like textarea, dropdown, radio button
        widgets={'text': forms.Textarea(attrs={'cols':80})}
