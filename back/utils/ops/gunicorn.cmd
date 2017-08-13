gunicorn -b 0.0.0.0 app:App --log-file=- -w $1 --reload --access-logfile=/tmp/access.log --access-logformat='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%(D)s"'
