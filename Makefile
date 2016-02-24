#!/usr/bin/make -f
#export DH_VERBOSE=1
#echo $(CURDIR)
DEBDIR=$(CURDIR)/debian/pi-web-agent
APPLICATION_PATH=usr/libexec/pi-web-agent
SERVICE_PATH=etc/init.d/pi-web-agent
VNC_SERVICE=etc/init.d/vncboot
#remove debdir modules and run
ETC_PATH=etc/pi-web-agent
SHARE=usr/share/pi-web-agent
PI_UPDATE=usr/bin/pi-update
PI_UPGRADE=usr/bin/pi-upgrade
PI_FIX=usr/bin/pi-fix
APT_QUERY=usr/bin/apt-query
SUDOERS_D=etc/sudoers.d/pi-web-agent
GPIO_QUERY=usr/bin/gpio-query
CRON_JOBS=etc/cron.daily
EXECUTE_BIN=usr/bin/execute-pwa.sh
PI_APT=usr/bin/pi-package-management
htpasswd_PATH=usr/libexec/pi-web-agent/.htpasswd
UPDATE_APP_BIN=usr/bin/pi-web-agent-update
UPDATE_CHECK_PY=usr/bin/update_check.py
OTHER_BINS=$(CURDIR)/usr/bin/start-stream-cam.sh $(CURDIR)/usr/bin/pi-camera-stream.sh
SYSTEM_UPDATE_CHECK=usr/bin/system_update_check.sh
STARTUP_PWA=usr/bin/startup-manager-pwa.py
LOGS=$(CURDIR)/var/log/pi-web-agent
CRONJOB=etc/cron.d/
CRONJOB_REBOOT=etc/cron.d/cronpwa



install:
	echo $(CURDIR)
	mkdir -p $(DEBDIR)/usr/libexec
	install -d $(CURDIR)/$(APPLICATION_PATH) $(DEBDIR)/$(APPLICATION_PATH)
	cp -rfv $(CURDIR)/$(APPLICATION_PATH)/* $(DEBDIR)/$(APPLICATION_PATH)
	install -d $(CURDIR)/$(SHARE) $(DEBDIR)/$(SHARE)
	cp -rfv $(CURDIR)/$(SHARE)/* $(DEBDIR)/$(SHARE)
	install -D $(CURDIR)/$(SERVICE_PATH) $(DEBDIR)/$(SERVICE_PATH)
	install -D $(CURDIR)/$(EXECUTE_BIN) $(DEBDIR)/$(EXECUTE_BIN)
	install -D  $(CURDIR)/$(PI_APT) $(DEBDIR)/$(PI_APT)
	install -D  $(CURDIR)/$(UPDATE_APP_BIN) $(DEBDIR)/$(UPDATE_APP_BIN)
	install -D  $(CURDIR)/$(UPDATE_CHECK_PY) $(DEBDIR)/$(UPDATE_CHECK_PY)
	install -D  $(CURDIR)/$(SYSTEM_UPDATE_CHECK) $(DEBDIR)/$(SYSTEM_UPDATE_CHECK)
	install -D  $(CURDIR)/$(STARTUP_PWA) $(DEBDIR)/$(STARTUP_PWA)
	install -D  $(OTHER_BINS) $(DEBDIR)/usr/bin/.
	mkdir -p  $(DEBDIR)/$(CRONJOB)
	touch $(DEBDIR)/$(CRONJOB_REBOOT)
	echo @reboot\ root\ /$(STARTUP_PWA) > $(DEBDIR)/$(CRONJOB_REBOOT)
	/bin/cp -rv $(CURDIR)/$(ETC_PATH) $(DEBDIR)/$(ETC_PATH)
	rm -rf $(CURDIR)/$(ETC_PATH)/modules $(DEBDIR)/$(ETC_PATH)/run
	[ ! -L  $(DEBDIR)/$(ETC_PATH)/modules ] || ln -s /usr/lib/apache2/modules $(DEBDIR)/$(ETC_PATH)/modules
#        ln -s /var/run/httpd $(DEBDIR)/$(ETC_PATH)/run
	#chown -R pi-web-agent $(DEBDIR)/$(APPLICATION_PATH)/etc
	#chown -R pi-web-agent:pi-web-agent $(DEBDIR)/$(SHARE)
	ln -s /var/run/httpd $(DEBDIR)/$(ETC_PATH)/run
	mkdir -p $(LOGS)
	install -D  $(CURDIR)/$(VNC_SERVICE) $(DEBDIR)/$(VNC_SERVICE)
	chmod +x $(DEBDIR)/$(VNC_SERVICE)
	install -D $(CURDIR)/$(PI_UPDATE) $(DEBDIR)/$(PI_UPDATE)
	install -D $(CURDIR)/$(PI_UPGRADE) $(DEBDIR)/$(PI_UPGRADE)
	install -D $(CURDIR)/$(PI_FIX) $(DEBDIR)/$(PI_FIX)
	install -D $(CURDIR)/$(APT_QUERY) $(DEBDIR)/$(APT_QUERY)
	chmod +x $(DEBDIR)/$(EXECUTE_BIN)
	chmod +x $(DEBDIR)/$(SERVICE_PATH)
	chmod +x $(DEBDIR)/$(UPDATE_APP_BIN)
	chmod +x $(DEBDIR)/$(UPDATE_CHECK_PY)
	chmod +x $(DEBDIR)/$(SYSTEM_UPDATE_CHECK)
	chmod +x $(DEBDIR)/$(STARTUP_PWA)
	chmod +x $(DEBDIR)/usr/bin/*
