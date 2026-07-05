# My ws4 .bashrc for CS131
# Useful shortcuts for working on the cs131 repo

alias cs131='cd ~/cs131'
alias gl='git log --oneline'

if [ -d "$HOME/cs131/ws4" ]; then
    alias ws4='cd ~/cs131/ws4'
fi

mkcd () {
    if [ -z "$1" ]; then
        echo "Usage: mkcd folder_name"
        return 1
    fi
    mkdir -p "$1" && cd "$1"
}
