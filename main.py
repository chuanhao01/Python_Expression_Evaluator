from src.basic.cli import CLI as BasicCLI
from src.advance import CLI as AdvanceCLI

if __name__ == '__main__':
    application_choice = None
    while True:
        print("Please select an application (Enter the number of your choice):")
        print("1: Basic Application")
        print("2: Advanced Application")
        print('3: Exit')
        application_choice = input('Your Choice: ')
        if application_choice in set(['1', '2', '3']):
            cli = None
            if application_choice == '1':
                cli = BasicCLI()
                cli.run()
            elif application_choice == '2':
                cli = AdvanceCLI()
            elif application_choice == '3':
                print('Thanks for using our application, bye :D')
                break