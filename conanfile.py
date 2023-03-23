from conan import ConanFile, tools
from conan.tools.files import get
from conans.errors import ConanInvalidConfiguration

import os

class JavaJdkRecipe(ConanFile):
    name = "openjdk"
    version = "11.0.18"

    license = "https://openjdk.org/"
    author = "Manuel Eberle (manueleberle9@gmail.com)"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Java OpenJDK 11 installer distributed via Conan"
    topics = ("java", "jdk", "jdk11")

    settings = {"os" : ["Windows", "Linux", "Macos"], "arch": ["x86_64"]}

    def validate(self):
        if self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration("Unsupported Architecture. This package currently only supports x86_64.")

    def build(self):
        filename = "OpenJDK11U-jdk_x64_{0}_hotspot_11.0.18_10.{1}"
        dstDiretory = "jdk-11.0.18+10"

        if self.settings.os == "Windows":
            filename = filename.format("windows", "zip")
            checksum = "0cfa5991a8e372b3f8eacacbb2a336663ead0cc6ec9c9ab6cd53206602fb0062"
        if self.settings.os == "Macos":
            filename = filename.format("mac", "tar.gz")
            checksum = "75d79315d7265cc4b89fd9e844161ff90798bc6482ace8c1ac75f862a5b3b565"
        if self.settings.os == "Linux":
            filename = filename.format("linux", "tar.gz")
            checksum = "4a29efda1d702b8ff38e554cf932051f40ec70006caed5c4857a8cbc7a0b7db7"

        downloadUrl = "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.18%2B10/" + filename
        self.output.info("Download: {0}".format(downloadUrl))
        get(self, downloadUrl, sha256=checksum)
        os.rename(dstDiretory, "sources")

    def package(self):
        if self.settings.os == "Windows" or self.settings.os == "Linux":
            self.copy(pattern="*", dst=".", src="sources")
        if self.settings.os == "Macos":
            self.copy(pattern="*", dst=".", src=os.path.join("sources","Contents", "Home"))

    def package_info(self):
        javaHome = os.path.join(self.package_folder)
        binPath = os.path.join(javaHome, "bin")

        self.output.info("Creating JAVA_HOME environment variable with : {0}".format(javaHome))
        self.env_info.JAVA_HOME = javaHome
        self.output.info("Appending PATH environment variable with : {0}".format(binPath))
        self.env_info.path.append(binPath)
