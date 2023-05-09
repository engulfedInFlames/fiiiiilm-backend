from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from reviews.models import Review, Comment
from reviews.serializers import ReviewListSerializer, CreateReviewListSerializer, CommentListSerializer, CreateCommentSerializer
import requests
import json
from django.http import JsonResponse
# Create your views here.

class MovieApi(APIView):
    def get(self, request):
        url = 'https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key=f5eef3421c602c6cb7ea224104795888&targetDt=20230501&weekGb=0'
        response = requests.get(url)
        data = response.json()
        return JsonResponse(data)

class ReviewList(APIView):
    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewListSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateReviewListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('작성완료', status=status.HTTP_200_OK)


class ReviewListDetail(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        serializer = CreateReviewListSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(f'수정완료{serializer.data}', status=status.HTTP_200_OK)
        
        # if request.user == review.user:
        #     serializer = CreateReviewListSerializer(review, data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(f'수정완료{serializer.data}', status=status.HTTP_200_OK)
        #     else:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response("로그인 후 작성해주세요.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        review.delete()
        return Response("삭제완료",status=status.HTTP_204_NO_CONTENT)
        # if request.user == review.user:
        #     review.delete()
        #     return Response("삭제완료!",status=status.HTTP_204_NO_CONTENT)
        # else:
        #     return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN)


class ReviewListRecent(APIView):
    pass


class CommentList(APIView):
    def get(self, resquest, review_id):
        review = Review.objects.get(id=review_id)
        comments = review.comment_set.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, review_id):
        print(request.user)
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review_id=review_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):

    def put(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CreateCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제되었습니다!", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)