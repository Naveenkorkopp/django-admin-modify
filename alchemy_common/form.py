from django import forms


class CustomerSegmentForm(forms.Form):
    name = forms.CharField(
        max_length=128,
        min_length=4,
        strip=True
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 10})
    )
