# cmusic
An program which used to get user's comments in netease music 

# Usage
 
### Import the module
```python
from App import RequestInfo
```

### Get the userid by username

```python
info = RequestInfo(username)
info.request_user_id()
print(info.userid)
```
### Get the user playlist ids by userid

```python
info.request_user_playlist()
print(info.playlist_id)
```

### Get the user songs ids by all playlist ids
```python
info.request_user_songs_list()
print(len(info.song_id))

```
### Get user comments in all songs
```python
info.request_user_comments()
print(info.comments)
```

# To-Do

* Add web page 
* Add proxy-change 
* Make speed faster 


# IN THE END
Happy for your star ^_^ or contribute your code

