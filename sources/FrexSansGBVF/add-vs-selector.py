import pathlib
import plistlib

### CUSTOMISE VARIABLES HERE ###
# List of UFO paths to process
ufos = [
    "./masters/Bold.ufo",
    "./masters/Regular.ufo",
    "./masters/Thin.ufo",
]

for ufo in ufos:
    ufo = pathlib.Path(ufo).resolve()
    print("Processing UFO: %s" % ufo)

    ufo_lib = plistlib.load(open(ufo / "lib.plist", "rb"))
    if "public.unicodeVariationSequences" not in ufo_lib:
        print("Adding public.unicodeVariationSequences to %s" % ufo)
        ufo_lib["public.unicodeVariationSequences"] = {
            "FE00": {
                "0030": "uni0030.alt02",
                "2018": "uni2018.latn",
                "2019": "uni2019.latn",
                "201C": "uni201C.latn",
                "201D": "uni201D.latn",
            },
            "FE01": {
                "2018": "uni2018",
                "2019": "uni2019",
                "201C": "uni201C",
                "201D": "uni201D",
            },
        }
    
    ufo_lib["public.skipExportGlyphs"] = [
        "C_2FFA_8FB6",
        "C_4EBA",
        "C_51F5",
        "C_7E9F",
        "C_8FB6",
        "C_9AA8",
        "uni53F0.LUKE",
        "uni4E4F.MY2L",
    ]

    plistlib.dump(ufo_lib, open(ufo / "lib.plist", "wb"))
    print("Updated lib.plist for %s" % ufo)