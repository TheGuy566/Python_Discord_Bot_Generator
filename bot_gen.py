import os
import click
import difflib


@click.command()
def main(quick_bot):
    while True:
        path = click.prompt('Folder Path').strip()

        if "." in path:
            print ('Error: File names can not be in path.')
        elif not path:
            print ('Error: Enter a folder path.')
        elif not os.path.exists(path):
            print ("Error: That folder does not exist.")
        elif not os.access(path, os.W_OK | os.X_OK):
            print ("Error: You do not have permission to write in that folder.")
        else:
            break
    
    while True:
        name = click.prompt('Bot file name')
        
        if len(name) == 0:
            print ("Error: Please enter a name.")
        elif "." in name or '/' in name:
            print ("Error: '.' and '/' can't be in file name.")
        else:
            break

    while True:
        env = click.prompt('Add .env file').lower()
        env = difflib.get_close_matches(env, ["yes", "no"], n=1)[0]

        if not env:
            print ("Error: Please enter yes or no.")
        else:
            break

    while True:
        git_ignore = click.prompt('Add .gitignore file').lower()
        git_ignore = difflib.get_close_matches(git_ignore, ["yes", "no"], n=1)[0]

        if not git_ignore:
            print ("Error: Please enter yes or no.")
        else:
            break

    while True:
        commands = click.prompt('Number of Commands')

        try:
            commands = int(commands)
            if commands <= 0:
                print ("Error: Please select a number >= 1")
            else:
                break
        except:
            pass


    if env:
        env_file = open(f"{path}/.env", "a")
        env_file.write(f"TOKEN=secret_key")
        env_file.close()
    if git_ignore:
        git_file = open(f"{path}/.git_ignore", "a")
        git_file.write("__pycache__/\n*.py[cod]\n*$py.class\n")
        if env:
            git_file.write("\n.env")
        git_file.close()


    bot_file = open(f"{path}/{name}.py", "a")

    if env:
        bot_file.write("import os\n")
    bot_file.write("import discord\n")
    if env:
        bot_file.write("from dotenv import load_dotenv\n")
    bot_file.write("from discord.ext import commands, tasks\n\n\n")

    bot_file.write("bot = commands.Bot(command_prefix='.')\n")
    bot_file.write("bot.remove_command('help')\n\n")
    if env:
        bot_file.write("load_dotenv()\ntoken = os.getenv('TOKEN')\n\n\n")
    else:
        bot_file.write("token = ''\n\n\n")
    
    bot_file.write("@bot.event\n")
    bot_file.write("async def on_ready():\n")
    bot_file.write("    print(f'Logged on as {bot.user.name}.')\n")
    bot_file.write("    return\n\n\n")

    for x in range(1, commands + 1):
        bot_file.write("@bot.command(name='', description='')\n")
        bot_file.write(f"async def command_{x}(ctx, value):\n")
        bot_file.write("    return\n\n\n")

    bot_file.write("bot.run(token)\n")
    bot_file.close()

    print ("Discord Bot generated!")


if __name__ == "__main__":
    main()
