from FileBuilder import FileBuilder
import unittest.mock
import unittest


class TestFileBuilder(unittest.TestCase):

    def setUp(self):
        self.test = FileBuilder()

    def tearDown(self):
        del self.test

    @unittest.mock.patch("builtins.open")
    def test_make_file(self, mock_builtins):
        self.test.file_name = "TestFile"
        self.test.format = "csv"
        self.test.overwrite = True
        self.test.make_file()
        mock_builtins.assert_called_with("TestFile.csv", "w")

    @unittest.mock.patch("builtins.input", return_value="True")
    def test_new_file_q_t(self, mock_inputs):
        self.test.new_file_q()
        assert self.test.new_file == True

    @unittest.mock.patch("builtins.input", return_value="false")
    def test_new_file_q_f(self, mock_inputs):
        self.test.new_file_q()
        assert self.test.new_file == False

    @unittest.mock.patch("builtins.input", return_value="")
    def test_new_file_q_e(self, mock_inputs):
        self.test.new_file_q()
        assert self.test.new_file == ""

    @unittest.mock.patch("builtins.input", return_value="yes")
    def test_new_file_q_w(self, mock_inputs):
        self.test.new_file_q()
        assert self.test.new_file == ""

    @unittest.mock.patch("builtins.input", return_value="yes")
    def test_overwrite_q_w(self, mock_inputs):
        self.test.overwrite_q()
        assert self.test.overwrite == ""

    @unittest.mock.patch("builtins.input", return_value="")
    def test_overwrite_q_e(self, mock_inputs):
        self.test.overwrite_q()
        assert self.test.overwrite == ""

    @unittest.mock.patch("builtins.input", return_value="True")
    def test_overwrite_q_t(self, mock_inputs):
        self.test.overwrite_q()
        assert self.test.overwrite == True

    @unittest.mock.patch("builtins.input", return_value="false")
    def test_overwrite_q_f(self, mock_inputs):
        self.test.overwrite_q()
        assert self.test.overwrite == False

    @unittest.mock.patch("builtins.input", return_value="csv")
    def test_what_format_q_csv(self, mock_inputs):
        self.test.what_format_q()
        assert self.test.format == "csv"

    @unittest.mock.patch("builtins.input", return_value="")
    def test_what_format_q_e(self, mock_inputs):
        self.test.what_format_q()
        assert self.test.format == ""

    @unittest.mock.patch("builtins.input", return_value="JSON")
    def test_what_format_q_json(self, mock_inputs):
        self.test.what_format_q()
        assert self.test.format == ""

    def test_convert_to_bool_true(self):
        assert self.test.convert_to_bool("true") == True

    def test_convert_to_bool_false(self):
        assert self.test.convert_to_bool("false") == False

    def test_convert_to_bool_empty(self):
        assert self.test.convert_to_bool("") == ""

    @unittest.mock.patch("os.path.exists", return_value=True)
    @unittest.mock.patch("builtins.input", return_value="something.csv")
    def test_take_filename_t(self, mock_input, mock_path):
        self.test.take_filename()
        assert self.test.file_name == "something.csv"

    @unittest.mock.patch("builtins.input", return_value="")
    def test_take_filename_e(self, mock_input):
        self.test.take_filename()
        assert self.test.file_name == ""

    @unittest.mock.patch("os.path.exists", return_value=False)
    @unittest.mock.patch("builtins.input", return_value="something.json")
    def test_take_filename_w(self, mock_input, mock_path):
        self.test.take_filename()
        assert self.test.file_name == ""

if __name__ == "__main__":
    unittest.main()