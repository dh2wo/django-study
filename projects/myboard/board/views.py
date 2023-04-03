from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.decorators import login_required

from json import loads # 문자열화한 JSON객체 받을수 있다?

from .models import Board, Reply

# Create your views here.

# localhost:8000으로 왔을때 board로 연결
def home(request):
    return HttpResponseRedirect('/board/')

# 게시판 목록 보기
def index(request):
    print('index() 실행')

    # 반환되는 queryset에 대해서 order_by함수 이용하면 특정 필드 기준으로 정렬
    # order_by에 들어가는 필드 이름 앞에 -를 붙히면 내림차순(DESC) 아니면 오름차순(ASC)
    # board_list = Board.objects.all().order_by('-id')

    result = None # 필터링된 리스트

    context = { }

    # request.GET : GET 방식으로 보낸 데이터들을 딕셔너리 타입으로 저장
    print(request.GET)

    # 검색 조건과 검색 키워드가 있어야 필터링 실행
    if 'searchType' in request.GET and 'searchWord' in request.GET:
        search_Type = request.GET['searchType'] # GET안의 문자열은
        search_Word = request.GET['searchWord'] # HTML의 name속성

        print("search_Type : {}, search_Word : {}".format(search_Type, search_Word))

        # match : Jave의 switch 비슷
        match search_Type:
            case 'title': # 검색 기준이 제목일 때
                result = Board.objects.filter(title__contains = search_Word)
            case 'writer': # 검색 기준이 글쓴이일 때
                result = Board.objects.filter(writer__contains = search_Word)
            case 'content': # 검색 기능이 내용일 때
                result = Board.objects.filter(content__contains = search_Word)

        # 검색을 했을때만 검색 기준과 키워드를 context에 넣는다
        context['searchType'] = search_Type
        context['searchWord'] = search_Word

    else: # QueryDict에 검색 조건과 키워드가 없을 때
        result = Board.objects.all()

    # 검색 결과 또는 전체 목록을 id 내림차순 정렬
    result = result.order_by('-id')

    # context['board_list'] = result

    # 페이징 넣기
    # Paginator(목록, 목록에 보여줄 개수)
    paginator = Paginator(result, 10)

    # Paginator 클래스를 이용해서 자른 목록의 단위에서
    # 몇번째 단위를 보여줄 것인지 정한다
    page_obj = paginator.get_page(request.GET.get('page'))

    # 페이징한 일부 목록을 반환
    context['page_obj'] = page_obj

    return render(request, 'board/index.html', context)

# 글 읽기
def read(request, id):
    # print("id : ", id)

    board = Board.objects.get(id = id)
    # 고전적인 방법으로 댓글 가져오기
    # reply_list = Reply.objects.filter(board_obj = id).order_by('-id')

    # 조회수 올리기
    board.view_count += 1
    board.save()

    context = {
        'board' : board,
        # 'replyList' : reply_list
    }

    return render(request, 'board/read.html', context)

# 글 쓰기
# 내가 따로 만든 로그인 URL이 있다면 login_url 키워드 변수를 적어야한다
@login_required(login_url='common:login')
def write(request):
    if request.method == 'GET': # 요청방식이 GET이면 화면 표시
        return render(request, 'board/board_form.html')
    else: # 요청방식이 POST일 때 할일
        # 폼의 데이터를 DB에 저장
        title = request.POST['title']
        content = request.POST['content']
        author = request.user # 요청에 들어있는 User 객체

        # 현재 세션정보의 writer라는 키를 가진 데이터 취득
        # session_writer =  request.session.get('writer')
        # if not session_writer: # 세션에 정보가 없는 경우
        #     # 폼에서 가져온 writer 값 세션에 저장
        #     request.session['writer'] = request.POST['writer']
        # print("session_writer : ", session_writer)

        # 방법1, 객체.save()
        board = Board(
            title = title,
            author = author,
            content = content
        )

        # get메서드 사용하는 이유
        # 딕셔너리에서 존재하지 않는 키를 딕셔너리[키] -> KeyError
        # 딕셔너리.get('키') - > None
        if request.FILES.get('uploadFile'): # 파일 키가 있다면
            upload_file = request.FILES['uploadFile']
            # 요청에 들어있던 첨부파일을 모델에 설정
            board.attached_file = upload_file
            board.original_file_name = upload_file.name

    board.save() # db에 insert

        # 방법2, 모델.objects.create(값)
        # Board.objects.create(
        # title = title,
        # author = author, # user 객체 저장
        # # writer = request.session.get('writer'), # 세션에 있는 값 저장
        # content = content
        # )

    return HttpResponseRedirect('/board/')

# 글 수정
@login_required(login_url='common:login')
def update(request, id):
    board = Board.objects.get(id = id)

    # 로그인 정보가 맞지 않을 때
    if board.author.username != request.user.username:
        return HttpResponseRedirect('/board/')

    if request.method == 'GET':
        context = {'board' : board }
        return render(request , 'board/board_update.html', context)
    else:
        board.title = request.POST['title']
        # board.writer = request.POST['writer']
        board.content = request.POST['content']

        # 첨부파일이 있다면
        if request.FILES.get('uploadFile'):
            upload_file = request.FILES['uploadFile']
            # 요청에 들어있던 첨부파일을 모델에 설정
            board.attached_file = upload_file
            board.original_file_name = upload_file.name
        else: # 첨부파일이 없다면
            board.attached_file = None
            board.original_file_name = None

        board.save() # save를 해야 DB에 반영됨!!!

        # 수정 후에 해당 글로 다시 이동
        redirect_url  = '/board/' + str(id) + '/'
        return HttpResponseRedirect(redirect_url)

# 글 삭제
@login_required(login_url='common:login')
def delete(request, id):
    print("id : ", id)
    # 해당 객체를 가져오기
    board = Board.objects.get(id = id)

    # 글 작성자의 id와 접속한 사람의 id가 같을때
    if board.author.username == request.user.username:
        board.delete()
    # 다를때
    return HttpResponseRedirect('/board/')

# 댓글 쓰기
def write_reply(request, id):
    print('POST', request.POST)

    user = request.user
    # reply_text = request.POST['replyText'] # html의 [name]
    reply = loads(request.body) # 요청의 body를 해석
    print(reply) # {'replyText': '댓글내용'}

    reply_text = reply['replyText']
    print('reply_text', reply_text) # 댓글내용

    # 댓글(1)
    # Reply.objects.create(
    #     user = user,
    #     reply_content = reply_text,
    #     board_obj = Board.objects.get(id = id)
    # )

    # 댓글(2) : queryset 이용
    board = Board.objects.get(id = id)
    board.reply_set.create(
        reply_content = reply_text,
        user = user
    )

    # return JsonResponse({"result":reply_text}) # ajax response로 보내진다
    # return HttpResponseRedirect('/board/' + str(id))
    return JsonResponse({'result' : 'success' })

# 댓글 삭제
def delete_reply(request, id):
    # id = request.POST['id']
    # rid = request.POST['rid']
    rid = (loads(request.body))['rid']

    Board.objects.get(id = id).reply_set.get(id = rid).delete()
    # Reply.objects.get(id = rid).delete() 윗줄 같은 느낌

    return JsonResponse({"result":"이현종"}) # 아무튼 딕셔너리로 보내야 오류가 안뜬다

# 댓글 수정
def update_reply(request, id):
    if request.method == 'GET':
        # board = Board.objects.get(id = id)
        rid = request.GET['rid']

        # 댓글 번호에 해당하는 객체 가져오기
        reply = Board.objects.get(id = id).reply_set.get(id = rid)

        context = {
            # rid에 해당하는 Reply객체의 id, replyText
            'rid' : reply.id,
            'replyText' : reply.reply_content
            # 'update' : 'update',
            # 'board' : board, # id에 해당하는 Board 객체
            # 'reply' : board.reply_set.get(id = rid) # rid에 해당하는 Reply 객체
        }
        # return render(request, 'board/read.html', context)
        return JsonResponse(context)
    else:
        # id = request.POST['id']
        # rid = request.POST['rid']

        # JSON으로 받기
        request_body = loads(request.body)
        print('request_body : ', request_body)
        rid = request_body['rid']
        reply_text = request_body['replyText']
        print(rid, reply_text)

        reply = Board.objects.get(id = id).reply_set.get(id = rid)

        # 폼에 들어있던 새로운 댓글 텍스트로 갱신
        # reply.reply_content = request.POST['replyText']
        reply.reply_content = reply_text

        reply.save()

        return JsonResponse({"result":"이현종"})

# AJAX
def call_ajax(request):
    print('ajax 성공이다')
    print(request.POST)
    # JSON.stringify 하면 아래 표현은 사용할 수 없음
    # print(request.POST['txt'])
    data = loads(request.body)
    print('템플릿에서 보낸 데이터', data)
    print(data['txt']) # JSON.stringify로 이렇게 가능
    print(type(data))

    return JsonResponse({'result' : 'ㅊㅋㅊㅋ'})

# AJAX 댓글 목록
# def load_reply(request):
#     id = request.POST['id']
#     # 해당하는 board id에 달려있는 모든 Reply 가져오기
#     # 1번 방법
#     #Reply.objects.filter(board = id)

#     # 2번 방법
#     reply_list = Board.objects.get(id = id).reply_set.all()
#     # print(reply_list) QuerySet 뭉탱이

#     # QuerySet 그 자체는 JS에서는 알 수 없는 타입..
#     # 그래서 JSON 타입으로 형변환
#     serializers_list = serializers.serialize("json", reply_list)
#     # print(serializers_list)

#     response = {'response' : serializers_list}
#     return JsonResponse(response)

# AJAX 댓글 목록2
def load_reply(request, id):

    reply_list = Board.objects.get(id = id).reply_set.all()

    reply_dict_list = []

    # reply_list의 정보를 가지고 dictionary 만들기
    for reply in reply_list:
        reply_dict = {
            'id' : reply.id,
            'username' : reply.user.username,
            'replyText' : reply.reply_content,
            'inputDate' : reply.input_date
        }

        reply_dict_list.append(reply_dict)

    context = {'replyList' : reply_dict_list }

    return JsonResponse(context)


# 파일 다운로드
def download(request, id):
    board = Board.objects.get(id = id)
    attached_file = board.attached_file
    original_file_name = board.original_file_name

    # 글 번호에 달려있던 첨부파일로 파일형식 응답 객체 생성
    response = FileResponse(attached_file)
    response['Content-Disposition'] = 'attachment; filename = %s' %original_file_name

    return response