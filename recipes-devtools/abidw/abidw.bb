SUMMARY = "The ABI Generic Analysis and Instrumentation Library"
HOMEPAGE = "https://sourceware.org/libabigail"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=0bcd48c3bdfef0c9d9fd17726e4b7dab"

DEPENDS = "elfutils libxml2"

PV = "1.8.1"

SRC_URI = "git://sourceware.org/git/libabigail.git;nobranch=1"
SRCREV = "1d29610d51280011a5830166026151b1a9a95bba"
S = "${WORKDIR}/git"

inherit autotools

BBCLASSEXTEND += "native nativesdk"
