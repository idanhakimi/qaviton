import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Remote
from qaviton import crosstest
from qaviton import settings
from qaviton.utils import path


platforms = crosstest.Platforms()
platforms.web.add(DesiredCapabilities.CHROME)
platforms.web.add(DesiredCapabilities.FIREFOX)
platforms.mobile.add({
    "platformName": "Android",
    "platformVersion": "6.0",
    "deviceName": "emulator-5554",
    "app": path.get(__file__)('../../../sample-code/apps/ContactManager/ContactManager.apk')})
mod = crosstest.Models(platforms).get


@pytest.mark.parametrize('platform', platforms.get, ids=(lambda test: str(test.id)))
def test_platforms(platform):
    assert platform["testing_type"] == crosstest.TestingTypes.WEB
    assert platform["desired_capabilities"] == DesiredCapabilities.CHROME or \
           platform["desired_capabilities"] == DesiredCapabilities.FIREFOX


@pytest.mark.parametrize('test', mod, ids=(lambda test: str(test.id)))
def test_models(test: crosstest.Model):
    assert test.desired_capabilities == DesiredCapabilities.CHROME or test.desired_capabilities == DesiredCapabilities.FIREFOX
    assert test.testing_type == crosstest.TestingTypes.WEB
    assert test.driver_url == settings.driver_url
    assert test.driver_api == Remote
