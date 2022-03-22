class Change:
    changed_object = None
    attribute = ""
    value = None

    def __init__(self, changed_object, attribute, value):
        """ summary: initializes the object

            params:
                changed_object: Object; the object that should be changed
                attribute: String; the name of the object that should be changed
                value: Anything; the value of the attribute that should be changed

            returns: None
        """
        
        self.changed_object, self.attribute = changed_object, attribute
        self.value = value


class Changer:
    changes = []

    def add_change(self, changed_object, attribute, value):
        """ summary: Does the change to the object, but it is at the end of a code cycle; NOTE: order matters: FIFO

            params:
                changed_object: Object; the object that will be changed
                attribute: String; the name of the attribute that should be changed
                value: Anything; the value of the attribute that should be changed
        """

        self.changes.append(Change(changed_object, attribute, value))


    def run_changes(self):
        """Runs all the changes to the objects; NOTE: must be called at the end of the cycle to function properly"""

        for change in self.changes:
            change.changed_object.__dict__[change.attribute] = change.value

        self.changes = []



