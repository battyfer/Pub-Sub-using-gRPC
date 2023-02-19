import grpc
import gRPC_pb2
import gRPC_pb2_grpc
from concurrent import futures
import uuid
import datetime
from datetime import datetime, date


# class MyClient(object):
# def run_rs():
#     with grpc.insecure_channel('localhost:50052') as channel:
#         stub_rs = gRPC_pb2_grpc.Registry_Server_ServiceStub(channel)
#         response = stub_rs.GetServerList(gRPC_pb2.Registry_Server(id=str(uuid.uuid1()),address ='0.0.0.0:50052'))
#         print("Server status: " + response.status)


def run_s():
    # with grpc.insecure_channel('localhost:50051') as channel:
    #     stub_s = gRPC_pb2_grpc.Server_ServiceStub(channel)

    channel_r = grpc.insecure_channel('localhost:50052')
    stub_rs = gRPC_pb2_grpc.Registry_Server_ServiceStub(channel_r)
    channel_s = grpc.insecure_channel('localhost:50051')
    stub_s = gRPC_pb2_grpc.Server_ServiceStub(channel_s)
        
    while True:
        print("\nChoose an option:")
        print("1. Get Server List")
        print("2. Join a server")
        print("3. Leave a server")
        print("4. Get Articles")
        print("5. Publish Article")
        print("6. Quit")

        choice = input("Enter your choice:\n")

        if choice == "1":
            response = stub_rs.GetServerList(gRPC_pb2.Registry_Server(id=str(uuid.uuid1()),address ='0.0.0.0:50052'))
            for res in response:
                print("Server ID: " + res.serverss.server_id)
                print("Server Address: " + res.serverss.address)


        elif choice == "2":
            response = stub_s.JoinServer(client)
            print("Server status: " + response.status)

        elif choice == "3":
            response = stub_s.LeaveServer(client)
            print("Server status: " + response.status)
        
        
        elif choice == "4":        #get articles
            typ = input("Enter the type:\n")
            if(typ!="SPORTS" and typ!="FASHION" and typ!="POLITICS"):
                print("Illegal Format!")
                break

            auth = input("Enter the author:\n")
            datee = input("Enter the date(DD/MM/YYYY):\n")
            content = "dgdvf"
            article = gRPC_pb2.Article(type=typ, author = auth,time = datee, content = content)
            request = gRPC_pb2.Article_Client(article=article,client = client)

            response = stub_s.GetArticles(request)
            for res in response:
                print("Article Type: " + res.articles.type)
                print("Article Author: " + res.articles.author)
                print("Article Date: " + res.articles.time)
                print("Article Content: " + res.articles.content)

            # print("Server status: " + response.status)



        elif choice == "5":             #publish article
            typ = input("Enter the type:\n")
            if(typ!="SPORTS" and typ!="FASHION" and typ!="POLITICS"):
                print("Illegal Format!")
                break

            author = input("Enter the author:\n")
            content = input("Enter the content of article:\n")
            if not (typ and author and content):
                print("Illegal Format!")
                break

            article=gRPC_pb2.Article(type=typ, author=author, time=date.today().strftime('%d/%m/%Y'), content = content)
            request = gRPC_pb2.Article_Client(article=article,client = client)
            response = stub_s.PublishArticle(request)
            print("Server status: " + response.status)

        elif choice == "6":
            break

        else:
            continue

if __name__ == '__main__':
    namee = input("Enter your name:\n")
    client = gRPC_pb2.Client(client_id=str(uuid.uuid1()),name =namee)
    # result = client.get_url(message="Hello Server you there?")
    # client = grpc.(futures.ThreadPoolExecutor(max_workers=5))
    # gRPC_pb2_grpc.add_Server_ServiceServicer_to_server(Server_ServiceServicer(), server)
    # print("Server Started!")
    # # server.add_insecure_port('[::]:50051')
    # server.start()
    run_s()
    # server.wait_for_termination()
