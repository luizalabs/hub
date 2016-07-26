$(function () {
    var tagcloud = {
        get: function () {
            $.ajax({
                url: ['/get_tags_json'].join(''),
                cache: true,
                type: 'GET',
                dataType: "json",
                success: function (payload) {
                    if (payload != null) {
                        tagcloud.serialize(payload);
                    }
                }
            });
        },
        serialize: function (data) {
            if (data == undefined) {
                return;
            }
            var word_list = new Array();
            for (i = 0; i < data.length; i++) { 
                var tag = data[i].tag;
                var weight_ = data[i].weight;
                var link_ = data[i].url;
                word_list.push({
                    text: tag, 
                    weight: weight_,
                    link: link_,
                })
            }
            tagcloud.render(word_list)
        },
        render:  function (word_list) {
            $("#wordcloud").jQCloud(word_list);
        },
    };
    tagcloud.get();
});
