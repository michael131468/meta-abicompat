SUMMARY = "Application for counting alpacas"
HOMEPAGE = "https://github.com/michael131468/alpaca-farm"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

DEPENDS = "alpaca"

PV = "1.0.0"
PR = "r1"

SRC_URI = "git://github.com/michael131468/alpaca-farm.git;protocol=https;branch=main"
SRCREV = "723bd54089de8448505d98f397799f09b4e4ea3c"
S = "${WORKDIR}/git"

inherit cmake

do_compile_append() {
    bbwarn "**************************"
    bbwarn "* Compiling alpaca-farm! *"
    bbwarn "**************************"
}
