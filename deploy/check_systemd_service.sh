if (! systemctl -q is-active $1)
    then
    exit 1
fi
