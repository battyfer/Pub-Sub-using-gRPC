import grpc
import gRPC_pb2
import gRPC_pb2_grpc
from concurrent import futures
import time

MAXSERVERS = 5
list_servers = []

class Registry_Server_ServiceServicer(gRPC_pb2_grpc.Registry_Server_ServiceServicer):
    def __init__(self):
        self.address = '0.0.0.0:50052'
        self.servers = []
        # gRPC_pb2.Registry_Server.address = '0.0.0.0:50052'
        # gRPC_pb2.Registry_Server.servers = []

    

    def Register(self, request, context):
        # _result = gRPC_pb2.Registry_Response.status
        print("REGISTRY JOIN REQUEST FROM: ", request.server_id)

        if len(list_servers)<MAXSERVERS:
            _result = "SUCCESS"
            
            new_server = gRPC_pb2.Server(server_id=request.server_id,address=request.address) ####
            list_servers.append(new_server)
            # list_servers.append(request.server_id)
            print("SERVER SUCCESSFULLY ADDED")

        else:
            _result = "FAILURE"
            print("SORRY, UNABLE TO ADD SERVER")           

        return gRPC_pb2.Registry_Response(status = _result)


    def GetServerList(self, request, context):
        # request.input
        # listt = gRPC_pb2.Registry_Server.servers
        print("SERVER LIST REQUEST FROM: ", request.id)

        for server in list_servers:
            yield gRPC_pb2.Server_with_Address(serverss = server)
        print("SERVER LIST RETURNED")
        # return gRPC_pb2.Server_with_Address(serverss = list_servers)
        # return list_servers
        



def main():
    r_server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    gRPC_pb2_grpc.add_Registry_Server_ServiceServicer_to_server(Registry_Server_ServiceServicer(), r_server)
    print("Welcome to Discord!\nRegistry Server Started!")
    r_server.add_insecure_port('0.0.0.0:50052')
    r_server.start()
    r_server.wait_for_termination()

main()