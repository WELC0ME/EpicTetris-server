from requests import get, post, put

server = 'https://epic-tetris-server.herokuapp.com/api/users'

print('Create user')
print(post(server, json={
    'nickname': 'bright-star',
    'password': '12345'
}).json())
print(get(server).json())

print('Create user with same nickname')
print(post(server, json={
    'nickname': 'bright-star',
    'password': '54321'
}).json())
print(get(server).json())

print('Login with incorrect password')
print(get(server + '/bright-star', json={
    'password': '54321'
}).json())

print('Login with correct password')
print(get(server + '/bright-star', json={
    'password': '12345'
}).json())

print('Add game result')
print(put(server + '/bright-star', json={
    'game_result': '10',
    'token': '12345',
}).json())
print(get(server).json())

print('Add game result without token')
print(put(server + '/bright-star', json={
    'game_result': '10',
}).json())
print(get(server).json())

print('Add game result for non-existent user')
print(put(server + '/unknown', json={
    'game_result': '10',
    'token': '12345',
}).json())
print(get(server).json())

print('Add another game result')
print(put(server + '/bright-star', json={
    'game_result': '10',
    'token': '12345',
}).json())
print(get(server).json())
