from django.urls import path
from . import views


urlpatterns=[
    path('',views.landing_page,name='landing_page'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('chatRooms/<str:room_id>',views.chat_rooms,name='chat_rooms'),
    path('logout',views.logout,name='logout'),
    path('friends',views.friends,name='friends'),
    path('friends/send_request',views.send_friend_request),
    path('friends/add_friend/<str:user>',views.add_friend,name="add_f"),
    path('friends/reject_request/<str:asked_user>',views.remove_from_list,name="reject_r")
]