from backend.auth_service import authenticate_user

user = authenticate_user("viewer1", "viewerpass")   # used initially to test login

print(user)
