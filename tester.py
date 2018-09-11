import subprocess
import datetime
import uuid
import shutil
import os

class Tester():

    def __init__(self, commands):
        self.commands = commands
        self.log_name = "crash-{}.log".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    def run(self):
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")
        if not os.path.exists("./passlogs"):
            os.makedirs("./passlogs")
        if not os.path.exists("./crashlogs"):
            os.makedirs("./crashlogs")
        main_log = open(self.log_name, "a")
        for command in self.commands:
            run_id = str(uuid.uuid4())
            runlog_name = "./tmp/{}.log".format(run_id)
            runlog = open(runlog_name, "w")
            retcode = subprocess.call(command, stdout=runlog, shell=True)
            logdir = "passlogs"
            if not retcode == 0:
                logdir = "crashlogs"
                main_log.write("Command returned non-zero code:\n\t{} - {}\n".format(
                    " ".join(command), retcode))
                main_log.write("\tLog available at: ./crashlogs/{}.log\n".format(run_id))
            else:
                main_log.write("Command completed successfully:\n\t{}\n".format(
                    " ".join(command)
                ))
                main_log.write("\tLog available at: ./passlogs/{}.log\n".format(run_id))
            runlog.close()
            shutil.move(runlog_name, "./{}/{}.log".format(logdir, run_id))
        main_log.close()
            