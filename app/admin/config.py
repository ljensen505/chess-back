import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: str


@lru_cache()
def get_settings():
    domain = os.getenv("AUTH0_DOMAIN")
    audience = os.getenv("AUTH0_API_AUDIENCE")
    issuer = os.getenv("AUTH0_ISSUER")
    algorithms = os.getenv("AUTH0_ALGORITHMS")

    if None in [domain, audience, issuer, algorithms]:
        raise ValueError("Missing environment variables")
    return Settings(
        auth0_domain=domain,  # type: ignore
        auth0_api_audience=audience,  # type: ignore
        auth0_issuer=issuer,  # type: ignore
        auth0_algorithms=algorithms,  # type: ignore
    )
