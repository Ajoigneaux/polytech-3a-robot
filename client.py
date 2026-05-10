from martypy import Marty
my_marty = Marty("wifi","192.168.0.101")
# my_marty.dance()
# print(my_marty.wiggle(1000))
print("go")
print(my_marty.get_battery_remaining())
my_marty.get_ready(True)
# my_marty.walk(3,move_time=1000)
# my_marty.send_file()
my_marty.get


# print("test")
# my_marty.close()

# import requests

# r = requests.get("http://192.168.0.105/")
# print(r.status_code)
# print(r.text)


# r = requests.get("http://192.168.0.105/")
# print(r.status_code)
# print(r.text)

# p = requests.post("http://192.168.0.105/hello")
# print(p.status_code)
# print(p.content)