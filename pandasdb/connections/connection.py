from sshtunnel import SSHTunnelForwarder
from pandasdb.utils import string_to_python_attr, AutoComplete


class Connection:

    def __init__(self, host="", schema="public", username="", password="", port=-1, database="", tunnel=None,
                 ssh_username=None,
                 ssh_key=None):

        self.schema = schema
        self._tunnel = tunnel
        self._ssh_username = ssh_username
        self._ssh_key = ssh_key
        self._port = port
        self._host = host

        self.forwarder = None
        self.host = None
        self.port = None
        self.username = username
        self.password = password
        self.database = database
        self.reserved_words = []

    def maybe_start_tunnel(self):
        if not self.forwarder and self._tunnel:
            IP, PORT = self._tunnel
            self.forwarder = SSHTunnelForwarder((IP, int(PORT)),
                                                ssh_private_key=self._ssh_key,
                                                ssh_username=self._ssh_username,
                                                remote_bind_address=(self._host, int(self._port)))
            self.forwarder.daemon_forward_servers = True
            self.forwarder.start()

            self.port = self.forwarder.local_bind_port
            self.host = "localhost"
        else:
            self.host = self._host
            self.port = self._port

    @property
    def conn(self):
        self.maybe_start_tunnel()
        if hasattr(self, "_conn"):
            return getattr(self, "_conn")
        else:
            setattr(self, "_conn", self.connect())
            return self.conn

    @property
    def TBL(self):
        try:
            return self._TBL
        except:
            TBL = AutoComplete("Tables", {string_to_python_attr(table.name): table for table in self.get_tables()})
            setattr(self, "_TBL", TBL)
            return self._TBL

    def connect(self):
        raise NotImplementedError("connect() should be implemented by all children")

    @staticmethod
    def str_representation(operator):
        raise NotImplementedError("operator(operator) should be implemented by all children")

    @staticmethod
    def dict_representation(operator):
        raise NotImplementedError("dict_operator(operator) should be implemented by all children")

    def accepted_types(self, operator):
        raise NotImplementedError("accepted_types(operator) should be implemented by all children")

    def query(self, action, columns, table_name, joins, where, groups, having, meta):
        raise NotImplementedError(
            "query( action, columns, table_name, joins, where, groups, having, meta) should be implemented by all children")

    def execute(self, action, target_columns, table_name, joins, where, groups, having, meta):
        raise NotImplementedError(
            "execute( action, target_columns, table_name, joins, where, groups, having, meta) should be implemented by all children")

    def optimize(self, action, target_columns, table_name, joins, where, groups, having, meta):
        raise NotImplementedError(
            "optimize( action, target_columns, table_name, joins, where_conditions, groups, having_conditions, meta) should be implemented by all children")

    def get_tables(self):
        raise NotImplementedError("get_tables() should be implemented by all children")

    def get_columns(self, table):
        raise NotImplementedError("get_columns(table) should be implemented by all children")
