from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

from .models import item

# Create your views here.
def index(request):
  return render(request, 'item/index.html')

# 상품 등록
def addItem(request):
  if request.method == 'GET':
    return render(request, 'item/addItem.html')
  else:
    item_name = request.POST['item_name']
    item_count = request.POST['item_count']

    item.objects.create(
      item_name = item_name,
      item_count = item_count
    )
    return HttpResponseRedirect('/item/')

# 상품 목록
def listItem(request):
  list = item.objects.all()

  context = {
    'list' : list
  }

  return render(request, 'item/listItem.html', context)

# 상품 수정
def updateItem(request, id):
  list = item.objects.get(id = id)

  if request.method == 'GET':
    context = { 'list' : list }

    return render(request, 'item/updateItem.html', context)
  else:
      list.item_name = request.POST['item_name']
      list.item_count = request.POST['item_count']
      list.save()

      return HttpResponseRedirect('/item/listItem/')

# 상품 삭제
def deleteItem(request):
  id = request.POST['id']

  item.objects.get(id = id).delete()

  return JsonResponse("",safe=False)

# 상품 검색
def searchItem(request):
  search = request.GET['search']
  list = item.objects.filter(item_name__contains = search)

  context = { 'list' : list }

  return render(request, 'item/listItem.html', context)

# 상품 주문
def orderItem(request):
  if request.method == 'GET':
    list = item.objects.all()

    context = { 'list' : list }
    return render(request, 'item/orderItem.html', context)
  else:
    pass
