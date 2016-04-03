function initialiseGPIO() {
    var url = '/cgi-bin/toolkit/gpio_manager_api.py';
    processing();
    getJSONResponse(url, renderGPIO);
}

function renderGPIO(data) {

    $.each(data, function (index, value) {
        var leftPin = value[0];
        
        
        //create inout widget
        var tdInOutL$ = getInOutWidget(leftPin);
        
        //create on off widget
        var tdOnOffL$ = getOnOffWidget(leftPin);
        
        //create name
        var tdNameL$="<td>" + leftPin['Name'].trim() + "</td>";
        
        var rightPin = value[1];
        
        //create inout widget
        var tdInOutR$ = getInOutWidget(rightPin);
        
        //create on off widget
        var tdOnOffR$ = getOnOffWidget(rightPin);
        
        //create name
        var tdNameR$="<td>" + rightPin['Name'].trim() + "</td>";
        
        var row$ = "<tr></tr>";
        row$ = $(row$).append(tdInOutL$, tdOnOffL$, tdNameL$,
                              tdNameR$, tdOnOffR$, tdInOutR$);      
        $('table#gpio_table').append(row$);
    });
    
    endProcessing();

}

function getOnOffWidget(pin) {
    
    
    if (pin['Mode'] != 'IN' && pin['Mode'] != 'OUT') {
        if (pin['Mode'] != null)
            return '<td><span class="label label-warning">' + pin['Mode'] + '</span></td>';
        else
            return '<td><span class="label label-warning">' + pin['Name'].trim() + '</span></td>';
    }
    var input$ = '<input type="checkbox" onclick="submit_gpio_value(this)">';
    
    input$ = $(input$).prop('checked', pin['Val'] == "1");
    input$ = $(input$).attr('name', pin['Name'].trim());
    input$ = $(input$).attr('direction', pin['Mode'].trim());
    input$ = $(input$).attr('id', 'wPiV-'+pin['wPi']);
    if (pin['Mode'] != 'IN' && pin['Mode'] != 'OUT') {
        input$ = $(input$).prop('disabled', true);
    }
    var divSwitch$ = '<div class="switch"></div>';
    var label$ = '<label>off</label>';
    label$ = $(label$).append(input$);
    var span$ = '<span class="lever"></span>';

    label$ = $(label$).append(span$);
    label$ = $(label$).append('on');

    divSwitch$ = $(divSwitch$).append(label$); 
    
    var tdInOut$ = "<td></td>";
    tdInout$ = $(tdInOut$).append(divSwitch$);
    
    return tdInout$;
}

function getInOutWidget(pin) {
    if (pin['Mode'] != 'IN' && pin['Mode'] != 'OUT') {
        if (pin['Mode'] != null)
            return '<td><span class="label label-warning">' + pin['Mode'] + '</span></td>';
        else
            return '<td><span class="label label-warning">' + pin['Name'].trim() + '</span></td>';
    }

    var input$ = '<input type="checkbox" onclick="submit_gpio_direction(this)">';
    
    input$ = $(input$).prop('checked', pin['Mode'] == "OUT");
    input$ = $(input$).attr('name', pin['Name'].trim());
    input$ = $(input$).attr('direction', pin['Mode'].trim());
    input$ = $(input$).attr('id', 'wPiD-'+pin['wPi']);
    if (pin['Mode'] != 'IN' && pin['Mode'] != 'OUT') {
        input$ = $(input$).prop('disabled', true);
    }
    var divSwitch$ = '<div class="switch"></div>';
    var label$ = '<label>off</label>';
    label$ = $(label$).append(input$);
    var span$ = '<span class="lever"></span>';

    label$ = $(label$).append(span$);
    label$ = $(label$).append('on');

    divSwitch$ = $(divSwitch$).append(label$); 
    
    var tdInOut$ = "<td></td>";
    tdInout$ = $(tdInOut$).append(divSwitch$);
    
    return tdInout$;
}

function gpio_clear() {
    alert("The cleanup is problematic for the moment, it may hung your Pi. Remember to set the inputs you switched on to IN mode");
}

function submit_gpio_direction(element) {
     
     var url='/cgi-bin/toolkit/onOffPin.py?op=direction&id='+element.id.split('-')[1]+'&direction='
     var direction='IN';
     if (element.attributes["direction"].value=="IN")
     {
        direction='OUT';
     }
     url+=direction+"&from="+element.attributes["direction"].value
     var info=getJSONResponse(url, null);

}

function submit_gpio_value(element) {
     
     var url='/cgi-bin/toolkit/onOffPin.py?op=value&id='+element.id.split('-')[1]+'&value='
     var value='0';
     if (element.checked)
     {
        value='1';
     }
     url+=value
     var info=getResponse(url, null);
}

$(function() {
    initialiseGPIO();
});
