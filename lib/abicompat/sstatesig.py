import re
import subprocess

from oe.package import is_elf

def ABICompatBasicHash(path, sigfile, task, d):
    """
    Basic output hash function using abidw for shared libraries

    Calculates the output hash of a task by hashing all output file metadata,
    and file contents.
    """
    import hashlib
    import stat
    import pwd
    import grp

    def update_hash(s):
        s = s.encode('utf-8')
        h.update(s)
        if sigfile:
            sigfile.write(s)

    h = hashlib.sha256()
    prev_dir = os.getcwd()
    include_owners = os.environ.get('PSEUDO_DISABLED') == '0'
    if "package_write_" in task or task == "package_qa":
        include_owners = False
    include_timestamps = False
    if task == "package":
        include_timestamps = d.getVar('BUILD_REPRODUCIBLE_BINARIES') == '1'
    extra_content = d.getVar('HASHEQUIV_HASH_VERSION')

    # Avoid issues with unsatisfiable dependencies by ignoring native recipes (not so useful there anyways).
    abichecker_active = False
    if task == "populate_sysroot" and not bb.data.inherits_class('native', d) and not bb.data.inherits_class('cross', d):
        # We can ignore checking all recipes by configuring the abi checker to check a select list to save cpu time
        if d.getVar("ABICOMPAT_RESTRICT_TO_PN_LIST"):
            pn = d.getVar("PN")
            pn_list = (d.getVar("ABICOMPAT_PN_LIST") or "").split()
            if pn in pn_list:
                abichecker_active = True
        else:
            abichecker_active = True

    try:
        os.chdir(path)

        update_hash("ABICompatBasicHash\n")
        if extra_content:
            update_hash(extra_content + "\n")

        # It is only currently useful to get equivalent hashes for things that
        # can be restored from sstate. Since the sstate object is named using
        # SSTATE_PKGSPEC and the task name, those should be included in the
        # output hash calculation.
        sstate_pkgspec = d.getVar("SSTATE_PKGSPEC")
        if abichecker_active:
            #bb.plain("[ABICompatBasicHash]: %s" % (sigfile.name,))
            sstate_pkgspec = d.getVar("POPULATE_SYSROOT_SSTATE_PKGSPEC")
        update_hash("SSTATE_PKGSPEC=%s\n" % sstate_pkgspec)
        update_hash("task=%s\n" % task)

        # Capture all abi dumps temporarily into this dictionary and add them to
        # the hash only at the end (in a sorted manner).
        abi_dumps = {}

        for root, dirs, files in os.walk('.', topdown=True):
            # Sort directories to ensure consistent ordering when recursing
            dirs.sort()
            files.sort()

            # Special handling for populate_sysroot
            # Here we want to use the ABI as the hash of the SO instead of the checksum
            # We also purposely ignore timestamps and permissions
            def process_sysroot(path):
                #bb.plain("[ABICompatBasicHash]: %s: process(%s)" % (task, path,))
                s = os.lstat(path)

                path_is_shared_lib = False
                if stat.S_ISREG(s.st_mode):
                    # Determine if path is an shared library so object
                    # Restrict to .so filenames to save some time...
                    if ".so" in path:
                        #bb.plain("[ABICompatBasicHash]: %s,%s" % (is_elf(path)))
                        result = is_elf(path)
                        if result[1] & 1 and result [1] & 8:
                            bb.plain("[ABICompatBasicHash]: ABI Dumping: %s" % (path,))
                            path_is_shared_lib = True

                # If path is an so object then dump the ABI and store it in the dictionary with the soname as the key
                # Otherwise use the file checksum for the hash
                if path_is_shared_lib:
                    abi_dump_successful = False
                    try:
                        result = subprocess.run(["abidw", "--no-corpus-path", path], check=True, capture_output=True, universal_newlines=True)
                        soname_search = re.search("soname='(.*)'", result.stdout)
                        if soname_search:
                            soname = soname_search.group(1)
                            abi_dumps[soname] = result.stdout
                            abi_dump_successful = True
                    except subprocess.CalledProcessError as e:
                        bb.warn("[ABICompatBasicHash]: Could not abi dump %s" % (path,))

                    # Don't capture any details of this file in the hash if the abi dump is successful
                    # If unsuccessful at dumping the file, continue and use the checksum
                    if abi_dump_successful:
                        return

                if stat.S_ISDIR(s.st_mode):
                    update_hash('d')
                elif stat.S_ISCHR(s.st_mode):
                    update_hash('c')
                elif stat.S_ISBLK(s.st_mode):
                    update_hash('b')
                elif stat.S_ISSOCK(s.st_mode):
                    update_hash('s')
                elif stat.S_ISLNK(s.st_mode):
                    update_hash('l')
                elif stat.S_ISFIFO(s.st_mode):
                    update_hash('p')
                else:
                    update_hash('-')

                update_hash(" ")
                if stat.S_ISBLK(s.st_mode) or stat.S_ISCHR(s.st_mode):
                    update_hash("%9s" % ("%d.%d" % (os.major(s.st_rdev), os.minor(s.st_rdev))))
                else:
                    update_hash(" " * 9)

                update_hash(" ")
                if stat.S_ISREG(s.st_mode):
                    update_hash("%10d" % s.st_size)
                else:
                    update_hash(" " * 10)

                update_hash(" ")
                fh = hashlib.sha256()
                if stat.S_ISREG(s.st_mode):
                    with open(path, 'rb') as d:
                        for chunk in iter(lambda: d.read(4096), b""):
                            fh.update(chunk)
                    update_hash(fh.hexdigest())
                else:
                    update_hash(" " * len(fh.hexdigest()))

                update_hash(" %s" % path)

                if stat.S_ISLNK(s.st_mode):
                    # Replace symlink destinations with the soname if it's an so file
                    symlink_dest = os.readlink(path)
                    if ".so" in path:
                        result = is_elf(os.path.realpath(path))
                        if result[1] & 1 and result [1] & 8:
                            result = subprocess.run(["abidw", "--no-corpus-path", path], check=True, capture_output=True, universal_newlines=True)
                            soname_search = re.search("soname='(.*)'", result.stdout)
                            if soname_search:
                                soname = soname_search.group(1)
                                bb.plain("[ABICompatBasicHash]: Re-writing symlink: %s -> %s -> %s" % (path, os.readlink(path), soname))
                                symlink_dest = soname
                    
                    update_hash(" -> %s" % symlink_dest)

                update_hash("\n")

            def process(path):
                s = os.lstat(path)

                if stat.S_ISDIR(s.st_mode):
                    update_hash('d')
                elif stat.S_ISCHR(s.st_mode):
                    update_hash('c')
                elif stat.S_ISBLK(s.st_mode):
                    update_hash('b')
                elif stat.S_ISSOCK(s.st_mode):
                    update_hash('s')
                elif stat.S_ISLNK(s.st_mode):
                    update_hash('l')
                elif stat.S_ISFIFO(s.st_mode):
                    update_hash('p')
                else:
                    update_hash('-')

                def add_perm(mask, on, off='-'):
                    if mask & s.st_mode:
                        update_hash(on)
                    else:
                        update_hash(off)

                add_perm(stat.S_IRUSR, 'r')
                add_perm(stat.S_IWUSR, 'w')
                if stat.S_ISUID & s.st_mode:
                    add_perm(stat.S_IXUSR, 's', 'S')
                else:
                    add_perm(stat.S_IXUSR, 'x')

                add_perm(stat.S_IRGRP, 'r')
                add_perm(stat.S_IWGRP, 'w')
                if stat.S_ISGID & s.st_mode:
                    add_perm(stat.S_IXGRP, 's', 'S')
                else:
                    add_perm(stat.S_IXGRP, 'x')

                add_perm(stat.S_IROTH, 'r')
                add_perm(stat.S_IWOTH, 'w')
                if stat.S_ISVTX & s.st_mode:
                    update_hash('t')
                else:
                    add_perm(stat.S_IXOTH, 'x')

                if include_owners:
                    try:
                        update_hash(" %10s" % pwd.getpwuid(s.st_uid).pw_name)
                        update_hash(" %10s" % grp.getgrgid(s.st_gid).gr_name)
                    except KeyError:
                        bb.warn("KeyError in %s" % path)
                        raise

                if include_timestamps:
                    update_hash(" %10d" % s.st_mtime)

                update_hash(" ")
                if stat.S_ISBLK(s.st_mode) or stat.S_ISCHR(s.st_mode):
                    update_hash("%9s" % ("%d.%d" % (os.major(s.st_rdev), os.minor(s.st_rdev))))
                else:
                    update_hash(" " * 9)

                update_hash(" ")
                if stat.S_ISREG(s.st_mode):
                    update_hash("%10d" % s.st_size)
                else:
                    update_hash(" " * 10)

                update_hash(" ")
                fh = hashlib.sha256()
                if stat.S_ISREG(s.st_mode):
                    # Hash file contents
                    with open(path, 'rb') as d:
                        for chunk in iter(lambda: d.read(4096), b""):
                            fh.update(chunk)
                    update_hash(fh.hexdigest())
                else:
                    update_hash(" " * len(fh.hexdigest()))

                update_hash(" %s" % path)

                if stat.S_ISLNK(s.st_mode):
                    update_hash(" -> %s" % os.readlink(path))

                update_hash("\n")

            # Process this directory and all its child files
            if abichecker_active:
                process_sysroot(root)
                for f in files:
                    if f == 'fixmepath':
                        continue
                    process_sysroot(os.path.join(root, f))
            else:
                process(root)
                for f in files:
                    if f == 'fixmepath':
                        continue
                    process(os.path.join(root, f))

        # Append all ABI dump values to hash now
        for soname in sorted(abi_dumps):
            abi_dump = abi_dumps[soname].encode("utf-8")
            abi_checksum = hashlib.sha256(abi_dump).hexdigest()
            bb.plain("Adding %s:%s to hash" % (soname, abi_checksum))
            #bb.plain("%s" % (abi_dump,))
            update_hash(soname + ":" + abi_checksum)

    finally:
        os.chdir(prev_dir)

    return h.hexdigest()


