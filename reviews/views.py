from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from reviews.models import Review, Comment
from reviews.serializers import CreateReviewSerializer, ReviewListSerializer, CommentListSerializer, CreateCommentSerializer, ReviewSerializer
import requests
import os
from django.http import JsonResponse
# Create your views here.


class MovieApiDetail(APIView):
    def get(self, request):
        API_KEY = os.environ.get('MOVIE_API_KEY')
        url = "https://api.themoviedb.org/3/movie/now_playing?language=ko-KR&page=1&region=KR"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        results = []
        for movie in data["results"][:10]:
            results.append({
                "id": movie["id"],
                "title": movie["title"],
                "genre_ids": movie["genre_ids"],
                "original_title": movie["original_title"],
                "overview": movie["overview"],
                "poster_path": movie["poster_path"],
                "release_date": movie["release_date"],
                "vote_average": movie["vote_average"],
            })
        return JsonResponse(results, safe=False)


class MovieApiMain(APIView):
    def get(self, request):
        API_KEY = os.environ.get('MOVIE_API_KEY')
        url = "https://api.themoviedb.org/3/movie/now_playing?language=ko-KR&page=1&region=KR"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        results = []
        for movie in data["results"][:10]:
            results.append({
                # "id": movie["id"], # 필요하면추가
                "title": movie["title"],
                "original_title": movie["original_title"],
                "poster_path": movie["poster_path"],
            })
        return JsonResponse(results, safe=False)


class ReviewList(APIView):
    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewListSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"글을 쓰고 싶다면! 로그인해~"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"message":"작성완료"}, status=status.HTTP_200_OK)


class ReviewUpdate(APIView):
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
                return Response(f'수정완료{serializer.data}', status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"다른 계정 이거나 로그인 후 작성해주세요."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        if request.user == review.user:
            review.delete()
            return Response({"message":"삭제완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"다른 계정 이거나 로그인 후 작성해주세요."}, status=status.HTTP_403_FORBIDDEN)


class ReviewLike(APIView):
    def post(self,request, pk):
        review = get_object_or_404(Review,id=pk)
        if request.user in review.like_users.all():
            review.like_users.remove(request.user)
            return Response({"message":"안! 좋아요!!"},status=status.HTTP_200_OK)
        else:
            review.like_users.add(request.user)
            return Response({"message":"좋아요!"},status=status.HTTP_200_OK)



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
        reviews = Review.objects.order_by('-created_at')
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

