import asyncio
from typing import Optional
from urllib.parse import urlparse, parse_qs

from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.network_manager import Request
from requests.models import PreparedRequest

from config import config, logging
from token_request import request_token

BROWSER: Optional[Browser] = None

LL = logging.getLogger(__name__)


def build_url():
    url = config.authz_endpoint
    params = {
        'response_type': 'code',
        'client_id': config.client_id,
        'scope': config.get_scopes_as_str(),
        'redirect_uri': config.redirect_uri
    }
    req = PreparedRequest()
    req.prepare_url(url, params)
    return req.url


def extract_code(url: str):
    o = urlparse(url)
    query = parse_qs(o.query)
    return query.get('code')[0]


def found(code: str):
    request_token(code)


async def intercept_request(request: Request):
    if back_to_redirect_uri(request.url):
        LL.info("Got redirect back to redirect_uri.")
        if code := extract_code(request.url):
            LL.info(f"Code extracted from callback URL: {code}")
            found(code)
    else:
        LL.debug(f'ON REQUEST (CONTINUE): {request.url}')


def back_to_redirect_uri(destination):
    return config.redirect_uri in destination


async def main():
    global BROWSER
    login_url = build_url()
    LL.info(f'URL: {login_url}')

    browser, page = await set_up()
    BROWSER = browser

    await login(login_url, page)
    await browser.close()


async def set_up():
    browser = await launch(headless=False,
                           devtools=False)
    page = await browser.newPage()

    await page.setRequestInterception(False)

    return browser, page


async def login(login_url, page):
    await page.goto(login_url)
    await page.type('#accountId', config.user.cpf)
    await page.click('button[name="action"')
    await asyncio.sleep(1)

    # Watch all requests waiting for the request leading back to REDIRECT_URI
    captcha_solved = asyncio.ensure_future(
        page.waitForNavigation(timeout=1000 * 100))
    page.on('request', lambda req: asyncio.ensure_future(intercept_request(req)))

    await page.type('#password', config.user.senha)
    await page.click('button[value="enterPassword"')

    await captcha_solved
    LL.info("Captcha solved")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
