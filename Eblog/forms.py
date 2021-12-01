from django import forms
from .models import *
from mptt.forms import TreeNodeChoiceField

#Django built in ModelForm automatically creates a model in database defining a form containing
#fields asscoiated with the model instance fields
class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

 #this function 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#here we remove parent element in page
        self.fields['parent'].widget.attrs.update(  #remove the select option
            {'class': 'd-none'})
        self.fields['parent'].label = ''#remove the label element for parent(text wont appear)
        self.fields['parent'].required = False #to remove input required atttribute for parent so its gonna be optional

    class Meta:
        model = Comment
        fields = ( 'parent', 'content')

#widrgets allow styling and customization of html elements
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
        
'''
class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False
    
class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title',  'content', 'thumbnail', 
        'category', 'featured', 'previous_post', 'next_post')
        
        #fields="__all__"
'''    

