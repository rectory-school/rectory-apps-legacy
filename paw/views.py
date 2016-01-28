from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from paw.models import Page, IconFolder, PageTextLink, PageIconDisplay, EntryPoint

from django.views.decorators.cache import cache_page

def _getPageDict(page):
  iconFolders = IconFolder.objects.all()
  leftText = [pageTextLink.text_link for pageTextLink in PageTextLink.objects.filter(page=page, position='LEFT')]
  rightText = [pageTextLink.text_link for pageTextLink in PageTextLink.objects.filter(page=page, position='RIGHT')]
  
  icons = [pageIconDisplay.icon for pageIconDisplay in PageIconDisplay.objects.filter(page=page)]
  
  return {'page': page, 'icons': icons, 'iconFolders': iconFolders, 'leftText': leftText, 'rightText': rightText}
  
@cache_page(5)
def static(request, slug):
  page = get_object_or_404(Page, slug=slug)
  
  return render(request, 'static.html', _getPageDict(page))

def page_for_email(request):
    email = request.GET.get("email")
    if email:
        parts = email.lower().split("@", 1)
        user = parts[0]
        
        if len(parts) == 2:
            domain = parts[1]
        else:
            domain = None
    else:
        user = None
        domain = None
        
    if domain:
        try:
            entry_point = EntryPoint.objects.get(domain=domain)
        except EntryPoint.DoesNotExist:
            try:
                entry_point = EntryPoint.objects.get(domain="")
            except EntryPoint.DoesNotExist:
                entry_point = None
    else:
        try:
            entry_point = EntryPoint.objects.get(domain="")
        except EntryPoint.DoesNotExist:
            entry_point = None
            
    if entry_point:
        data = {'page': entry_point.page.slug}
    else:
        data = {'page': None}
        
    response = JsonResponse(data)
    response["Access-Control-Allow-Origin"] = "*"
    
    return response

def dynamic_data(request, slug):
    page = get_object_or_404(Page, slug=slug)
    
    iconFolders = []
    icons = []
    leftText = []
    rightText = []
    
    for folder in IconFolder.objects.all():
        out = []
        for icon in folder.icons():
            out.append({
                'checkURL': icon.check_url,
                'icon': icon.display_icon.url,
                'display_icon': request.build_absolute_uri(icon.display_icon.thumbnail["90x90"].url),
                'href': icon.href,
                'title': icon.title,
                'classAttr': icon.classAttr,
                'id': 'folder_{folder_id}_icon_{icon_id}'.format(folder_id=folder.id, icon_id=icon.id)
            })

        iconFolders.append({
            'uuid': folder.uuid, 
            'title': folder.title, 
            'id': 'folder_{folder_id}'.format(folder_id=folder.id),
            'icons': out})
    
    for pageIconDisplay in PageIconDisplay.objects.filter(page=page):
        icons.append({
            'startHidden': pageIconDisplay.icon.start_hidden,
            'checkURL': pageIconDisplay.icon.check_url,
            'icon': pageIconDisplay.icon.display_icon.url,
            'display_icon': request.build_absolute_uri(pageIconDisplay.icon.display_icon.thumbnail["90x90"].url),
            'classAttr': pageIconDisplay.icon.classAttr,
            'href': pageIconDisplay.icon.href,
            'title': pageIconDisplay.icon.title,
            'id': 'page_icon_display_{page_icon_display_id}'.format(page_icon_display_id=pageIconDisplay.id)
        })
    
    for position, positionList in (('LEFT', leftText), ('RIGHT', rightText)):
        for pageTextLink in PageTextLink.objects.filter(page=page, position=position):
            if pageTextLink.text_link.page_link:
                positionList.append({
                    'page': pageTextLink.text_link.page_link.slug,
                    'title': pageTextLink.text_link.title,
                    'id': 'page_text_link_{page_text_link_id}'.format(page_text_link_id=pageTextLink.id)
                })
                
            else:                
                positionList.append({
                    'href': pageTextLink.text_link.url,
                    'title': pageTextLink.text_link.title,
                    'id': 'page_text_link_{page_text_link_id}'.format(page_text_link_id=pageTextLink.id)
                })
    
    jsonData = {
        'title': page.title,
        'folders': iconFolders,
        'icons': icons,
        'leftText': leftText,
        'rightText': rightText,
    }
    
    response = JsonResponse(jsonData)
    response["Access-Control-Allow-Origin"] = "*"
    
    return response