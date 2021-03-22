from requests import get, post, put, delete

server = 'https://epic-tetris-server.herokuapp.com/api/users'

print('Create user')
print(post(server, json={
    'nickname': 'TEST_01',
    'password': '12345'
}).json())
print(get(server).json())

print('Create user with same nickname')
print(post(server, json={
    'nickname': 'TEST_01',
    'password': '54321'
}).json())
print(get(server).json())

print('Login with incorrect password')
print(get(server + '/TEST_01', json={
    'password': '54321'
}).json())

print('Login with correct password')
print(get(server + '/TEST_01', json={
    'password': '12345'
}).json())

print('Add game result')
print(put(server + '/TEST_01', json={
    'game_result': '10'
}).json())
print(get(server).json())

print('Add game result for non-existent user')
print(put(server + '/TEST_02', json={
    'game_result': '10'
}).json())
print(get(server).json())

print('Add another game result')
print(put(server + '/TEST_01', json={
    'game_result': '10'
}).json())
print(get(server).json())

print('Delete all users')
print(delete(server).json())
print(get(server).json())
