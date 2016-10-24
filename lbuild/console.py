#!/usr/bin/env python3
#
# Copyright (c) 2016, Fabian Greif
# All Rights Reserved.
#
# The file is part of the lbuild project and is released under the
# 2-clause BSD license. See the file `LICENSE.txt` for the full license
# governing this code.

import os
import sys
import logging

LOGGER = logging.getLogger("lbuild.console")

class Console:

    def __init__(self, enable_markdown=True):
        self._formatter = None
        if self._supports_color() and enable_markdown:
            self._load_markdown()

        if self._formatter is None:
            self._formatter = self.__forward

    @staticmethod
    def _supports_color():
        """
        Returns True if the running system's terminal supports color, and False
        otherwise.
        """
        plat = sys.platform
        supported_platform = (plat != 'win32' or 'ANSICON' in os.environ)

        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        if not supported_platform or not is_a_tty:
            return False
        else:
            return True
    
    def _load_markdown(self):
        try:
            from .mdv import main
            self._markdownviewer = main
            self._formatter = self.__markdown
            LOGGER.debug("Found Markdown formatter")
        except ImportError as error:
            LOGGER.warning("Disable Markdown formatting due to: %s", str(error))

    def __forward(self, text):
        return text
    
    def __markdown(self, text):
        output = self._markdownviewer(md=text,
                                      c_no_guess=1,
                                      theme=663.6093,
                                      c_theme=579.6579,
                                      c_def_lexer='cpp')
        return output.rstrip()

    def format(self, text=" "):
        return self._formatter(text)
