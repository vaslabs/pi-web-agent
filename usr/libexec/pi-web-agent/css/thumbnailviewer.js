function initialiseGallery() {
        processing();
        getJSONResponse('/cgi-bin/toolkit/camera_manager_api.py?cmd=gallery', galleryUI);
    }
    var images = {};
    
    
    
    function galleryUI(data) {
        $.each(data, function (index, value) {
            images[index] = value;
            var row_index = Math.floor(index/6);
            if (index % 6 == 0) {
                var row = '<div class="row" id="row_' + row_index + '"></div>';
                $('#gallery_thumbnails').append(row);    
            }
            var thumb_div = '<div class="span3"><a href="#" onclick="openImageDialog(\''+value + '\');"><div id="image_' + index + '" class="thumbnail_view"></div></a></div>';
            
            $('#row_' + row_index).append(thumb_div);
            $('#image_'+index).css('background-image', 'url(/cgi-bin/toolkit/image_manager.py?image='+ value + ')');
        });
        endProcessing();
    }
    
    function displaySnapshot(data) {
        var value = data['name'].split('.')[0] + '.png'
        var image_url = '/cgi-bin/toolkit/image_manager.py?image='+value;
        append_image(image_url, value);
        endProcessing();
    
    }
    
    function append_image(image_url, value) {
        var total_images = Object.keys(images).length;
        var index = total_images;
        var row_index = Math.floor(index/6);
        images[total_images] = image_url;
        if (index % 6 == 0) {
            var row = '<div class="row" id="row_' + row_index + '"></div>';
            $('#gallery_thumbnails').append(row);    
        }
        var thumb_div = '<div class="span3"><a href="#" onclick="openImageDialog(\''+value + '\');"><div id="image_' + index + '" class="thumbnail_view"></div></a></div>';
        
        $('#row_' + row_index).append(thumb_div);
        $('#image_'+index).css('background-image', 'url(' + image_url + ')');
        
    }
    
    function openImageDialog(value) {
        var image_url = '/cgi-bin/toolkit/image_manager.py?image=' + value.split('.')[0]+'.jpg';
        showDialog('Camera image', '<div align="center"><img class="dialoged_image" src="' + image_url + '"/></div>');
    }
    
    $( document ).ready(function() {
        initialiseGallery();
    });
