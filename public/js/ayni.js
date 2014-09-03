(function(){
    var ready = setInterval(function(){
        if (document.readyState == "complete") onReady();
    }, 30);

    function createDiv(_class, _id, contentArray){
          var div = document.createElement("div");
          if (_class) {
            div.className = _class;
          }

          if (_id) {
            div.id = _id
          }

          for (var i = 0; i < contentArray.length; i++) {
            div.appendChild(contentArray[i]);
          }
          return div;
    };

    function InsertHtml(links){
          var footer = document.createElement("div");
          footer.className = "ayni-footer";

          links = createDiv("ayni-versions", null, links);
          footer.appendChild(links);

          document.body.appendChild(footer);

    };

    function onReady(){
        clearInterval(ready);
        // Inject the css
        var link = document.createElement("link");
        // FIXME: this needs to be configurable
        link.href = "http://ayni.ceph.com/public/css/ayni.css";
        link.type = "text/css";
        link.rel = "stylesheet";
        document.getElementsByTagName("head")[0].appendChild(link);

        var request = new XMLHttpRequest();
        // FIXME: this needs to be configurable
        request.open('GET', 'http://ayni.ceph.com/projects/ceph-deploy/', true);

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
                    var link = document.createElement('a')
                    link.setAttribute('href', redirect_to);
                    link.setAttribute('title', name);
                    links.push(link);
                }

                InsertHtml(links);

            }
        };

        request.send();
    };
})();
