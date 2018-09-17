import subprocess
import argparse

from tester import Tester

# commands = [
#     ['ls', '-l'],
#     ['exit 1'],
#     ['exit 0']
# ]
commands = [
    ['rm -rf ../appData/cache/'],
    ['rm -rf ./appData/cache/'],
    ['./vrvStealth.exe --showConsole --plugin vrvAutoTestPlugin.dll -e "SavedViewTest(,0)" "../userData/terrains/Ala Moana.mtf" -n 3']
]

email_recipients = [
    'thagberg@mak.com',
    'tgeorge@mak.com'
]

email_sender = 'crashes@mak.com'

parser = argparse.ArgumentParser(description="Run commands and log any crashes")
parser.add_argument('--loop', type=bool, action='store', default=False)
args = parser.parse_args()

def main():
    tester = Tester(commands)
    should_run = True
    while should_run:
        tester.run(email_recipients, email_sender)
        should_run = args.loop

if __name__ == '__main__':
    main()