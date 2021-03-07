SUMMARY = "Library for counting alpacas"
HOMEPAGE = "https://github.com/michael131468/alpaca"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a2f70620c56804345aa7545defce3c48"

SRC_URI = "git://github.com/michael131468/alpaca.git;protocol=https;branch=v1.0.3"
SRCREV = "5607bf4fefab336db50d5357e053d86306cfdb57"
S = "${WORKDIR}/git"

inherit cmake
