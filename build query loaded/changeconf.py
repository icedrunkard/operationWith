# -*- coding:utf-8 -*-


f=open('nginx.conf','r+')
lines=f.readlines()
lines[11]='        server_name  ;\n'
f=open('nginx.conf','w+')
f.writelines(lines)
f.close()
f=open('nginx.conf','r+')
lines=f.readlines()
for i in range(len(lines)):
    print(i,lines[i])
