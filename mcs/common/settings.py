from pydantic import BaseSettings


class Settings(BaseSettings):
    controller_hostname: str
    controller_http_port: str
    controller_tcp_port: str

    class Config:
        env_file = ".env"
