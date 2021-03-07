SUMMARY = "Library for counting bandicoots"
HOMEPAGE = "https://github.com/michael131468/bandicoot-farm"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

DEPENDS = "bandicoot"

PV = "1.0.0"
PR = "r1"

SRC_URI = "git://github.com/michael131468/bandicoot-farm.git;protocol=https;branch=main"
SRCREV = "e83ade82c6e07f6cebb666b1aa3da9322c517546"
S = "${WORKDIR}/git"

inherit cmake

do_compile_append() {
    bbwarn "*****************************"
    bbwarn "* Compiling bandicoot-farm! *"
    bbwarn "*****************************"
}
