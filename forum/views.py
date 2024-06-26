from rest_framework import generics, status
from rest_framework.response import Response
from .models import LiveForum
from .serializers import ForumSerializer
from core.models import User
from core.serializers import CustomUserSerializer




class LiveForumListAPIView(generics.ListCreateAPIView):
    queryset = LiveForum.objects.all()
    serializer_class = ForumSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        forum_serializer = self.get_serializer(queryset, many=True)

        # Serialize the list of interested users for each forum
        user_data_list = []
        for forum in queryset:
            user_queryset = forum.interested_users.all()
            user_serializer = CustomUserSerializer(user_queryset, many=True)
            user_data_list.append({
                "forum_id": forum.id,
                "interested_users": user_serializer.data,
            })

        data = {
            "message": "Forum list retrieved successfully",
            "status_code": status.HTTP_200_OK,
            "data": forum_serializer.data,
                #"interested_users": user_data_list,
        }

        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            "message": "Forum created successfully",
            "data": serializer.data,
            "status_code": status.HTTP_201_CREATED,
        }
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)



class LiveForumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LiveForum.objects.all()
    serializer_class = ForumSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        forum_serializer = self.get_serializer(instance)

        # Serialize the list of interested users
        user_queryset = instance.interested_users.all()
        user_serializer = CustomUserSerializer(user_queryset, many=True)

        data = {
            "message": "Forum details retrieved successfully",
            "data": {
                "forum": forum_serializer.data,
                "interested_users": user_serializer.data,
            },
            "status_code": status.HTTP_200_OK,
        }

        return Response(data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {
            "message": "Forum updated successfully",
            "data": serializer.data,
            "status_code": status.HTTP_200_OK,
        }
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            "message": "Forum deleted successfully",
            "data": None,
            "status_code": status.HTTP_204_NO_CONTENT,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


