SUMMARY = "Library for counting bandicoots"
HOMEPAGE = "https://github.com/michael131468/bandicoot"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

SRC_URI = "git://github.com/michael131468/bandicoot.git;protocol=https;branch=v1.0.1"
SRCREV = "4d6acd92a8209b1eca3aa686ecd49d5112e6872d"
S = "${WORKDIR}/git"

inherit cmake
