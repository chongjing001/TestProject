from django import forms

from article.models import Article


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=20, min_length=1,required=True)
    part = forms.CharField(required=True)
    tags = forms.CharField(max_length=15, required=True)
    content = forms.Textarea
    icon = forms.ImageField(required=True)

    def clean(self):
        title = self.cleaned_data.get('title')
        article = Article.objects.filter(a_title=title).first()
        if article:
            raise forms.ValidationError({'title':'文章标题重复'})
        return self.cleaned_data



