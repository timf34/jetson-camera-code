from awscrt import io
from dataclasses import dataclass
from typing import Optional

@dataclass
class IOTCredentials:
    cert_path: str
    client_id: str
    endpoint: str
    priv_key_path: str
    
    ca_path: Optional[str] = None
    port: int = 443
    region: str = "eu-west-1"

class IOTContext:
    client_bootstrap: io.ClientBootstrap
    event_loop_group: io.EventLoopGroup
    host_resolver: io.DefaultHostResolver

    def __init__(self):
        self.event_loop_group = io.EventLoopGroup(1)
        self.host_resolver = io.DefaultHostResolver(self.event_loop_group)
        self.client_bootstrap = io.ClientBootstrap(self.event_loop_group, self.host_resolver)