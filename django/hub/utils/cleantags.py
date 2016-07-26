# coding: utf-8

class CleanTagsMixin(object):

    def clean_tags(self):
        return [tag.lower() for tag in self.cleaned_data.get('tags', [])] 
