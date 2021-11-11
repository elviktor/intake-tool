from django.contrib import admin

from .models import Entity, Issue, Keyword, Rating, Move

admin.site.register(Entity)
admin.site.register(Issue)
admin.site.register(Keyword)
admin.site.register(Rating)
admin.site.register(Move)
