from django.db import models
from django.core.exceptions import ValidationError

from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable

from versatileimagefield.fields import VersatileImageField

from django.core.urlresolvers import reverse

import uuid
import os

def iconUploadTo(instance, filename):
  originalName, ext = os.path.splitext(filename)
  newName = "{uuid:}{ext:}".format(uuid=uuid.uuid4().hex, ext=ext)
  
  return os.path.join("icons", newName)

class TextLink(models.Model):
  title = models.CharField(max_length=255)
  explicit_url = models.CharField(max_length=4096, blank=True)
  page_link = models.ForeignKey('Page', blank=True, null=True)
  
  @property
  def url(self):
    if self.explicit_url:
      return self.explicit_url
    
    if self.page_link:
      return reverse('paw_static', kwargs={'slug': self.page_link.slug})
  
  def clean(self):
    if not self.explicit_url and not self.page_link:
      raise ValidationError('Either explicit URL or page link must be filled')
    
    if self.explicit_url and self.page_link:
      raise ValidationError('Only one of explicit URL or page link must be filled')
  
  def __str__(self):
    return self.title
  
class PageIcon(models.Model):
  icon_height = models.IntegerField(blank=True, null=True)
  icon_width = models.IntegerField(blank=True, null=True)
  display_icon = VersatileImageField(height_field='icon_height', width_field='icon_width', upload_to=iconUploadTo)
   
  check_url = models.URLField(max_length=4096, blank=True)
  start_hidden = models.BooleanField(default=False)
  
  title = models.CharField(max_length=255)
  
  classAttr = models.CharField(max_length=255)
  href = models.CharField(max_length=4096)
  
  internal_description = models.CharField(max_length=255, blank=True)

  class Meta:
    ordering = ['title']
  
  def __str__(self):
    if self.internal_description:
      return self.internal_description
      
    return self.title

# Create your models here.
class IconLink(PageIcon):
  url = models.CharField(max_length=4096)
  
  def clean(self):
    self.href = self.url
    self.classAttr = "iconLink"
  
class IconFolder(PageIcon):
  uuid = models.CharField(max_length=32)
  
  def icons(self):
    return [iconFolderIcon.icon for iconFolderIcon in IconFolderIcon.objects.filter(iconFolder=self).all()]
  
  def clean(self):
    if not self.uuid:
      self.uuid = uuid.uuid4().hex
      
    self.href = "div#%s" % self.uuid  
    self.classAttr = 'dialogLauncher'
      
class IconFolderIcon(Sortable):
  iconFolder = models.ForeignKey(IconFolder)
  icon = SortableForeignKey(IconLink)

class Page(models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  
  def get_absolute_url(self):
    return reverse('paw_static', kwargs={'slug': self.slug})
  
  def __str__(self):
    return self.title

class PageTextLink(Sortable):
  page = models.ForeignKey(Page)
  text_link = SortableForeignKey(TextLink)
  
  POSITIONCHOICES = (('LEFT', 'Left'), ('RIGHT', 'Right'))
  
  position = models.CharField(max_length=max([len(c[0]) for c in POSITIONCHOICES]), choices=POSITIONCHOICES)
  
  def __str__(self):
    return str(self.text_link)

class PageIconDisplay(Sortable):
  page = models.ForeignKey(Page)
  icon = SortableForeignKey(PageIcon)
  
  def __str__(self):
    return str(self.icon)

class EntryPoint(models.Model):
    domain = models.CharField(max_length=254, unique=True, blank=True)
    page = models.ForeignKey(Page)
    
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        
        self.domain = self.domain.lower()
        
    def __str__(self):
        if self.domain:
            return self.domain
        else:
            return "Default"