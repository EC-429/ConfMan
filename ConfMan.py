import argparse
import json
import time
import hashlib
from colorama import Style, Back, Fore

# Global variables
green = Back.GREEN
red = Back.RED
grey = Back.LIGHTBLACK_EX
rst = Style.RESET_ALL


def baseline(x, y, z):
    # Create empty json template to be populate later
    template = {
        "name": "",
        "path": "",
        "established": "",
        "approver": "",
        "baseline": "",
        "checks": [
            {"date": "", "hash": ""},
        ]
    }

    # Print banner and request user input
    print(f'\n[+] Configuration Baseline Function\n')
    fpath = x
    fname = y
    approver = z

    # Define time variable
    tm = time.localtime()
    dt = str(tm[0]) + "/" + str(tm[1]) + "/" + str(tm[2]) + " " +str(tm[3]) + ":" + str(tm[4]) + ":" + str(tm[5])

    # Determine if file exists from user input
    try:
        # Open file, hash file, and define hash variable
        md5_hash = hashlib.md5()
        with open(fpath, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
            base_hash = md5_hash.hexdigest()

    # Raise an error if file doesnt exist
    except OSError:
        # print failure information banner
        print(red + "Error\t" + rst + f' File path not found: \t{fpath}\n')

    # Proceed if file exist
    else:
        # Populate template
        template["name"] = fname
        template["path"] = fpath
        template["established"] = dt
        template["approver"] = approver
        template["baseline"] = base_hash
        template["checks"][0]["date"] = dt
        template["checks"][0]["hash"] = base_hash

        with open(f'Managed/{fname}.json', 'w') as f:  # writing JSON object
            json.dump(template, f)

        # Print success information banner
        print(green + "\nSUCCESS" + rst)
        print(f'[-] File created:\t\t./Managed/{fname}.json\n'
              f'[-] Baseline name:\t\t{fname}\n'
              f'[-] Baseline date:\t\t{dt}\n'
              f'[-] Approved by:\t\t{approver}\n'
              f'[-] Baseline hash:\t\t{base_hash}\n')


def audit(x):

    # Print banner and assign user input
    print(f'\n[+] Configuration Audit Function')
    fname = x

    # Define time variable
    tm = time.localtime()
    dt = str(tm[0]) + "/" + str(tm[1]) + "/" + str(tm[2]) + " " + str(tm[3]) + ":" + str(tm[4]) + ":" + str(tm[5])

    # Determine if file exists from user input
    try:

        # open file and load as json object
        with open(f'Managed/{fname}.json') as json_file:
            file = json.load(json_file)
            # JSON Data: assign objects to variables
            fpath = file["path"]

        # Open file, hash file, and define hash variable
        md5_hash = hashlib.md5()
        with open(fpath, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
            base_hash = md5_hash.hexdigest()

    # Raise an error if file doesnt exist
    except OSError:
        # print failure information banner
        print(red + "Error\t" + rst + f' Either baseline name doesnt exist or original file doesnt exist')

    # Proceed if file exist
    else:
        # open file and load as json object
        with open(f'Managed/{fname}.json') as json_file:
            data = json.load(json_file)

            # add new json config check
            add = {'date': str(dt), 'hash': str(base_hash)}
            data["checks"].append(add)

        # open file and dump newly modified json to file
        with open(f'Managed/{fname}.json', 'w') as outfile:
            json.dump(data, outfile)

        # Print success information banner
        print("\n" + green + "SUCCESS\t" + rst)
        print(f'[-] File audited:\t\t./Managed/{fname}.json\n'
              f'[-] Baseline name:\t\t{fname}\n'
              f'[-] Checked date:\t\t{dt}\n'
              f'[-] Baseline hash:\t\t{base_hash}\n')


def detect(x):
    # Print banner and assign user input
    print(f'\n[+] Configuration Change Identification Function')
    fname = x

    # Determine if file exists from user input
    try:
        # open file and load as json object
        with open(f'Managed/{fname}.json') as json_file:
            file = json.load(json_file)

    # Raise an error if file doesnt exist
    except OSError:
        print(red + "Error\t" + rst + f' Baseline file not found: \t{fname}\n')

    # Proceed if file exist
    else:
        # JSON Data: assign objects to variables
        est = file["established"]
        approver = file["approver"]
        base_hash = file["baseline"]
        base_index = 0

        # Print banner
        print(f'[-] File checked:\t\t./Managed/{fname}.json\n'
              f'[-] Baseline name:\t\t{fname}\n'
              f'[-] Baseline date:\t\t{est}\n'
              f'[-] Approved by:\t\t{approver}\n'
              f'[-] Baseline hash:\t\t{base_hash}\n')

        # JSON DATA: loop through all checks to determine current baseline index
        for i in enumerate(file["checks"]):
            index = i[0]        # index of check
            dat = i[1]["date"]  # date of check
            hsh = i[1]["hash"]  # hash content of check

            # if check eq to baseline
            if str(dat) == str(est) and str(hsh) == str(base_hash):
                base_index = index

        # JSON DATA: loop through all checks and compare to baseline
        for i in enumerate(file["checks"]):
            index = i[0]        # index of check
            dat = i[1]["date"]  # date of check
            hsh = i[1]["hash"]  # hash content of check

            if index < base_index:                                      # ignore baselines prior to approved
                print(grey + f'{index}\t' + rst + f' {dat}\t{hsh}')

            elif str(hsh) == str(base_hash):                            # if check eq to baseline (nochange=green)
                print(green + f'{index}\t' + rst + f' {dat}\t{hsh}')
            else:                                                       # else not eq (change=red)
                print(red + f'{index}\t' + rst + f' {dat}\t{hsh}')

        print("\n")


def promote(x):
    # Print banner and request user input
    print(f'\n[+] Configuration Promotion Function\n')
    fname = x

    def select(x):
        # Determine if file exists from user input
        try:
            # open file and load as json object
            with open(f'Managed/{fname}.json') as json_file:
                file = json.load(json_file)

        # Raise an error if file doesnt exist
        except OSError:
            print(red + "Error\t" + rst + f' Baseline file not found: \t{fname}\n')

        # Proceed if file exist
        else:
            # JSON Data: assign objects to variables
            est = file["established"]
            approver = file["approver"]
            base_hash = file["baseline"]
            base_index = 0

            # Print banner
            print(f'[-] File checked:\t\t./Managed/{fname}.json\n'
                  f'[-] Baseline name:\t\t{fname}\n'
                  f'[-] Baseline date:\t\t{est}\n'
                  f'[-] Approved by:\t\t{approver}\n'
                  f'[-] Baseline hash:\t\t{base_hash}\n')

            # JSON DATA: loop through all checks to determine current baseline index
            for i in enumerate(file["checks"]):
                index = i[0]  # index of check
                dat = i[1]["date"]  # date of check
                hsh = i[1]["hash"]  # hash content of check

                # if check eq to baseline
                if str(dat) == str(est) and str(hsh) == str(base_hash):
                    base_index = index

            # JSON DATA: loop through all checks and compare to baseline
            for i in enumerate(file["checks"]):
                index = i[0]  # index of check
                dat = i[1]["date"]  # date of check
                hsh = i[1]["hash"]  # hash content of check

                if index < base_index:  # ignore baselines prior to approved
                    print(grey + f'{index}\t' + rst + f' {dat}\t{hsh}')

                elif str(hsh) == str(base_hash):  # if check eq to baseline (nochange=green)
                    print(green + f'{index}\t' + rst + f' {dat}\t{hsh}')
                else:  # else not eq (change=red)
                    print(red + f'{index}\t' + rst + f' {dat}\t{hsh}')

    def promo():
        # User Input; new baseline selection
        promo_bline = int(input("\nEnter number of baseline to promote: ").strip())
        promo_approver = input("Enter baseline approver: ").strip()

        # Determine if file exists from user input
        try:
            # open file and load as json object
            with open(f'Managed/{fname}.json') as json_file:
                file = json.load(json_file)

        # Raise an error if file doesnt exist
        except OSError:
            print(red + "Error\t" + rst + f' Baseline file not found: \t{fname}\n')

        # Proceed if file exist
        else:
            # open file and load as json object
            with open(f'Managed/{fname}.json') as json_file:
                data = json.load(json_file)

                promo_date = data["checks"][promo_bline]["date"]
                promo_hash = data["checks"][promo_bline]["hash"]

                # Promote new baseline date and hash based on user index input
                data["established"] = promo_date
                data["approver"] = promo_approver
                data["baseline"] = promo_hash

                # Print banner
                print("\n" + green + "SUCCESS\t" + rst)
                print(f'[-] File baselined:\t\t./Managed/{fname}.json\n'
                      f'[-] Baseline name:\t\t{fname}\n'
                      f'[-] New baseline date:\t\t{promo_date}\n'
                      f'[-] Approved by:\t\t{promo_approver}\n'
                      f'[-] Baseline hash:\t\t{promo_hash}\n')

            # open file and dump newly modified json to file
            with open(f'Managed/{fname}.json', 'w') as outfile:
                json.dump(data, outfile)

    # Run functions
    select(fname)
    promo()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", default="None", nargs=3, metavar=("{FILE PATH}", "{BASELINE NAME}", "{APPROVER}"), help="Perform configuration baseline")
    parser.add_argument("--audit", default="None", metavar="{BASELINE NAME}", type=str, help="Perform configuration audit")
    parser.add_argument("--detect", default="None", metavar="{BASELINE NAME}", type=str, help="Perform configuration change detection")
    parser.add_argument("--promote", default="None", metavar="{BASELINE NAME}", help="Perform configuration baseline promotion")
    args = parser.parse_args()

    Abaseline = args.baseline
    Aaudit = str(args.audit)                                 # store arguments as variables
    Adetect = str(args.detect)
    Apromote = str(args.promote)

    if Abaseline != "None":
        x = Abaseline[0]
        y = Abaseline[1]
        z = Abaseline[2]
        baseline(x, y, z)

    elif Aaudit != "None":
        audit(Aaudit)

    elif Adetect != "None":
        detect(Adetect)

    elif Apromote != "None":
        promote(Apromote)

    else:
        "Opps! Try again. Must be smarter than the menu."

