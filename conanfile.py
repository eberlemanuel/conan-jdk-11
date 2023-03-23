from conan import ConanFile, tools
from conans.tools import os_info
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

    settings = {"os" : ["Windows", "Macos"], "arch": ["x86_64"]}

    def validate(self):
        if self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration("Unsupported Architecture. This package currently only supports x86_64.")
        if self.settings.os != "Windows" and self.settings.os != "Macos":
            raise ConanInvalidConfiguration("Unsupported OS. This package currently only supports Windows.")

    def build(self):
        filename = "OpenJDK11U-jdk_x64_{0}_hotspot_11.0.18_10.{1}"
        dstDiretory = ""

        if os_info.is_windows:
            filename = filename.format("windows", "zip")
            checksum = "0cfa5991a8e372b3f8eacacbb2a336663ead0cc6ec9c9ab6cd53206602fb0062"
            dstDiretory = filename
        if os_info.is_macos:
            filename = filename.format("mac", "tar.gz")
            checksum = "75d79315d7265cc4b89fd9e844161ff90798bc6482ace8c1ac75f862a5b3b565"
            dstDiretory = "jdk-11.0.18+10"

        downloadUrl = "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.18%2B10/" + filename
        self.output.info("Download: {0}".format(downloadUrl))
        get(self, downloadUrl, sha256=checksum)
        os.rename(dstDiretory, "sources")

    def package(self):
        if self.settings.os == "Windows":
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