from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Movie, Review

# Create your views here.

def index(request):
  movie = Movie.objects.all()
  review = Review.objects.all()

  if 'select_genre' in request.GET:
      select_genre = request.GET['select_genre']
      movie = Movie.objects.filter(genre__contains = select_genre)

  context = {
    'movie' : movie,
    'review' : review
  }
  return render(request, 'review/index.html', context)

# 영화 등록
def add_movie(request):
  if request.method == 'GET':
    return render(request, 'review/add_movie.html')
  else:
    genre = request.POST['select_genre']
    movie_name = request.POST['movie_name']
    movie_summary = request.POST['movie_summary']

    Movie.objects.create(
      genre = genre,
      movie_name = movie_name,
      movie_summary = movie_summary,
    )
    return HttpResponseRedirect('/review/')

# 영화 정보
def review_movie(request, id):
  movie = Movie.objects.get(id=id)
  review = Review.objects.filter(movie = id).order_by('-reg_date')

  context = {
    'movie' : movie,
    'review' : review
  }
  return render(request, 'review/review_movie.html', context)

# 영화 수정
def update_movie(request, id):
  movie = Movie.objects.get(id=id)

  if request.method == 'GET':
    context = {
      'movie' : movie
    }
    return render(request, 'review/update_movie.html', context)
  else:
    movie.genre = request.POST['select_genre']
    movie.movie_name = request.POST['movie_name']
    movie.movie_summary = request.POST['movie_summary']

    movie.save()
    return HttpResponseRedirect('/review/review_movie/' + str(id))

# 영화 삭제
def delete_movie(request, id):
  Movie.objects.get(id=id).delete()

  return JsonResponse({ 'result' : 'success' })

# 리뷰
def reply(request, id):
  movie = Movie.objects.get(id = id)

  reviewer_name = request.POST['reviewer_name']
  review_text = request.POST['review_text']
  score = request.POST['score']
  print(review_text)

  movie.review_set.create(
    reviewer_name = reviewer_name,
    review_text = review_text,
    score = score
  )
  return JsonResponse({ 'result' : 'success' })

# 정렬
def recently(request):
  movie = Movie.objects.all().order_by('-reg_date')
  review = Review.objects.all()

  context = {
      'movie' : movie,
      'review' : review
  }

  return render(request, 'review/index.html', context)