import unittest
from unittest.mock import patch, MagicMock, mock_open
import os 
from cli_agent import read_file, ask_llm, format_llm_answer

class TestCliGpt(unittest.TestCase):

    def test_read_file(self):
        m = mock_open(read_data="file's content")
        with patch("builtins.open", m):
            res = read_file("path")
            self.assertEqual(res, "file's content")
            m.assert_called_once_with("path", 'r')
    
