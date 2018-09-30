import cognitive_face as CF
from secrets import subscription_key

CF.Key.set(subscription_key)

BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)


# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
#img_url = 'https://images-ssl.gotinder.com/5b8a4aa382b1fa4111329ca3/640x640_0bccda0d-dcba-4405-83ba-7d25ffdd762d.jpg'
#faces = CF.face.detect(img_url, attributes='age,gender')
#print(faces)

#CF.face_list.create('t_face_list',name='t_face_list')

similars = CF.face.find_similars('', face_list_id='t_face_list')
print(similars)

print(CF.face_list.get('t_face_list')