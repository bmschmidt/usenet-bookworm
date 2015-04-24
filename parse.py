import tarfile
import email.parser
import os
import dateutil.parser
import json

parser = email.parser.Parser()    
id = 0

def writeMessage(string):
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
    try: metadata["username"] = metadata["From"].split("@")[0]
    except: pass
    try: metadata["domain"] = metadata["From"].split("@")[1]
    except: pass
    try: metadata["date"] = dateutil.parser.parse(metadata["Date"]).isoformat()
    except: pass

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
