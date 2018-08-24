import sys
import requests
from flask import Flask
from MicroTwisted.utils import MicroServiceArgumentParser


class Flask(Flask):

    def __init__(self, *args, **kwargs):
        self.__routes = []
        self.app_routes = []
        self.serviceParser = MicroServiceArgumentParser()
        self.serviceArgs, _ = self.serviceParser.parse_known_args()
        return super(Flask, self).__init__(*args, **kwargs)

    def running_url(self, host, port):
        host = host if host else '0.0.0.0'
        if self.serviceArgs.service_port:
            port = self.serviceArgs.service_port
        elif port:
            port = port
        else:
            port = 5000
        port = int(port)
        return "http://" + host + ":" + str(port)

    def register_service(self, host, port):
        if not self.serviceArgs.service_register:
            return
        service_url = self.running_url(host, port)
        try:
            response = requests.post(
                self.serviceArgs.service_register,
                json={
                    'service-url': service_url,
                    'service-hash': self.serviceArgs.service_hash,
                })
            print("Master response: %s" % response)
            return response
        except requests.exceptions.ConnectionError:
            # if the service started with a --master argument
            # and cannot connect to the master service
            # then exit process
            print("master service is unreachable '%s'" % self.serviceArgs.service_register)
            sys.exit(1)
        except OSError:
            print("Socket closed :(")

    def run(self, host='0.0.0.0', port=5000, debug=False,
            load_dotenv=True, **options):
        port = self.serviceArgs.service_port or port
        print("Service Listening on '%s'" % port)
        self.register_service(host, port)
        return super(Flask, self).run(
            host=host, port=port, debug=debug,
            load_dotenv=load_dotenv, **options)

    def route(self, rule, **options):
        self.__routes.append(rule)
        return super(Flask, self).route(rule, **options)

    def route_get(self):
        return self.__routes
