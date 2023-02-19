import grpc
import gRPC_pb2
import gRPC_pb2_grpc
from concurrent import futures
import uuid
import datetime
from datetime import datetime, date

client_list = []
MAXCLIENTS = 10
article_list = []
addr = '0.0.0.0:50051'

class Server_ServiceServicer(gRPC_pb2_grpc.Server_ServiceServicer):
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50052
        # self.address = '0.0.0.0:50051'

        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        self.stub = gRPC_pb2_grpc.Server_ServiceStub(self.channel)
        

    
    def JoinServer(self, request, context):
        print("SERVER JOIN REQUEST FROM: ", request.client_id)
        
        if len(client_list)<MAXCLIENTS:
            _result = "SUCCESS"
            client_list.append(request.client_id)
            print("CLIENT SUCCESSFULLY ADDED")
        else:
            _result = "FAILURE"
            print("SORRY, UNABLE TO ADD CLIENT")

        return gRPC_pb2.Server_Response(status = _result)



    def LeaveServer(self, request, context):
        print("SERVER LEAVE REQUEST FROM: ", request.client_id)
        
        if(request.client_id not in client_list):
            _result = "FAILURE"
            print("CLIENT NOT FOUND")

        else:
            client_list.remove(request.client_id)
            _result = "SUCCESS"
            print("CLIENT SUCCESSFULLY REMOVED")

        return gRPC_pb2.Server_Response(status = _result)





    def GetArticles(self, request, context):
        print("ARTICLE LIST REQUEST FROM: ", request.client.client_id)
        
        if(request.client.client_id not in client_list):
            print("CLIENT NOT FOUND")

        else:
            print("CLIENT FOUND")
            print("FETCHING ARTICLE LIST...")

            typ = request.article.type
            authorr = request.article.author
            date_get = request.article.time
            print("FOR", typ,"," ,authorr,",",date_get)

            if(typ and authorr):
                filtered_data = [d for d in article_list if d.type == typ and d.author == authorr and datetime.strptime(d.time, '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
            elif(typ and not(authorr)):
                filtered_data = [d for d in article_list if d.type == typ and datetime.strptime(d.time, '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
            elif(authorr and not(typ)):
                filtered_data = [d for d in article_list if d.author == authorr and datetime.strptime(d.time, '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
            else:
                filtered_data = [d for d in article_list if datetime.strptime(d.time, '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
        
            print("ARTICLE LIST RETURNED")

        # return gRPC_pb2.Server_with_Address(serverss = list_servers)
        for art in filtered_data:
            yield gRPC_pb2.Article_List(articles = art)
        # pass

                


    def PublishArticle(self, request, context):
        print("ARTICLE PUBLISH REQUEST FROM: ", request.client.client_id)
        
        if(request.client.client_id not in client_list):
            print("CLIENT NOT FOUND SO CANNOT PUBLISH ARTICLE.")
            _result = "FAILURE"

        else:
            print("CLIENT FOUND")
            print("FETCHING ARTICLE...")

            new_article = gRPC_pb2.Article(type=request.article.type,author = request.article.author,time = request.article.time, content = request.article.content)
            # print("1")
            article_list.append(new_article)
            _result = "SUCCESS"
            print("YOUR ARTICLE HAS BEEN PUBLISHED!")

        # return gRPC_pb2.Server_with_Address(serverss = list_servers)
        return gRPC_pb2.Article_Response(status = _result)

            

# class Article_ServiceServicer(gRPC_pb2_grpc.Article_ServiceServicer):
#     def GetArticle(self, request, context):


def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = gRPC_pb2_grpc.Registry_Server_ServiceStub(channel)
        response = stub.Register(gRPC_pb2.Server(server_id=str(uuid.uuid1()),address=addr))
        print("Server status: " + response.status)

        # response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
        # print("Greeter client received: " + response.status)

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    gRPC_pb2_grpc.add_Server_ServiceServicer_to_server(Server_ServiceServicer(), server)
    addr = input("Enter Server Address: ")
    if addr == '0.0.0.0:50052':
        print("Server Address is already in use!")
        exit()

    print("Server Started!")
    server.add_insecure_port(addr)  #'0.0.0.0:50051'
    server.start()
    run()
    server.wait_for_termination()
