# Simple script that accumulates time
# No external dependencies
import io
import os
import sys
import cmd
import datetime
import pickle
import os.path

class TimeEntry(object):
    def __init__(self):
        self.total_hours = 0.0
        self.curr_hours = 0.0
        self.period_start = None

    def __str__(self):
        ss = "Current: {0} hours\nTotal: {1} hours".format(self.curr_hours, self.total_hours)
        if self.period_start is not None:
            ss += "\nPeriod started: {0}".format(self.period_start)
        return ss

    def add_time(self, num_hours):
        self.total_hours += num_hours
        self.curr_hours += num_hours
    def unadd_time(self, num_hours):
        self.curr_hours -= num_hours

    def start_period(self):
        self.period_start = datetime.datetime.now()
    def end_period(self, round_to_qtrhour=True):
        period_end = datetime.datetime.now()
        td = period_end - self.period_start

        nh = td.total_seconds() / (60*60)
        if round_to_qtrhour:
            nh = round(nh*4) / 4

        self.add_time(nh)
        self.period_start = None


class TimecardCmd(cmd.Cmd):
    def __init__(self, db):
        super(TimecardCmd, self).__init__()

        self.db = db
        self.entry = None
        self.prompt = "> "

        self.intro = "Use 'help' for commands\n\n{0}".format(self.entries_str())

    def entries_str(self):
        with io.StringIO() as ss:
            ss.write("List of timecard entries:\n")
            for (k, v) in self.db.items():
                ss.write("\t{0}\n".format(k))
            return ss.getvalue()

    def do_quit(self, line):
        return True

    def do_newcard(self, line):
        name = line.strip().split()[0]
        if name in self.db:
            print("Entry already exists")
            return
        e = TimeEntry()
        self.db[name] = e
        self.entry = e
        self.prompt = "({0}) > ".format(name)

    def do_ls(self, line):
        print(self.entries_str())

    def do_use(self, line):
        name = line.strip().split()[0]
        if name not in self.db:
            print("No such entry")
            return
        self.entry = self.db[name]
        self.prompt = "({0}) > ".format(name)
    def complete_use(self, text, line, begidx, endidx):
        results = []
        for (k,v) in self.db.items():
            if k.startswith(text):
                results.append(k)
        return results

    def do_view(self, line):
        if self.entry is None:
            print("No entry selected")
            return
        print(self.entry.__str__())
    
    def do_add(self, line):
        if self.entry is None:
            print("No entry selected")
            return
        num_hours = float(line.strip().split()[0])
        self.entry.add_time(num_hours)

    def do_unadd(self, line):
        if self.entry is None:
            print("No entry selected")
            return
        num_hours = float(line.strip().split()[0])
        self.entry.unadd_time(num_hours)

    def do_start(self, line):
        if self.entry is None:
            print("No entry selected")
            return
        self.entry.start_period()
        print("Starting time period at {0}".format(self.entry.period_start))

    def do_end(self, line):
        if self.entry is None:
            print("No entry selected")
            return
        old_hours = self.entry.total_hours
        if line.strip().lower() == 'noround':
            self.entry.end_period(False)
        else:
            self.entry.end_period()
        print("Added {0} hours".format(self.entry.total_hours - old_hours))


def main(argv=None):
    if sys.version_info[0] < 3:
        print("This program requires Python 3")
        sys.exit(1)
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        db_filename = os.path.expanduser("~/.timecarddb")
    else:
        db_filename = argv[1]

    if os.path.exists(db_filename):
        with open(db_filename, 'rb') as db_file:
            db = pickle.load(db_file)
    else:
        db = {}
        resp = None
        while resp is None:
            resp = input("Okay to create new DB at {0} (Y/n)? ".format(db_filename))
            if len(resp) == 0:
                resp = 'y'
            resp = resp.strip().lower()
            if resp != 'y' and resp != 'n':
                resp = None
        if resp == 'n':
            print("No DB, aborting")
            sys.exit(1)

    cc = TimecardCmd(db)
    cc.cmdloop()

    print("Writing database")
    with open(db_filename, 'wb') as db_file:
        db = pickle.dump(db, db_file)


if __name__ == "__main__":
    main()
