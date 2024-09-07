from django.shortcuts import render,redirect,get_object_or_404
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.contrib import messages
from .models import chatRoom,Messages,FriendsList
import string,random,json
# Create your views here.

def landing_page(request):
    return render(request,'landing_page.html')

def chat_rooms(request,room_id):
    if (request.user.is_active):
        chat_name=get_object_or_404(chatRoom,Room_name=room_id)
        chat_messages=chat_name.chat_messages.all()[:30]
        return render(request,'index.html',{'chat_messages':chat_messages,'room_id':room_id})
    else:
        messages.info(request,"Login in first")
        return redirect('login',)

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
       
        if user is not None:
            auth.login(request, user)
            return redirect('/friends')
        else:
            messages.info(request,"Credential invalid")
            return redirect('login')
    else:
        
        return render(request,'login.html',)

def signup(request):
    if request.method=='POST':
        email=request.POST['myEmail']
        username=request.POST['Username']
        password=request.POST['Password']
        password2=request.POST['Password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already exist")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                friend_obj=FriendsList.objects.create(author=user,Friends_List='{  }')
                friend_obj.save()

                return redirect('login')
        else:
            messages.info(request,"password is not matching")
            return redirect('signup')
    else:
        return render(request,'signup.html')
def logout(request):
    auth.logout(request)
    return redirect('landing_page')

def friends(request):
    #Used to show friends on friends page
    room=get_object_or_404(FriendsList,author=request.user)
    dict=room.Friends_List
    friends_list=json.loads(dict)
  
    return render (request,'friends.html',{'friend_list':friends_list})

# Function to add a person in friendlist
def add_friend(request):
    if request.method=='POST':
        
        asked_user=request.POST["user"]

        #checking if the enterd username is valid

        try:
            User.objects.get(username=asked_user)
        except:
            return render(request,'add_friend.html',{'message':"Invalid User"})
        
        #checking if the perosn is already a friend or not
        

        curr_obj=FriendsList.objects.get(author=request.user)
        curr_list=curr_obj.Friends_List
        curr_list=json.loads(curr_list)
        if asked_user in curr_list.keys():
            return render(request,'add_friend.html',{'message':"Already a Friend"})
        
        # Creating new room
        new_room_code=generate_code().upper()
        room_obj=chatRoom.objects.create(Room_name=new_room_code)
        room_obj.save()

        # adding the perosn as Friend to the User 
        curr_list[asked_user]=new_room_code
        curr_list=json.dumps(curr_list)
        curr_obj.Friends_List=curr_list
        curr_obj.save()
        return redirect('friends')


        
    return render(request,'add_friend.html')



def generate_code(length=6):
    #Generates a random alphanumeric code of the specified length.
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))




