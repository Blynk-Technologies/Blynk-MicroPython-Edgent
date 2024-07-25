#!/usr/bin/env python3

#
# Example usage:
#   python3 ./tools/mpota.py app_ota.tar.gz main.py some_module.py data.txt
#
# 1. Creates Blynk firmware binary tag based on the configuration
# 2. Packages input files into a tar (or tar.gz) file that can be used for OTA updates
#

import sys, os, io, time
import re
import json
import tarfile
import datetime
import blynk_tag
import shutil
from subprocess import Popen, PIPE, DEVNULL

do_minify = False
do_compile = True

MPY_CROSS = shutil.which("mpy-cross")
now = datetime.datetime.now(datetime.timezone.utc)


def mpy_cross(source, filename):
    if not MPY_CROSS:
        raise RuntimeError(f"mpy-cross not found in PATH")
    p = Popen([MPY_CROSS, "-s", filename, "-O3", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(input=source)
    if p.returncode != 0:
        raise RuntimeError(f"mpy-cross failed: {err.decode('utf-8')}")
    return out


def minify(source, filename):
    import python_minifier

    return python_minifier.minify(
        source,
        filename,
        remove_annotations=True,
        remove_pass=True,
        remove_literal_statements=True,
        combine_imports=True,
        hoist_literals=False,
        remove_object_base=False,
        remove_debug=True,
        remove_asserts=False,
        rename_locals=True, preserve_locals=None,
        rename_globals=False, preserve_globals=None,
        convert_posargs_to_args=True,
        preserve_shebang=False,
    )


def create_tagged_tar(input_files, output_tar_file):

    fw_ver = None
    fw_type = None

    try:
        with open("cfg/fw.json", "r") as f:
            fwconfig = json.load(f)
        fw_ver = fwconfig.get("ver")
        fw_type = fwconfig.get("type")
    except:
        pass

    if not fw_ver:
        raise Exception("Firmware version must be configured in 'cfg/fw.json'")
    if not fw_type or "xxxxxxx" in fw_type:
        raise Exception("Firmware type must be configured in 'cfg/fw.json'")

    # Create Blynk binary tag
    taginfo = ["blnkinf"]
    taginfo.extend(["mcu", fw_ver])
    taginfo.extend(["fw-type", fw_type])
    taginfo.extend(["build", now.strftime("%b %d %Y %H:%M:%S")])
    tag = blynk_tag.create_tag(taginfo)

    # Create a tar.gz file
    with tarfile.open(output_tar_file, "w:gz", format=tarfile.GNU_FORMAT) as tar:
        # Add firmware version info
        with io.BytesIO(tag) as f:
            ti = tarfile.TarInfo(name="fw_info.bin")
            ti.size = len(tag)
            ti.mtime = now.timestamp()
            tar.addfile(tarinfo=ti, fileobj=f)

        # Add the original files to the tar as raw data
        for fn in input_files:
            try:
                with open(fn, "rb") as f:
                    data = f.read()

                if fn.endswith(".py"):
                    base_fn = os.path.basename(fn)
                    if do_minify:
                        data = minify(data, base_fn).encode("utf-8")

                    if do_compile and base_fn not in ("main.py"):
                        data = mpy_cross(data, base_fn)
                        fn = fn.replace(".py", ".mpy")

                ti = tarfile.TarInfo(name=fn)
                ti.size = len(data)
                ti.mtime = now.timestamp()
                tar.addfile(tarinfo=ti, fileobj=io.BytesIO(data))

                print(f"{fn:30} [{len(data)}]")
            except Exception as e:
                print(f"Error processing {fn}: ", e)
                os.unlink(output_tar_file)
                sys.exit(1)

    if any(item.startswith("cfg/") for item in input_files):
        # Express concerns
        print()
        print(" = WARNING: System config (cfg/sys.json) should NOT be updated using OTA =")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py output_tar_file input_file1 [input_file2 ...]")

    create_tagged_tar(sys.argv[2:], sys.argv[1])
