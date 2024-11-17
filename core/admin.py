from django.contrib import admin
from core.models.event import Event
from core.models.event_data_selection import EventDateSelection
from core.models.event_location_selection import EventLocationSelection
from core.models.meeting_group import MeetingGroup
from core.models.user import CustomUser
from core.models.group_member import GroupMember
from core.models.vote import Vote


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'is_active')
    search_fields = ('username',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Status', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active')},
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MeetingGroup)
admin.site.register(GroupMember)
admin.site.register(Event)
admin.site.register(EventDateSelection)
admin.site.register(EventLocationSelection)
admin.site.register(Vote)