SUMMARY = "Library for counting alpacas"
HOMEPAGE = "https://github.com/michael131468/alpaca"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

SRC_URI = "git://github.com/michael131468/alpaca.git;protocol=https;branch=v1.1.0"
SRCREV = "0321e50b86b2961af6505824750a8d0d417e4e16"
S = "${WORKDIR}/git"

inherit cmake
