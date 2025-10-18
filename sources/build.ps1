cd frex-sc-src
git pull
cd ..

echo "Cleaning up old UFOs..."
Remove-Item -Path frex-sc-han/han_Bold.ufo -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path frex-sc-han/han_Regular.ufo -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path frex-sc-han/han_Thin.ufo -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path FrexSansGBVF/masters/han_Bold.ufo -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path FrexSansGBVF/masters/han_Regular.ufo -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path FrexSansGBVF/masters/han_Thin.ufo -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path FrexSansGBVF/masters/Bold.ufo -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path FrexSansGBVF/masters/Regular.ufo -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path FrexSansGBVF/masters/Thin.ufo -Recurse -Force -ErrorAction SilentlyContinue

# require installing fontra and fontra-rcjk in venv
echo "Converting RCJK to designspace..."
mkdir -Force frex-sc-han
fontra-copy export-rcjk.yaml frex-sc-han\han.designspace

echo "Copying RCJK UFOs to FrexSansGB masters..."
Copy-Item "frex-sc-han\han_Bold.ufo" "FrexSansGBVF\masters\han_Bold.ufo" -Recurse -Force
Copy-Item "frex-sc-han\han_Regular.ufo" "FrexSansGBVF\masters\han_Regular.ufo" -Recurse -Force
Copy-Item "frex-sc-han\han_Thin.ufo" "FrexSansGBVF\masters\han_Thin.ufo" -Recurse -Force

cd "FrexSansGBVF\masters"

echo "Merging FrexSansGB Latin and CJK UFOs..."
ufomerge --skip-existing --layout-closure --output Bold.ufo "FrexSansGBVF-Bold.ufo\" "han_Bold.ufo"
ufomerge --skip-existing --layout-closure --output Regular.ufo "FrexSansGBVF-Regular.ufo\" "han_Regular.ufo"
ufomerge --skip-existing --layout-closure --output Thin.ufo "FrexSansGBVF-Thin.ufo\" "han_Thin.ufo"

cd ..
python add-ufo-vert-info.py
python add-vs-selector.py

Remove-Item -Path "instance_ufos" -Recurse -Force -ErrorAction SilentlyContinue

echo "Building FrexSansGB fonts..."
gftools builder config.yaml

echo "Building FrexSansGBVF font..."
fontmake -m "Frex Sans GB.designspace" -o variable --output-path "../../fonts/variable/Frex Sans GB[wght].ttf"
gftools gen-stat "../../fonts/variable/Frex Sans GB[wght].ttf" --src stat.yaml --inplace

# Stop-Computer -Force