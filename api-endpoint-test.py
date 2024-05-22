import requests

############### Background Image endpoint test ################

url = 'http://127.0.0.1:5000/bg-process?key=mykey'

files = {'photo':('background_remove_input.jpg',open('background_remove_input.jpg','rb'))}

r = requests.post(url,files=files)

print(r.content)

############### Dominant Color endpoint test ################

url = 'http://127.0.0.1:5000/dm-process?key=mykey'

files = {'photo':('dominant_input.jpg',open('dominant_input.jpg','rb'))}

r = requests.post(url,files=files)

print(r.content)


############### Image recognition endpoint test ################


url = 'http://127.0.0.1:5000/rg-process?key=mykey'

files = {'photo':('recognition_input.jpg',open('recognition_input.jpg','rb'))}

r = requests.post(url,files=files)

print(r.content)
