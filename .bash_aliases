# Environment variables
export EDITOR="$VISUAL"
export YOUTUBE="$HOME/youtube"

# Command Aliases
alias venv='. env/bin/activate'
alias youtube='cd $YOUTUBE; venv'
alias dc='docker-compose'
alias container='docker exec -ti youtube_info_django_1 /bin/bash'
dclogs(){
    dc logs --tail=100 --follow $@
}
dcrestart(){
	dc stop $@
	dc rm -f -v $@
	dc up --build -d $@
}

