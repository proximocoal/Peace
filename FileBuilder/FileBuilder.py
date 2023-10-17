import os


class FileBuilder():

    """Create a file for entering card data

    Class variables:
        available_formats - set

    Instance Variables:
        new_file - boolean
        format - string
        file_name - string
        overwrite - boolean
        active_file - file object
        repeat - integer

    Methods:
        __init__ - constructor
        make_file - Make a file object depending on input variables
        new_file_q - Take user input if new file wanted
        what_format_q - Take user input what format option wanted
        convert_to_bool - change strings true and false to boolean values
        overwrite_q - Take user input if they want to overwrite file contents
        take_filename - Take user input of filename and check
        file_interface - combine class methods to create relevant file

    Dependencies:
        import OS
    """

    available_formats = {"csv"}

    def __init__(self):
        """Constructor. No arguments. Initialises empty variables"""
        self.new_file = ""
        self.format = ""
        self.file_name = ""
        self.overwrite = ""
        self.active_file = ""
        self.repeat = 0

    def make_file(self):
        """Make or open a newfile based on arguments.

        Dependencies:
            self.active_file
            self.overwrite
            self.file_name
            self.format
        """

        mode = "a"
        if self.overwrite:
            mode = "w"
        self.active_file = open(f"{self.file_name}.{self.format}", mode)

    def new_file_q(self):
        """Ask for user to input if new file wanted until True or False.

        Dependencies:
            self.convert_to_bool()
            self.new_file
            self.repeat
            self.repeat_check()
        """
        test = True
        new = ""
        while test:
            new = input("""Do you want to make a new file?
                             Enter True or False or leave empty to escape""")
            new = new.lower()
            new = self.convert_to_bool(new)
            if self.repeat_check():
                new = ""
            if type(new) is bool or new == "":
                test = False
        self.new_file = new
        self.repeat = 0

    def what_format_q(self):
        """Ask user to input file type until valid option entered

        Dependencies:
            FileBuilder.available_formats
            self.format
            self.repeat
            self.repeat_check()
        """
        test = True
        format = ""
        while test:
            format = input(f"""What format do you want the file to be?
                        Input must be one of the following:
                        {FileBuilder.available_formats}
                        Leave input empty to escape""")
            format = format.lower()
            if self.repeat_check():
                format = ""
            if format in FileBuilder.available_formats or format == "":
                test = False
        self.format = format
        self.repeat = 0

    def convert_to_bool(self, input):
        """Return a boolean if input is "true" or "false", else return input"""
        response = input
        if input == "true":
            response = True
        elif input == "false":
            response = False
        return (response)

    def overwrite_q(self):
        """Ask user if they want to overwrite existing file
           until True or False entered.

        Dependencies:
            self.convert_to_bool()
            self.overwrite
            self.repeat
            self.repeat_check()
        """
        test = True
        while test:
            overwrite_a = input("""Do you want to overwrite existing file?
                                     Enter True or False.
                                     Leave empty to escape""")
            overwrite_a = overwrite_a.lower()
            overwrite_a = self.convert_to_bool(overwrite_a)
            if self.repeat_check():
                overwrite_a = ""
            if type(overwrite_a) is bool or overwrite_a == "":
                test = False
        self.overwrite = overwrite_a
        self.repeat = 0

    def take_filename(self):
        """Take filename and check if file exists if not ask again.

        Dependencies:
            import OS
            self.filename
            self.repeat
            self.repeat_check()
        """
        test = True
        while test:
            filename = input("Enter filename or leave input empty to escape")
            if self.repeat_check():
                filename = ""
            if filename == "":
                test = False
            elif os.path.exists(filename):
                test = False
            else:
                print("File not found, please try again")
        self.file_name = filename
        self.repeat = 0

    def repeat_check(self):
        """Increase self.repeat unless greater than 10, then return True"""
        response = False
        if self.repeat > 9:
            response = True
        else:
            self.repeat += 1
        return (response)

    def fileinterface(self):
        """Co-ordinating method. Create or Open file based on user input.

        Dependencies:
            self.new_file()
            self.what_format()
            self.overwrite_q()
            self.take_filename()
            self.make_file()
            self.new_file()
            self.overwrite
            self.file_name
            self.format
            self.active_file
            self.repeat_check()
            self.repeat
        """
        self.new_file_q()
        if self.new_file:
            self.what_format_q
        else:
            self.take_filename
            self.overwrite_q
        self.make_file()