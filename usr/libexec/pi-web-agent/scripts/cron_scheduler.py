

DAYS=['SUNDAY','MONDAY','TUESDAY',\
'WEDNESDAY','THURSDAY','FRIDAY',\
'SATURDAY']

MONTHS=['JANUARY', 'FABRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',\
'JULY','AUGUST','SEPTEMBER','OCTOBER', 'NOVEMBER', 'DECEMBER']

class CrontabSyntaxError(Exception):
    
    def __init__(self, msg):
        Exception.__init__(self)
        self.strerror = msg
    
    def __str__(self):
        return "CrontabSyntaxError: " + self.strerror

class CronJob(object):
        
    def __init__(self, command):
        self.schedule={'day_of_month':'*', 'month':'*',\
        'week':'*', 'hour':'*', 'day_of_week':'*', 'minute':'*'}
        self.command = command
        self.newline='<br>'
        
    def __iter__(self):
        return self.schedule        

    def __str__(self):
        return self['minute'] + ' ' +\
            self['hour'] + ' ' +\
            self['day_of_month'] + ' ' +\
            self['month'] + ' ' +\
            self['day_of_week'] + ' ' + self.command
    
    def _hour(self, symbol):
        if symbol == '*':
            return "at every hour"
        elif symbol[0:2] == '*/':
            return "at every " + symbol[2:] + " hour(s)"    
        return "at hour(s): " + symbol
    
    def _minute(self, symbol):
        if symbol == '*':
            return "at every minute"
        elif symbol[0:2] == '*/':
            return "at every " + symbol[2:] + " minute(s)"    
        return "on minute(s): " + symbol    
    
    def _week(self, symbol):
        if symbol == '*':
            return "on every week"
        elif symbol[0:2] == '*/':
            return "at every " + symbol[2:] + " week(s)"     
        return "on weekday(s): " + symbol        
    
    def _day_of_month(self, symbol):
        if symbol == '*':
            return "on every day"
        elif symbol[0:2] == '*/':
            return "at every " + symbol[2:] + " day(s)"
                 
        return "on month day(s): " + symbol    
    
    def _month(self, symbol):
        
        if symbol == '*':
            return "every month"
        elif symbol[0:2] == '*/':
            return "at every " + symbol[2:] + " month(s)"
            
        elements = symbol.split(',')
        msg=''
        
        for element in elements:
            dash_elements = element.split('-')
            msg = MONTHS[int(dash_elements[0])]
            
            if len(dash_elements) > 2:
                raise CrontabSyntaxError("Invalid syntax, multiple dashes")
            
            if len(dash_elements) > 1:
                msg+= ' to ' + MONTHS[int(dash_elements[0])]
            elif not (elements.index(element) == (len(elements) - 1)):      
                msg+=','
        
        return message
        
    def _day_of_week(self, symbol):
        
        if symbol == '*':
            return "every day"
        elif symbol[0:2] == '*/':
            return "at every " + symbol[2:] + " day(s)"
            
        elements = symbol.split(',')
        msg=''
        
        for element in elements:
            dash_elements = element.split('-')
            msg = MONTHS[int(dash_elements[0])]
            
            if len(dash_elements) > 2:
                raise CrontabSyntaxError("Invalid syntax, multiple dashes")
            
            if len(dash_elements) > 1:
                msg+= ' to ' + DAYS[int(dash_elements[0])]
            elif not (elements.index(element) == (len(elements) - 1))      
                msg+=','
        
        return message
    
            
    def cronMessageParser(self):
        msg = "Command " + self.command " is set to be run on: " + self.newline
        msg += self._minute(self['minute']) + self.newline
        msg += self._hour(self['hour']) + self.newline
        msg += self._day_of_month(self['day_of_month']) + self.newline
        msg += self._month(self['month']) + self.newline
        msg += self._day_of_week(self['day_of_week'])
            
    def toHTML(self):
        self.newline = '<br>'
        return cronMessageParser(self)
        
    def __str__(self):    
        return cronMessageParser(self)        
           

class ScheduleManager(object):
    
    def __init__(self):
        scheduled_jobs=[]
    
    def doTransaction(self):
        #TODO
        #calls crontab and installs a new cronjob
        pass
    
    def generateHTMLView(self):
        #creates an HTML view as an interface for
        #installing new cronjobs or modifying existing
        #ones
        pass
        
    def getData(self, cgiForm):
        #TODO
        #gets a form with the data for cronjobs
        #and creates a new cronjob or modifies an
        #existing one    
        pass
