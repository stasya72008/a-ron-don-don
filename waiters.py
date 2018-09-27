class element_has_attribute(object):
    """An expectation for checking that an element has a particular attribute.

    returns the WebElement once it has the particular attribute
    """

    def __init__(self, locator, attribute_name, attribute_value):
        self.locator = locator
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.attribute_value in element.get_attribute(self.attribute_name):
            return element
        else:
            return False
