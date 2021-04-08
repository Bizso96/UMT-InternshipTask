
class PasswordChecker:
    def __init__(self):
        self.lengthError = 0
        self.repeatingErrors = []
        self.missingErrors = []

        self.insertions = 0
        self.deletions = 0
        self.replacements = 0

    def readString(self):
        return input("Password: ")

    def findProblems(self, s):
        '''
        Find the errors in the string. Sets the attributes of the class:
            - lengthError to a positive number representing how many characters are in addition to 20 or a negative
            number representing how many are needed to reach the count of 6
            - repeatingErrors to a list of numbers, each representing a separate sequence of that many of the same
            characters
            - missingErrors to a list of the possible strings "upperCase", "lowerCase", "number", containing the types
             of characters missing
        :param s: password
        :return: None
        '''

        self.lengthError = 0
        self.repeatingErrors = []
        self.missingErrors = []

        # Update lengthError if the number of characters is incorrect
        if len(s) < 6:
            self.lengthError = len(s) - 6
        elif len(s) > 20:
            self.lengthError = len(s) - 20
        else:
            self.lengthError = 0

        sequence = 1

        foundUpperCase = False
        foundLowerCase = False
        foundNumber = False

        # Check the type of the first character
        if s[0].isupper():
            foundUpperCase = True

        if s[0].islower():
            foundLowerCase = True

        if s[0].isnumeric():
            foundNumber = True

        # Starting from the second character, compare the characters to the previous ones and find repeating sequences.
        # Also check types
        for i in range(1, len(s)):
            if s[i].isupper():
                foundUpperCase = True

            if s[i].islower():
                foundLowerCase = True

            if s[i].isnumeric():
                foundNumber = True

            if s[i] == s[i - 1]:
                sequence += 1
            else:
                if sequence > 2:
                    self.repeatingErrors.append(sequence)
                sequence = 1

        if sequence > 2:
            self.repeatingErrors.append(sequence)

        # Add missing errors for types that were not found
        if not foundUpperCase:
            self.missingErrors.append("upperCase")

        if not foundLowerCase:
            self.missingErrors.append("lowerCase")

        if not foundNumber:
            self.missingErrors.append("number")

        # Sort the repeating errors, so that the shorter ones are solved sooner
        self.repeatingErrors.sort()


    def doInsertion(self):
        self.insertions += 1

        # Doing an insertion means we increase the length of the password.
        # We increase lengthError by 1, meaning that we get closer to the value 0, which means no length error
        self.lengthError += 1

        # If we do an insertion, we might as well do it so we solve a repeating error.
        # We insert the new character after the first 2 repeating ones, which means we decrease the
        # number of repeating characters by 2.
        # If the length of the repeating sequence falls below 3, we delete it (since it is no longer a problem)
        if self.repeatingErrors:
            self.repeatingErrors[0] -= 2
            if self.repeatingErrors[0] < 3:
                self.repeatingErrors.pop(0)

        # With insertion we can also solve one missing type problem
        if self.missingErrors:
            self.missingErrors.pop()

    def doDeletion(self):
        self.deletions += 1

        # Doing an insertion means we decrease the length of the password.
        # We decrease lengthError by 1, meaning that we get closer to the value 0, which means no length error
        self.lengthError -= 1

        # A deletion can decrease the length of a sequence by 1.
        # Our repeating sequence error is decreased by 1, and if it falls below 3, we delete it
        if self.repeatingErrors:
            self.repeatingErrors[0] -= 1
            if self.repeatingErrors[0] < 3:
                self.repeatingErrors.pop(0)

    def doReplacement(self):
        self.replacements += 1

        # A replacement decreases the repeating sequence error by 3. If the value falls bellow 3, we delete it
        if self.repeatingErrors:
            self.repeatingErrors[0] -= 3
            if self.repeatingErrors[0] < 3:
                self.repeatingErrors.pop(0)

        # We also solve a missing type error, if any exist
        if self.missingErrors:
            self.missingErrors.pop()

    def nrOfActions(self):
        '''
        Find the minimum number of actions required to solve all problems
        :return: nr of actions
        '''
        self.insertions = 0
        self.deletions = 0
        self.replacements = 0

        # If lengthError is greater than 0 (length of password greater than 20) then we apply deletions.
        # This can also solve repeating sequence errors
        while self.lengthError > 0:
            self.doDeletion()

        # If lengthError is less than 0 (length of password is less than 6) then we apply insertions.
        # This can also solve repeating sequence and missing type errors
        while self.lengthError < 0:
            self.doInsertion()

        # If there are repeating errors remaining, we use replacement to solve them.
        # This can also solve missing type errors
        while len(self.repeatingErrors) > 0:
            self.doReplacement()

        # If there are missing type errors remaining, we use replacement to solve them
        while len(self.missingErrors) > 0:
            self.doReplacement()

        return self.insertions + self.deletions + self.replacements

    def run(self):
        while True:
            s = self.readString()
            if s == "exit":
                break
            elif s == "":
                print("Please enter a password")
            else:
                self.findProblems(s)
                print("Length error:", self.lengthError)
                print("Repeating errors: ", self.repeatingErrors)
                print("Missing errors: ", self.missingErrors)
                print()

                nrOfActions = self.nrOfActions()

                print("Insertions: ", self.insertions)
                print("Deletions: ", self.deletions)
                print("Replacements: ", self.replacements)
                print()

                print("Total number of actions: ", nrOfActions)


passwordChecker = PasswordChecker()
passwordChecker.run()
