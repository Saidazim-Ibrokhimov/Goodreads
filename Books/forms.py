from django import forms
from Books.models import BookReview, Shelf

class BookReviewForm(forms.ModelForm):
	stars_given = forms.IntegerField(min_value=1, max_value=5)
	class Meta:
		model = BookReview
		fields = ('stars_given', 'comment')

# class WantToReadShelveForm(forms.ModelForm):
# 	class Meta:
# 		model = BookShelves

class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].choices = [
            ('currently_reading', 'Currently Reading'),
            ('want_to_read', 'Want to Read'),
        ]




