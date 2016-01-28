from django.contrib import admin
from paw.models import TextLink, IconLink, IconFolder, Page, PageTextLink, PageIconDisplay, IconFolderIcon, EntryPoint
from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline, SortableTabularInline, SortableAdmin

class PageTextLinkInline(SortableStackedInline):
  model = PageTextLink
  extra = 1

class PageIconDisplayInline(SortableTabularInline):
  model = PageIconDisplay
  extra = 1
  
  fields = ['icon', 'icon_thumbnail']
  readonly_fields = ['icon_thumbnail']
  
  def icon_thumbnail(self, o):
      return '<img src="{url:}" />'.format(url=o.icon.display_icon.thumbnail['50x50'].url)
  
  icon_thumbnail.short_description = 'Thumbnail'
  icon_thumbnail.allow_tags = True
  
class IconFolderIconInline(SortableTabularInline):
  model = IconFolderIcon
  extra = 1
  
  def icon_thumbnail(self, o):
    return '<img src="{url:}" />'.format(url=o.icon.display_icon.thumbnail['50x50'].url)
  
  icon_thumbnail.short_description = 'Thumbnail'
  icon_thumbnail.allow_tags = True
  
  
  fields = ['icon', 'icon_thumbnail']
  readonly_fields = ['icon_thumbnail']

class PageAdmin(NonSortableParentAdmin):
  inlines = [PageIconDisplayInline, PageTextLinkInline]
  
  prepopulated_fields = {"slug": ("title",)}

class IconFolderAdmin(NonSortableParentAdmin):
  inlines = [IconFolderIconInline]
  
  list_display = ['title', 'admin_icon']
  readonly_fields = ['form_icon']
  
  def admin_icon(self, o):
    return '<img src="{url:}" />'.format(url=o.display_icon.thumbnail['50x50'].url)
  
  def form_icon(self, o):
    return '<img src="{url:}" />'.format(url=o.display_icon.thumbnail['100x100'].url)
    
  admin_icon.short_description = 'Icon'
  admin_icon.allow_tags = True
  
  form_icon.short_description = 'Thumbnail'
  form_icon.allow_tags = True
  
  
  fields = ['display_icon', 'form_icon', 'title', 'internal_description']

class IconLinkAdmin(admin.ModelAdmin):
  list_display=['title', 'admin_icon']
  fields = ['display_icon', 'form_icon', 'title', 'internal_description', 'url', 'check_url', 'start_hidden', 'mac_pc_only']
  readonly_fields = ['form_icon']
  
  def admin_icon(self, o):
    return '<img src="{url:}" />'.format(url=o.display_icon.thumbnail['50x50'].url)
  
  def form_icon(self, o):
    return '<img src="{url:}" />'.format(url=o.display_icon.thumbnail['100x100'].url)
    
  admin_icon.short_description = 'Icon'
  admin_icon.allow_tags = True
  
  form_icon.short_description = 'Thumbnail'
  form_icon.allow_tags = True

class EntryPointAdmin(admin.ModelAdmin):
  list_display=['__str__', 'page']
  
# Register your models here.
admin.site.register(TextLink)
admin.site.register(Page, PageAdmin)
admin.site.register(IconLink, IconLinkAdmin)
admin.site.register(IconFolder, IconFolderAdmin)
admin.site.register(EntryPoint, EntryPointAdmin)
