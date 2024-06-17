#!/usr/bin/python3
""" Unittest for console """
import unittest
from io import StringIO
from unittest.mock import patch
import os
from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage


class ConsoleTests(unittest.TestCase):
    """Unittests for Console"""
    def setUp(self):
        '''deletes file.json before every test '''
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}


    def test_help_create(self):
        """test for help and ? create output"""

        expected = """Creates a new instance of a Class, saves it to the JSON
        file and prints the id.
        Usage: create <classname> <param> <param>"""

        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            print_out = output.getvalue().strip()
            self.assertEqual(expected, print_out)

        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("? create"))
            print_out = output.getvalue().strip()
            self.assertEqual(expected, print_out)

    def test_create(self):
        """test the create cmd"""
        
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            print_out = output.getvalue().strip()
            self.assertEqual("** class name missing **", print_out)

        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create base"))
            print_out = output.getvalue().strip()
            self.assertEqual("** class doesn't exist **", print_out)

        
        with patch('sys.stdout', new=StringIO()) as output:
            cmd_str = 'create BaseModel name="Gilbert" age=89'
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            new_instance_id = output.getvalue().strip()
            key = 'BaseModel' + '.' + new_instance_id
            new_obj = FileStorage._FileStorage__objects[key]
            self.assertTrue(hasattr(new_obj, 'name'))
            self.assertTrue(hasattr(new_obj, 'age'))





