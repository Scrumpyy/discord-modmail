"""
MIT License

Copyright (c) 2022-present Scrumpy (Jay)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os.path
import textwrap

if not os.path.exists(".env"):
    bot_token = str(input("What is your Discord bot's token?: "))
    with open(".env", "w+") as env_file:
        env_file.write(textwrap.dedent(f"""
            TOKEN = "{bot_token}"
        """)

if not os.path.exists("config.py"):
    bot_status = str(input("What do you want your Discord Bot's status to be?: Playing "))
    bot_prefix = str(input("What do you want your Discord Bot's prefix to be?: "))
    project_nickname = str(input("What do you want the projects nickname to be?: "))
    bot_commander_role_id = int(input("What is the Role ID for the bot commander role?: "))
    with open("config.py", "w+") as config_file:
        config_file.write(textwrap.dedent(f"""
            STATUS = "{bot_status}"
            PREFIX = "{bot_prefix}"
            PROJECT_NICKNAME = "{project_nickname}"
            BOT_COMMANDER_ROLE_ID = {bot_commander_role_id}
        """)