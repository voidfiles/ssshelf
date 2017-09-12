import asyncio
import pytest
from aiobotocore.config import AioConfig
import aiobotocore
import requests
import shutil
import signal
import subprocess as sp
import sys
import time


@pytest.fixture
def region():
    return 'us-east-1'


@pytest.yield_fixture
def loop(request):
    try:
        old_loop = asyncio.get_event_loop()
    except RuntimeError:
        old_loop = None

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)

    yield loop

    loop.close()
    asyncio.set_event_loop(old_loop)


def moto_config(endpoint_url):
    AWS_ACCESS_KEY_ID = "xxx"
    AWS_SECRET_ACCESS_KEY = "xxx"
    kw = dict(endpoint_url=endpoint_url,
              aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
              aws_access_key_id=AWS_ACCESS_KEY_ID)
    return kw


def create_client(client_type, request, loop, session, region, config, **kw):
    @asyncio.coroutine
    def f():
        return session.create_client(client_type, region_name=region,
                                     config=config, **kw)
    client = loop.run_until_complete(f())

    def fin():
        loop.run_until_complete(client.close())
    request.addfinalizer(fin)
    return client


@pytest.fixture
def signature_version():
    return 's3'


@pytest.fixture
def config(region, signature_version):
    return AioConfig(region_name=region, signature_version=signature_version,
                     read_timeout=5, connect_timeout=5)


@pytest.fixture
def session(loop):
    session = aiobotocore.get_session(loop=loop)
    return session


@pytest.fixture
def s3_client(request, session, region, config, loop, s3_server):
    kw = {
        "endpoint_url": s3_server
    }

    client = create_client('s3', request, loop, session, region, config, **kw)

    return client

_proxy_bypass = {
  "http": None,
  "https": None,
}


def start_service(service_name, host, port):
    moto_svr_path = shutil.which("moto_server")
    args = [sys.executable, moto_svr_path, service_name, "-H", host,
            "-p", str(port)]
    process = sp.Popen(args, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.DEVNULL)
    url = "http://{host}:{port}".format(host=host, port=port)

    for i in range(0, 30):
        if process.poll() is not None:
            break

        try:
            # we need to bypass the proxies due to monkeypatches
            requests.get(url, timeout=0.5, proxies=_proxy_bypass)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    else:
        stop_process(process)  # pytest.fail doesn't call stop_process
        pytest.fail("Can not start service: {}".format(service_name))

    return process


def stop_process(process):
    try:
        process.send_signal(signal.SIGTERM)
        process.communicate(timeout=20)
    except sp.TimeoutExpired:
        process.kill()
        outs, errors = process.communicate(timeout=20)
        exit_code = process.returncode
        msg = "Child process finished {} not in clean way: {} {}" \
            .format(exit_code, outs, errors)
        raise RuntimeError(msg)


@pytest.yield_fixture(scope="session")
def s3_server():
    host = "127.0.0.1"
    port = 5000
    url = "http://{host}:{port}".format(host=host, port=port)
    process = start_service('s3', host, port)
    yield url
    stop_process(process)
