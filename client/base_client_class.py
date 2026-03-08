class BaseClass:

    def pick_method(self, choices):
        """
        input for the client to pick a method from the class
        run the chosen method
        """
        print('what do you like to you do?')
        for key, value in choices.items():
            print(f"{key}: {value.replace('_', ' ')}")
        choice = input('your choice: ')
        picked_method = choices.get(choice)
        if picked_method:
            getattr(self, picked_method)()
        else:
            print('you must pick one of the presented options')
            self.pick_method(choices)
