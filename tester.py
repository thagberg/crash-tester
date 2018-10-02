import subprocess
import datetime
import uuid
import shutil
import os
import smtplib

from email.mime.text import MIMEText

class Tester():

    def __init__(self, commands):
        self.commands = commands
        self.log_name = "crash-{}.log".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    def run(self, email_recipients=None, email_sender=None):
        os.environ['MAK_MINIDUMPER_PROMPT_DISABLE'] = '1'
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
            runlog = open(runlog_name, "a+")
            p = subprocess.Popen(command, stdout=runlog)
            pid = p.pid
            retcode = p.wait()
            logdir = "passlogs"
            if not retcode == 0:
                logdir = "crashlogs"
                main_log.write("Command returned non-zero code:\n\t{} - {}\n".format(
                    " ".join(command), retcode))
                main_log.write("\tProcess ID was: {}".format(pid))
                main_log.write("\tLog available at: ./crashlogs/{}.log\n".format(run_id))
                if email_recipients and email_sender:
                    self.send_email(email_recipients, email_sender, command, runlog.read())
            else:
                main_log.write("Command completed successfully:\n\t{}\n".format(
                    " ".join(command)
                ))
                main_log.write("\tLog available at: ./passlogs/{}.log\n".format(run_id))
            runlog.close()
            shutil.move(runlog_name, "./{}/{}.log".format(logdir, run_id))
        main_log.close()

    def send_email(self, recipients, sender, command, message):
        if not isinstance(recipients , list):
            recipients = [recipients]
        msg = MIMEText(message)
        msg['Subject'] = "Crash detected: {}".format(command)
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        s = smtplib.SMTP('localhost')
        s.sendmail(sender, recipients, msg.as_string())
        s.quit()
            