from django.urls import path
from . import views


urlpatterns=[
    path('',views.landing_page,name='landing_page'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('chatRooms/<str:room_id>',views.chat_rooms,name='chat_rooms'),
    path('logout',views.logout,name='logout'),
    path('friends',views.friends,name='friends'),
    path('friends/add_friend',views.add_friend)
]