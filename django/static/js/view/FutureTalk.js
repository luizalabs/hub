var futureTalk = {

	init: function() {
		this.bindButtons();
		this.loadImage = window.LOAD_IMAGE;
		this.doneImage = window.DONE_IMAGE;
		this.errorImage = window.ERROR_IMAGE;
	},
	bindButtons: function() {
		$('.vote-up').click(this.voteUp);
		$('.vote-down').click(this.voteDown);
	},
	voteUp: function() {
		futureTalk.vote(1, $(this).parent());
	},
	voteDown: function() {
		futureTalk.vote(0, $(this).parent());
	},
	vote: function(vote, element) {
		var id = element.data('id');
		$.ajax({
            type: 'POST',
            url: window.VOTE,
            dataType: 'json',
            beforeSend: function(){
                $('body').css('cursor', 'wait');
                element.find('.vote-up').html(futureTalk.getLoaderImage());
                element.find('.vote-down').html(futureTalk.getLoaderImage());
            },
            data: {
                id: id,
                vote: vote,
                csrfmiddlewaretoken: window.CSRF_TOKEN
            },
            success: function(ret) {
            	element.html(futureTalk.getDoneImage());
            },
            error: function(ret) {
            	if (ret.status === 403) {
                    alert('Faça o login para votar.');
            	} else {
                    alert('Xiiiiiiii..');
                    element.html(futureTalk.getErrorImage());
            	}
            },
            complete: function() {
                $('body').css('cursor', 'default');
                
            }
        });
	},
	getLoaderImage: function() {
		return '<img src="' + futureTalk.loadImage + '" />';
	},
	getDoneImage: function() {
		return '<img src="' + futureTalk.doneImage + '" />';	
	},
	getErrorImage: function() {
		return '<img src="' + futureTalk.errorImage + '" />';		
	}

}