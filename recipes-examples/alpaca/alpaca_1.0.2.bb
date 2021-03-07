SUMMARY = "Library for counting alpacas"
HOMEPAGE = "https://github.com/michael131468/alpaca"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

SRC_URI = "git://github.com/michael131468/alpaca.git;protocol=https;branch=v1.0.2"
SRCREV = "2161884c1b37d7d12f707e85ccba99d4da91345d"
S = "${WORKDIR}/git"

inherit cmake
