PIP=`find $1 -name "pip3"`

if [ -z "$PIP" ]; then
    echo "Exiting because no pip executable was found in '$1'"
    exit 0
fi

$PIP install --upgrade pip &&
$PIP install -r $1/requirements.txt
