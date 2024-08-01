#!/usr/bin/env python3

import sys
import os
import io
import json
import tarfile
import datetime
import shutil
from subprocess import Popen, PIPE

MPY_CROSS = shutil.which("mpy-cross")
now = datetime.datetime.now(datetime.timezone.utc)

#
# Tools
#

def mpy_cross(source, options):
    """ Compile MicroPython to bytecode """
    if not MPY_CROSS:
        raise RuntimeError("mpy-cross not found in PATH")
    p = Popen([MPY_CROSS, *options, "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(input=source)
    if p.returncode != 0:
        raise RuntimeError(f"mpy-cross failed: {err.decode('utf-8')}")
    return out

def minify(source, filename):
    """ Minify Python source """
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

def create_tag(taginfo):
    """ Create a Blynk OTA package binary tag """
    taginfo = map(lambda x: x.encode("utf-8"), taginfo)
    return b"\0".join(taginfo) + b"\0\0"

def bytes2py(data):
    """ Create a Python module with data """
    result = """
# Generated module, DO NOT EDIT

import io
def data():
  return io.BytesIO(
"""
    offset = 0
    while offset < len(data):
        line = ""
        for size in range(1, 128):
            line = f"    {data[offset:offset+size]!r}"
            if len(line) > 120:
                break
        offset += size
        result += line + "\n"
    result += "  )\n"
    return result

#
# Package creation
#

def create_tagged_tar(args):
    fw_ver = None
    fw_type = None

    try:
        with open("cfg/fw.json", "r") as f:
            fwconfig = json.load(f)
        fw_ver = fwconfig.get("ver")
        fw_type = fwconfig.get("type")
    except Exception:
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
    tag = create_tag(taginfo)

    # Create a package file
    tar_fileobj = io.BytesIO()
    with tarfile.open(fileobj=tar_fileobj, mode="w:gz", format=tarfile.GNU_FORMAT) as tar:
        # Add firmware version info
        with io.BytesIO(tag) as f:
            ti = tarfile.TarInfo(name="fw_info.bin")
            ti.size = len(tag)
            ti.mtime = now.timestamp()
            tar.addfile(tarinfo=ti, fileobj=f)

        # Add the original files to the tar as raw data
        for fn in args.files:
            try:
                with open(fn, "rb") as f:
                    data = f.read()

                if fn.endswith(".py"):
                    base_fn = os.path.basename(fn)
                    if args.minify:
                        data = minify(data, base_fn).encode("utf-8")

                    if args.compile and base_fn not in ("main.py"):
                        options =  [ "-s", base_fn ]
                        if args.march:
                            options.append("-march=" + args.march)
                        data = mpy_cross(data, options)
                        fn = fn.replace(".py", ".mpy")

                ti = tarfile.TarInfo(name=fn)
                ti.size = len(data)
                ti.mtime = now.timestamp()
                tar.addfile(tarinfo=ti, fileobj=io.BytesIO(data))

                print(f"{fn:30} [{len(data)}]")
            except Exception as e:
                print(f"ERROR: cannot process {fn}: ", e)
                sys.exit(1)

    return tar_fileobj.getvalue()

def main(input_args=None):
    import argparse

    parser = argparse.ArgumentParser(
        description="Blynk MPOTA Utility",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""\
Create App OTA package:
  mpota.py -o app_ota.tar.gz main.py cert/ca-bundle.pem
Create a Factory/Recovery module:
  mpota.py --factory -o _factory.py main.py cert/ca-bundle.pem cfg/sys.json
""")

    parser.add_argument("files",            nargs="+",           help="Input files")
    parser.add_argument("--output", "-o",   required=True,       help="The output package file")
    parser.add_argument("--factory",        action="store_true", help="Generate factory app image")
    parser.add_argument("--minify",         action="store_true", help="Minify the files")
    parser.add_argument("--compile", "-c",  action="store_true", help="Compile the files")
    parser.add_argument("-march",           type=str,            help="Specify the architecture for compilation")

    args = parser.parse_args(input_args)
    if args.factory:
        data = create_tagged_tar(args)
        if args.output.endswith(".tar.gz"):
            pass
        elif args.output.endswith(".py"):
            data = bytes2py(data).encode()
        elif args.output.endswith(".mpy"):
            data = bytes2py(data).encode()
            data = mpy_cross(data, ["-O3", "-s", "raw"])
        else:
            raise RuntimeError(f"Output format not supported: {args.output}")

        with open(args.output, "wb") as f:
            f.write(data)
    else:
        if any(item.endswith("cfg/sys.json") for item in args.files):
            print("ERROR: System config (cfg/sys.json) should NOT be updated using OTA")
            sys.exit(1)
        data = create_tagged_tar(args)
        with open(args.output, "wb") as f:
            f.write(data)

if __name__ == "__main__":
    main()
