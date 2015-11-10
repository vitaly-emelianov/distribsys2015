from ServerProxy import ServerProxy 

proxy = ServerProxy("http://localhost:8001/")
print("3 is even: %s" % str(proxy.div(3)))
print("100 is even: %s" % str(proxy.div(12, 3)))