from django.shortcuts import render
import random, string
from main.models import *

# Create your views here.

# https://stackoverflow.com/questions/2030053/how-to-generate-random-strings-in-python#2030081
def randomword(length: int):
   letters = string.ascii_letters
   return ''.join(random.choice(letters) for i in range(length))

def create(request):
    if request.method == "POST":
        t_dict = {}
        t_dict["sname"] = request.META["SERVER_NAME"]
        data = request.POST
        try:
            title = data["title"]
            content = data["content"]
            t_dict["title"] = title
            t_dict["content"] = content
        except KeyError:
            t_dict["status"] = "Missing Data"
            return render(request, "makepaste.html",t_dict,status=400)
        for x in Ban.objects.all():
            if not x.enabled: continue
            if content.lower().__contains__(x.keyword.lower()) or title.lower().__contains__(x.keyword.lower()):
                t_dict["status"] = "Ban keyword match: " + x.keyword
                return render(request, "makepaste.html",t_dict,status=400)
        t_dict["access_token"] = randomword(10)
        t_dict["delete_token"] = randomword(10)
        p = Paste.objects.create(title=title,content=content,access_token=t_dict["access_token"],delete_token=t_dict["delete_token"])
        p.save()
        t_dict["status"] = "Paste Created!"
        t_dict["access_id"] = p.id
        return render(request, "makepaste.html",t_dict)
    else:
        return render(request, "makepaste.html")

def access(request, id: int, token: str):
    if Paste.objects.filter(id=id,access_token=token).exists():
        p = Paste.objects.get(id=id,access_token=token)
        t_dict = {
            "title": p.title,
            "content": p.content,
        }
        return render(request, "view.html",t_dict)
    else:
        return render(request, "error.html",{"errorMSG": "Paste not found"},status=404)

def delete(request, id: int, token: str):
    if Paste.objects.filter(id=id,delete_token=token).exists():
        p = Paste.objects.get(id=id,delete_token=token)
        if request.method == "GET":
            t_dict = {
                "title": p.title,
                "id": id,
                "delete_token": token,
            }
            return render(request, "del_confirm.html",t_dict)
        elif request.method == "POST":
            Paste.objects.filter(id=id,delete_token=token).delete()
            return render(request, "del_done.html")
    else:
        return render(request, "error.html",{"errorMSG": "Paste not found"},status=404)




