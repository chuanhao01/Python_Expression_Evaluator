import click

@click.command()
@click.option('--count', default = 1, help = "Number of greetings")
@click.option('--name', prompt = "Your Name", help = "The name of the user")
@click.option('--greeting', "-g", default = "Hello")
@click.option('--question', is_flag = True)
def hello(count, name, greeting, question):
    '''
        Click Program that greets Name for Count number of times
    '''
    for i in range(count):
        if question:
            click.echo(f"{greeting}, {name}?")
        else:
            click.echo(f"{greeting}, {name}!")

    click.clear()


if __name__ == "__main__":
    hello()