import tarfile
import email.parser
import email.utils
import os
import dateutil.parser
import json
import sys

parser = email.parser.Parser()    
id = 0

class emailName(str):
    """
    An object initialized with a string that should be
    an e-mail address: performs operations to parse out
    the names and addresses associated.
    """

    def split(self):
        return email.utils.parseaddr(self)
    
    def elements(self):
        """
        Returns a dictionary with, where possible, the
        - name
        - address
        - username (address before the @)
        - domain (address after the @)
           - top-level domain
           - mid-level domain (oxford.ac.uk, berkeley.edu)
        of the initialized e-mail.
        """
        elements = dict()
        try:
            splat = self.split()
            elements['name'] = splat[0]
            elements['address'] = splat[1].lower()
        except IndexError:
            pass
        try:
            splitName = elements['address'].split("@")
            elements['username'] = splitName[0].lower()
            elements['domain'] = splitName[1].lower()
            domains = list(reversed(elements['domain'].split(".")))
            elements["tld"] = domains[0]
            # mid-level domains are things like 'ge.com' or 'nasa.gov'
            elements["mld"] = ".".join(list(reversed(domains[:2])))
            try:
                # The 'oxford.ac.uk' exception
                if domains[1] in ["ac","edu","co","com","gov","oz"]:
                    elements["mld"] = ".".join(list(reversed(domains[:3])))
            except IndexError:
                pass
        except IndexError:
            pass
        return elements
            
def writeMessage(string,yearlims = [1970,2020]):
    global id
    global parser
    global catalog
    global input
    parsed = parser.parsestr(string)
    metadata = dict(parsed)

    # Clean the metadata and make some elements into arrays.
    try: metadata["Path"] = metadata["Path"].split("!")
    except: pass
    try: metadata["Newsgroups"] = metadata["Newsgroups"].split(",")
    except: pass
    if "From" in metadata:
        email = emailName(metadata["From"])
        emailFields = email.elements()
        for key in emailFields.keys():
            metadata[key] = emailFields[key]
    try: 
        metadata["date"] = dateutil.parser.parse(metadata["Date"]).isoformat()
        year = metadata["date"][:4]
        if int(year) < yearlims[0] or int(year) > yearlims[1]:
            year = ""
    except: 
        pass

    id += 1
    metadata["filename"] = str(id)

    catalog.write(json.dumps(metadata) + "\n")
    input.write(str(id) + "\t" + parsed.get_payload().replace("\n"," ").replace("\t"," ") + "\n")


def main():
    global catalog
    global input
    catalog = open("jsoncatalog.txt","w")
    input = open("input.txt","w")
    files = [file for file in os.listdir(".") if file.endswith(".tgz")]
    for file in files:
        sys.stderr.write("reading " + file + "\n")
        tar = tarfile.open(file)
        for member in tar.getmembers():
            if member.isfile():
                file = tar.extractfile(member)
                content = file.read()
                if content != "":
                    try:
                        writeMessage(content)
                    except UnicodeDecodeError:
                        pass

if __name__=="__main__":
    main()
