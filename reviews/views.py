import requests
import os

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from reviews.models import Review, Comment
from reviews.serializers import (
    CreateReviewSerializer,
    ReviewListSerializer,
    CommentListSerializer,
    CreateCommentSerializer,
    ReviewSerializer,
)

# Create your views here.


class MovieApiMain(APIView):
    def get(self, request):
        API_KEY = os.environ.get("MOVIE_API_KEY")
        url = "https://api.themoviedb.org/3/movie/now_playing?language=ko-KR&page=1&region=KR"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        poster_url = "https://image.tmdb.org/t/p/w500"

        results = []
        for idx, movie in enumerate(data["results"][:10], start=1):
            results.append(
                {
                    "rank": idx,
                    "movieCode": str(movie["id"]),
                    "title": movie["title"],
                    "posterPath": (f'{poster_url}{movie["poster_path"]}'),
                }
            )
        return JsonResponse(results, safe=False)


class MovieApiDetail(APIView):
    def get(self, request, movie_code):
        API_KEY = os.environ.get("MOVIE_API_KEY")
        url = f"https://api.themoviedb.org/3/movie/{movie_code}?append_to_response=credits%252C&language=ko-KR"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        poster_url = "https://image.tmdb.org/t/p/w500"
        result = {
            "movieCode": data["id"],
            "title": data["title"],
            "genre": data["genres"][0]["name"],
            "overview": data["overview"],
            "posterPath": (f'{poster_url}{data["poster_path"]}'),
            "releaseDate": data["release_date"],
            "runtime": (f'{data["runtime"]}min'),
            "rating": data["vote_average"],
        }
        return JsonResponse(result, safe=False)


class ReviewList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, movie_code):
        review = Review.objects.filter(movie_code=movie_code)
        serializer = ReviewListSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, movie_code):
        movie_title = request.data.get("movie_title", None)

        if movie_title is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            movie_code=movie_code,
            movie_title=movie_title,
        )
        return Response(status=status.HTTP_200_OK)


class ReviewDetail(APIView):
    def get(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        if request.user == review.user:
            serializer = CreateReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(f"수정완료{serializer.data}", status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "다른 계정 이거나 로그인 후 작성해주세요."}, status=status.HTTP_403_FORBIDDEN
            )

    def delete(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        if request.user == review.user:
            review.delete()
            return Response({"message": "삭제완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "다른 계정 이거나 로그인 후 작성해주세요."}, status=status.HTTP_403_FORBIDDEN
            )


class ReviewLike(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        if request.user in review.like_users.all():
            review.like_users.remove(request.user)
            return Response(status=status.HTTP_200_OK)
        else:
            review.like_users.add(request.user)
            return Response(status=status.HTTP_200_OK)


class CommentList(APIView):
    def get(self, request, pk):
        review = Review.objects.get(id=pk)
        comments = review.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    def put(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        if request.user == comment.user:
            serializer = CreateCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제되었습니다!", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


class ReviewRecent(APIView):
    def get(self, request):
        reviews = Review.objects.order_by("-created_at")
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
