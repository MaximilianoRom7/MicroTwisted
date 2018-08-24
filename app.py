import json
import treq
import queue
import random
import subprocess
from klein import Klein
from pprint import pprint
from twisted.internet import defer, reactor
from MicroTwisted.utils import MasterServiceArgumentParser, inlineCallbacksCatch


app = Klein()


class Route(object):

    service = None
    route = ""
    handler = None

    def __init__(self, service=None, route="", handler=None):
        # assert service and route and handler
        self.service = service
        self.route = route
        self.handler = handler


class Service(object):

    def __init__(self, module=None, source="", urls=None):
        assert module or source
        self.module = module
        self.source = module.__path__[0] + "/main.py" if module else source
        self.requests = 0
        self._urls = urls or set()
        self.pending_requests = queue.Queue()
        self.urls = self.urls_iter()
        self._hash = self.get_hash()

    def get_hash(self, bits=128):
        return str(random.getrandbits(bits))

    def urls_iter(self):
        while True:
            if self._urls:
                for url in self._urls:
                    yield url
            else:
                yield None


class MasterService(object):

    app = None
    port = None
    # route -> Route
    routes = {}
    # hash -> Service
    services = {"123": Service(source="service1")}
    # python modules
    service_modules = []

    def __init__(self, app=None, autorun=False,
                 argumentParser=MasterServiceArgumentParser):
        assert issubclass(app.__class__, Klein), "MasterService needs a Klein App"
        self.random_ports = []
        self.app = app
        self.argumentParser = argumentParser()
        self.loadConfig()
        self.create_routes()
        if autorun:
            self.app.run('0.0.0.0', self.port)

    def loadServiceModules(self):
        services = self.arguments.master_services
        self.service_modules = list(map(__import__, services))

    def loadConfig(self):
        self.arguments, unknown = self.argumentParser.parse_known_args()
        self.port = self.arguments.master_port
        self.register_url = "/service/register"
        self.register_url_full = 'http://0.0.0.0:%s' % self.port + self.register_url
        self.loadServiceModules()

    @inlineCallbacksCatch
    def _service_register(self, request):
        response = yield str({"Status": "OK"})
        data_str = yield request.content.read()
        data_json = yield json.loads(data_str)
        service_hash = data_json.get('service-hash')
        service_url = data_json.get('service-url')
        if not service_hash or not service_url:
            response = yield str({
                "Error": "Cannot register service without 'service-hash' or 'service-url'"
            })
            return response
        service = self.services.get(service_hash)
        if not service:
            response = yield str({
                "Error": "No existe un servicio con ese hash"
            })
            return response
        service._urls.add(service_url)
        print("Service URLs: ", service._urls)
        print("Pending Requests Size: ", service.pending_requests.qsize())
        while not service.pending_requests.empty():
            d, args, kwargs = service.pending_requests.get()
            print("Calling Callback '%s'" % d)
            # is important to callLater otherwise the
            # request fails with connection refused
            reactor.callLater(0.2, d.callback, args[0])
        return response

    def get_random_port(self, min_port=3333, max_port=4333):
        assert max_port > min_port
        for n in range(1 + (max_port - min_port)):
            random_port = random.randint(min_port, max_port)
            if not random_port in self.random_ports:
                self.random_ports.append(random_port)
                return str(random_port)

    def service_start(self, service):
        print("Starting service process with hash '%s'" % service._hash)
        args = [
            '/home/skyline/code/python/MicroTwisted/bin/python3', service.source,
            '--service-register', self.register_url_full,
            '--service-hash', service._hash,
            '--service-port', self.get_random_port(),
        ]
        pprint(args)
        print(" ".join(args))
        subprocess.Popen(args)

    def endpoint_broker(self, route_path):
        def broker(*args, **kwargs):
            route = self.routes[route_path]
            service = route.service
            url = service.urls.send(None)
            print("Service URL: ", url)
            if not url:
                if service.pending_requests.empty():
                    print("Starting Service")
                    self.service_start(service)
                # call this same function again after the service
                # started and the url exists
                d = defer.Deferred()
                d.addCallback(route.handler)
                service.pending_requests.put((d, args, kwargs))
            else:
                endpoint_url = url + route_path
                print("Making Request to Micro Service '%s'" % endpoint_url)
                d = treq.get(endpoint_url)
                d.addCallback(treq.content)
            return d
        return broker

    def create_endpoint_brokers(self):
        for module in self.service_modules:
            module_app = module.main.app
            service = Service(module=module)
            self.services[service._hash] = service
            for route_path in module_app.route_get():
                if route_path in self.routes:
                    msg = "Ruta utilizada en mas de un servicio '%s'" % route_path
                    raise Exception(msg)
                route_handler = self.endpoint_broker(route_path)
                route_handler.__name__ = route_path.replace('/', '_')
                route = Route(service=service, route=route_path, handler=route_handler)
                #route = Route()
                #route.service = service
                #route.route = route_path
                #route.hander = route_handler
                self.routes[route_path] = route
                self.app.route(route_path)(route_handler)
        pprint(self.services)
        for r in list(map(lambda r: (r[0], r[1], r[1].service), self.routes.items())):
            print(r)

    def create_routes(self):
        self.create_endpoint_brokers()
        self.app.route(self.register_url, methods=['POST'])(self._service_register)


if __name__ == '__main__':
    masterService = MasterService(app=app, autorun=True)
