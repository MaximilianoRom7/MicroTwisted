import os
from twisted.internet import defer
from configargparse import ArgParser


def create_test_routes(app, service_name, routes_count, log=False):
    routes_start = 1
    for s in range(routes_start, routes_count + routes_start):
        route_path = "/" + service_name + "/route" + str(s)
        def new_handler(route_path):
            def route_handler():
                return route_path
            return route_handler
        route_handler = new_handler(route_path)
        #if log:
        print("Ruta: ", route_path)
        route_handler.__name__ = route_path.replace("/", "_")
        app.route(route_path)(route_handler)


def inlineCallbacksCatch(func):
    """
    Wrapper for defer.inlineCallbacks decorator
    catches all exceptiosn and returns "Internal Service Error"
    """
    @defer.inlineCallbacks
    def wrapper(*args, **kwargs):
        try:
            response = yield from func(*args, **kwargs)
        except Exception as error:
            print("Error: ", error)
            response = yield str({'Error': "Internal Service Error"})
        print("Response: ", response)
        return response
    return wrapper


class MasterServiceArgumentParser(ArgParser):

    def __init__(self, *args, **kwargs):
        super(MasterServiceArgumentParser, self).__init__(*args, **kwargs)
        file_config = 'service-master.cfg'
        if os.path.isfile(file_config):
            self.add('--master-config', is_config_file=True, default=file_config)
        self.add('--master-port', required=True, type=int, nargs='?')
        self.add('--master-services', required=True, type=str, nargs='+')
        args, unknown = self.parse_known_args()
        assert list(filter(bool, args.master_services)), \
            "Need at least one service to start --master-services []"


class MicroServiceArgumentParser(ArgParser):

    def __init__(self, *args, **kwargs):
        super(MicroServiceArgumentParser, self).__init__(*args, **kwargs)
        file_config = 'service-slave.cfg'
        if os.path.isfile(file_config):
            self.add('--service-config', is_config_file=True, default=file_config)
        self.add('--service-register', type=str, nargs='?')
        self.add('--service-hash', type=str, nargs='?')
        self.add('--service-port', type=int, nargs='?')
        args, unknown = self.parse_known_args()
