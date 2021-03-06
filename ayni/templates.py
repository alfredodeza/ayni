
js = """
(function(){
    var ready = setInterval(function(){
        if (document.readyState == "complete") onReady();
    }, 30);

    function createUL(items){
      return "<ul>" + items.join('') + "</ul>";

    };

    function createLI(items, _class){
      var li_items = [];
      for (var i = 0; i < items.length; i++) {
        if (_class) {
          var item = '<li class="'+_class+'">';
        } else {
            var item = "<li>";
        }

        item += items[i];
        item += "</li>";
        li_items.push(item);
      };
      return li_items

    };

    function createA(href, title){
      var link = '<a href="';
      link += href
      link += '">';
      link += title;
      link += '</a>';
      return link
    }

    function createDiv(_class, _id, contentArray){
      if ((_class) && (!_id)) {
        var div = '<div class="';
        div +=  _class;
        div +=  '">';
      } else if ((!_class) && (_id)) {
        var div = '<div id="' + _id + '">';
      } else if ((_class) && (_id)) {
        var div = '<div id="' + _id + '" class="' + _class + '">';
      };

      for (var i = 0; i < contentArray.length; i++) {
        div += contentArray[i];
      };

      div += '</div>';
      return div;
    };

    function currentlyReading(data) {
      var url = window.location.href

      for (var i = 0; i < data.length; i++) {
        var obj = data[i];
        var end_url = obj['end_url'];
        if (url.indexOf(end_url) > -1) {
          return obj['name'];
        };
      };
      return "development"
    }

    function InsertHtml(links, doc_version){
      var li_links = createLI(links, "ayni-versions");
      var current_version = '<li id="ayni-version-anchor"><span>Doc version: '+doc_version+'</span></li>';
      li_links.push(current_version);
      var ul_links = createUL(li_links);
      var version_links = createDiv("ayni-footer", null, [ ul_links]);
      var container = createDiv("ayni-container", null, [version_links]);

      // HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE
      // I usually tell people not to hate, but I HATE THIS THING.
      // HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE HATE
      document.body.innerHTML += container;
    };

    function onReady(){
        clearInterval(ready);
        // Inject the css
        var link = document.createElement("link");
        link.href = "$ayni_css_file";
        link.type = "text/css";
        link.rel = "stylesheet";
        document.getElementsByTagName("head")[0].appendChild(link);

        var request = new XMLHttpRequest();
        request.open('GET', '$project_url', true);

        request.onload = function() {
            if (request.status >= 200 && request.status < 400){
                var data = JSON.parse(request.responseText);

                // loop over all the projects available
                var arrayLength = data.length;
                var links = [];
                for (var i = 0; i < arrayLength; i++) {
                    var obj = data[i];
                    var redirect_to = obj['redirect_to'];
                    var name = obj['name'];
                    var link = createA(redirect_to, name);
                    links.push(link);
                };

                var doc_version = currentlyReading(data);
                InsertHtml(links, doc_version);
            }
        };

        request.send();
    };
})();
"""
