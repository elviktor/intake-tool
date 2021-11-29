from django.contrib import admin

from .models import Entity, Issue, Keyword, Rating, Move, Script, Sequence, SequenceRecord, Area

admin.site.register(Entity)
admin.site.register(Issue)
admin.site.register(Keyword)
admin.site.register(Rating)
admin.site.register(Move)
admin.site.register(Script)
admin.site.register(Sequence)
admin.site.register(SequenceRecord)
admin.site.register(Area)
