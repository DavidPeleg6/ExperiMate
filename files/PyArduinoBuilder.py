import subprocess
import os
import shutil
import time
import fileinput


def build_ino(arduino_location, libraries_location, ino_file, com_num):
    # ===========================
    # create some background data
    # these need to reflect the details of your system

    # where is the Arduino program
    arduinoIdeVersion = {"1.5.6-r2": arduino_location,
                         "1.6.3": arduino_location}

    # where are libraries stored
    arduinoExtraLibraries = libraries_location

    # where this program will store stuff
    # these directories will be beside this Python program
    compileDirName = "ArduinoTemp"
    archiveDirName = "ArduinoUploadArchive"

    # default build options
    build_options = {"action": "upload", "board": "arduino:avr:uno", "port": "COM" + str(com_num), "ide": "1.5.6-r2"}

    # some other important variables - just here for easy reference
    archiveRequired = False
    usedLibs = []
    hFiles = []

    # ============================
    # ensure directories exist
    # and empty the compile directory

    # first the directory used for compiling
    pythonDir = os.path.dirname(os.path.realpath(__file__))
    compileDir = os.path.join(pythonDir, compileDirName)
    if not os.path.exists(compileDir):
        os.makedirs(compileDir)

    existingFiles = os.listdir(compileDir)
    for f in existingFiles:
        os.remove(os.path.join(compileDir, f))

    # then the directory where the Archives are saved
    archiveDir = os.path.join(pythonDir, archiveDirName)
    if not os.path.exists(archiveDir):
        os.makedirs(archiveDir)

    # =============================
    # get the .ino file and figure out the build options
    # the stuff in the .ino file will have this format
    # and will start at the first line in the file
    # // python-build-start
    # // python-build-end

    inoFileName = ino_file
    inoBaseName, inoExt = os.path.splitext(os.path.basename(inoFileName))

    ''' kept for when dynamic parsing is added
    numLines = 1  # in case there is no end-line
    maxLines = 6
    buildError = ""
    if inoExt.strip() == ".ino":
        codeFile = open(inoFileName, 'r')
        startLine = codeFile.readline()[3:].strip()
        if startLine == "python-build-start":
            nextLine = codeFile.readline()[3:].strip()
            while nextLine != "python-build-end":
                buildCmd = nextLine.split(',')
                if len(buildCmd) > 1:
                    buildOptions[buildCmd[0].strip()] = buildCmd[1].strip()
                numLines += 1
                if numLines >= maxLines:
                    buildError = "No end line"
                    break
                nextLine = codeFile.readline()[3:].strip()
        else:
            buildError = "No start line"
    else:
        buildError = "Not a .ino file"

    if len(buildError) > 0:
        print("Sorry, can't process file - %s" % buildError)
    '''

    # print buid Options
    print("BUILD OPTIONS")
    for n, m in build_options.items():
        print("%s  %s" % (n, m))

    # =============================
    # get the program filename for the selected IDE
    arduinoProg = arduinoIdeVersion[build_options["ide"]]

    # =============================
    # prepare archive stuff
    #
    # create name of directory to save the code = name-yyyymmdd-hhmmss
    # this will go inside the directory archiveDir
    inoArchiveDirName = inoBaseName + time.strftime("-%Y%m%d-%H:%M:%S")
    # note this directory will only be created if there is a successful upload
    # the name is figured out here to be written into the .ino file so it can be printed by the Arduino code
    # it will appear as char archiveDirName[] = "nnnnn";

    # if the .ino file does not have a line with char archiveDirName[] then it will be assumed
    # that no archiving is required
    # check for existence of line
    for line in fileinput.input(inoFileName):
        if "char archiveDirName[]" in line:
            archiveRequired = True
            break
    fileinput.close()

    if archiveRequired:
        for line in fileinput.input(inoFileName, inplace=1):
            if "char archiveDirName[]" in line:
                print('char archiveDirName[] = "%s";' % inoArchiveDirName)
            else:
                print(line.rstrip())
        fileinput.close()
    # ~ os.utime(inoFileName, None)

    # =============================
    # figure out what libraries and .h files are used
    # if there are .h files they will need to be copied to ArduinoTemp

    # first get the list of all the extra libraries that exist
    extraLibList = os.listdir(arduinoExtraLibraries)

    # go through the .ino file to get any lines with #include
    includeLines = []
    for line in fileinput.input(inoFileName):
        if "#include" in line:
            includeLines.append(line.strip())
    fileinput.close()
    print("#INCLUDE LINES")
    print(includeLines)

    # now look for lines with < signifying libraries
    for n in includeLines:
        angleLine = n.split('<')
        if len(angleLine) > 1:
            lib_name = angleLine[1].split('>')
            lib_name = lib_name[0].split('.')
            lib_name = lib_name[0].strip()
            # add the name to usedLibs if it is in the extraLibList
            if lib_name in extraLibList:
                usedLibs.append(lib_name)
    print("LIBS TO BE ARCHIVED")
    print(usedLibs)

    # then look for lines with " signifiying a reference to a .h file
    # NB the name will be a full path name
    for n in includeLines:
        quoteLine = n.split('"')
        if len(quoteLine) > 1:
            hName = quoteLine[1].split('"')
            hName = hName[0].strip()
            # add the name to hFiles
            hFiles.append(hName)
    print(".h FILES TO BE ARCHIVED")
    print(hFiles)

    # ==============================
    # copy the .ino file to the directory compileDir and change its name to match the directory
    saveFile = os.path.join(compileDir, compileDirName + ".ino")
    shutil.copy(inoFileName, saveFile)

    # ===============================
    # generate the Arduino command
    arduino_command = "%s --%s --board %s --port %s %s" % (
        arduinoProg, build_options["action"], build_options["board"], build_options["port"], saveFile)
    print("ARDUINO COMMAND")
    print(arduino_command)

    # ===============================
    # call the IDE
    print("STARTING ARDUINO -- %s\n" % (build_options["action"]))

    presult = subprocess.call([arduinoProg, "--%s" % build_options["action"], "--board", build_options["board"],
                               "--port", build_options["port"], saveFile], shell=True)

    if presult != 0:
        raise SystemError("Error, wrong COM number")
    else:
        print("\nARDUINO SUCCESSFUL")


    # ================================
    # after a successful upload we may need to archive the code
    if archiveRequired:
        print("\nARCHIVING")
        # create the Archive directory
        ar_dir = os.path.join(archiveDir, inoArchiveDirName)
        print(ar_dir)
        # this ought to be a unique name - hence no need to check for duplicates
        os.makedirs(ar_dir)
        # copy the code into the new directory
        shutil.copy(inoFileName, ar_dir)
        # copy the .h files to the new directory
        for n in hFiles:
            shutil.copy(n, ar_dir)
        # copy the used libraries to the new directory
        for n in usedLibs:
            lib_name = os.path.join(arduinoExtraLibraries, n)
            dest_dir = os.path.join(ar_dir, "libraries", n)
            shutil.copytree(lib_name, dest_dir)
        print("\nARCHIVING DONE")

    # ==============================

