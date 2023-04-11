from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

from .models import item, order

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
  id = request.POST['id'] # ajax

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
    selected_item_id = request.POST['selected_item']
    quantity = request.POST['item_count']

    # 해당 id를 가진 상품 객체 가져오기
    selected_item = item.objects.get(id=selected_item_id)

    # 주문 생성
    order.objects.create(
      item=selected_item,
      quantity=quantity
    )

    # 해당 상품의 수량 감소시키기
    selected_item.item_count -= int(quantity)
    selected_item.save()

    return HttpResponseRedirect('/item/orderList/')

def orderList(request):

  context = {}

  return render(request, 'item/orderList.html', context)




