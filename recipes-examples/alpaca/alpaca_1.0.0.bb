SUMMARY = "Library for counting alpacas"
HOMEPAGE = "https://github.com/michael131468/alpaca"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

SRC_URI = "git://github.com/michael131468/alpaca.git;protocol=https;branch=v1.0.0"
SRCREV = "188418978fbfe7bf53d98610273c686aa9d6e9f2"
S = "${WORKDIR}/git"

inherit cmake
