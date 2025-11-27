import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cli_agent import read_file, ask_llm, format_llm_answer

class TestCliGpt(unittest.TestCase):

    def test_read_file(self):
        m = mock_open(read_data="file's content")
        with patch("builtins.open", m):
            res = read_file("path")
            self.assertEqual(res, "file's content")
            m.assert_called_once_with("path", 'r')
    
    def test_format_llm_answer(self):

        # Test replacing single backslash escaped codes
        # Supported codes: 033[91m (Red) & 033[0m (Reset)
        input_str = "Hy \\033[91mab\\033[0m"
        expected_str = "Hy \033[91mab\033[0m"
        self.assertEqual(format_llm_answer(input_str), expected_str)

        # Test replacing double backslash escaped codes
        # Supported code 033[92m (Green) 
        input_str_2 = "Hy \\\\033[92mGreen\\\\033[0m"
        expected_str_2 = "Hy \033[92mGreen\033[0m"
        self.assertEqual(format_llm_answer(input_str_2), expected_str_2)

        # Test no changes
        input_str_3 = "Mock Testing"
        self.assertEqual(format_llm_answer(input_str_3), "Mock Testing")

    @patch("cli_agent.Groq")
    @patch("cli_agent.read_file")
    @patch.dict(os.environ, {"GROQ_KEY": "fake_key"})
    def test_ask_llm(self, mock_read_file, mock_groq):
        #Set Up Mocks

        mock_read_file.return_value = "Mock Context"

        mock_client  = MagicMock()
        mock_groq.return_value = mock_client

        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message.content = "Mock Answer"
        mock_client.chat.completions.create.return_value = mock_completion

        res = ask_llm("Why the sky is blue?")

        # Assertions
        self.assertEqual(res, "Mock Answer")
        mock_groq.assert_called_once_with(api_key="fake_key")
        mock_client.chat.completions.create.assert_called_once()
        
        # Check arguments passed to create
        call_args = mock_client.chat.completions.create.call_args
        self.assertEqual(call_args.kwargs['messages'][0]['content'], "Mock Context")
        self.assertEqual(call_args.kwargs['messages'][1]['content'], "Why the sky is blue?")