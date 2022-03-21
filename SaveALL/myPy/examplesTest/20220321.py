infomarker=[[["l1.1","l1.2"],["l2","l2.2"],["l3","l3.2"]],[["l1.1.2","l1.1.2"],["l2.2","l2.2.2"],["l3.2","l3.2.2"]]]
ls=[]

class tag:
    def __init__(self,_id,_corns) -> None:
        self.id=_id
        self.corns=_corns

print(str(infomarker.count(1)))        
for i in infomarker:
    for j,k in enumerate(i[0]):
        ls.append(tag(k,i[1][j]))
    
print(ls)
for i in ls:
    print(i.id)
    print(i.corns)