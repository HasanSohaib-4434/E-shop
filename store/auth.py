from django.shortcuts import redirect



def auth_middleware(get_respone):
    
    def middleware(request):
        #print(request.session.get('customer'))
        retrunUrl=request.META['PATH_INFO']
       # print()
        if not request.session.get('customer'):
           return  redirect(f'login?return_url={retrunUrl}')
        
        respone=get_respone(request)
        return respone
    

    return middleware