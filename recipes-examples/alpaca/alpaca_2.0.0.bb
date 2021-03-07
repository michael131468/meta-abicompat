SUMMARY = "Library for counting alpacas"
HOMEPAGE = "https://github.com/michael131468/alpaca"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

SRC_URI = "git://github.com/michael131468/alpaca.git;protocol=https;branch=v2.0.0"
SRCREV = "f980dd06f8a94dc3630207f7d73fb2cab393830a"
S = "${WORKDIR}/git"

inherit cmake
