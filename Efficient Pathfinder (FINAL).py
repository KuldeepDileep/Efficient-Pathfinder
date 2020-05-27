import urllib.request
import json
import csv
from gmplot import gmplot
import requests

filename='Order.csv'    
source_name="FAST"
source_address="22-G، Pakistan Employees Co-Operative Housing Society Block 6 PECHS, Karachi, Karachi City, Sindh"
source_capacity=100

def addNodes(G,nodes):
    for i in nodes:
        if i not in G.keys():
            G[i]=[]
    return G


def addEdges(G,edges,directed=False):
    for i in range(len(edges)):
        if directed==False:
            if len(edges[i])==3:
                G[edges[i][0]].append((edges[i][1],edges[i][2]))
                G[edges[i][1]].append((edges[i][0],edges[i][2]))
            else:
                G[edges[i][0]].append((edges[i][1],1))
                G[edges[i][1]].append((edges[i][0],1))
        else:
            if len(edges[i])==3:
                G[edges[i][0]].append((edges[i][1],edges[i][2]))
            else:
                G[edges[i][0]].append((edges[i][1],1))         
    return G
        
def listOfNodes(G):
    lst=[]
    for i in G.keys():
        lst.append(i)
    return lst

def listOfEdges(G):
    lst=[]
    for i in G.keys():
        for x,y in G[i]:
            s=()
            s=(i,x,y)
            lst.append(s)
    return lst

def getNeighbor(G,node):
    neighbours=[]
    for x in G[node]:
        neighbours.append(x[0])
    return neighbours

def Weight(G,U,V):
    edges=listOfEdges(G)
    for i,j,k in edges:
        if i==U and j==V:
            return k

def Djikstra(graph,SV):
    UV=listOfNodes(graph)
    V=[]
    SD=[]
    U=SV
    for i in UV:
        SD.append((None,i,float('inf')))
    for x in range(len(SD)):
        if U in SD[x]:
            SD[x]=(U,SD[x][1],0)
            break    
    while UV!=[]:
        lst=[]
        for i,j,k in SD:
            if j not in V:
                lst.append(k)
        minimum=min(lst)
        for i,j,k in SD:
            if minimum==k and j not in V:
                U=j
                break
        for i in range(len(getNeighbor(graph,U))):
            node=getNeighbor(graph,U)[i]
            if node not in V:
                for i in range(len(SD)):
                    if SD[i][1]==node:
                        change=i
                        prev=SD[i][2]                
                        break
        
                if prev>(minimum)+Weight(graph,U,node):
                    SD[change]=(U,SD[change][1],minimum+Weight(graph,U,node))
        V.append(UV.pop(UV.index(U)))
    for i in range(len(SD)-1):
        if SD[i][2]==0:
            SD.pop(i)
    return SD

def getShortestPath(graph,SV,to):
    UV=listOfNodes(graph)
    V=[]
    SD=[]
    U=SV
    for i in UV:
        SD.append((None,i,float('inf')))
    for x in range(len(SD)):
        if U in SD[x]:
            SD[x]=(U,SD[x][1],0)
            break    
    while UV!=[]:
        lst=[]
        for i,j,k in SD:
            if j not in V:
                lst.append(k)
        minimum=min(lst)
        for i,j,k in SD:
            if minimum==k and j not in V:
                U=j
                break
        for i in range(len(getNeighbor(graph,U))):
            node=getNeighbor(graph,U)[i]
            if node not in V:
                for i in range(len(SD)):
                    if SD[i][1]==node:
                        change=i
                        prev=SD[i][2]                
                        break
                if prev>minimum+Weight(graph,U,node):
                    SD[change]=(U,SD[change][1],minimum+Weight(graph,U,node))
        V.append(UV.pop(UV.index(U)))
    SD_final=[]
    start=""
    end=to
    while start!=SV:
        for x in SD:
            if x[1]==end:
                SD_final.append(x)
                end=x[0]
                start=x[1]
    for i in range(len(SD_final)):
        if SD_final[i][2]==0:
            SD_final.pop(i)

    return SD_final[::-1]
G={}
##addNodes(G,['A','C','D','E','G'])
##addEdges(G,[('A','D',25),('A','C',22),('A','E',10),('A','G',30),('G','D',40),('G','C',35),
##            ('G','E',25),('E','D',20),('E','C',15),('C','D',10)])
##nodeswithamount={'E':30,'G':50,'A':20,'D':50}
##addNodes(G,['A','B','C','D','E','F'])
##addEdges(G,[('A','B',15),('A','C',5),('A','D',10),('B','C',1),('B','E',25),('E','D',3),('D','F',2)])
##
##
##nodeswithamount={'A':100,'B':20,'C':30,'D':50,'E':10,'F':30}
##addNodes(G,['A','B','C','D','E'])
##addEdges(G,[('A','B',5),('A','D',2),('B','D',5),('B','E',58),('D','C',14),('D','E',4),('C','E',34)])
##nodeswithamount={'B':50,'C':30,'D':60,'E':50}

def sort(lst):
    for i in range(len(lst)):
        j=i
        while (j>0 and lst[j][2]<lst[j-1][2]):
            lst[j],lst[j-1]=lst[j-1],lst[j]
            j-=1
    return lst
def LoadData(filename):
    with open(filename,'r') as csvfile:
        data=csv.reader(csvfile,delimiter=',')
        datalist=[]
        for row in data:
            tup=()
            for index in range(len(row)):
                    tup+=(row[index],)
            datalist.append(tup)
    return datalist

def Extract(lst):
    nodeswithamount={}
    nodeswithaddresses={}
    returnnodes={}
    for i in lst[1:]:
        nodeswithamount[i[0]]=int(i[2])
        nodeswithaddresses[i[0]]=i[1]
        returnnodes[i[1]]=i[0]
    return nodeswithamount,nodeswithaddresses,returnnodes

def weightAPI(origin,destination):
    endpoint= "https://maps.googleapis.com/maps/api/directions/json?"
    api_key='AIzaSyCxv8yNbHnfRckDFvjQiNRi5tvMjL1NvKE'
    source=origin.replace(" ","+").replace(",","").replace("،","")
    dest=destination.replace(" ","+").replace(",","").replace("،","")
    nav_request= "origin="+source+'&destination='+dest+'&key='+api_key
    request=endpoint+nav_request
    response = urllib.request.urlopen(request).read()
    directions=json.loads(response)
    distance=directions['routes'][0]['legs'][0]['distance']['text']
    return distance[:len(distance)-3]
    

def GraphMaker(filename,source_name,source_address,source_capacity):
    lst=LoadData(filename)
    nodeswithamount,nodeswithaddresses,returnnodes=Extract(lst)
    AddressList=[source_address]+list(returnnodes.keys())
    Graph={}
    returnnodes[source_address]=source_name
    addNodes(Graph,[source_name])
    checklst=[]
    for i in AddressList:
        for j in AddressList:
            addNodes(Graph,[returnnodes[i],returnnodes[j]])
            if j!=i and ((i,j) and (j,i) not in checklst):
                checklst.append((i,j))
                weight=float(weightAPI(i,j))
                addEdges(Graph,[(returnnodes[i],returnnodes[j],weight)])
    return Graph,nodeswithamount
G,nodeswithamount=GraphMaker(filename,source_name,source_address,source_capacity)
nodeswithamount[source_name]=source_capacity
print(G)
print(nodeswithamount)

def pathfinder(G,source_name,source_capacity,nodeswithamount):
        tobedelivered=[]
        totaldist=0
        source=source_name
        capacity=source_capacity
        path=[]
        while len(tobedelivered)!=len(nodeswithamount):
                SD=Djikstra(G,source)
                SD=sort(SD)
                for i,j,k in SD:
                        if j not in tobedelivered and capacity!=0 and j!=source_name:
                                least=j
                                break
                        elif capacity==0:
                            least=source_name
                            break                  
                if least==source_name:
                        capacity= source_capacity       #REFILL
                        dist=getShortestPath(G,source,least)
                        for i,j,k in dist:
                            path.append((i,j,Weight(G,i,j)))
                        totaldist+=dist[-1][2]
                        nodeswithamount[least]=0
                        source=least
                elif least==source:
                        dist=getShortestPath(G,least,source_name)
                        for i,j,k in dist:
                            path.append((i,j,Weight(G,i,j)))
                        for i,j,k in dist:
                            if j==source_name:
                                capacity=source_capacity
                                break
                        totaldist+=dist[-1][2]
                        break
                        
                elif least!=source_name and capacity>=nodeswithamount[least]:
                        dist=getShortestPath(G,source,least)
                        for i,j,k in dist:
                            path.append((i,j,Weight(G,i,j)))
                        for i,j,k in dist:
                            if j==source_name:
                                capacity=source_capacity
                                break
                        totaldist+=dist[-1][2]
                        capacity=capacity-nodeswithamount[least]
                        nodeswithamount[least]=0
                        if least!=source_name:
                            tobedelivered.append(least)
                        source=least
                else:
                     dist=getShortestPath(G,source,least)
                     for i,j,k in dist:
                            path.append((i,j,Weight(G,i,j)))
                     for i,j,k in dist:
                            if j==source_name:
                                capacity=source_capacity
                                break
                     var=nodeswithamount[least]-capacity
                     nodeswithamount[least]=var
                     totaldist+=dist[-1][2]
                     capacity=0
                     dist2=getShortestPath(G,source_name,least)
                     totaldist+=dist2[-1][2]
                     source=least
                
                print("PATH",path)
                print("LOAD",nodeswithamount)
        string=''+"(START)"+source_name+'---->'
        for x in range(1,len(path)):
            if path[x][0]==source_name:
                string+=path[x][0]+'(REFILL)'+'---->'
            else:
                string+=path[x][0]+'---->'
        string+=source_name+'(END)'
        print("PATH".center(80,' '))
        print(string)
        return totaldist                    
                
                
                
print('Minimum Distance to deliver to all the nodes:',pathfinder(G,source_name,source_capacity,nodeswithamount))                      
                        
                        
                        
                        
                        
        
        
