import pathlib
from lxml import etree as ET
from fontTools.misc.plistlib import (
    fromtree,
    totree,
    load as plist_load,
    dump as plist_dump,
)

### CUSTOMISE VARIABLES HERE ###
# List of UFO paths to process
ufos = [
    "./masters/Bold.ufo",
    "./masters/Regular.ufo",
    "./masters/Thin.ufo",
]

# Default vertical metrics to be added to the vhea/vmtx table
required_vhea_keys = {
    "openTypeVheaCaretOffset": 0,
    "openTypeVheaCaretSlopeRise": 0,
    "openTypeVheaCaretSlopeRun": 1,
    "openTypeVheaVertTypoAscender": 500,
    "openTypeVheaVertTypoDescender": -500,
    "openTypeVheaVertTypoLineGap": 0,
}
default_vert_origin = 880
default_vert_height = 1000

# List of special glyphs with vertical origin and height overrides
vhea_glyph_override_list = {
    # "emdash.long.vert": (880, 2000),
    # "ellipsis.vert": (806, 818),
    # "comma-han.vert": (880, 340),
    # "period-han.vert": (880, 290),
    # "comma.full.vert": (880, 364),
    # "exclam.full.vert": (880, 854),
    # "period.full.vert": (880, 253),
    # "question.full.vert": (880, 963),
    # "colon.full.vert": (880, 553),
    # "semicolon.full.vert": (880, 664),
    # "endash.vert": (586, 491),
}

for ufo in ufos:
    ufo = pathlib.Path(ufo).resolve()
    print("Processing UFO: %s" % ufo)

    # EDIT fontinfo.plist for vhea keys
    fontinfo_path = ufo / "fontinfo.plist"
    if not fontinfo_path.exists():
        print("Fontinfo plist not found in %s, skipping." % ufo)
        continue
    fontinfo = plist_load(open(fontinfo_path))
    for key, value in required_vhea_keys.items():
        if key not in fontinfo:
            print("Adding missing key '%s' with default value %s." % (key, value))
            fontinfo[key] = value
    # Save the updated fontinfo back to the plist file
    with open(fontinfo_path, "wb") as f:
        plist_dump(fontinfo, f)

    # EDIT glifs for vertical advance and origin
    count = 0
    for glif in (ufo / "glyphs").iterdir():
        if not glif.is_file() or glif.suffix != ".glif":
            continue

        filename = glif.stem

        tree = ET.parse(glif)
        root = tree.getroot()

        # default values
        vert_start = default_vert_origin
        vert_height = default_vert_height

        # check if file need override
        if filename in vhea_glyph_override_list.keys():
            vert_start = vhea_glyph_override_list[filename][0]
            vert_height = vhea_glyph_override_list[filename][1]

        if len(list(root)) <= 1 and root.find("advance") is None:
            count += 1
            # empty glyph, only has unicode or nothing
            continue

        # set vertical height
        adv = root.find("advance")
        adv.set("height", str(vert_height))

        # add vertical advance
        lib = root.find("lib")
        if lib is None:
            lib = ET.SubElement(root, "lib")

        try:
            lib_data = fromtree(lib)
        except ValueError:
            # if the lib is not a valid plist, we create a new one
            lib_data = {}
        if "public.verticalOrigin" not in lib_data:
            lib_data["public.verticalOrigin"] = vert_start

        # save the updated lib data back to the XML
        root.remove(lib)
        lib = ET.SubElement(root, "lib")
        lib.append(totree(lib_data))
        root.append(lib)

        ET.indent(tree, space="  ", level=0)
        tree.write(glif, encoding="utf-8", xml_declaration=True)

        # counting
        count += 1
        if count % 2500 == 0:
            print("Done %d glyphs." % (count))

    print("Total %d glyphs in font." % (count))
