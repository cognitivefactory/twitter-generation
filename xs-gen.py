#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#! Xs (former tweets) Generator
#!
#! Copyright (c) 2023, ThomasByr
#! AGPL-3.0-or-later (https://www.gnu.org/licenses/agpl-3.0.en.html)
#! All rights reserved.
#!
#! Redistribution and use in source and binary forms, with or without
#! modification, are permitted provided that the following conditions are met:
#!
#! * Redistributions of source code must retain the above copyright notice,
#!   this list of conditions and the following disclaimer.
#!
#! * Redistributions in binary form must reproduce the above copyright notice,
#!   this list of conditions and the following disclaimer in the documentation
#!   and/or other materials provided with the distribution.
#!
#! * Neither the name of this software's authors nor the names of its
#!   contributors may be used to endorse or promote products derived from
#!   this software without specific prior written permission.
#!
#! This program is free software: you can redistribute it and/or modify
#! it under the terms of the GNU Affero General Public License as published by
#! the Free Software Foundation, either version 3 of the License, or
#! (at your option) any later version.
#!
#! This program is distributed in the hope that it will be useful,
#! but WITHOUT ANY WARRANTY; without even the implied warranty of
#! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#! GNU Affero General Public License for more details.
#!
#! You should have received a copy of the GNU Affero General Public License
#! along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys


if sys.version_info < (3, 8):
    raise RuntimeError("This program requires Python 3.10")


if __name__ == "__main__":
    from termcolor import colored
    from alive_progress import config_handler
    from alive_progress.animations.bars import bar_factory
    from alive_progress.animations.spinners import frame_spinner_factory

    from src.cli import gp_parser, CliApp

    bar = bar_factory("\u2501", borders=(" ", " "), background=" ")
    spinner = frame_spinner_factory([colored(p, "cyan") for p in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"])
    config_handler.set_global(length=40, max_cols=110, enrich_print=False, bar=bar, spinner=spinner)

    CliApp().check_args(gp_parser().parse_args()).run()
