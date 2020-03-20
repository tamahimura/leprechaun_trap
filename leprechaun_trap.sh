#! /bin/sh

### BEGIN INIT INFO
# Provides:          leprechaun_trap.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting leprechaun_trap.py"
    /home/pi/leprechaun_trap/leprechaun_trap.py &
    ;;
  stop)
    echo "Stopping garageserver.py"
    pkill -f /usr/local/bin/leprechaun_trap.py
    ;;
  *)
    echo "Usage: /etc/init.d/leprechaun_trap.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
