# activate the virtualenv
#  (expects it to be two levels up and be called venv_dko)

platform=`python -c "import platform; print(platform.system())"`

if [[ "$platform" == 'Linux' ]]; then
    source ../../../venv_dko/bin/activate
elif [[ "$platform" == 'Windows' ]]; then
    source ../../../venv_dko/Scripts/activate
else
    echo "Unsupported platform: $platform"
fi
