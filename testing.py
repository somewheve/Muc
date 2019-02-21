from App import RequestInfo
from time import time

old = time()
info = RequestInfo("西瓜醋l")

info.request_user_id()
new = time()
print(new-old)
print(info.userid)