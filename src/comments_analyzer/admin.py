from django.contrib import admin
from .models import YoutubeVideo, YoutubeComment, AnalysisSession

# Register your models here.

admin.site.register(YoutubeVideo)
admin.site.register(YoutubeComment)
admin.site.register(AnalysisSession)
