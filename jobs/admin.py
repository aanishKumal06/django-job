from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Job, Category, GenderChoices

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    
    # Custom styling for the admin panel
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
            'description': 'Basic information about the job category'
        }),
    )


class JobInline(TabularInline):
    model = Job
    extra = 0
    fields = ('title', 'location', 'salary', 'gender')
    readonly_fields = ('title', 'location', 'salary', 'gender')
    can_delete = False
    show_change_link = True


@admin.register(Job)
class JobAdmin(ModelAdmin):
    list_display = ('title', 'category', 'location', 'salary', 'gender_display', 'recruiter')
    list_filter = ('category', 'gender', 'location')
    search_fields = ('title', 'description', 'location', 'recruiter__email')
    raw_id_fields = ('recruiter',)  # Use raw_id_fields instead of autocomplete_fields for recruiter
    autocomplete_fields = ('category',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'recruiter'),
            'description': 'Basic job details'
        }),
        ('Job Details', {
            'fields': ('description', 'responsibilities', 'location', 'salary', 'gender'),
            'description': 'Detailed information about the job'
        }),
    )
    
    def gender_display(self, obj):
        return obj.get_gender_display()
    gender_display.short_description = 'Gender'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # If the user is not a superuser and is an agency, show only their jobs
        if not request.user.is_superuser and hasattr(request.user, 'is_agency') and request.user.is_agency:
            return queryset.filter(recruiter=request.user)
        return queryset

# Register the Category admin with the inline Job admin
CategoryAdmin.inlines = [JobInline]
