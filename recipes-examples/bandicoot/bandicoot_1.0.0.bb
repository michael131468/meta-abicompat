SUMMARY = "Library for counting bandicoots"
HOMEPAGE = "https://github.com/michael131468/bandicoot"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

SRC_URI = "git://github.com/michael131468/bandicoot.git;protocol=https;branch=v1.0.0"
SRCREV = "9d535ab902b46fd2206d37c22f8ea20e71d178c7"
S = "${WORKDIR}/git"

inherit cmake
