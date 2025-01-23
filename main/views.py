from django.shortcuts import render,redirect,get_object_or_404
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.contrib import messages
from .models import chatRoom,Messages,FriendsList,RequestList
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
                request_obj=RequestList.objects.create(author=user,Friend_Request_List='{ }')
                request_obj.save()

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

    obj=get_object_or_404(RequestList,author=request.user)
    dict2=obj.Friend_Request_List
    friend_request_list=json.loads(dict2)
  
    return render (request,'friends.html',{'friend_list':friends_list,'request_list':friend_request_list})

#Function to send a friend request
def send_friend_request(request):
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
        
        user_obj=User.objects.get(username=asked_user)
        request_obj=RequestList.objects.get(author=user_obj)
        request_list=request_obj.Friend_Request_List
        request_list=json.loads(request_list)
        request_list[request.user.username]="sadasd"
        request_list=json.dumps(request_list)
        request_obj.Friend_Request_List=request_list
        request_obj.save()
    return render(request,'add_friend.html')
        
        
        
    


# Function to add a person in friendlist
def add_friend(request,user):
    
        
    asked_user=user
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
    #adding current user in friend list of asked user
    asked_user_obj=User.objects.get(username=asked_user)
    asked_obj=FriendsList.objects.get(author=asked_user_obj)
    asked_user_list=asked_obj.Friends_List
    asked_user_list=json.loads(asked_user_list)
    asked_user_list[request.user.username]=new_room_code
    asked_user_list=json.dumps(asked_user_list)
    asked_obj.Friends_List=asked_user_list
    asked_obj.save()
    # adding the perosn as Friend to the User 
    curr_list[asked_user]=new_room_code
    curr_list=json.dumps(curr_list)
    curr_obj.Friends_List=curr_list
    curr_obj.save()
    remove_from_list(request,asked_user)
    return redirect('friends')


        
def remove_from_list(request,asked_user):
    curr_obj=RequestList.objects.get(author=request.user)
    curr_list=curr_obj.Friend_Request_List
    curr_list=json.loads(curr_list)

    curr_list.pop(asked_user)
    curr_list=json.dumps(curr_list)
    curr_obj.Friend_Request_List=curr_list
    curr_obj.save()
    return redirect('friends')



def generate_code(length=6):
    #Generates a random alphanumeric code of the specified length.
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))




