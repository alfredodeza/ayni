
js = """
(function(){
    var ready = setInterval(function(){
        if (document.readyState == "complete") onReady();
    }, 30);

    function createUL(items){
      return "<ul>" + items.join('\n') + "</ul>";

    };

    function createLI(items){
      var li_items = [];
      for (var i = 0; i < items.length; i++) {
        var item = "<li>";
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

    function InsertHtml(links){
      var li_links = createLI(links);
      var ul_links = createUL(li_links);
      var version_links = createDiv("ayni-versions", null, [ul_links]);
      var current_version = '<span>Doc version: stable</span>';
      var footer = createDiv("ayni-footer", null, [version_links, current_version]);
      var container = createDiv("ayni-container", null, [footer]);

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
                }

                InsertHtml(links);
            }
        };

        request.send();
    };
})();
"""
