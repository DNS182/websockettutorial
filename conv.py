import json

x =  '{ "name":"John", "age":30, "city":"New York"}'
y = {
  "name": "John",
  "age": 30,
  "city": "New York"
}


#  loads lay python format ma convert garauxa
# dumps lay json maa

jsan = json.loads(x)  
dict = json.dumps(y)  

print("Dict FoRMAT :" , jsan)
print("JSON FORMAT : " , dict)
