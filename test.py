import ast
f1 = open('data_wth.txt','r')
f = open('testing.txt','r')
#
s = f.readline()
print(len(s))
print()
n = f1.read()
d = ast.literal_eval(n)
print(d)
print(type(d))