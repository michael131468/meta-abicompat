POPULATE_SYSROOT_SSTATE_PKGSPEC = "sstate:${PN}:${PACKAGE_ARCH}${TARGET_VENDOR}-${TARGET_OS}::${SSTATE_PKGARCH}:${SSTATE_VERSION}:"

# Uncomment below to restrict the abi checker to a set list of recipes
# ABICOMPAT_RESTRICT_TO_PN_LIST = "1"
# ABICOMPAT_PN_LIST = "\
#     alpaca \
# "
