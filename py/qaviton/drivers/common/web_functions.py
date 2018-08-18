from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from qaviton.drivers.common.webelement import WebElement
from qaviton.locator import ByExtension
from qaviton.locator import Locator
from qaviton.drivers.support import expected_conditions_extension as EC


class WebFunctions:
    """this class is added to ~( webdriver & webelement )~
    to add same functionality to both driver & element
    """

    def heal(self, element, locators_to_heal, locators):
        """ find element attributes and try to send healing info to qaviton.com/proj/heal
        :type element: WebElement
        :type locators_to_heal: list
        :type locators: tuple
        :return:
        """
        pass

    def find(self, locator: tuple, timeout: int = 0, index=0):
        """find element with locator value
        :param locator: locate by method like id and value
        :param timeout: how long to search
        :param index: parameter for special cases
                  where a list of elements is in the locator,
                  the default element to return is elements[0]
        :rtype: WebElement
        """

        # use this locate method if timeout is 0
        def fast(locate):
            return self.find_element(*locate)

        # use this locate method if timeout > 0
        def slow(locate):
            return WebDriverWait(self, timeout).until(EC.presence_of_element_located(locate))

        # classify locator method
        by, value = Locator.any(locator)
        if by == ByExtension.ELEMENTS:
            return value[index]
        elif by == ByExtension.ELEMENT:
            return value

        # healing functionality
        elif by in (ByExtension.TUPLE, ByExtension.LIST):
            # choose finding method
            if timeout > 0:
                get = slow
            else:
                get = fast

            # set healing parameters
            locators_to_heal = []
            element = None
            for location in value:
                try:
                    # find element
                    element = get(location)
                    break
                except:
                    locators_to_heal.append(location)

            # raise error if healing is impossible
            if element is None:
                raise NoSuchElementException

            # heal and return
            else:
                if len(locators_to_heal) > 0:
                    self.heal(element, locators_to_heal, locator)
                return element

        # choose finding method
        if timeout > 0:
            get = slow
        else:
            get = fast

        # find element
        return get((by, value))

    def find_all(self, locator: tuple, timeout: int = 0):
        """find all elements with locator value
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: list[WebElement]"""

        # use this locate method if timeout is 0
        def fast(locate):
            return self.find_elements(*locate)

        # use this locate method if timeout > 0
        def slow(locate):
            return WebDriverWait(self, timeout).until(EC.presence_of_all_elements_located(locate))

        # classify locator method
        by, value = Locator.any(locator)
        if by == ByExtension.ELEMENTS:
            return value
        elif by == ByExtension.ELEMENT:
            return [value]

        # healing functionality
        elif by in (ByExtension.TUPLE, ByExtension.LIST):
            # choose finding method
            if timeout > 0:
                get = slow
            else:
                get = fast

            # set healing parameters
            locators_to_heal = []
            elements = None
            for location in value:
                try:
                    # find elements
                    elements = get(location)
                    break
                except:
                    locators_to_heal.append(location)

            # raise error if healing is impossible
            if elements is None:
                raise NoSuchElementException

            # heal and return
            else:
                if len(locators_to_heal) > 0:
                    self.heal(elements[0], locators_to_heal, locator)
                return elements

        # choose finding method
        if timeout > 0:
            get = slow
        else:
            get = fast

        # find elements
        return get((by, value))

    def get_elements_text(self, locator, timeout=0):
        """ get text from elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[str]
        """
        element_list, elements_text = self.find_all(locator, timeout), []
        for i in range(len(element_list)):
            elements_text.append(element_list[i].text)
        return elements_text

    def try_to_find(self, locator: tuple, timeout=0, index=0):
        """try to find element
        :param index: parameter for special cases
                      where a list of elements is in the locator,
                      the default element to return is elements[0]
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: WebElement | None"""
        try:
            return self.find(locator, timeout, index)
        except:
            return None

    def try_to_find_all(self, locator: tuple, timeout=0):
        """try to find elements
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: list[WebElement] | None"""
        try:
            return self.find_all(locator, timeout)
        except:
            return None

    def try_to_get_elements_text(self, locator, timeout=0):
        """ get text from elements if any elements are located
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[str] | []
        """
        element_list, elements_text = self.try_to_find_all(locator, timeout), []
        for i in range(len(element_list)):
            elements_text.append(element_list[i].text)
        return elements_text