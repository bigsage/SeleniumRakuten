class Browser:
    def __init__(self, driver):
        self.driver = driver

    def scroll_by_elem_and_offset(self, element, offset=0):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        if offset != 0:
            script = "window.scrollTo(0, window.pageYOffset + " + str(offset) + ");"
            self.driver.execute_script(script)