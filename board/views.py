from django.shortcuts import render,redirect
from .models import Board,Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

def creply(request,bpk):
  b = Board.objects.get(id=bpk)
  c = request.POST.get('com')
  Reply(board=b, replyer=request.user, comment=c).save()
  return redirect('board:detail',bpk)


def dreply(request,bpk,rpk):
  r = Reply.objects.get(id=rpk)
  if request.user == r.replyer:
    r.delete()
  else:
    messages.error(request,"계정정보가 일치하지 않습니다.")
  return redirect('board:detail',bpk)

def update(request,bpk):
  b = Board.objects.get(id=bpk)

  if b.writer != request.user:
    return redirect('board:index')

  if request.method == 'POST':
    s= request.POST.get('su')
    c=request.POST.get('co')
    b.subject, b.content = s,c
    b.save()
    return redirect('board:detail',bpk)
  context={
    'b': b
  }
  return render(request,'board/update.html',context)

def create(request):
  if request.method =='POST':
    s = request.POST.get('sub')
    c =request.POST.get('con')
    t = timezone.now()
    Board(subject=s, writer=request.user, content=c, pubdate=t).save()
    return redirect("board:index")
  return render(request,'board/create.html')

def delete(request,bpk):
  b = Board.objects.get(id=bpk)
  if request.user == b.writer:
    b.delete()
  else:
    messages.error(request,"계정정보가 일치하지 않습니다.")
  return redirect('board:index')

def detail(request,bpk):
  b = Board.objects.get(id=bpk)
  r = b.reply_set.all()
  context = {
    'b' : b,
    'rset' : r
  }
  return render(request,'board/detail.html',context)


def index(request):
  pg = request.GET.get("page",1)
  cate = request.GET.get('cate',"")
  kw = request.GET.get('kw',"")

  if kw:
    if cate == 'sub':
      b = Board.objects.filter(subject__startswith=kw)
    elif cate == 'wri':
      try:
        from acc.models import User
        u = User.objects.get(username=kw)
        b = Board.objects.filter(writer=u)
      except:
        b = Board.objects.none()

    elif cate == 'con':
      b = Board.objects.filter(content__contains=kw)
    else:
      b = Board.objects.none()
  else:
    b = Board.objects.all()

  b = b.order_by("-pubdate")

  pag = Paginator(b,2)
  obj = pag.get_page(pg)
  
  context = {
    'bset' : obj,
    'cate' :cate,
    'kw' : kw
  }
  return render(request,'board/index.html',context) 