SUMMARY = "Library for counting alpacas"
HOMEPAGE = "https://github.com/michael131468/alpaca"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

SRC_URI = "git://github.com/michael131468/alpaca.git;protocol=https;branch=v1.0.1"
SRCREV = "992c668d323da93c6b831756617c0a07db60c3f9"
S = "${WORKDIR}/git"

inherit cmake
