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

def _json_for_page(request, page):
    iconFolders = []
    icons = []
    leftText = []
    rightText = []
    
    for folder in IconFolder.objects.all():
        out = []
        for icon in folder.icons():
            out.append({
                'mac_pc_only': icon.mac_pc_only,
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
            'mac_pc_only': pageIconDisplay.icon.mac_pc_only,
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
        'code': 200
    }
    
    return jsonData
  
@cache_page(5)
def static(request, slug):
  page = get_object_or_404(Page, slug=slug)
  
  return render(request, 'static.html', _getPageDict(page))

def json_from_page(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        response = JsonResponse({})
        response.status_code = 404
        response["Access-Control-Allow-Origin"] = "*"
        return response
    
    data = _json_for_page(request, page)
    response = JsonResponse(data)
    response["Access-Control-Allow-Origin"] = "*"
    return response

def json_from_email(request):
    email = request.GET.get("email")
    
    #Check for an entry point with the given e-mail (or lack thereof), setting
    #entry_point to none if it wasn't found
    if email:
        domain = email.split("@")[-1]
        try:
            entry_point = EntryPoint.objects.get(domain=domain)
        except EntryPoint.DoesNotExist:
            entry_point = None
    else:
        entry_point = None
    
    #Try to get the default entry point if we don't have one already from the e-mail
    if not entry_point:
        try:
            entry_point = EntryPoint.objects.get(domain="")
        except EntryPoint.DoesNotExist:
            #Do nothing, entry_point is already None
            pass
    
    if entry_point:
        page = entry_point.page
        data = _json_for_page(request, page)
        
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response
    
    #After all that, we still couldn't figure out what to serve.
    response = JsonResponse({})
    response.status_code = 404
    response["Access-Control-Allow-Origin"] = "*"
    return response

def json_default(request):
    try:
        page = EntryPoint.objects.get(domain="").page
        data = _json_for_page(request, page)
        
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response
        
    except EntryPoint.DoesNotExist:
        response = JsonResponse({})
        response.status_code = 404
        response["Access-Control-Allow-Origin"] = "*"
        return response
    